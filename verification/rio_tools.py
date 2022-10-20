import numpy as np
from affine import Affine
from rasterio.features import shapes


def get_geopandas_features_from_array(arr: np.ndarray,
                                      transform: Affine,
                                      label_name: str = 'label',
                                      mask: np.ndarray = None,
                                      connectivity: int = 4) -> list:
    """
    Obtains a list of geopandas features in which contigious integers are
    grouped as polygons for use as:
        df =  gpd.GeoDataFrame.from_features(geo_features)
    Parameters
    ----------
    arr : np.ndarray
        The array of integers to group into contiguous polygons. Note some
        labels that are connected through diagonals May be separated depending
        on connectivity.
    transform : Affine
        Rasterio transform related to arr
    label_name : str
        The label name used for each different polygonal feature, default is
        `label`.
    mask : np.ndarray
        Nodata mask in which true values indicate where nodata is located.
    connectivity : int
        4- or 8- connectivity of the polygonal features.  See rasterio:
        https://rasterio.readthedocs.io/en/latest/api/rasterio.features.html#rasterio.features.shapes
        And see: https://en.wikipedia.org/wiki/Pixel_connectivity
    Returns
    -------
    list:
        List of features to use for constructing geopandas dataframe with
        gpd.GeoDataFrame.from_features
    """
    # see rasterio.features.shapes - needs all false values to be no data areas
    if mask is None:
        mask = np.zeros(arr.shape, dtype=bool)
    feature_list = list(shapes(arr,
                               mask=~mask,
                               transform=transform,
                               connectivity=connectivity))
    geo_features = list({'properties': {label_name: (value)},
                         'geometry': geometry}
                        for i, (geometry, value) in enumerate(feature_list))
    return geo_features
