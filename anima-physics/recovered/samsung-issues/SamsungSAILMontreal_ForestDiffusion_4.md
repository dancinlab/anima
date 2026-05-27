https://github.com/SamsungSAILMontreal/ForestDiffusion/issues/4
# KeyError:  not in index then try to pass categorical index

Reproducibly example:

```
from ForestDiffusion import ForestDiffusionModel
import pandas as pd
import numpy as np

train = pd.DataFrame(
        np.random.randint(-10, 150, size=(100, 4)), columns=list("ABCD")
    )
forest_model = ForestDiffusionModel(train, label_y=None, n_t=50,
                                    duplicate_K=100,
                                    cat_indexes=[1],
                                    diffusion_type='flow', n_jobs=-1)
 
generated_df = forest_model.generate(batch_size=train.shape[0])
```



ERROR


```
KeyError                                  Traceback (most recent call last)
Cell In[26], line 13
      5 train = pd.DataFrame(
      6         np.random.randint(-10, 150, size=(100, 4)), columns=list("ABCD")
      7     )
      8 forest_model = ForestDiffusionModel(train, label_y=None, n_t=50,
      9                                     duplicate_K=100,
     10                                     cat_indexes=[1],
     11                                     diffusion_type='flow', n_jobs=-1)
---> 13 generated_df = forest_model.generate(batch_size=train.shape[0])

File ~\mambaforge\lib\site-packages\ForestDiffusion\diffusion_with_trees_class.py:275, in ForestDiffusionModel.generate(self, batch_size, n_t)
    273 solution = ode_solved.reshape(y0.shape[0], self.c) # [b, c]
    274 solution = self.unscale(solution)
--> 275 solution = self.clean_onehot_data(solution)
    276 solution = self.clip_extremes(solution)
    278 # Concatenate y label if needed

File ~\mambaforge\lib\site-packages\ForestDiffusion\diffusion_with_trees_class.py:186, in ForestDiffusionModel.clean_onehot_data(self, X)
    184     X_names_after[cat_vars_indexes[0]] = unique_prefixes[i] # gender_a -> gender
    185   df = pd.DataFrame(X, columns = X_names_after) # to Pandas
--> 186   df = df[self.X_names_before] # remove all gender_b, gender_c and put everything in the right order
    187   X = df.to_numpy()
    188 return X

File ~\mambaforge\lib\site-packages\pandas\core\frame.py:3813, in DataFrame.__getitem__(self, key)
   3811     if is_iterator(key):
   3812         key = list(key)
-> 3813     indexer = self.columns._get_indexer_strict(key, "columns")[1]
   3815 # take() does not accept boolean indexers
   3816 if getattr(indexer, "dtype", None) == bool:

File ~\mambaforge\lib\site-packages\pandas\core\indexes\base.py:6070, in Index._get_indexer_strict(self, key, axis_name)
   6067 else:
   6068     keyarr, indexer, new_indexer = self._reindex_non_unique(keyarr)
-> 6070 self._raise_if_missing(keyarr, indexer, axis_name)
   6072 keyarr = self.take(indexer)
   6073 if isinstance(key, Index):
   6074     # GH 42790 - Preserve name from an Index

File ~\mambaforge\lib\site-packages\pandas\core\indexes\base.py:6133, in Index._raise_if_missing(self, key, indexer, axis_name)
   6130     raise KeyError(f"None of [{key}] are in the [{axis_name}]")
   6132 not_found = list(ensure_index(key)[missing_mask.nonzero()[0]].unique())
-> 6133 raise KeyError(f"{not_found} not in index")

KeyError: "['1'] not in index"
```
