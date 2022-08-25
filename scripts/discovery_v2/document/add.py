"""
Watson Discovery V2 API を使用してドキュメントを追加
"""

import glob
import json
import logging
import sys
from typing import Any
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV2


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authentication_v2(api_key: str, url: str) -> DiscoveryV2:
    """
    Watson Discovery の認証
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#authentication-cloud  # noqa: E501
    """

    authenticator = IAMAuthenticator(api_key)
    discovery = DiscoveryV2(
        version="2020-08-30",
        authenticator=authenticator
        )
    discovery.set_service_url(url)
    return discovery


def add_document_v2(
        discovery: DiscoveryV2,
        project_id: str,
        collection_id: str,
        filename: str = None,
        file_content_type: str = "application/json",
        metadata: str = None) -> Any:
    """
    ドキュメント追加の実行
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#adddocument  # noqa: E501
    """

    with open(filename, "r", encoding="UTF-8") as file:
        add_doc = discovery.add_document(
            project_id=project_id,
            collection_id=collection_id,
            file=file,
            filename=filename,
            file_content_type=file_content_type,
            metadata=metadata,
            ).get_result()
    return json.dumps(add_doc, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    api_key_v2 = "<api key>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/projects/<your project id>/workspace から抜粋  # noqa: E501
    project_id = "<project id>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/collections/<your collection id>/activity  # noqa: E501
    collection_id = "<collection id>"
    url = "https://<host>/instances/<instance id>"
    # ファイルを取得
    data_files = glob.glob("data/*.json")
    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")
        for i in range(len(data_files)):
            data_file = data_files[i]
            document_id = data_file[5:].replace(".", "-")  # ピリオド「.」は document_id として使用できないため。<ファイル名-拡張子>に変更。  # noqa: E501
            logger.info(f"input data. | document_id: {document_id}, file: {data_file}")  # noqa: E501
            jsonized_response = add_document_v2(
                discovery=discovery,
                project_id=project_id,
                collection_id=collection_id,
                filename=data_file
            )
            logger.info(f"********** respose of [document_id: {document_id}] ********** :\n{jsonized_response}")  # noqa: E501
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
