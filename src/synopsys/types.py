import typing as t

NULL: t.Type[None] = type(None)

DataT = t.TypeVar("DataT")
MetaT = t.TypeVar("MetaT")
ScopeT = t.TypeVar("ScopeT")
ReplyT = t.TypeVar("ReplyT")
ReplyMetaT = t.TypeVar("ReplyMetaT")
