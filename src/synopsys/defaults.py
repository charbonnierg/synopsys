from .adapters import PseudoJSONCodec
from .entities.syntax import SubjectSyntax

DEFAULT_CODEC = PseudoJSONCodec()
DEFAULT_SYNTAX = SubjectSyntax()


__all__ = ["DEFAULT_CODEC", "DEFAULT_SYNTAX"]
