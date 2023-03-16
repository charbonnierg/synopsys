import typing as t
from dataclasses import dataclass
from datetime import datetime

import pytest
from pydantic import BaseModel

from synopsys.adapters.codec import PseudoJSONCodec


@pytest.fixture
def codec() -> PseudoJSONCodec:
    return PseudoJSONCodec()


class TestCodecDecode:
    def test_init(self, codec: PseudoJSONCodec):
        """Test that no error are raised when creating a Codec instance"""
        assert isinstance(codec, PseudoJSONCodec)

    def test_decode_to_null(self, codec: PseudoJSONCodec):
        assert codec.decode_headers({}, type(None)) is None

    def test_decode_to_null_raises_an_error_when_headers_not_empty(
        self, codec: PseudoJSONCodec
    ):
        with pytest.raises(
            ValueError, match="Expected None but got non-null data instead"
        ):
            assert codec.decode_headers({"this": "will fail"}, type(None)) is None

    def test_decode_to_string_mapping(self, codec: PseudoJSONCodec):
        assert codec.decode_headers({"a": "b"}, t.Dict[str, str]) == {"a": "b"}

    def test_decode_to_numerical_mapping(self, codec: PseudoJSONCodec):
        assert codec.decode_headers({"a": "1"}, t.Dict[str, int]) == {"a": 1}

    def test_decode_to_base_model(self, codec: PseudoJSONCodec):
        class MyModel(BaseModel):
            a: int

        assert codec.decode_headers({"a": "1"}, MyModel) == MyModel(a=1)

    def test_decode_to_dataclass(self, codec: PseudoJSONCodec):
        @dataclass
        class MyModel:
            a: int

        assert codec.decode_headers({"a": "1"}, MyModel) == MyModel(a=1)


class TestHeaderCodecEncode:
    def test_encode_null_to_headers(self, codec: PseudoJSONCodec):
        assert codec.encode_headers(None) == {}

    def test_encode_empty_dict_to_headers(self, codec: PseudoJSONCodec):
        assert codec.encode_headers({}) == {}

    @pytest.mark.parametrize(
        "obj,result",
        [
            ({"a": "ok"}, {"a": "ok"}),
            ({"a": 1}, {"a": "1"}),
            ({1: "a"}, {"1": "a"}),
            ({"date": datetime(2023, 3, 13, 0, 0, 0)}, {"date": "2023-03-13T00:00:00"}),
            (
                {"foo": {"date": datetime(2023, 3, 13, 0, 0, 0)}},
                {"foo": '{"date": "2023-03-13T00:00:00"}'},
            ),
        ],
        ids=[
            "str-str",
            "str-int",
            "int-str",
            "str-datetime",
            "str-mapping-str-datetime",
        ],
    )
    def test_encode_mapping_to_headers(
        self, obj: t.Any, result: t.Any, codec: PseudoJSONCodec
    ):
        assert codec.encode_headers(obj) == result

    def test_encode_base_model_to_headers(self, codec: PseudoJSONCodec):
        class MyModel(BaseModel):
            foo: int
            bar: str

        assert codec.encode_headers(MyModel(foo=1, bar="test")) == {
            "foo": "1",
            "bar": "test",
        }

    def test_encode_dataclasses_to_headers(self, codec: PseudoJSONCodec):
        @dataclass
        class MyModel:
            foo: int
            bar: str

        assert codec.encode_headers(MyModel(foo=1, bar="test")) == {
            "foo": "1",
            "bar": "test",
        }
