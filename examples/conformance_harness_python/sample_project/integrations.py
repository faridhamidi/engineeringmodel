class VendorClient:
    def send(self, payload: str) -> str:
        return f"sent:{payload}"


def build_vendor_client() -> VendorClient:
    return VendorClient()
