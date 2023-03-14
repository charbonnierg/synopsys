import abc
import typing as t

T = t.TypeVar("T")


class CodecBackend(metaclass=abc.ABCMeta):
    """Codec used to encode/decode message data and message headers.

    All messaging systems are expected to send and receive message data as bytes,
    and message headers as string mappings.
    """

    @abc.abstractmethod
    def encode_payload(self, data: t.Any) -> bytes:
        """Encode some object into bytes."""

    @abc.abstractmethod
    def decode_payload(self, raw: bytes, schema: t.Type[T]) -> T:
        """Decode some bytes into typed object"""

    @abc.abstractmethod
    def encode_headers(self, data: t.Any) -> t.Dict[str, str]:
        """Encode some object into headers."""

    @abc.abstractmethod
    def decode_headers(self, raw: t.Dict[str, str], schema: t.Type[T]) -> T:
        """Decode some headers into typed object"""
