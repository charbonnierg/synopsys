import typing as t

NULL: t.Type[None] = type(None)

DataT = t.TypeVar("DataT")
MetadataT = t.TypeVar("MetadataT")
ScopeT = t.TypeVar("ScopeT")
ReplyT = t.TypeVar("ReplyT")
