from typing import TypeVar

from dataclasses_json import DataClassJsonMixin, config
from loguru import logger
from marshmallow import Schema, ValidationError, fields

from network.common.message import Message

schema_cache: dict[type[Message], Schema] = {}


def get_schema(cls: type[Message]) -> Schema:
    if cls not in schema_cache:
        schema_cache[cls] = cls.schema()
    return schema_cache[cls]


T = TypeVar("T", bound="DataClassJsonMixin")


def parse_message(cls: type[T], data: dict, error_category: str) -> T | None:
    try:
        get_schema(cls).load(data)
    except ValidationError as e:
        logger.error(f"[{error_category}] {e.messages}")
        return

    return cls.from_dict(data)


def is_not_empty(s: str) -> None:
    return len(s) != 0 and not s.isspace()


NON_EMPTY_STRING = config(mm_field=fields.Str(validate=is_not_empty))
