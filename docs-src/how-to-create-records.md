---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

How to create arrays of records
===============================

In Awkward Array, a "record" is a structure containing a fixed-length set of typed, possibly named fields. This is a "struct" in C or an "object" in Python (though the association of executable methods to record types is looser than the binding of methods to classes in object oriented languages).

All methods in Awkward Array are implemented as "[structs of arrays](https://en.wikipedia.org/wiki/AoS_and_SoA)," rather than arrays of structs, so making and breaking records are inexpensive operations that you can perform frequently in data analysis.

```{code-cell}
import awkward as ak
import numpy as np
```

From a list of Python dicts
---------------------------

Records have a natural representation in JSON and Python as dicts, but only if all dicts in a series have the same set of field names. The [ak.Array](https://awkward-array.readthedocs.io/en/latest/_auto/ak.Array.html) invokes [ak.from_iter](https://awkward-array.readthedocs.io/en/latest/_auto/ak.from_iter.html) whenever presented with a list (or other non-string, non-dict iterable).

```{code-cell}
python_dicts = [
    {"x": 1, "y": 1.1, "z": "one"},
    {"x": 2, "y": 2.2, "z": "two"},
    {"x": 3, "y": 3.3, "z": "three"},
    {"x": 4, "y": 4.4, "z": "four"},
    {"x": 5, "y": 5.5, "z": "five"},
]
python_dicts
```

```{code-cell}
awkward_array = ak.Array(python_dicts)
awkward_array
```

It is important that all of the dicts in the series have the same set of field names, since Awkward Array has to identify all of the records as having a single type:

```{code-cell}
awkward_array.type
```

That is to say, an array of records is not a mapping from one type to another, such as from strings to numbers. The above record has exactly three fields: _x_, _y_, and _z_, and they have fixed types: `int64`, `float64`, and `string`. A mapping could have a variable set of keys, but the value type would have to be uniform.

If you _try_ to mix field types in [ak.from_iter](https://awkward-array.readthedocs.io/en/latest/_auto/ak.from_iter.html) (ultimately from [ak.ArrayBuilder](https://awkward-array.readthedocs.io/en/latest/_auto/ak.ArrayBuilder.html)), the union of all sets of fields will be assumed, and any that aren't filled in every item will be presumed "missing."

```{code-cell}
array = ak.Array([
    {"a": 1, "b": 1, "c": 1},
    {"b": 2, "c": 2},
    {"c": 3, "d": 3, "e": 3, "f": 3},
    {"c": 4},
])
array
```

```{code-cell}
array.tolist()
```

```{code-cell}
array.type
```

From a single dict of columns
-----------------------------

If a _single dict_ is passed to [ak.Array](https://awkward-array.readthedocs.io/en/latest/_auto/ak.Array.html), it will be interpreted as a set of columns, like [Pandas's DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) constructor. This is to provide a familiar interface to Pandas users.

```{code-cell}
from_columns = ak.Array({"x": [1, 2, 3, 4, 5], "y": [1.1, 2.2, 3.3, 4.4, 5.5], "z": ["one", "two", "three", "four", "five"]})
from_columns
```

```{code-cell}
from_columns.tolist()
```

```{code-cell}
from_columns.type
```

This is _not_ the same as calling [ak.from_iter](https://awkward-array.readthedocs.io/en/latest/_auto/ak.from_iter.html) on the same input, which could not be a valid [ak.Array](https://awkward-array.readthedocs.io/en/latest/_auto/ak.Array.html) because a single dict would be an [ak.Record](https://awkward-array.readthedocs.io/en/latest/_auto/ak.Record.html).

```{code-cell}
from_rows = ak.from_iter({"x": [1, 2, 3, 4, 5], "y": [1.1, 2.2, 3.3, 4.4, 5.5], "z": ["one", "two", "three", "four", "five"]})
from_rows
```

```{code-cell}
from_rows.tolist()
```

```{code-cell}
from_rows.type
```

Using ak.zip
------------

The [ak.zip](https://awkward-array.readthedocs.io/en/latest/_auto/ak.zip.html) function combines columns into an array of records, similar to the Pandas-style constructor described above.

```{code-cell}
from_columns = ak.zip({"x": [1, 2, 3, 4, 5], "y": [1.1, 2.2, 3.3, 4.4, 5.5], "z": ["one", "two", "three", "four", "five"]})
from_columns
```

```{code-cell}
from_columns.tolist()
```

```{code-cell}
from_columns.type
```

The difference is that [ak.zip](https://awkward-array.readthedocs.io/en/latest/_auto/ak.zip.html) attempts to nested lists deeply, up to a `depth_limit`.

Given columns with nested lists:

```{code-cell}
zipped = ak.zip({"x": ak.Array([[1, 2, 3], [], [4, 5]]), "y": ak.Array([[1.1, 2.2, 3.3], [], [4.4, 5.5]])})
zipped
```

```{code-cell}
zipped.tolist()
```

By contrast, the same input to [ak.Array](https://awkward-array.readthedocs.io/en/latest/_auto/ak.Array.html)'s Pandas-style constructor keeps nested lists separate.

```{code-cell}
not_zipped = ak.Array({"x": ak.Array([[1, 2, 3], [], [4, 5]]), "y": ak.Array([[1.1, 2.2, 3.3], [], [4.4, 5.5]])})
not_zipped
```

```{code-cell}
not_zipped.tolist()
```

The difference can be seen in a comparison of their types:

```{code-cell}
zipped.type, not_zipped.type
```

Also, [ak.zip](https://awkward-array.readthedocs.io/en/latest/_auto/ak.zip.html) can build records without field names, also known as "tuples."

```{code-cell}
tuples = ak.zip((ak.Array([[1, 2, 3], [], [4, 5]]), ak.Array([[1.1, 2.2, 3.3], [], [4.4, 5.5]])))
tuples
```

```{code-cell}
tuples.tolist()
```

```{code-cell}
tuples.type
```

Functions that return lists of pairs, such as [ak.cartesian](https://awkward-array.readthedocs.io/en/latest/_auto/ak.cartesian.html) and [ak.combinations](https://awkward-array.readthedocs.io/en/latest/_auto/ak.combinations.html), also use the tuple type.

```{code-cell}
one = ak.Array([[1, 2, 3], [], [4, 5], [6]])
two = ak.Array([["a", "b"], ["c"], ["d"], ["e", "f"]])

ak.cartesian((one, two))
```

```{code-cell}
ak.combinations(one, 2)
```

Record names
------------

In addition to optional field names, record types can also have names.

```{code-cell}
ak.Array([
    {"x": 1, "y": 1.1},
    {"x": 2, "y": 2.2},
    {"x": 3, "y": 3.3},
    {"x": 4, "y": 4.4},
    {"x": 5, "y": 5.5},
], with_name="XYZ")
```

```{code-cell}
ak.zip(
    (ak.Array([[1, 2, 3], [], [4, 5]]), ak.Array([[1.1, 2.2, 3.3], [], [4.4, 5.5]])),
    with_name="AB",
)
```

```{code-cell}
ak.cartesian({"L": ak.Array([1, 2, 3]), "R": ak.Array(["a", "b"])}, with_name="LeftRight", axis=0)
```

Names are for giving records [specialized behavior](how-to-specialize) through the [ak.behavior](https://awkward-array.readthedocs.io/en/latest/ak.behavior.html) registry. These are like attaching methods to a class in the sense that all records with a particular name can be given Python properties and methods.

```{code-cell}
class XYZRecord(ak.Record):
    def __repr__(self):
        return f"(X={self.x}:Y={self.y})"

class XYZArray(ak.Array):
    def diff(self):
        return abs(self.x - self.y)

ak.behavior["XYZ"] = XYZRecord
ak.behavior["*", "XYZ"] = XYZArray
ak.behavior["__typestr__", "XYZ"] = "XYZ"
ak.behavior[np.sqrt, "XYZ"] = lambda xyz: np.sqrt(xyz.x)

array = ak.Array([
    {"x": 1, "y": 1.1},
    {"x": 2, "y": 2.2},
    {"x": 3, "y": 3.3},
    {"x": 4, "y": 4.4},
    {"x": 5, "y": 5.5},
], with_name="XYZ")
array
```

```{code-cell}
array.diff()
```

```{code-cell}
array[0]
```

```{code-cell}
np.sqrt(array)
```

With ArrayBuilder
-----------------

[ak.ArrayBuilder](https://awkward-array.readthedocs.io/en/latest/_auto/ak.ArrayBuilder.html) is described in more detail [in this tutorial](how-to-create-arraybuilder), but you can also construct arrays of records using the `begin_record`/`end_record` methods or the `record` context manager.

(This is what [ak.from_iter](https://awkward-array.readthedocs.io/en/latest/_auto/ak.from_iter.html) uses internally to accumulate records.)

```{code-cell}
builder = ak.ArrayBuilder()

builder.begin_record()
builder.field("x").append(1)
builder.field("y").append(1.1)
builder.end_record()

builder.begin_record()
builder.field("x").append(2)
builder.field("y").append(2.2)
builder.end_record()

builder.begin_record()
builder.field("x").append(3)
builder.field("y").append(3.3)
builder.end_record()

array = builder.snapshot()
array
```

```{code-cell}
builder = ak.ArrayBuilder()

with builder.record():
    builder.field("x").append(1)
    builder.field("y").append(1.1)

with builder.record():
    builder.field("x").append(2)
    builder.field("y").append(2.2)

with builder.record():
    builder.field("x").append(3)
    builder.field("y").append(3.3)

array = builder.snapshot()
array
```

The `begin_record` method and `record` context manager can take a name, which allows you to name your records on the spot.

```{code-cell}
builder = ak.ArrayBuilder()

for i in range(3):
    with builder.record("XY"):
        builder.field("x").append(i)
        builder.field("y").append(i * 1.1)

array = builder.snapshot()
array
```

Record names also let you decide between two ways of dealing with changing sets of fields among the input records.

   * The default/generic way: all records at a given level are taken to belong to the same type and some instances of that type are missing fields.
   * Named records: different names mean different types, whether they have the same fields or not. Different record names at the same level result in a union type.

Here is an illustration of that difference.

```{code-cell}
def fill_A(builder, use_name):
    with builder.record("A" if use_name else None):
        builder.field("x").append(len(builder))
        builder.field("y").append(len(builder) * 1.1)

def fill_B(builder, use_name):
    with builder.record("B" if use_name else None):
        builder.field("y").append(len(builder) * 1.1)
        builder.field("z").append(str(len(builder)))
```

Without names:

```{code-cell}
builder = ak.ArrayBuilder()

fill_A(builder, use_name=False)
fill_A(builder, use_name=False)

fill_B(builder, use_name=False)
fill_B(builder, use_name=False)

fill_A(builder, use_name=False)

without_names = builder.snapshot()
without_names
```

```{code-cell}
without_names.tolist()
```

With names:

```{code-cell}
builder = ak.ArrayBuilder()

fill_A(builder, use_name=True)
fill_A(builder, use_name=True)

fill_B(builder, use_name=True)
fill_B(builder, use_name=True)

fill_A(builder, use_name=True)

with_names = builder.snapshot()
with_names
```

```{code-cell}
with_names.tolist()
```

The difference can be seen in the type: `without_names` has only one record type, but the _x_ and _z_ fields are optional, and `with_names` has a union of two record types, neither of which have optional fields.

```{code-cell}
without_names.type
```

```{code-cell}
with_names.type
```

In Numba
--------

Functions that Numba Just-In-Time (JIT) compiles can use [ak.ArrayBuilder](https://awkward-array.readthedocs.io/en/latest/_auto/ak.ArrayBuilder.html) to accumulate records or columns can be accumulated in the compiled part and later combined with [ak.zip](https://awkward-array.readthedocs.io/en/latest/_auto/ak.zip.html). Combining columns outside of a JIT-compiled function is generally faster.

([At this time](https://numba.pydata.org/numba-doc/dev/reference/pysupported.html#language), Numba can't use context managers, the `with` statement, in fully compiled code. [ak.ArrayBuilder](https://awkward-array.readthedocs.io/en/latest/_auto/ak.ArrayBuilder.html) can't be constructed or converted to an array using `snapshot` inside a JIT-compiled function, but can be outside the compiled context. Similarly, `ak.*` functions like [ak.zip](https://awkward-array.readthedocs.io/en/latest/_auto/ak.zip.html) can't be called inside a JIT-compiled function, but can be outside.)

```{code-cell}
import numba as nb
```

```{code-cell}
@nb.jit
def append_record(builder, i):
    builder.begin_record()
    builder.field("x").append(i)
    builder.field("y").append(i * 1.1)
    builder.end_record()

@nb.jit
def example(builder):
    append_record(builder, 1)
    append_record(builder, 2)
    append_record(builder, 3)
    return builder

builder = example(ak.ArrayBuilder())

array = builder.snapshot()
array
```

```{code-cell}
@nb.jit
def faster_example():
    x = np.empty(3, np.int64)
    y = np.empty(3, np.float64)
    x[0] = 1
    y[0] = 1.1
    x[1] = 2
    y[1] = 2.2
    x[2] = 3
    y[2] = 3.3
    return x, y

array = ak.zip(dict(zip(["x", "y"], faster_example())))
array
```

Combining columns into arrays is a metadata-only operation, which does not scale with the size of the dataset. The second example is faster because it only requires Numba to fill NumPy arrays, which it's designed for, without involving the machinery of [ak.ArrayBuilder](https://awkward-array.readthedocs.io/en/latest/_auto/ak.ArrayBuilder.html) to identify types at runtime.
