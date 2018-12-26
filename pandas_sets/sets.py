from pandas.api.extensions import register_series_accessor
from pandas.core import strings
from pandas.core.base import NoNewAttributesMixin
from pandas.core.common import ABCSeries
from pandas.core.dtypes.common import is_bool_dtype
from pandas.core.dtypes.common import is_list_like
from pandas.core.dtypes.common import is_object_dtype

copy = strings.copy


def is_set_type(data):
    return isinstance(data, set)


def _map(*args, **kwargs):
    return strings._map(*args, **kwargs)


def _na_map(*args, **kwargs):
    return strings._na_map(*args, **kwargs)


def set_contains(arr, elem):
    pass


def set_isdisjoint(arr, other):
    pass


def set_issubset(arr, other):
    pass


def set_issuperset(arr, other):
    pass


def set_union(arr, *others):
    pass


def set_intersection(arr, *others):
    pass


def set_difference(arr, *others):
    pass


def set_symmetic_difference(arr, other):
    pass


def set_copy(arr):
    pass


def set_update(arr, *others):
    pass


def set_intersection_update(arr, *others):
    pass


def set_difference_update(arr, *others):
    pass


def set_symmetric_difference_update(arr, other):
    pass


def set_add(arr, elem):
    def f(x):
        x.add(elem)
        return x

    return _map(f, arr)


def set_remove(arr, elem):
    pass


def set_discard(arr, elem):
    pass


def set_pop(arr):
    pass


def set_clear(arr):
    pass


@register_series_accessor("set")
class SetMethods(NoNewAttributesMixin):
    """
    Intends to have an implementation similar to `pandas.core.strings.StringMethods`

    Vectorized string functions for Series. NAs stay NA unless
    handled otherwise by a particular method. Patterned after Python's set
    methods.

    Examples
    --------
    >>> s.set.union({ 1, 2 ,3})
    >>> s.set.intersection({})
    """

    def __init__(self, data):
        self._validate(data)
        self._data = data
        self._orig = data

    def _wrap_result(self, result, use_codes=True,
                     name=None, expand=None):

        # TODO: this was blindly copied from `strings.StringMethods._wrap_result` for noew
        from pandas.core.index import Index, MultiIndex

        # for category, we do the stuff on the categories, so blow it up
        # to the full series again
        # But for some operations, we have to do the stuff on the full values,
        # so make it possible to skip this step as the method already did this
        # before the transformation...
        # if use_codes and self._is_categorical:
        #    result = take_1d(result, self._orig.cat.codes)

        if not hasattr(result, 'ndim') or not hasattr(result, 'dtype'):
            return result
        assert result.ndim < 3

        if expand is None:
            # infer from ndim if expand is not specified
            expand = False if result.ndim == 1 else True

        elif expand is True and not isinstance(self._orig, Index):
            # required when expand=True is explicitly specified
            # not needed when inferred

            def cons_row(x):
                if is_list_like(x):
                    return x
                else:
                    return [x]

            result = [cons_row(x) for x in result]
            if result:
                # propagate nan values to match longest sequence (GH 18450)
                max_len = max(len(x) for x in result)
                result = [x * max_len if len(x) == 0 or x[0] is np.nan
                          else x for x in result]

        if not isinstance(expand, bool):
            raise ValueError("expand must be True or False")

        if expand is False:
            # if expand is False, result should have the same name
            # as the original otherwise specified
            if name is None:
                name = getattr(result, 'name', None)
            if name is None:
                # do not use logical or, _orig may be a DataFrame
                # which has "name" column
                name = self._orig.name

        # Wait until we are sure result is a Series or Index before
        # checking attributes (GH 12180)
        if isinstance(self._orig, Index):
            # if result is a boolean np.array, return the np.array
            # instead of wrapping it into a boolean Index (GH 8875)
            if is_bool_dtype(result):
                return result

            if expand:
                result = list(result)
                out = MultiIndex.from_tuples(result, names=name)
                if out.nlevels == 1:
                    # We had all tuples of length-one, which are
                    # better represented as a regular Index.
                    out = out.get_level_values(0)
                return out
            else:
                return Index(result, name=name)
        else:
            index = self._orig.index
            if expand:
                cons = self._orig._constructor_expanddim
                return cons(result, columns=name, index=index)
            else:
                # Must be a Series
                cons = self._orig._constructor
                return cons(result, name=name, index=index)

    @staticmethod
    def _validate(data):
        """
        For now we assume that the dtype is already a `set`.
        Remains to be decided if list-like structures should be implicitly converted to sets
        """
        if not (isinstance(data, ABCSeries)
                and is_object_dtype(data)
                and data.map(is_list_like).all()
                and data.map(is_set_type).all()
        ):
            raise AttributeError("Can only use .set accessor with object dtype."
                                 "All values must be of `set` type too."
                                 "Null values` are rejected. "
                                 "Better use something like fillna([]) before.")

    def len(self):
        # TODO make it use _no_args_wrapper like the StringMethods equivalent does
        # return self._data.map(set).map(len)
        return self._wrap_result(_na_map(len, self._data))

    def contains(self, elem):
        f = lambda x: elem in x
        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def isdisjoint(self, other):
        f = lambda x: x.isdisjoint(other)
        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def issubset(self, other):
        f = lambda x: x.issubset(other)
        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def issuperset(self, other):
        f = lambda x: x.issuperset(other)
        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def union(self, *others):
        f = lambda x: x.union(others)
        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def intersection(self, *others):
        f = lambda x: x.intersection(others)
        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def difference(self, *others):
        f = lambda x: x.difference(others)
        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def symmetric_difference(self, other):
        f = lambda x: x.symmetric_difference(other)
        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def copy(self):
        # TODO make it use _no_args_wrapper like the StringMethods equivalent does
        return self._wrap_result(_na_map(set.copy, self._data))

    def update(self, *others):
        def f(x):
            x.update(*others)
            return x

        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def intersection_update(self, *others):
        def f(x):
            x.intersection_update(*others)
            return x

        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def difference_update(self, *others):
        def f(x):
            x.difference_update(others)
            return x

        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def symmetric_difference_update(self, other):
        def f(x):
            x.symmetric_difference_update(other)
            return x

        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def add(self, elem):
        result = set_add(self._data, elem)
        return self._wrap_result(result)

    def remove(self, elem):
        def f(x):
            x.remove(elem)
            return x

        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def discard(self, elem):
        def f(x):
            x.discard(elem)
            return x

        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def pop(self):
        # TODO make it use _no_args_wrapper like the StringMethods equivalent does
        def f(x):
            x.pop()
            return x

        result = _na_map(f, self._data)

        return self._wrap_result(result)

    def clear(self):
        # TODO make it use _no_args_wrapper like the StringMethods equivalent does
        def f(x):
            x.clear()
            return x

        result = _na_map(f, self._data)

        return self._wrap_result(result)

    @classmethod
    def _make_accessor(cls, data):
        cls._validate(data)
        return cls(data)
