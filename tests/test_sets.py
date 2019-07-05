from unittest import TestCase
import pandas_sets
import pandas.util.testing as tm
from pandas import Series, DataFrame

"""
Currently testing "ideal-world scenarios"

TODO
* Test with nulls etc. Default values there? E.g. with set.pop / set.discard
* Decide what to do when series are of iterable types etc.
"""


class APITestCase(TestCase):
    def setUp(self):
        pass

    @property
    def simple_case_no_na_with_empty(self):
        return Series({
            'a': set([1]),
            'b': set([3, 4, 5]),
            'c': set([])
        })

    @property
    def frozenset_no_na_with_empty(self):
        return Series({
            'a': frozenset([1]),
            'b': frozenset([3, 4, 5]),
            'c': frozenset([])
        })

    @property
    def simple_case_no_na_without_empty(self):
        return Series({
            'a': set([1]),
            'b': set([3, 4, 5])
        })

    def test_validate(self):
        # TODO
        pass

    def test_len(self):
        tm.assert_series_equal(self.simple_case_no_na_with_empty.set.len(), Series({
            'a': 1,
            'b': 3,
            'c': 0
        }))

    def test_add(self):
        tm.assert_series_equal(self.simple_case_no_na_with_empty.set.add(1), Series({
            'a': {1},
            'b': {1, 3, 4, 5},
            'c': {1}
        }))

    def test_contains(self):
        tm.assert_series_equal(self.simple_case_no_na_with_empty.set.contains(1), Series({
            'a': True,
            'b': False,
            'c': False
        }))

    def test_isdisjoint(self):
        tm.assert_series_equal(self.simple_case_no_na_with_empty.set.isdisjoint({3, 4}),
                               Series({
                                   'a': True,
                                   'b': False,
                                   'c': True
                               }))

    def test_issubset(self):
        pass

    def test_issuperset(self):
        pass

    def test_union(self):
        pass

    def test_pop(self):

        # Assert raises KeyError on empty set
        with self.assertRaises(KeyError):
            self.simple_case_no_na_with_empty.set.pop()

        s = self.simple_case_no_na_without_empty.set.pop()
        tm.assert_series_equal(s.set.len(),
                               Series({
                                   'a': 0,
                                   'b': 2
                               }))

    def test_frozensets_are_allowed(self):
        tm.assert_series_equal(self.frozenset_no_na_with_empty.set.contains(1), Series({
            'a': True,
            'b': False,
            'c': False
        }))
