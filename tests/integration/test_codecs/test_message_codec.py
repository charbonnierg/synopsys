import json
import typing as t
from dataclasses import dataclass
from datetime import datetime
from re import escape

import pytest
from pydantic import BaseModel, ValidationError

from synopsys.adapters.codec import PseudoJSONCodec


@pytest.fixture
def codec() -> PseudoJSONCodec:
    return PseudoJSONCodec()


class TestCodecDecode:
    def test_init(self, codec: PseudoJSONCodec):
        """Test that no error are raised when creating a Codec instance"""
        assert isinstance(codec, PseudoJSONCodec)

    @pytest.mark.parametrize(
        "schema,result",
        [
            (bytes, b""),
            (bytearray, bytearray()),
            (str, ""),
            (None, None),
        ],
        ids=["bytes", "bytearray", "str", "null"],
    )
    def test_decode_empty_bytes(
        self, schema: t.Type[t.Any], result: t.Any, codec: PseudoJSONCodec
    ):
        assert codec.decode_payload(b"", schema) == result

    @pytest.mark.parametrize(
        "schema",
        [
            t.List[t.Any],
            t.Tuple[t.Any],
            t.Dict[t.Any, t.Any],
            BaseModel,
        ],
        ids=["list", "tuple", "dict", "basemodel"],
    )
    def test_decode_empty_bytes_into_structure_raises_an_error(
        self, schema: t.Type[t.Any], codec: PseudoJSONCodec
    ):
        with pytest.raises(
            json.decoder.JSONDecodeError,
            match=escape("Expecting value: line 1 column 1 (char 0)"),
        ):
            codec.decode_payload(b"", schema)

    @pytest.mark.parametrize(
        "schema,result",
        [
            (bytes, b"hello"),
            (bytearray, bytearray([104, 101, 108, 108, 111])),
            (str, "hello"),
        ],
        ids=["bytes", "bytearray", "str"],
    )
    def test_decode_string_bytes(
        self, schema: t.Type[t.Any], result: t.Any, codec: PseudoJSONCodec
    ):
        assert codec.decode_payload(b"hello", schema) == result

    def test_decode_string_bytes_into_null_raises_an_error(
        self, codec: PseudoJSONCodec
    ):
        with pytest.raises(ValueError, match="Expected None but got non-null data"):
            codec.decode_payload(b"hello", None)

    @pytest.mark.parametrize(
        "schema,result",
        [
            (int, 12),
            (float, 12.100000000000001),
        ],
        ids=["int", "float"],
    )
    def test_decode_numerical_bytes_into_numbers(
        self, schema: t.Type[t.Any], result: t.Any, codec: PseudoJSONCodec
    ):
        assert codec.decode_payload(b"12.100000000000001", schema) == result

    @pytest.mark.parametrize(
        "schema",
        [
            int,
            float,
        ],
        ids=["int", "float"],
    )
    def test_decode_padded_numerical_bytes_raises_an_error(
        self, schema: t.Type[t.Any], codec: PseudoJSONCodec
    ):
        with pytest.raises(
            json.decoder.JSONDecodeError,
            match=escape("Extra data: line 1 column 2 (char 1)"),
        ):
            codec.decode_payload(b"01", schema)

    @pytest.mark.parametrize("schema", [int, float], ids=["int", "float"])
    def test_decode_string_bytes_into_numbers_an_error(
        self, schema: t.Type[t.Any], codec: PseudoJSONCodec
    ):
        with pytest.raises(
            json.decoder.JSONDecodeError,
            match=escape("Expecting value: line 1 column 1 (char 0)"),
        ):
            codec.decode_payload(b"hello", schema)

    @pytest.mark.parametrize(
        "schema",
        [
            t.List[t.Any],
            t.Tuple[t.Any],
            t.Dict[t.Any, t.Any],
            BaseModel,
        ],
        ids=["list", "tuple", "dict", "basemodel"],
    )
    def test_decode_string_bytes_into_structure_raises_an_error(
        self, schema: t.Type[t.Any], codec: PseudoJSONCodec
    ):
        with pytest.raises(
            json.decoder.JSONDecodeError, match="Expecting value: line 1 column 1 "
        ):
            codec.decode_payload(b"hello", schema)

    @pytest.mark.parametrize(
        "raw,result",
        [
            (b"[]", []),
            (b"[null]", [None]),
            (b"[1]", [1]),
            (b'["a"]', ["a"]),
            (b"[1.2]", [1.2]),
        ],
        ids=["empty-list", "list-null", "list-int", "list-str", "list-float"],
    )
    def test_decode_array_bytes_into_list_cast_json_types(
        self, raw: bytes, result: t.List[t.Any], codec: PseudoJSONCodec
    ):
        assert codec.decode_payload(raw, t.List[t.Any]) == result

    @pytest.mark.parametrize(
        "raw,result",
        [
            (b"{}", {}),
            (b'{"a":null}', {"a": None}),
            (b'{"a": 1}', {"a": 1}),
            (b'{"a": "test"}', {"a": "test"}),
            (b'{"a": 1.2}', {"a": 1.2}),
            (b'{"a": [null]}', {"a": [None]}),
            (b'{"a": [1]}', {"a": [1]}),
            (b'{"a": ["test"]}', {"a": ["test"]}),
            (b'{"a": [1.2]}', {"a": [1.2]}),
        ],
        ids=[
            "empty-dict",
            "dict-str-null",
            "dict-str-int",
            "dict-str-str",
            "dict-str-float",
            "dict-str-list-null",
            "dict-str-list-int",
            "dict-str-list-str",
            "dict-str-list-float",
        ],
    )
    def test_decode_mapping_bytes_into_dict_cast_json_types(
        self, raw: bytes, result: t.Dict[str, t.Any], codec: PseudoJSONCodec
    ):
        assert codec.decode_payload(raw, t.Dict[str, t.Any]) == result

    def test_decode_json_bytes_into_dataclass(self, codec: PseudoJSONCodec):
        @dataclass
        class MyModel:
            foo: int
            bar: t.Optional[float] = None

        assert codec.decode_payload(b'{"foo": 1, "bar": 2.1}', MyModel) == MyModel(
            foo=1, bar=2.1
        )
        assert codec.decode_payload(b'{"foo": 1}', MyModel) == MyModel(foo=1, bar=None)

    def test_decode_json_bytes_into_dataclass_raises_validation_error(
        self, codec: PseudoJSONCodec
    ):
        @dataclass
        class MyModel:
            foo: int
            bar: float

        assert codec.decode_payload(b'{"foo": 1, "bar": 2.1}', MyModel) == MyModel(
            foo=1, bar=2.1
        )
        with pytest.raises(
            ValidationError,
            match=escape(
                "1 validation error for ParsingModel[MyModel]\n__root__\n  __init__() missing 1 required positional argument: 'bar' (type=type_error)"
            ),
        ):
            codec.decode_payload(b'{"foo": 1}', MyModel)

    def test_decode_json_bytes_into_basemodel(self, codec: PseudoJSONCodec):
        class MyModel(BaseModel):
            foo: int
            bar: t.Optional[float] = None

        assert codec.decode_payload(
            MyModel(foo=1, bar=2).json().encode(), MyModel
        ) == MyModel(foo=1, bar=2)
        assert codec.decode_payload(MyModel(foo=1).json().encode(), MyModel) == MyModel(
            foo=1, bar=None
        )

    def test_decode_json_bytes_into_basemodel_raises_validation_error(
        self, codec: PseudoJSONCodec
    ):
        class MyModel(BaseModel):
            foo: int
            bar: float

        assert codec.decode_payload(
            MyModel(foo=1, bar=2).json().encode(), MyModel
        ) == MyModel(foo=1, bar=2)
        with pytest.raises(
            ValidationError,
            match=escape(
                "1 validation error for ParsingModel[MyModel]\n__root__ -> bar\n  field required (type=value_error.missing)"
            ),
        ):
            codec.decode_payload(b'{"foo": 1}', MyModel)


class TestCodecEncode:
    @pytest.mark.parametrize(
        "obj,result",
        [
            (b"", b""),
            (b"hello", b"hello"),
            (b"hello\n", b"hello\n"),
            ("", b""),
            (None, b""),
            ("hello", b"hello"),
            ("hello\n", b"hello\n"),
            (datetime(2023, 3, 13, 0, 0, 0), b"2023-03-13T00:00:00"),
        ],
    )
    def test_encode_to_bytes_string(
        self, obj: t.Any, result: bytes, codec: PseudoJSONCodec
    ):
        assert codec.encode_payload(obj) == result

    @pytest.mark.parametrize(
        "obj,result",
        [
            (0, b"0"),
            (1, b"1"),
            (1.2, b"1.2"),
        ],
    )
    def test_encode_to_numerical_bytes_string(
        self, obj: t.Any, result: t.Any, codec: PseudoJSONCodec
    ):
        assert codec.encode_payload(obj) == result

    @pytest.mark.parametrize(
        "obj,result",
        [
            ({}, b"{}"),
            ([], b"[]"),
            (set(), b"[]"),
            (tuple(), b"[]"),
        ],
    )
    def test_encode_to_empty_json_bytes(
        self, obj: t.Any, result: t.Any, codec: PseudoJSONCodec
    ):
        assert codec.encode_payload(obj) == result

    @pytest.mark.parametrize(
        "obj,result",
        [
            ({1: "2"}, b'{"1": "2"}'),
            (
                {"date": datetime(2023, 3, 13, 0, 0, 0)},
                b'{"date": "2023-03-13T00:00:00"}',
            ),
            ([1, "a"], b'[1, "a"]'),
            (set([1.2, 1.3, 1, 1, 1]), b"[1.2, 1.3, 1]"),
            (tuple([[1, 2], [2, 3]]), b"[[1, 2], [2, 3]]"),
        ],
    )
    def test_encode_to_json_bytes(
        self, obj: t.Any, result: t.Any, codec: PseudoJSONCodec
    ):
        assert codec.encode_payload(obj) == result

    def test_encode_dataclass_to_json_bytes(self, codec: PseudoJSONCodec):
        @dataclass
        class NestedModel:
            foo: int

        @dataclass
        class MyModel:
            model: NestedModel

        assert (
            codec.encode_payload(MyModel(model=NestedModel(foo=1)))
            == b'{"model": {"foo": 1}}'
        )
        assert (
            codec.encode_payload([MyModel(model=NestedModel(foo=1))])
            == b'[{"model": {"foo": 1}}]'
        )

    def test_encode_basemodel_and_dataclasses_to_json_bytes(
        self, codec: PseudoJSONCodec
    ):
        @dataclass
        class NestedModel:
            foo: int

        class MyModel(BaseModel):
            model: NestedModel

        assert (
            codec.encode_payload(MyModel(model=NestedModel(foo=1)))
            == b'{"model": {"foo": 1}}'
        )
        assert (
            codec.encode_payload({"my_model": MyModel(model=NestedModel(foo=1))})
            == b'{"my_model": {"model": {"foo": 1}}}'
        )
