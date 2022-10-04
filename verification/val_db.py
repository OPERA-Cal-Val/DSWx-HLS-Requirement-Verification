import os
from functools import lru_cache

import geopandas as gpd
import rasterio

os.environ["AWS_NO_SIGN_REQUEST"] = "YES"


@lru_cache
def get_finalized_validation_datasets() -> gpd.GeoDataFrame:
    df_image_calc = gpd.read_file('s3://opera-calval-database-dswx/image_calc.geojson')

    #  Group by upload date and image name and get the most recent
    df_image_calc = df_image_calc.sort_values(by=['image_name', 'upload_date'], ascending=True)
    df_image_calc = df_image_calc.groupby('image_name').tail(1)

    # Check if "final" is in processing level
    df_image_calc.dropna(subset=['processing_level'], inplace=True)
    temp = df_image_calc.processing_level.str.lower()
    df_image_calc = df_image_calc[temp.str.contains('final')].reset_index(drop=True)
    return df_image_calc


@lru_cache
def get_image_table() -> gpd.GeoDataFrame:
    return gpd.read_file('s3://opera-calval-database-dswx/image.geojson')


def get_val_s3_path(planet_id: str, exclusion_patterns: list = None) -> str:
    df = get_finalized_validation_datasets()
    df_temp = df[df.image_name == planet_id]
    assert(df_temp.shape[0] == 1)

    record = df_temp.to_dict('records')[0]
    bucket = record['bucket']
    keys = record['s3_keys'].split(',')
    if (len(keys) > 1) and exclusion_patterns:
        keys = list(filter(lambda key: any([patt in key for patt in exclusion_patterns], keys)))

    if len(keys) != 1:
        raise ValueError(f'Specify exclusion patterns to narrow down {len(keys)} s3 keys: {", ".join(keys)}')

    key = keys[0]
    s3_path = f's3://{bucket}/{key}'
    return s3_path


def read_validation_dataset(planet_id: str, exclusion_patterns: list = None) -> tuple:

    s3_path = get_val_s3_path(planet_id, exclusion_patterns=exclusion_patterns)

    with rasterio.open(s3_path) as ds:
        X = ds.read(1)
        p = ds.profile

    return X, p


def get_HLS_id(planet_id: str) -> str:
    df = get_image_table()
    df_temp = df[df.image_name == planet_id]
    assert(df_temp.shape[0] == 1)
    return df_temp.collocated_dswx.iloc[0]
