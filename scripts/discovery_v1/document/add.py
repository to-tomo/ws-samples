"""
Watson Discovery V1 API を使用してドキュメント追加
"""

import glob
import json
import logging
import sys
from typing import Any
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authentication_v1(api_key: str, url: str) -> DiscoveryV1:
    """
    Watson Discovery の認証
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#authentication-cloud  # noqa: E501
    """

    authenticator = IAMAuthenticator(api_key)
    discovery = DiscoveryV1(
        version="2019-04-30",
        authenticator=authenticator
        )
    discovery.set_service_url(url)
    return discovery


def add_document_v1(
    discovery: DiscoveryV1,
    environment_id: str,
    collection_id: str,
    filename: str = None,
    file_content_type: str = "application/json",
    metadata: str = None,
        ) -> Any:
    """
    ドキュメント更新の実行
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#adddocument  # noqa: E501
    """
    with open(filename, "r", encoding="UTF-8") as file:
        add_doc = discovery.add_document(
            environment_id=environment_id,
            collection_id=collection_id,
            file=file,
            filename=filename,
            file_content_type=file_content_type,
            metadata=metadata,
            ).get_result()
    return json.dumps(add_doc, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    api_key_v1 = "<api key>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/projects/<your project id>/workspace から抜粋  # noqa: E501
    environment_id = "<environment id>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/collections/<your collection id>/activity  # noqa: E501
    collection_id = "<collection id>"
    url = "https://<host>/instances/<instance id>"
    # ファイルを取得
    data_files = glob.glob("data/*.json")
    try:
        discovery = authentication_v1(api_key_v1, url)
        logger.info("authenticated.")

        for i in range(len(data_files)):
            data_file = data_files[i]
            document_id = data_file[5:].replace(".", "-")  # ピリオド「.」は document_id として使用できないため。<ファイル名-拡張子>に変更。　# noqa: E501
            logger.info(f"input data. | document_id: {document_id}, file: {data_file}")  # noqa: E501
            jsonized_response = add_document_v1(
                discovery=discovery,
                environment_id=environment_id,
                collection_id=collection_id,
                filename=data_file
            )
            logger.info(f"********** respose of [document_id: {document_id}] ********** :\n{jsonized_response}")  # noqa: E501
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
