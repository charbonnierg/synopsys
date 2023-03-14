import typing as t
from dataclasses import asdict, is_dataclass
from datetime import datetime
from json import dumps

from pydantic import BaseModel, parse_obj_as, parse_raw_as

from synopsys.interfaces.codec import CodecBackend as CodecABC
from synopsys.interfaces.codec import T

NULL = type(None)


class PseudoJSONCodec(CodecABC):
    """Codec used to encode/decode message data.

    All messaging systems are expected to send and receive message data as bytes.
    """

    def encode_payload(self, data: t.Any) -> bytes:
        if data is None:
            return b""
        if isinstance(data, bytes):
            return data
        if isinstance(data, str):
            return data.encode("utf-8")
        if isinstance(data, BaseModel):
            return data.json().encode("utf-8")
        if isinstance(data, datetime):
            return data.isoformat().encode("utf-8")
        if is_dataclass(data):
            data = asdict(data)
        return dumps(data, default=_default_serializer).encode("utf-8")

    def decode_payload(self, raw: bytes, schema: t.Type[T]) -> T:
        if schema is NULL or schema is None:
            if not raw:
                return None  # type: ignore[return-value]
            raise ValueError("Expected None but got non-null data instead")
        if schema is bytes:
            return bytes(raw)  # type: ignore[return-value]
        if schema is bytearray:
            return bytearray(raw)  # type: ignore[return-value]
        if schema is str:
            return raw.decode("utf-8")  # type: ignore[return-value]
        return parse_raw_as(schema, raw)

    def encode_headers(self, data: t.Any) -> t.Dict[str, str]:
        if data is None:
            return {}
        if is_dataclass(data):
            data = asdict(data)
        # Parse to dict
        dict_data = parse_obj_as(t.Dict[str, t.Any], data)
        # Handle special cases
        return {key: _normalize_header_value(value) for key, value in dict_data.items()}

    def decode_headers(self, raw: t.Dict[str, str], schema: t.Type[T]) -> T:
        if schema is NULL or schema is None:
            if not raw:
                return None  # type: ignore[return-value]
            raise ValueError("Expected None but got non-null data instead")
        return parse_obj_as(schema, raw)


def _default_serializer(obj: t.Any) -> t.Any:
    """Bytes are not supported by default. It's up to the user to convert it either to base64, hex, or a list of integers for example."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, BaseModel):
        return obj.dict()
    if is_dataclass(obj):
        return asdict(obj)
    raise TypeError  # pragma no cover


def _normalize_header_value(obj: t.Any) -> str:
    if isinstance(obj, str):
        return obj
    if isinstance(obj, datetime):
        return obj.isoformat()
    return dumps(obj, default=_default_serializer)
