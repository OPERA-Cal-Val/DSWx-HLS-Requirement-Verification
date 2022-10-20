from pystac_client import Client


BANDS = [f'B{n:02d}' for n in range(1, 13)] + ['Fmask']


def get_hls_urls(hls_id: str) -> dict:
    STAC_URL = 'https://cmr.earthdata.nasa.gov/stac'
    api = Client.open(f'{STAC_URL}/LPCLOUD/')
    hls_collections = ['HLSL30.v2.0', 'HLSS30.v2.0']

    search_params = {"collections": hls_collections,
                     "ids": hls_id}
    search_hls = api.search(**search_params)

    assert(search_hls.matched() == 1)
    hls_collection = list(search_hls.get_all_items())
    metadata = hls_collection[0].to_dict()
    urls = [metadata['assets'].get(band, {'href': ''})['href']
            for band in BANDS]
    hls_urls_dict = {f'hls_url_{band_name}': url for (band_name, url) in zip(BANDS, urls)}
    return hls_urls_dict
