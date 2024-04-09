from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Status:
    verified: Optional[bool] = None
    sent_count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Status':
        assert isinstance(obj, dict)
        verified = from_union([from_bool, from_none], obj.get("verified"))
        sent_count = from_union([from_int, from_none], obj.get("sentCount"))
        return Status(verified, sent_count)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.verified is not None:
            result["verified"] = from_union([from_bool, from_none], self.verified)
        if self.sent_count is not None:
            result["sentCount"] = from_union([from_int, from_none], self.sent_count)
        return result


@dataclass
class Name:
    first: Optional[str] = None
    last: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Name':
        assert isinstance(obj, dict)
        first = from_union([from_str, from_none], obj.get("first"))
        last = from_union([from_str, from_none], obj.get("last"))
        return Name(first, last)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.first is not None:
            result["first"] = from_union([from_str, from_none], self.first)
        if self.last is not None:
            result["last"] = from_union([from_str, from_none], self.last)
        return result


@dataclass
class User:
    name: Optional[Name] = None
    id: Optional[str] = None
    photo: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        name = from_union([Name.from_dict, from_none], obj.get("name"))
        id = from_union([from_str, from_none], obj.get("_id"))
        photo = from_union([from_str, from_none], obj.get("photo"))
        return User(name, id, photo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.name is not None:
            result["name"] = from_union([lambda x: to_class(Name, x), from_none], self.name)
        if self.id is not None:
            result["_id"] = from_union([from_str, from_none], self.id)
        if self.photo is not None:
            result["photo"] = from_union([from_str, from_none], self.photo)
        return result


@dataclass
class FactByID:
    status: Optional[Status] = None
    id: Optional[str] = None
    user: Optional[User] = None
    text: Optional[str] = None
    type: Optional[str] = None
    deleted: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    v: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FactByID':
        assert isinstance(obj, dict)
        status = from_union([Status.from_dict, from_none], obj.get("status"))
        id = from_union([from_str, from_none], obj.get("_id"))
        user = from_union([User.from_dict, from_none], obj.get("user"))
        text = from_union([from_str, from_none], obj.get("text"))
        type = from_union([from_str, from_none], obj.get("type"))
        deleted = from_union([from_bool, from_none], obj.get("deleted"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        updated_at = from_union([from_datetime, from_none], obj.get("updatedAt"))
        v = from_union([from_int, from_none], obj.get("__v"))
        return FactByID(status, id, user, text, type, deleted, created_at, updated_at, v)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.status is not None:
            result["status"] = from_union([lambda x: to_class(Status, x), from_none], self.status)
        if self.id is not None:
            result["_id"] = from_union([from_str, from_none], self.id)
        if self.user is not None:
            result["user"] = from_union([lambda x: to_class(User, x), from_none], self.user)
        if self.text is not None:
            result["text"] = from_union([from_str, from_none], self.text)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.deleted is not None:
            result["deleted"] = from_union([from_bool, from_none], self.deleted)
        if self.created_at is not None:
            result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.updated_at is not None:
            result["updatedAt"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.v is not None:
            result["__v"] = from_union([from_int, from_none], self.v)
        return result


def fact_by_id_from_dict(s: Any) -> FactByID:
    return FactByID.from_dict(s)


def fact_by_id_to_dict(x: FactByID) -> Any:
    return to_class(FactByID, x)
