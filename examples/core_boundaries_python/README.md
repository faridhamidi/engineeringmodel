# Core Boundary Witness — Python

This specimen demonstrates three Core Hygiene claims without requiring an architecture framework:

1. decision logic can be tested without the external system;
2. external-client construction can be confined to one integration module;
3. an operation identifier can cross the service boundary into the external effect.

`tests/test_structure.py` is a structural ratchet. The allowed construction set contains one file. A new direct `VendorClient(...)` call anywhere else fails the test.

Run from the repository root:

```bash
python -m unittest discover -s examples/core_boundaries_python/tests -v
```
