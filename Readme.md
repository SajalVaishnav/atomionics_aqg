## Objective
Ideally we want data in the following form:
`observed_chirp_rate, [noise_data], [constants], observed_fraction`

So that we can learn the function `f(observed_chirp_rate, [noise_data]) -> corrected_chirp_rate`. Then we calculate `predicted_fraction = sine(corrected_chirp_rate, [constants])`. And if training succeeded, then we get increased overlap between 	`predicted_fractions` and `observed_fractions`.

So the codebase is divided between these two objectives. `compile_data.ipynb` produces the data in desired format, while `train.ipynb` handles the actual training on the data.

### compile_data.ipynb
The main objective with this file is to create datafiles which could then be used to train any models.

To re-iterate: we want data in the following form:
`observed_chirp_rate, [noise_data], [constants], observed_fraction`

To achieve this we go through the following steps.

>For each `master_run`:
>1. Get `data0`, `data1`, `data2`
> 		- Here data0, data1, data2 are raw pickle files 
>2. Get `windows0`, `windows1`, `windows2`
>		- We use the trigger column in the data files to identify raman pulse windows
>3. Get `window_stats0`, `window_stats1`, `window_stats2`
> 		- We obtain `[noise_data]` for every raman window
>4. Combine `window_stats0`, `window_stats1`, `window_stats2` into `combined_window_stats`
>5. `chirp_up_window_stats = combined_window_stats[0::2]`		
>6. `chirp_down_window_stats = combined_window_stats[1::2]`
>		- We can do the above two steps since we know that the experiment alternates between chirp_up and chirp_down
>7. Get `chirp_up_data` from `chirp_up_csv_path`
>8. Get `chirp_down_data` from `chirp_down_csv_path`
>		- We load `chirp_rate, fraction` columns from fringes_data.csv for both chirp_up and chirp_down directions
>9. Append `[constants]` to `compiled_constants.csv`
>		- We calculate the required `[constants]` for both chirp_up and chirp_down and append them to `compiled_constants.csv`
>10. Append `chirp_up_window_stats` to `chirp_up_data`
>11. Append `chirp_down_window_stats` to `chirp_down_data`
> 		- After this step chirp_up_data and chirp_down_data have the shape `master_run, chirp_rate, fraction, [noise_data]`
>12. Save the combined dataframe to `compiled_data\master_run_chirp_up.csv` and `compiled_data\master_run_chirp_down.csv` respectively

### train.ipynb

For training we go through the following steps:
>1. Choose a `chir_direction`
>2. Load corresponding `compiled_data\compiled_ + {chirp_direction}.pkl` and split it 80/20 into `train_data_df` and `test_data_df`
>3. Load `[constants]` into `compiled_constants_df`
>4. Get `training_data` and `observed_fractions` from `train_data_df`
>5. Define a `model` to approximate the function `f(observed_chirp_rate, [noise_data]) -> corrected_chirp_rate`
>		- `predicted_fraction = sine(corrected_chirp_rate, [constants])`
>6. Currently I am using a NN, but we'll need to try lots of different things:
>		- Symbolic regression
>		- Support Vector Regression
>		- Random Forest Regressor
>		- etc.
>7. Plot, for every `(master-run, chir_direction)`:
>		- `observed_fractions` vs `corrected_chirp_rates` as `plot1`
>		- `observed_fractions` vs `observed_chirp_rates` as `plot2`
>		- Ideally, if training succeeded then `plot1` will have more overlap with the `sine` function
>
