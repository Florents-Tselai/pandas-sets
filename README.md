# Pandas Sets: Set-oriented Operations in Pandas

If you store standard Python `set`s or `frozenset`s in your `Series` or `DataFrame` objects, you'll find this useful.

The `pandas_sets` package adds a `.set` accessor to any pandas `Series` object;
it's like `.dt` for `datetime` or `.str` for `string`, but for [`set`](https://docs.python.org/3.7/library/stdtypes.html#set).

It exposes all public methods available in the standard [`set`](https://docs.python.org/3.7/library/stdtypes.html#set).

## Installation
```bash
pip install pandas-sets
```
Just import the `pandas_sets` package and it will register a `.set` accessor to any `Series` object.

```python
import pandas_sets
```

## Examples
```python
import pandas_sets
import pandas as pd
df = pd.DataFrame({'post': [1, 2, 3, 4],
                    'tags': [{'python', 'pandas'}, {'philosophy', 'strategy'}, {'scikit-learn'}, {'pandas'}]
                   })

pandas_posts = df[df.tags.set.contains('pandas')]

pandas_posts.tags.set.add('data')

pandas_posts.tags.set.update({'data', 'analysis'})

pandas_posts.tags.set.len()
```

## Notes
* The implementation is primitive for now. It's based heavily on the pandas' core [`StringMethods`](https://github.com/pandas-dev/pandas/blob/52a2bb490556a86c5f756465320c18977dbe1c36/pandas/core/strings.py#L1783) implementation.
* The public API has been tested for most expected scenarios.
* The API will need to be extended to handle `NA` values appropriately.
