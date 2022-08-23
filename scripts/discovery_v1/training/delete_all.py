"""
Watson Discovery V1 API
    3. 全てのトレーニングクエリの削除
"""

import logging
import pandas as pd
from requests import Response
import sys

from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV1

import config
from helper import authentication_v1


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


def delete_all_training_data_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str) -> Response:
    """
    指定されたコレクションの全てのトレーニングクエリを削除
    MEMO: https://cloud.ibm.com/apidocs/discovery#deletealltrainingdata  # noqa: E501
    """

    response = discovery.delete_all_training_data(
        environment_id=environment_id,
        collection_id=collection_id
        ).get_result()
    return response


if __name__ == "__main__":
    api_key_v1 = config.api_key_v1
    environment_id = config.environment_id
    collection_id = config.collection_id
    url = config.url
    try:
        discovery = authentication_v1(api_key_v1, url)
        logger.info("authenticated.")
        # 3. 全てのトレーニングデータを削除
        delete_all_training_data_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id)
        logger.info(f"deleted all training data. | collection_id: {collection_id}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
