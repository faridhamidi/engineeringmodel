from sample_project.integrations import VendorClient


def send_from_known_site(payload: str) -> str:
    return VendorClient().send(payload)
