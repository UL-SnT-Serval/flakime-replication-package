# Analysis

The python scripts contained in this repository allow the analysis of the data contained in the data folder and generated graphics that will be saved to the `$/figures/` folder and output statistics about the data directly in the console.

# Description
- `arja.py`: analyzes the results produced by `$/run/run-arja-all.sh` which executes the ARJA APR tool. It reads ARJA output files stored in `$/data/apr/arja` and generate the `$/figures/arja-*.pdf` files.
- `mutation.py`: analyzes the results produced by `$/run/run-pit-all.sh` which executes the PIT mutation tool. It reads custom csv files stored in `$/data/mutation` and generate the `$/figures/mutation-*.pdf` files.
- `prapr.py`: analyzes the results produced by `$/run/run-prapr-all.sh` which executes the PRAPR APR tool. It reads PRAPR output files stored in `$/data/apr/prapr` and generate the `$/figures/prapr-*.pdf` files.
- `probabilities.py`: analyzes the results from `$/data/overview` which are the probability of each test to flake according the the vocabulary model.
- `sbfl.py`: analyzes the results produced by `$/run/run-sbfl-all.sh` which executes the GZoltar SBFL tool. It reads GZoltar output files stored in `$/data/sbfl` and generate the `$/figures/prapr-*.pdf` files.

## Requirements

- Python `3.8.8`
- pip3
- **Extract the data archives** contained in `$/data/` using `$/run/extract-data.sh`.

## Running the scripts

0. Although not required, we recommend to create a dedicated **virtualenv** to avoid any conflicts.
1. move to the analysis directory ```cd $/analysis/```
2. run ```pip3 install -r requirements.txt``` to ensure all the dependencies are present.
3. run any script by calling ```python <script_name>.py```. None of the scripts require arguments.
4. the results are stored in the folder `$/figures/`.