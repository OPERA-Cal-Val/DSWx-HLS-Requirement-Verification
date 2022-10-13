from pathlib import Path

import click
import papermill as pm
from tqdm import tqdm

from verification.es_db import get_DSWX_doc
from verification.val_db import get_finalized_validation_datasets, get_HLS_id

ipynb_dir = Path('out_notebooks')
ipynb_dir.mkdir(exist_ok=True)


def check_dswx_status(hls_id):
    try:
        get_DSWX_doc(hls_id)
        return True
    except ValueError:
        return False


@click.command()
def main():

    df_val = get_finalized_validation_datasets()
    planet_ids = df_val.image_name.to_list()
    hls_ids = [get_HLS_id(planet_id) for planet_id in planet_ids]
    dswx_ready = [check_dswx_status(hls_id) for hls_id in hls_ids]

    # Filter
    planet_ids = [planet_id for (k, planet_id) in enumerate(planet_ids) if dswx_ready[k]]
    hls_ids = [hls_id for (k, hls_id) in enumerate(hls_ids) if dswx_ready[k]]
    print(f'There are {len(dswx_ready)} validation datasets, and of those, '
          f'there are {sum(dswx_ready)} dswx products available')

    dswx_ids = [get_DSWX_doc(hls_id)['id'] for hls_id in hls_ids]

    for planet_id, dswx_id in zip(tqdm(planet_ids, desc='Validation Datasets'), dswx_ids):

        print(f'Planet ID: {planet_id}')
        out_notebook_path = ipynb_dir / f'{dswx_id}.ipynb'
        pm.execute_notebook('0-Verify_Requirements.ipynb',
                            output_path=out_notebook_path,
                            parameters={'PLANET_ID': planet_id}
                            )


if __name__ == '__main__':
    main()
