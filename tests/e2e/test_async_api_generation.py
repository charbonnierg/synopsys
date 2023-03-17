from synopsys import create_event, create_flow
from synopsys.operations.specs import get_async_api_spec


class TestAsyncAPIGeneration:
    def test_basic_async_api_from_flows(self):
        event = create_event(
            "test-event",
            "test.*",
            schema=int,
            description="A test event",
            title="Test Event",
        )

        flow = create_flow("test-flow", event=event)

        result = get_async_api_spec([flow], "test-app", "0.10.0")

        assert result == {
            "asyncapi": "2.6.0",
            "info": {"title": "test-app", "version": "0.10.0"},
            "channels": {
                "test-flow": {
                    "subscribe": {
                        "message": {
                            "name": "test-event",
                            "payload": {"$ref": "#/components/schemas/int"},
                            "description": "A test event",
                        }
                    }
                }
            },
            "components": {"schemas": {"int": {"title": "int", "type": "integer"}}},
        }, result
