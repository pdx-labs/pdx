import json
import hashlib
from pdx.agent.metadata import AgentRequest


def _hash_request_values(request_values: AgentRequest) -> str:
    _request_string = json.dumps(request_values, sort_keys=True, indent=2)
    _hash = hashlib.md5(_request_string.encode("utf-8")).hexdigest()
    return _hash
