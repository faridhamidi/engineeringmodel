from sample_project.integrations import VendorClient


def legacy_send(payload: str) -> str:
    return VendorClient().send(payload)
