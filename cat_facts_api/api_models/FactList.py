from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast
from datetime import datetime
import typing
from .Fact import Fact
import dateutil.parser

@dataclass
class FactList:
    items: Optional[typing.List[Fact]] = None

    @staticmethod
    def from_list(obj: typing.List) -> 'FactList':
        res = []
        for item in obj:
            try:
                res.append(Fact.from_dict(item))
            except Exception as e:
                raise Exception( "Failed to convert/append item. " + item)
        return FactList(res)

    @staticmethod
    def from_single(obj: any) -> 'FactList':
        res = []
        try:
            res.append(Fact.from_dict(obj))
        except Exception as e:
            raise Exception( "Failed to convert/append item. " + item)
        return Fact(res)