# Midas Touch Project

A project in collaboration with https://vela.partners to rank VC investors. The ranking is done by a graph ranking algorithm based on around ~100 000 datapoints of the investments of the respective VC funds. The ranking algorithm is constructed so that it assigns a higher score to investors which invest with a fixed set of brand-name investors (hand-picked).

## Installation and basic usage

An installation of python with version at least 3.10 is assumed.

### Conda environmnent

From the root of the repository, run
```
conda env create -f env.yml
conda activate midas_env
python -m ipykernel install --user --name midas_env
```
Then to install the midastouch package (locally in editable mode) run
```
conda deactivate
conda install conda-build
conda activate midas_env
conda develop midastouch
```

# Adding the data into the project

First, download the data from the following link https://drive.google.com/drive/folders/1E5RHuTIr77K4Wb8CDRzimMnjjG1Pvwpn?usp=sharing, and place the `Data/` folder along with its content into the root directory. The resulting data should look something like this:
```
root/
    Data/
        test_data/ ...
        ventech_RMap.csv
        midas_touch_brand_investor_list.csv
        midas_touch_dataset_eduard.csv
```
Second, download the data of the performed experiments from the following link https://drive.google.com/drive/folders/1HUzklJK3kZdm90moTBeyEjYUTh9xbdqr?usp=sharing, and place the `experiments/` folder along with its content into the root directory. The resulting data should look something like this:
```
root/
    experiments/
        experiment_timestamp_1/
            experiment_timestamp_1.csv
            params_timestamp_1.py
        experiment_timestamp_2/..
        .
        .
        .
```

# Analyzing the data

Once the data is downloaded and placed in the correct directories, run
`
jupyter lab analysis.ipynb
`
from the root of the directory, choose the `midas_env` kernel in the jupyter notebook, and go through the jupyter notebook which guides one through the analysis of a sample experiment.
In the folder 
```
experiments/
    midas/
        selected_experiments/
                10_or_more_investments/
                    .
                    .
                30_or_more_investments/
                    .
                    .
```
there are 6 selected experiments (different in the parameters used). Go to their folders and there you will find similar `analysis.ipynb` notebooks
which guide through the analysis of the data. 

# Running new experiments

To run new experiments create a new folder `new_experiment` in `experiments/midas/` and create a `run.py` file inside `experiments/midas/new_experiment`. 
Look at `experiments/midas/experiment_2021_12_17_18_00_00/run.py` to find out how the new `run.py` file should look like and customize it to your needs.
Finally, run 
```
python run.py
```
from `experiments/midas/new_experiment`.






