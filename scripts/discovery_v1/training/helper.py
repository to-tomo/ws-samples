"""
Watson Discovery V1 API 関連のヘルパー
"""

import pandas as pd
from typing import Any, List

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1
from ibm_watson.discovery_v1 import TrainingExample


def authentication_v1(api_key: str, url: str) -> DiscoveryV1:
    """
    Watson Discovery の認証
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#authentication-cloud  # noqa: E501
    """

    authenticator = IAMAuthenticator(api_key)
    discovery = DiscoveryV1(
        version="2019-04-30",
        authenticator=authenticator
        )
    discovery.set_service_url(url)
    return discovery


def conver_df_to_training_exaples(df: pd.DataFrame) -> Any:
    """
    num_queries 毎のデータフレームを TrainingExample のリストに変換
    """

    natural_language_query: str = None  # トレーニング クエリとして使用される自然テキストクエリ
    examples: List[TrainingExample] = []  # TrainingExample の配列
    for data in df.itertuples():
        training_example = TrainingExample(
            document_id=data.examples_document_id,
            cross_reference=data.examples_document_id,
            relevance=data.examples_relevance)
        examples.append(training_example)
        # num_queries 毎に同一の natural_language_query になるため、そのまま上書き
        natural_language_query = data.natural_language_query
    return natural_language_query, examples
