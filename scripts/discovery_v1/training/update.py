"""
Watson Discovery V1 API
    9. トレーニングクエリ例のラベルまたは相互参照の変更
"""

import logging
import pandas as pd
from requests import Response
import sys

from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV1

import config
from helper import authentication_v1
from list import list_training_data_v1
from utils import json_dumps


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


def update_training_exampl_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str,
        query_id: str,
        example_id: str,
        cross_reference: str,
        relevance: int) -> Response:
    """
    トレーニングクエリ例を更新
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#updatetrainingexample  # noqa: E501
    """

    response = discovery.update_training_example(
        environment_id=environment_id,
        collection_id=collection_id,
        query_id=query_id,
        example_id=example_id,
        cross_reference=cross_reference,
        relevance=relevance).get_result()
    return response


if __name__ == "__main__":
    api_key_v1 = config.api_key_v1
    environment_id = config.environment_id
    collection_id = config.collection_id
    url = config.url
    try:
        discovery = authentication_v1(api_key_v1, url)
        logger.info("authenticated.")
        list_response = list_training_data_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id
        )
        logger.info("listed training queries.")
        # NOTE: 代表的な1件目の query_id に対象に update_training_exampl_v1() を実行
        #       代表的な1件目の document_id に対象に update_training_exampl_v1() を実行
        query = list_response["queries"][0]
        example = query["examples"][0]
        # 9. トレーニングクエリ例のラベルまたは相互参照の変更
        update_response = update_training_exampl_v1(
                discovery=discovery,
                environment_id=environment_id,
                collection_id=collection_id,
                query_id=query["query_id"],
                example_id=example["document_id"],
                cross_reference=example["cross_reference"],
                relevance=example["relevance"])
        logger.info(f"********** respose of update_training_exampl_v1() ********** :\n{json_dumps(update_response)}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
