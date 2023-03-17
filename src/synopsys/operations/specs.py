import typing as t

from pydantic import schema_of

from synopsys.entities import Event, Flow


def _schema_of(_type: t.Type[t.Any], title: str) -> t.Dict[str, t.Any]:
    values = schema_of(_type, ref_template="#/components/schemas/{model}")
    values["title"] = title
    if "definitions" in values:
        return values["definitions"]  # type: ignore[no-any-return]
    else:
        return {title: values}


def get_async_api_spec(
    flows: t.List[Flow], title: str, version: str
) -> t.Dict[str, t.Any]:
    channels = {}
    schemas = {}
    for channel in flows:
        flow_spec = get_async_api(
            channel,
            version,
        )
        channels.update(flow_spec["channels"])
        schemas.update(flow_spec["components"]["schemas"])
    return {
        "asyncapi": "2.6.0",
        "info": {
            "title": title,
            "version": version,
        },
        "channels": channels,
        "components": {"schemas": schemas},
    }


def get_async_api(flow: Flow, version: str) -> t.Dict[str, t.Any]:
    """Produce AsyncAPI spec for the service."""
    channels: t.Dict[str, t.Dict[str, t.Any]] = {}
    schemas: t.Dict[str, t.Dict[str, t.Any]] = {}
    if flow.kind == "SUBSCRIPTION":
        event: Event[t.Any, t.Any, t.Any, t.Any, t.Any] = getattr(flow, "event")
        edef, schema = async_api_component(event, "subscribe")
        channels[flow.name] = edef
        schemas.update(schema)
    for event in flow.emits or []:
        edef, schema = async_api_component(event, "publish")
        channels[event.name] = edef
        schemas.update(schema)

    return {
        "asyncapi": "2.6.0",
        "info": {
            "title": flow.name,
            "version": version,
        },
        "channels": channels,
        "components": {"schemas": schemas},
    }


def async_api_component(
    event: Event[t.Any, t.Any, t.Any, t.Any, t.Any], operation: str
) -> t.Tuple[t.Dict[str, t.Any], t.Dict[str, t.Any]]:
    schema_name = str(getattr(event.schema, "__name__", str(event.schema)))
    edef: t.Dict[str, t.Any] = {
        operation: {
            "message": {
                "name": event.name,
                "payload": {"$ref": f"#/components/schemas/{schema_name}"},
                "description": event.description,
            },
        },
    }
    return edef, _schema_of(event.schema, title=schema_name)
