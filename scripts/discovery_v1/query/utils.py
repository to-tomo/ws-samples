"""
ユーティリティ
"""

import json
from requests import Response
from typing import Any


def json_dumps(response: Response) -> Any:
    """
    response を json に整形
    """
    return json.dumps(response, indent=2, ensure_ascii=False)
