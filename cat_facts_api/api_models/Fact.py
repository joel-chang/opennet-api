from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast
from datetime import datetime
import dateutil.parser

from cat_facts_api.api_models.FactById import FactByID


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Status:
    sent_count: Optional[int] = None
    verified: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Status':
        assert isinstance(obj, dict)
        sent_count = from_union([from_int, from_none], obj.get("sentCount"))
        verified = from_union([from_bool, from_none], obj.get("verified"))
        return Status(sent_count, verified)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.sent_count is not None:
            result["sentCount"] = from_union(
                [from_int, from_none], self.sent_count)
        if self.verified is not None:
            result["verified"] = from_union(
                [from_bool, from_none], self.verified)
        return result


@dataclass
class Fact:
    v: Optional[int] = None
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    deleted: Optional[bool] = None
    source: Optional[str] = None
    status: Optional[Status] = None
    text: Optional[str] = None
    type: Optional[str] = None
    updated_at: Optional[datetime] = None
    used: Optional[bool] = None
    user: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Fact':
        assert isinstance(obj, dict)
        v = from_union([from_int, from_none], obj.get("__v"))
        id = from_union([from_str, from_none], obj.get("_id"))
        created_at = from_union(
            [from_datetime, from_none], obj.get("createdAt"))
        deleted = from_union([from_bool, from_none], obj.get("deleted"))
        source = from_union([from_str, from_none], obj.get("source"))
        status = from_union([Status.from_dict, from_none], obj.get("status"))
        text = from_union([from_str, from_none], obj.get("text"))
        type = from_union([from_str, from_none], obj.get("type"))
        updated_at = from_union(
            [from_datetime, from_none], obj.get("updatedAt"))
        used = from_union([from_bool, from_none], obj.get("used"))
        user = from_union([from_str, from_none], obj.get("user"))
        return Fact(v, id, created_at, deleted, source, status, text, type, updated_at, used, user)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.v is not None:
            result["__v"] = from_union([from_int, from_none], self.v)
        if self.id is not None:
            result["_id"] = from_union([from_str, from_none], self.id)
        if self.created_at is not None:
            result["createdAt"] = from_union(
                [lambda x: x.isoformat(), from_none], self.created_at)
        if self.deleted is not None:
            result["deleted"] = from_union(
                [from_bool, from_none], self.deleted)
        if self.source is not None:
            result["source"] = from_union([from_str, from_none], self.source)
        if self.status is not None:
            result["status"] = from_union(
                [lambda x: to_class(Status, x), from_none], self.status)
        if self.text is not None:
            result["text"] = from_union([from_str, from_none], self.text)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.updated_at is not None:
            result["updatedAt"] = from_union(
                [lambda x: x.isoformat(), from_none], self.updated_at)
        if self.used is not None:
            result["used"] = from_union([from_bool, from_none], self.used)
        if self.user is not None:
            result["user"] = from_union([from_str, from_none], self.user)
        return result

    def __eq__(self, other):
        if isinstance(other, FactByID):
            assert self.v == other.v
            assert self.id == other.id
            assert self.user == other.user.id  # different structure, lazy
            assert self.created_at == other.created_at
            assert self.deleted == other.deleted
            # would be better to to have a more solid model, lazy
            assert self.status.to_dict() == other.status.to_dict()
            assert self.text == other.text
            assert self.type == other.type
            assert self.updated_at == other.updated_at
            return True
        return False


def fact_from_dict(s: Any) -> Fact:
    return Fact.from_dict(s)


def fact_to_dict(x: Fact) -> Any:
    return to_class(Fact, x)
