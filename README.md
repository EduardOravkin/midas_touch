# vela_eo

### Create the conda environmnent by running
```
conda env create -f env.yml
conda activate midas_env
python -m ipykernel install --user --name midas_env
```
Then to install the midastouch package (locally in editable mode) go to the repo ``midastouch/`` and run
```
conda deactivate
conda install conda-build
conda activate midas_env
conda develop midastouch
```


