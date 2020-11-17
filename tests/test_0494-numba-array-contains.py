# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/master/LICENSE

from __future__ import absolute_import

import sys

import pytest

import numpy
import awkward1


numba = pytest.importorskip("numba")


def test_deep():
    array = awkward1.Array([[], [0], [1, 2, 3]])
    assert 0 in array
    assert 3 in array
    assert 4 not in array


def test_numba():
    @numba.njit
    def f1(array):
        return 0 in array, 3 in array, 4 in array

    assert f1(awkward1.Array([0, 1, 2, 3])) == (True, True, False)

    @numba.njit
    def f2(array):
        return 0 in array[0], 0 in array[2], 3 in array[2], 3 in array

    assert f1(awkward1.Array([[], [0], [1, 2, 3]])) == (True, True, False)
    assert f2(awkward1.Array([[], [0], [1, 2, 3]])) == (False, False, True, True)

    @numba.njit
    def f3(array):
        return None in array

    assert f1(awkward1.Array([0, 1, 2, None, 3])) == (True, True, False)
    assert f3(awkward1.Array([0, 1, 2, None, 3])) is True

    assert f1(awkward1.Array([[], [0], None, [1, 2, 3]])) == (True, True, False)
    assert f2(awkward1.Array([[], None, [1, 2, 3]])) == (False, False, True, True)

    assert f1(awkward1.Array([[], [0], [1, 2, None, 3]])) == (True, True, False)
    assert f2(awkward1.Array([[], [0], [1, 2, None, 3]])) == (False, False, True, True)

    assert f1(awkward1.Array([{"x": 0}, {"x": 1}, {"x": 2}, {"x": 3}])) == (True, True, False)
    assert f1(awkward1.Array([{"x": [0]}, {"x": []}, {"x": [2]}, {"x": [3]}])) == (True, True, False)

    assert f1(awkward1.Array([[], [{"x": 0}], [{"x": 1}, {"x": 2}, {"x": 3}]])) == (True, True, False)
    assert f1(awkward1.Array([[], [{"x": 0, "y": 999}], [{"x": 1, "y": 999}, {"x": 2, "y": 999}, {"x": 3, "y": 999}]])) == (True, True, False)
    assert f2(awkward1.Array([[], [{"x": 0}], [{"x": 1}, {"x": 2}, {"x": 3}]])) == (False, False, True, True)
    assert f2(awkward1.Array([[], [{"x": 0, "y": 999}], [{"x": 1, "y": 999}, {"x": 2, "y": 999}, {"x": 3, "y": 999}]])) == (False, False, True, True)

    assert f1(awkward1.Array([[], [{"x": [0]}], [{"x": []}, {"x": [2]}, {"x": [3]}]])) == (True, True, False)

    assert f1(awkward1.Array([{"x": 0}, {"x": 1}, {"x": None}, {"x": 3}])) == (True, True, False)
    assert f3(awkward1.Array([{"x": 0}, {"x": 1}, {"x": None}, {"x": 3}])) is True
    assert f1(awkward1.Array([{"x": 0}, {"x": 1}, None, {"x": 3}])) == (True, True, False)
    assert f3(awkward1.Array([{"x": 0}, {"x": 1}, None, {"x": 3}])) is True

    array = awkward1.Array([{"x": 0}, {"x": 1}, {"x": 2}, {"x": 3}])
    assert f1(array[0]) == (True, False, False)

    array = awkward1.Array([{"x": [0]}, {"x": [1]}, {"x": []}, {"x": [3]}])
    assert f1(array[0]) == (True, False, False)

    array = awkward1.Array([{"x": 0}, None, {"x": 2}, {"x": 3}])
    assert f1(array[0]) == (True, False, False)
    assert f3(array[0]) is False

    array = awkward1.Array([{"x": [0]}, None, {"x": []}, {"x": [3]}])
    assert f1(array[0]) == (True, False, False)
    assert f3(array[0]) is False
