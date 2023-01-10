import warnings

import numpy as np
from dem_stitcher.rio_tools import reproject_arr_to_match_profile


def resample_labels_into_percentage(X: np.ndarray,
                                    profile_src: dict,
                                    profile_dst: dict,
                                    class_label: int) -> np.ndarray:
    if 'float' not in profile_dst['dtype']:
        raise ValueError('dst dtype must be float')
    p = profile_src.copy()
    p['dtype'] = 'float32'
    p['nodata'] = np.nan

    X_float = X.astype(np.float32)
    if not np.isnan(profile_src['nodata']):
        nodata = profile_src['nodata']
        X_float[X_float == nodata] = np.nan

    X_true = ((X_float == class_label) & ~np.isnan(X_float)).astype(float)
    X_false = ((X_float != class_label) & ~np.isnan(X_float)).astype(float)
    mask = np.isnan(X_float).astype(float)

    X_true_r, p_perc = reproject_arr_to_match_profile(X_true,
                                                      p,
                                                      profile_dst,
                                                      resampling='average')
    X_true_r = X_true_r[0, ...]
    X_false_r, _ = reproject_arr_to_match_profile(X_false,
                                                  p,
                                                  profile_dst,
                                                  resampling='average')
    X_false_r = X_false_r[0, ...]

    mask_r, _ = reproject_arr_to_match_profile(mask,
                                               p,
                                               profile_dst,
                                               resampling='average')
    mask_r = mask_r[0, ...]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        X_percent = X_true_r / (X_true_r + X_false_r)
    X_percent[mask_r == 1] = np.nan
    return X_percent, p_perc


def reclassify_percentage_array_for_dswx(percentange_array: np.ndarray) -> np.ndarray:
    X_new_labels = np.full(percentange_array.shape, 255, dtype=np.uint8)

    mask = np.isnan(percentange_array)

    ind_w = ~mask & (percentange_array == 1)
    X_new_labels[ind_w] = 1

    ind_pw = ~mask & (percentange_array >= .5) & (percentange_array < 1)
    X_new_labels[ind_pw] = 2

    ind_nw = ~mask & (percentange_array < .5)
    X_new_labels[ind_nw] = 0

    X_new_labels[mask] = 255
    return X_new_labels
