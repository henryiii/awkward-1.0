# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import numbers

from awkward._v2.contents.content import Content


class RegularArray(Content):
    def __init__(self, content, size, zeros_length=0):
        if not isinstance(content, Content):
            raise TypeError(
                "{0} 'content' must be a Content subtype, not {1}".format(
                    type(self).__name__, repr(content)
                )
            )
        if not (isinstance(size, numbers.Integral) and size >= 0):
            raise TypeError(
                "{0} 'size' must be a non-negative integer, not {1}".format(
                    type(self).__name__, size
                )
            )
        if not (isinstance(zeros_length, numbers.Integral) and zeros_length >= 0):
            raise TypeError(
                "{0} 'zeros_length' must be a non-negative integer, not {1}".format(
                    type(self).__name__, zeros_length
                )
            )

        self._content = content
        self._size = size
        if size != 0:
            self._length = len(content) // size  # floor division
        else:
            self._length = zeros_length

    @property
    def size(self):
        return self._size

    @property
    def content(self):
        return self._content

    def __len__(self):
        return self._length

    def __repr__(self):
        return self._repr("", "", "")

    def _repr(self, indent, pre, post):
        out = [indent, pre, "<RegularArray len="]
        out.append(repr(str(len(self))))
        out.append(" size=")
        out.append(repr(str(self._size)))
        out.append(">\n")
        out.append(self._content._repr(indent + "    ", "<content>", "</content>\n"))
        out.append(indent)
        out.append("</RegularArray>")
        out.append(post)
        return "".join(out)

    def _getitem_at(self, where):
        if where < 0:
            where += len(self)
        if 0 > where or where >= len(self):
            raise IndexError("array index out of bounds")
        return self._content[(where) * self._size : (where + 1) * self._size]

    def _getitem_range(self, where):
        start, stop, step = where.indices(len(self))
        zeros_length = stop - start
        start *= self._size
        stop *= self._size
        return RegularArray(self._content[start:stop], self._size, zeros_length)

    def _getitem_field(self, where):
        return RegularArray(self._content[where], self._size, self._length)

    def _getitem_fields(self, where):
        return RegularArray(self._content[where], self._size, self._length)
