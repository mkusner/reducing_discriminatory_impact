# reducing_discriminatory_impact
Code for "Making Decisions that Reduce Discriminatory Impact" ICML, 2019

Detailed documentation will appear soon, as will serious code cleaning! For now you can run the following code to generate the results for Figures 4 and 5 in the paper:
```
python train_schools.py
python intervention.py
python for_map_plotting.py
```

To generate plots for Figure 4 run code in `plot.ipynb`.

To generate Figure 5 maps run code in `plot_intervention_maps.R`

The script `intervention_other.py` will compute results for parity and minority constraints and the above two scripts will generate plots for these results.
