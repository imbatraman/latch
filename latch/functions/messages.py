import os as _os
from typing import Any, Dict

import requests


NUCLEUS_URL = _os.environ.get("LATCH_CLI_NUCLEUS_URL", "https://nucleus.latch.bio")
ADD_MESSAGE_ENDPOINT = f"{NUCLEUS_URL}/sdk/add-task-execution-message"


def message(typ: str, data: Dict[str, Any]) -> None:
    try:
        task_project = _os.environ["FLYTE_INTERNAL_TASK_PROJECT"]
        task_domain = _os.environ["FLYTE_INTERNAL_TASK_DOMAIN"]
        task_name = _os.environ["FLYTE_INTERNAL_TASK_NAME"]
        task_version = _os.environ["FLYTE_INTERNAL_TASK_VERSION"]
        task_attempt_number = _os.environ["FLYTE_ATTEMPT_NUMBER"]
        execution_token = _os.environ["FLYTE_INTERNAL_EXECUTION_ID"]
    except KeyError:
        print(f"Local execution message:\n[{typ}]: {data}")
        return

    response = requests.post(
        url=ADD_MESSAGE_ENDPOINT,
        json={
            "execution_token": execution_token,
            "task": {
                "project": task_project,
                "domain": task_domain,
                "name": task_name,
                "version": task_version,
            },
            "task_attempt_number": task_attempt_number,
            "type": typ,
            "data": data,
        },
    )

    if response.status_code != 200:
        raise RuntimeError("Could not add task execution message to Latch.")
