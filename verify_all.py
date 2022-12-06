from pathlib import Path

import click
import papermill as pm
import pandas as pd

from tqdm import tqdm

from verification.val_db import get_finalized_validation_datasets, get_HLS_id

ipynb_dir = Path('out_notebooks')
ipynb_dir.mkdir(exist_ok=True)


@click.command()
def main():

    df_validation_table = pd.read_csv('validation_table_data.csv')
    planet_ids = df_validation_table.planet_id.to_list()
    #hls_ids = df_validation_table.hls_id.to_list()
    dswx_ready = df_validation_table.dswx_urls.to_list()

    # Filter
    planet_ids = [planet_id for (k, planet_id) in enumerate(planet_ids) if dswx_ready[k]]
    #hls_ids = [hls_id for (k, hls_id) in enumerate(hls_ids) if dswx_ready[k]]
    print(f'There are {len(planet_ids)} validation datasets, and of those, '
          f'there are {len(dswx_ready)} DSWx products available')

    dswx_ids = [dswx_ready for (k, dswx_ready) in enumerate(dswx_ready) if dswx_ready[k]]

    for planet_id, dswx_id in zip(tqdm(planet_ids, desc='Validation Datasets'), dswx_ids):

        print(f'Planet ID: {planet_id}')
        out_notebook_path = ipynb_dir / (dswx_ids[0].split('_B01')[0].split('/')[-1] + '.ipynb')
        pm.execute_notebook('0-Verify_Requirements.ipynb',
                            output_path=out_notebook_path,
                            parameters={'PLANET_ID': planet_id}
                            )

    pm.execute_notebook('1-Read_Verification.ipynb',
                        output_path=ipynb_dir / '1-Read_Verification.ipynb'
                        )


if __name__ == '__main__':
    main()
