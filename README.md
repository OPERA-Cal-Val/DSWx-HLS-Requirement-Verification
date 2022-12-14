# Verification of DSWx-HLS Validation Datasets

This repository compares provisional OPERA DSWx-HLS products with validation datasets.

## Setup

In your `~/.netrc`, place earthdata login credentials:

```
machine urs.earthdata.nasa.gov
    login <username>
    password <password>
```

## Install
It is recommended to install `mamba` in the user's base environment to speed up the installation process:

`conda install -c conda-forge mamba`

From this repo:

1. `mamba env create -f environment.yml`
3. `conda activate dswx_val`

## To run notebook with kernel

After activatating your environment (i.e. `conda activate dswx_val`), then

`python -m ipykernel install --user --name dswx_val`


## Checking All Validation Datasets with `verify_all.py`

Run the papermill script with:

```
python verify_all.py
```

## Contributing

1. Create a branch from dev and create a pull request.
2. Do you development.
3. Make sure to run before you commit:

   ```
   jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --ClearMetadataPreprocessor.preserve_cell_metadata_mask='[("tags")]' --ClearMetadataPreprocessor.preserve_nb_metadata_mask='{"language_info", "name", "kernelspec"}' --inplace *.ipynb
   ```

    This will clear ouput and transient cell metadata (including when you executed your notebook) for easier version control. It will preserve cell tags (for papermill and the kernel information)

4. For local `git diff`, use `nbdiff --ignore-id` as cell ids are required and updated on each change for newer versions of nbformat. Github will provide a prettier way of viewing notebook differences.
5. Run `pytest .` in this repository to ensure working of the notebooks. We do not use github actions (yet).
6. Have another member review.

