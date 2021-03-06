# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


vector = pytest.importorskip("vector")


def test():
    point = ak.Record(
        {"x": 1, "y": 2, "z": 3},
        with_name="Vector3D",
        behavior=vector._backends.awkward_.behavior,
    )
    assert np.matmul(point, vector.obj(x=1, y=0, z=2)) == 7
