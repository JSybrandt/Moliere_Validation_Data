Validation Set and Results
==========================

In this repo are the data and results for our validation effort corresponding with [THIS PAPER](http://sybrandt.com/publication/validation-and-topic-driven-ranking/).

Contents:

- `./evaluatedResults`
  - contains eval files, results from MOLIERE
  - contains scripts to create ROC charts from results

- `./wholeSet`
  - contains three `pair.txt` files, which are pairs of UMLS terms extracted from SemMedDB.
  - extraction uses cut-year of 2010
  - we sub-sampled this set to perform our validation.

- `./evaluatedSubset`
  - contains three `pair.txt` files, which are subsets of their `./wholeSet` counterparts.
  - these are the predicate pairs we actually used to generated our ROC curves.


You can replicate our results using the code and data provided in [THIS REPO](https://github.com/JSybrandt/Moliere_Query_Runner).

If you use our validation method or data, please cite us at:

```
@article {Sybrandt263897,
	author = {Sybrandt, Justin and Safro, Ilya},
	title = {Validation and Topic-driven Ranking for Biomedical Hypothesis Generation Systems},
	year = {2018},
	doi = {10.1101/263897},
	publisher = {Cold Spring Harbor Laboratory},
	URL = {https://www.biorxiv.org/content/early/2018/02/11/263897},
	eprint = {https://www.biorxiv.org/content/early/2018/02/11/263897.full.pdf},
	journal = {bioRxiv}
}
```

