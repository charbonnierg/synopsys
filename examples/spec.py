from events import FLOWS

from synopsys.operations.specs import get_async_api_spec

# Get an async API out of some flows
res = get_async_api_spec(FLOWS, title="PyHosting", version="0.1.0")


if __name__ == "__main__":
    import json

    print(json.dumps(res, indent=2))
