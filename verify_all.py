from pathlib import Path

import click
import pandas as pd
import papermill as pm
from tqdm import tqdm

ipynb_dir = Path('out_notebooks')
ipynb_dir.mkdir(exist_ok=True)


@click.option('--confidence_classes',
              default=None,
              type=list,
              help='See product spec - use only desired classes to be ')
@click.option('--class_selection_from',
              default='val',
              type=click.Choice(['dswx', 'val']),
              help='How pixels from each class are chosen - using labels from dswx or val classification')
@click.option('--downsample_to_3_ha',
              default=False,
              type=bool,
              help='Downsample both datasets to 3 ha - see notebooks for details'
              )
@click.command()
def main(confidence_classes, class_selection_from, downsample_to_3_ha):

    conf_temp = "-".join(str(confidence_classes)) if confidence_classes else 'none'
    conf_token = f'conf-classes-{conf_temp}'.lower()
    confidence_classes = confidence_classes or []

    df_validation_table = pd.read_csv('validation_table_data.csv')
    planet_ids = df_validation_table.planet_id.to_list()
    dswx_ready = df_validation_table.dswx_urls.to_list()

    # Filter
    planet_ids = [planet_id for (k, planet_id) in enumerate(planet_ids) if dswx_ready[k]]
    print(f'There are {len(planet_ids)} validation datasets, and of those, '
          f'there are {len(dswx_ready)} DSWx products available')

    dswx_ids = [dswx_ready for (k, dswx_ready) in enumerate(dswx_ready) if dswx_ready[k]]

    for planet_id, dswx_id in zip(tqdm(planet_ids, desc='Validation Datasets'), dswx_ids):

        print(f'Planet ID: {planet_id}')
        downsample_3ha_token = '_3-ha-downsample' if downsample_to_3_ha else ''
        parameters_dir_name = (f'sample-from-{class_selection_from}_'
                               f'{conf_token}'
                               f'{downsample_3ha_token}')
        parameters_dir = ipynb_dir / parameters_dir_name
        parameters_dir.mkdir(exist_ok=True, parents=True)
        out_notebook_path = parameters_dir / (dswx_id.split('_B01')[0].split('/')[-1] + '.ipynb')
        sample_from_dswx = True if (class_selection_from == 'dswx') else False
        pm.execute_notebook('0-Verify_Requirements.ipynb',
                            output_path=out_notebook_path,
                            parameters=dict(PLANET_ID=planet_id,
                                            SAMPLE_FROM_DSWX=sample_from_dswx,
                                            CONFIDENCE_CLASSES=confidence_classes,
                                            DOWNSAMPLE_BOTH_DS_TO_3_HA=downsample_to_3_ha
                                            )
                            )

    pm.execute_notebook('1-Read_Verification.ipynb',
                        output_path=ipynb_dir / '1-Read_Verification.ipynb'
                        )


if __name__ == '__main__':
    main()
