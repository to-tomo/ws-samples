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
    # ご自身の環境に合わせて修正
    # IBM Cloud 画面: 管理 -> 資格情報 -> API 鍵 よりコピー
    api_key_v1 = "<your api key>"
    # IBM Watson Discovery 画面 の右上の API アイコン -> Environment ID
    environment_id = "<your environment id>"
    # IBM Watson Discovery 画面 の右上の API アイコン -> Collection ID よりコピー
    collection_id = "<your collection id>"
    # IBM Cloud 画面: 管理 -> 資格情報 -> URL よりコピー
    url = "<your url>"
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
