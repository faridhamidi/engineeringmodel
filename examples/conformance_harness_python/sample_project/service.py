from sample_project.decisions import choose_payload
from sample_project.integrations import build_vendor_client


def run_operation(raw: str, operation_id: str) -> tuple[str, str]:
    payload = choose_payload(raw)
    result = build_vendor_client().send(payload)
    return operation_id, result
