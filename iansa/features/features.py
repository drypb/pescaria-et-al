from urllib.parse import urlparse
import pandas as pd
import re
import string
import scipy

from features.lexical_features import *
from features.distribution_features import *
from features.distributions import *

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    df['has_ip'] = df['url'].apply(has_ip)
    df['number_count'] = df['url'].apply(number_count)
    df['dash_symbol_count'] = df['url'].apply(dash_symbol_count)
    df['url_length'] = df['url'].apply(url_length)
    df['url_depth'] = df['url'].apply(url_depth)
    df['subdomain_count'] = df['url'].apply(subdomain_count)
    df['query_params_count'] = df['url'].apply(query_params_count)
    df['has_port'] = df['url'].apply(has_port)

    df['ks_char'] = df['url'].apply(lambda x: kolmogorov_smirnov(x, char_dist, frequency_char_ptbr))
    df['kl_char'] = df['url'].apply(lambda x: kullback_leibler(x, char_dist, frequency_char_ptbr))
    df['eucli_char'] = df['url'].apply(lambda x: euclidean_dist(x, char_dist, frequency_char_ptbr))
    df['eucli_char'] = df['url'].apply(lambda x: euclidean_dist(x, char_dist, frequency_char_ptbr))
    df['cs_char'] = df['url'].apply(lambda x: cheby_shev_dist(x, char_dist, frequency_char_ptbr))
    df['man_char'] = df['url'].apply(lambda x: manhattan_dist(x, char_dist, frequency_char_ptbr))
    
    return df




