"""
Watson Discovery V2 API 関連のヘルパー
"""

import pandas as pd
from requests import Response
from typing import Any, List

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV2
from ibm_watson.discovery_v2 import TrainingExample


def authentication_v2(api_key: str, url: str) -> DiscoveryV2:
    """
    Watson Discovery の認証
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#authentication-cloud  # noqa: E501
    """

    authenticator = IAMAuthenticator(api_key)
    discovery = DiscoveryV2(
        version="2020-08-30",
        authenticator=authenticator)
    discovery.set_service_url(url)
    return discovery


def conver_df_to_training_exaples(collection_id: str, df: pd.DataFrame) -> Any:
    """
    num_queries 毎のデータフレームを TrainingExample のリストに変換
    """

    natural_language_query: str = None  # トレーニング クエリとして使用される自然テキストクエリ
    examples: List[TrainingExample] = []  # TrainingExample の配列
    for data in df.itertuples():
        training_example = TrainingExample(
            document_id=data.examples_document_id,
            collection_id=collection_id,
            relevance=data.examples_relevance)
        examples.append(training_example)
        # num_queries 毎に同一の natural_language_query になるため、そのまま上書き
        natural_language_query = data.natural_language_query
    return natural_language_query, examples


def conver_res_to_training_exaples(examples: Response) -> List:
    """
    トレーニングクエリ例を含むレスポンスを TrainingExample のリストに変換
    """
    results: List[TrainingExample] = []
    for i in range(len(examples)):
        training_example = TrainingExample(
            document_id=examples[i]["document_id"],
            collection_id=examples[i]["collection_id"],
            relevance=examples[i]["relevance"])
        results.append(training_example)
    return results
