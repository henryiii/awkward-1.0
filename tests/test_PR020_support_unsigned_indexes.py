# BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

import sys
import os
import json

import pytest
import numpy
numba = pytest.importorskip("numba")

import awkward1

py27 = (sys.version_info[0] < 3)

def test_index():
    array_i1 = numpy.array([numpy.iinfo("i1").min, -1, 0, 1, numpy.iinfo("i1").max], dtype="i1")
    array_u1 = numpy.array([numpy.iinfo("u1").min, -1, 0, 1, numpy.iinfo("u1").max], dtype="u1")
    array_li2 = numpy.array([numpy.iinfo("<i2").min, -1, 0, 1, numpy.iinfo("<i2").max], dtype="<i2")
    array_lu2 = numpy.array([numpy.iinfo("<u2").min, -1, 0, 1, numpy.iinfo("<u2").max], dtype="<u2")
    array_li4 = numpy.array([numpy.iinfo("<i4").min, -1, 0, 1, numpy.iinfo("<i4").max], dtype="<i4")
    array_lu4 = numpy.array([numpy.iinfo("<u4").min, -1, 0, 1, numpy.iinfo("<u4").max], dtype="<u4")
    array_li8 = numpy.array([numpy.iinfo("<i8").min, -1, 0, 1, numpy.iinfo("<i8").max], dtype="<i8")
    array_lu8 = numpy.array([numpy.iinfo("<u8").min, -1, 0, 1, numpy.iinfo("<u8").max], dtype="<u8")
    array_bi2 = numpy.array([numpy.iinfo(">i2").min, -1, 0, 1, numpy.iinfo(">i2").max], dtype=">i2")
    array_bu2 = numpy.array([numpy.iinfo(">u2").min, -1, 0, 1, numpy.iinfo(">u2").max], dtype=">u2")
    array_bi4 = numpy.array([numpy.iinfo(">i4").min, -1, 0, 1, numpy.iinfo(">i4").max], dtype=">i4")
    array_bu4 = numpy.array([numpy.iinfo(">u4").min, -1, 0, 1, numpy.iinfo(">u4").max], dtype=">u4")
    array_bi8 = numpy.array([numpy.iinfo(">i8").min, -1, 0, 1, numpy.iinfo(">i8").max], dtype=">i8")
    array_bu8 = numpy.array([numpy.iinfo(">u8").min, -1, 0, 1, numpy.iinfo(">u8").max], dtype=">u8")

    index_i1 = awkward1.layout.Index8(array_i1)
    index_u1 = awkward1.layout.IndexU8(array_u1)
    index_li2 = awkward1.layout.Index32(array_li2)
    index_lu2 = awkward1.layout.Index32(array_lu2)
    index_li4 = awkward1.layout.Index32(array_li4)
    index_lu4 = awkward1.layout.IndexU32(array_lu4)
    index_li8 = awkward1.layout.Index64(array_li8)
    index_lu8 = awkward1.layout.Index64(array_lu8)
    index_bi2 = awkward1.layout.Index32(array_bi2)
    index_bu2 = awkward1.layout.Index32(array_bu2)
    index_bi4 = awkward1.layout.Index32(array_bi4)
    index_bu4 = awkward1.layout.IndexU32(array_bu4)
    index_bi8 = awkward1.layout.Index64(array_bi8)
    index_bu8 = awkward1.layout.Index64(array_bu8)

    assert index_i1[2] == 0
    assert index_u1[2] == 0
    assert index_li2[2] == 0
    assert index_lu2[2] == 0
    assert index_li4[2] == 0
    assert index_lu4[2] == 0
    assert index_li8[2] == 0
    assert index_lu8[2] == 0
    assert index_bi2[2] == 0
    assert index_bu2[2] == 0
    assert index_bi4[2] == 0
    assert index_bu4[2] == 0
    assert index_bi8[2] == 0
    assert index_bu8[2] == 0

    array_i1[2] = 10
    array_u1[2] = 10
    array_li2[2] = 10
    array_lu2[2] = 10
    array_li4[2] = 10
    array_lu4[2] = 10
    array_li8[2] = 10
    array_lu8[2] = 10
    array_bi2[2] = 10
    array_bu2[2] = 10
    array_bi4[2] = 10
    array_bu4[2] = 10
    array_bi8[2] = 10
    array_bu8[2] = 10

    assert index_i1[2] == 10
    assert index_u1[2] == 10
    assert index_li2[2] == 0
    assert index_lu2[2] == 0
    assert index_li4[2] == 10
    assert index_lu4[2] == 10
    assert index_li8[2] == 10
    assert index_lu8[2] == 0
    assert index_bi2[2] == 0
    assert index_bu2[2] == 0
    assert index_bi4[2] == 0
    assert index_bu4[2] == 0
    assert index_bi8[2] == 0
    assert index_bu8[2] == 0

content  = awkward1.layout.NumpyArray(numpy.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]))
starts1  = awkward1.layout.IndexU32(numpy.array([0, 3, 3, 5, 6], numpy.uint32))
stops1   = awkward1.layout.IndexU32(numpy.array([3, 3, 5, 6, 9], numpy.uint32))
offsets1 = awkward1.layout.IndexU32(numpy.array([0, 3, 3, 5, 6, 9], numpy.uint32))
starts2  = awkward1.layout.IndexU32(numpy.array([0, 2, 3, 3], numpy.uint32))
stops2   = awkward1.layout.IndexU32(numpy.array([2, 3, 3, 5], numpy.uint32))
offsets2 = awkward1.layout.IndexU32(numpy.array([0, 2, 3, 3, 5], numpy.uint32))

def test_listarray_basic():
    array1 = awkward1.layout.ListArrayU32(starts1, stops1, content)
    array2 = awkward1.layout.ListArrayU32(starts2, stops2, array1)
    assert awkward1.tolist(array1) == [[1.1, 2.2, 3.3], [], [4.4, 5.5], [6.6], [7.7, 8.8, 9.9]]
    assert awkward1.tolist(array1[2]) == [4.4, 5.5]
    assert awkward1.tolist(array1[1:-1]) == [[], [4.4, 5.5], [6.6]]
    assert awkward1.tolist(array2) == [[[1.1, 2.2, 3.3], []], [[4.4, 5.5]], [], [[6.6], [7.7, 8.8, 9.9]]]
    assert awkward1.tolist(array2[1]) == [[4.4, 5.5]]
    assert awkward1.tolist(array2[1:-1]) == [[[4.4, 5.5]], []]

def test_listoffsetarray_basic():
    array1 = awkward1.layout.ListOffsetArrayU32(offsets1, content)
    array2 = awkward1.layout.ListOffsetArrayU32(offsets2, array1)
    assert awkward1.tolist(array1) == [[1.1, 2.2, 3.3], [], [4.4, 5.5], [6.6], [7.7, 8.8, 9.9]]
    assert awkward1.tolist(array1[2]) == [4.4, 5.5]
    assert awkward1.tolist(array1[1:-1]) == [[], [4.4, 5.5], [6.6]]
    assert awkward1.tolist(array2) == [[[1.1, 2.2, 3.3], []], [[4.4, 5.5]], [], [[6.6], [7.7, 8.8, 9.9]]]
    assert awkward1.tolist(array2[1]) == [[4.4, 5.5]]
    assert awkward1.tolist(array2[1:-1]) == [[[4.4, 5.5]], []]

def test_listarray_at():
    array1 = awkward1.layout.ListArrayU32(starts1, stops1, content)
    array2 = awkward1.layout.ListArrayU32(starts2, stops2, array1)
    assert awkward1.tolist(array1[2]) == [4.4, 5.5]
    assert awkward1.tolist(array1[2,]) == [4.4, 5.5]
    assert awkward1.tolist(array1[2, 1:]) == [5.5]
    assert awkward1.tolist(array1[2:, 0]) == [4.4, 6.6, 7.7]
    assert awkward1.tolist(array1[2:, -1]) == [5.5, 6.6, 9.9]

def test_listoffsetarray_at():
    array1 = awkward1.layout.ListOffsetArrayU32(offsets1, content)
    array2 = awkward1.layout.ListOffsetArrayU32(offsets2, array1)
    assert awkward1.tolist(array1[2,]) == [4.4, 5.5]
    assert awkward1.tolist(array1[2, 1:]) == [5.5]
    assert awkward1.tolist(array1[2:, 0]) == [4.4, 6.6, 7.7]
    assert awkward1.tolist(array1[2:, -1]) == [5.5, 6.6, 9.9]

def test_listarray_slice():
    array1 = awkward1.layout.ListArrayU32(starts1, stops1, content)
    array2 = awkward1.layout.ListArrayU32(starts2, stops2, array1)
    assert awkward1.tolist(array1[1:-1]) == [[], [4.4, 5.5], [6.6]]
    assert awkward1.tolist(array1[1:-1,]) == [[], [4.4, 5.5], [6.6]]
    assert awkward1.tolist(array2[1:-1]) == [[[4.4, 5.5]], []]
    assert awkward1.tolist(array2[1:-1,]) == [[[4.4, 5.5]], []]

def test_listoffsetarray_slice():
    array1 = awkward1.layout.ListOffsetArrayU32(offsets1, content)
    array2 = awkward1.layout.ListOffsetArrayU32(offsets2, array1)
    assert awkward1.tolist(array1[1:-1]) == [[], [4.4, 5.5], [6.6]]
    assert awkward1.tolist(array1[1:-1,]) == [[], [4.4, 5.5], [6.6]]
    assert awkward1.tolist(array2[1:-1]) == [[[4.4, 5.5]], []]
    assert awkward1.tolist(array2[1:-1,]) == [[[4.4, 5.5]], []]

def test_listarray_slice_slice():
    array1 = awkward1.layout.ListArrayU32(starts1, stops1, content)
    array2 = awkward1.layout.ListArrayU32(starts2, stops2, array1)
    assert awkward1.tolist(array1[2:]) == [[4.4, 5.5], [6.6], [7.7, 8.8, 9.9]]
    assert awkward1.tolist(array1[2:, 1:]) == [[5.5], [], [8.8, 9.9]]
    assert awkward1.tolist(array1[2:,:-1]) == [[4.4], [], [7.7, 8.8]]

def test_listoffsetarray_slice_slice():
    array1 = awkward1.layout.ListOffsetArrayU32(offsets1, content)
    array2 = awkward1.layout.ListOffsetArrayU32(offsets2, array1)
    assert awkward1.tolist(array1[2:]) == [[4.4, 5.5], [6.6], [7.7, 8.8, 9.9]]
    assert awkward1.tolist(array1[2:, 1:]) == [[5.5], [], [8.8, 9.9]]
    assert awkward1.tolist(array1[2:,:-1]) == [[4.4], [], [7.7, 8.8]]

def test_listarray_ellipsis():
    array1 = awkward1.layout.ListArrayU32(starts1, stops1, content)
    array2 = awkward1.layout.ListArrayU32(starts2, stops2, array1)
    if not py27:
        assert awkward1.tolist(array1[Ellipsis, 1:]) == [[2.2, 3.3], [], [5.5], [], [8.8, 9.9]]
        assert awkward1.tolist(array2[Ellipsis, 1:]) == [[[2.2, 3.3], []], [[5.5]], [], [[], [8.8, 9.9]]]

def test_listoffsetarray_ellipsis():
    array1 = awkward1.layout.ListOffsetArrayU32(offsets1, content)
    array2 = awkward1.layout.ListOffsetArrayU32(offsets2, array1)
    if not py27:
        assert awkward1.tolist(array1[Ellipsis, 1:]) == [[2.2, 3.3], [], [5.5], [], [8.8, 9.9]]
        assert awkward1.tolist(array2[Ellipsis, 1:]) == [[[2.2, 3.3], []], [[5.5]], [], [[], [8.8, 9.9]]]

def test_listarray_array_slice():
    array1 = awkward1.layout.ListArrayU32(starts1, stops1, content)
    array2 = awkward1.layout.ListArrayU32(starts2, stops2, array1)
    assert awkward1.tolist(array2[[0, 0, 1, 1, 1, 0]]) == [[[1.1, 2.2, 3.3], []], [[1.1, 2.2, 3.3], []], [[4.4, 5.5]], [[4.4, 5.5]], [[4.4, 5.5]], [[1.1, 2.2, 3.3], []]]
    assert awkward1.tolist(array2[[0, 0, 1, 1, 1, 0], :]) == [[[1.1, 2.2, 3.3], []], [[1.1, 2.2, 3.3], []], [[4.4, 5.5]], [[4.4, 5.5]], [[4.4, 5.5]], [[1.1, 2.2, 3.3], []]]
    assert awkward1.tolist(array2[[0, 0, 1, 1, 1, 0], :, 1:]) == [[[2.2, 3.3], []], [[2.2, 3.3], []], [[5.5]], [[5.5]], [[5.5]], [[2.2, 3.3], []]]

def test_listoffsetarray_array_slice():
    array1 = awkward1.layout.ListOffsetArrayU32(offsets1, content)
    array2 = awkward1.layout.ListOffsetArrayU32(offsets2, array1)
    assert awkward1.tolist(array2[[0, 0, 1, 1, 1, 0]]) == [[[1.1, 2.2, 3.3], []], [[1.1, 2.2, 3.3], []], [[4.4, 5.5]], [[4.4, 5.5]], [[4.4, 5.5]], [[1.1, 2.2, 3.3], []]]
    assert awkward1.tolist(array2[[0, 0, 1, 1, 1, 0], :]) == [[[1.1, 2.2, 3.3], []], [[1.1, 2.2, 3.3], []], [[4.4, 5.5]], [[4.4, 5.5]], [[4.4, 5.5]], [[1.1, 2.2, 3.3], []]]
    assert awkward1.tolist(array2[[0, 0, 1, 1, 1, 0], :, 1:]) == [[[2.2, 3.3], []], [[2.2, 3.3], []], [[5.5]], [[5.5]], [[5.5]], [[2.2, 3.3], []]]

def test_listarray_array():
    array1 = awkward1.layout.ListArrayU32(starts1, stops1, content)
    array2 = awkward1.layout.ListArrayU32(starts2, stops2, array1)
    assert awkward1.tolist(array1[numpy.array([2, 0, 0, 1, -1])]) == [[4.4, 5.5], [1.1, 2.2, 3.3], [1.1, 2.2, 3.3], [], [7.7, 8.8, 9.9]]
    assert awkward1.tolist(array1[numpy.array([2, 0, 0, -1]), numpy.array([1, 1, 0, 0])]) == [5.5, 2.2, 1.1, 7.7]

    content_deep = awkward1.layout.NumpyArray(numpy.array([[0, 0], [1, 10], [2, 20], [3, 30], [4, 40], [5, 50], [6, 60], [7, 70], [8, 80]]))
    starts1_deep = awkward1.layout.IndexU32(numpy.array([0, 3, 6]))
    stops1_deep = awkward1.layout.IndexU32(numpy.array([3, 6, 9]))
    array1_deep = awkward1.layout.ListArrayU32(starts1_deep, stops1_deep, content_deep)

    assert awkward1.tolist(array1_deep) == [[[0, 0], [1, 10], [2, 20]], [[3, 30], [4, 40], [5, 50]], [[6, 60], [7, 70], [8, 80]]]
    s = (numpy.array([2, 0, 0, -1]), numpy.array([1, 1, 0, 0]), numpy.array([0, 1, 0, 1]))
    assert numpy.array([[[0, 0], [1, 10], [2, 20]], [[3, 30], [4, 40], [5, 50]], [[6, 60], [7, 70], [8, 80]]])[s].tolist() == awkward1.tolist(array1_deep[s])

    s = (numpy.array([2, 0, 0, -1]), numpy.array([1, 1, 0, 0]), slice(1, None))
    assert numpy.array([[[0, 0], [1, 10], [2, 20]], [[3, 30], [4, 40], [5, 50]], [[6, 60], [7, 70], [8, 80]]])[s].tolist() == awkward1.tolist(array1_deep[s])

def test_listoffsetarray_array():
    array1 = awkward1.layout.ListOffsetArrayU32(offsets1, content)
    array2 = awkward1.layout.ListOffsetArrayU32(offsets2, array1)
    assert awkward1.tolist(array1[numpy.array([2, 0, 0, 1, -1])]) == [[4.4, 5.5], [1.1, 2.2, 3.3], [1.1, 2.2, 3.3], [], [7.7, 8.8, 9.9]]
    assert awkward1.tolist(array1[numpy.array([2, 0, 0, -1]), numpy.array([1, 1, 0, 0])]) == [5.5, 2.2, 1.1, 7.7]

    content_deep = awkward1.layout.NumpyArray(numpy.array([[0, 0], [1, 10], [2, 20], [3, 30], [4, 40], [5, 50], [6, 60], [7, 70], [8, 80]]))
    starts1_deep = awkward1.layout.IndexU32(numpy.array([0, 3, 6]))
    stops1_deep = awkward1.layout.IndexU32(numpy.array([3, 6, 9]))
    array1_deep = awkward1.layout.ListArrayU32(starts1_deep, stops1_deep, content_deep)

    assert awkward1.tolist(array1_deep) == [[[0, 0], [1, 10], [2, 20]], [[3, 30], [4, 40], [5, 50]], [[6, 60], [7, 70], [8, 80]]]
    s = (numpy.array([2, 0, 0, -1]), numpy.array([1, 1, 0, 0]), numpy.array([0, 1, 0, 1]))
    assert numpy.array([[[0, 0], [1, 10], [2, 20]], [[3, 30], [4, 40], [5, 50]], [[6, 60], [7, 70], [8, 80]]])[s].tolist() == awkward1.tolist(array1_deep[s])

    s = (numpy.array([2, 0, 0, -1]), numpy.array([1, 1, 0, 0]), slice(1, None))
    assert numpy.array([[[0, 0], [1, 10], [2, 20]], [[3, 30], [4, 40], [5, 50]], [[6, 60], [7, 70], [8, 80]]])[s].tolist() == awkward1.tolist(array1_deep[s])

def test_getitem_array_U32():
    content = awkward1.layout.NumpyArray(numpy.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]))
    listarray = awkward1.layout.ListArrayU32(awkward1.layout.IndexU32(numpy.array([0, 3, 3, 5, 6], numpy.uint32)), awkward1.layout.IndexU32(numpy.array([3, 3, 5, 6, 10], numpy.uint32)), content)

    @numba.njit
    def f1(q):
        return q[[2, 0, 0, 1]]

    assert awkward1.tolist(f1(listarray)) == [[3.3, 4.4], [0.0, 1.1, 2.2], [0.0, 1.1, 2.2], []]

    @numba.njit
    def f2(q):
        return q[[2, 0, 0, -1], 1]

    assert awkward1.tolist(f2(listarray)) == [4.4, 1.1, 1.1, 7.7]

    @numba.njit
    def f3(q):
        return q[[2, 0, 0, -1], [-1, -1, 0, 0]]

    assert awkward1.tolist(f3(listarray)) == [4.4, 2.2, 0.0, 6.6]

    listarray.setidentities()
    assert numpy.asarray(f1(listarray).identities).tolist() == [[2], [0], [0], [1]]
    assert numpy.asarray(f2(listarray).identities).tolist() == [[2, 1], [0, 1], [0, 1], [4, 1]]
    assert numpy.asarray(f3(listarray).identities).tolist() == [[2, 1], [0, 2], [0, 0], [4, 0]]

def test_deep_listarrayU32():
    content = awkward1.layout.NumpyArray(numpy.arange(2*3*5*7).reshape(-1, 7))
    offsetsA = numpy.arange(0, 2*3*5 + 5, 5)
    offsetsB = numpy.arange(0, 2*3 + 3, 3)
    startsA, stopsA = offsetsA[:-1], offsetsA[1:]
    startsB, stopsB = offsetsB[:-1], offsetsB[1:]

    listarrayAU32 = awkward1.layout.ListArrayU32(awkward1.layout.IndexU32(startsA), awkward1.layout.IndexU32(stopsA), content)
    modelA = numpy.arange(2*3*5*7).reshape(2*3, 5, 7)

    listarrayBU32 = awkward1.layout.ListArrayU32(awkward1.layout.IndexU32(startsB), awkward1.layout.IndexU32(stopsB), listarrayAU32)
    modelB = numpy.arange(2*3*5*7).reshape(2, 3, 5, 7)

    @numba.njit
    def f1(q):
        return q[1, 2, 4]

    assert awkward1.tolist(f1(listarrayBU32)) == awkward1.tolist(f1(modelB))

    @numba.njit
    def f2(q):
        return q[1, -1, 4, -2]

    assert f2(listarrayBU32) == f2(modelB)

    @numba.njit
    def f3(q):
        return q[1:, ::2, 1:-1, 5::-1]

    assert awkward1.tolist(f3(listarrayBU32)) == awkward1.tolist(f3(modelB))

    @numba.njit
    def f4(q):
        return q[numpy.array([0, 1, 1, 0]), ::2, 1:-1, 5::-1]

    assert awkward1.tolist(f4(listarrayBU32)) == awkward1.tolist(f4(modelB))

def test_deep_listoffsetarrayU32():
    content = awkward1.layout.NumpyArray(numpy.arange(2*3*5*7).reshape(-1, 7))
    offsetsA = numpy.arange(0, 2*3*5 + 5, 5)
    offsetsB = numpy.arange(0, 2*3 + 3, 3)

    listoffsetarrayAU32 = awkward1.layout.ListOffsetArrayU32(awkward1.layout.IndexU32(offsetsA), content)
    modelA = numpy.arange(2*3*5*7).reshape(2*3, 5, 7)

    listoffsetarrayBU32 = awkward1.layout.ListOffsetArrayU32(awkward1.layout.IndexU32(offsetsB), listoffsetarrayAU32)
    modelB = numpy.arange(2*3*5*7).reshape(2, 3, 5, 7)

    @numba.njit
    def f1(q):
        return q[1, 2, 4]

    assert awkward1.tolist(f1(listoffsetarrayBU32)) == awkward1.tolist(f1(modelB))

    @numba.njit
    def f2(q):
        return q[1, -1, 4, -2]

    assert f2(listoffsetarrayBU32) == f2(modelB)

    @numba.njit
    def f3(q):
        return q[1:, ::2, 1:-1, 5::-1]

    assert awkward1.tolist(f3(listoffsetarrayBU32)) == awkward1.tolist(f3(modelB))

    @numba.njit
    def f4(q):
        return q[numpy.array([0, 1, 1, 0]), ::2, 1:-1, 5::-1]

    assert awkward1.tolist(f4(listoffsetarrayBU32)) == awkward1.tolist(f4(modelB))
