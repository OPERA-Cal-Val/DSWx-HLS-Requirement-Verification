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

## Generating the static `validation_table_data.csv`

This mirrors the current validation clone. To generate this table, one must additionally have:

1. JPL VPN access and be connected to the VPN
2. Have group access to the validation clone (that requires coordination with HySDS to be added to the appropriate LDAP group)
3. Create a `.env` file with JPL credentials.

Specifically, for 3. the `.env` should look like

```
ES_USERNAME='<JPL USERNAME>'
ES_PASSWORD='<JPL PASSWORD>'
```

After that is done, then run the notebook [_create_validation_table.ipynb](_create_validation_table.ipynb) to create this table.

## Contributing

1. Create a branch from dev and create a pull request.
2. Do you development.
3. For local `git diff`, use `nbdiff --ignore-id` as cell ids are required and updated on each change for newer versions of nbformat. Github will provide a prettier way of viewing notebook differences.
4. Run `pytest .` in this repository to ensure working of the notebooks. We do not use github actions (yet).
5. Have another member review.

<!--
3. Make sure to run before you commit:

   ```
   jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --ClearMetadataPreprocessor.preserve_cell_metadata_mask='[("tags")]' --ClearMetadataPreprocessor.preserve_nb_metadata_mask='{"language_info", "name", "kernelspec"}' --inplace *.ipynb
   ```

    This will clear ouput and transient cell metadata (including when you executed your notebook) for easier version control. It will preserve cell tags (for papermill and the kernel information) -->
