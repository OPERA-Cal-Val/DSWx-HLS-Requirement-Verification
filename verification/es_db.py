from functools import lru_cache

import urllib3
from dotenv import dotenv_values
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search

config = dotenv_values()
ES_USERNAME = config['ES_USERNAME']
ES_PASSWORD = config['ES_PASSWORD']
urllib3.disable_warnings()


@lru_cache
def get_search_client():
    GRQ_URL = 'https://100.104.62.10/grq_es/'
    grq_client = Elasticsearch(GRQ_URL,
                               http_auth=(ES_USERNAME, ES_PASSWORD),
                               verify_certs=False,
                               read_timeout=50000,
                               terminate_after=2500,
                               )
    search = Search(using=grq_client,
                    # wildcard is where the version is
                    index='grq_*_l3_dswx_hls')

    if not grq_client.ping():
        raise ValueError('Either JPL username/password is wrong or not connected to VPN')

    return search


def get_DSWX_doc(hls_id: str) -> dict:

    search = get_search_client()
    q_qs = Q('query_string',
             query=f'\"{hls_id}\"',
             default_field="metadata.input_granule_id")

    query = search.query(q_qs)
    resp = query.execute()
    n = len(resp.hits)

    if n > 1:
        raise ValueError('Multiple DSWx Products for current query')
    if n == 0:
        raise ValueError('No DSWx products match HLS ID')

    data = resp.hits[0].to_dict()
    return data


def get_dswx_urls(hls_id: str) -> list:
    base_url = 'https://opera-pst-rs-pop1.s3.us-west-2.amazonaws.com/'
    doc = get_DSWX_doc(hls_id)
    paths = doc['metadata']['product_s3_paths']
    paths_formatted = [path.replace('s3://opera-pst-rs-pop1/', '') for path in paths]
    urls = [f'{base_url}{path}' for path in paths_formatted]
    return urls
