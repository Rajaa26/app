from datetime import datetime
from typing import Optional, TypeVar, Generic

from pydantic import BaseModel

from .. import constants
# Result generic type: success -> T, error -> E


T = TypeVar("T")
E = TypeVar("E")
class ValueDefiend:
    pass

class Result(Generic[T, E]):
    '''
    Result type for returning either a value or an error
    Inspired by Rust's Result type
    '''

    def __init__(self, value: T = None, error: E | None= None):
        self.value = value
        self.error = error

    def is_ok(self) -> bool:
        return self.is_err() is False 

    def is_err(self) -> bool:
        if isinstance(self.value,ValueDefiend) or isinstance(self.error,ValueDefiend):
           return False

        return self.error is not None 

    def unwrap(self) -> T:
        if self.is_ok():
            return self.value
        raise Exception("Called unwrap on error result")

    def unwrap_err(self) -> E:
        if self.is_err():
            return self.error
        raise Exception("Called unwrap_err on ok result")

    def ok_else_raise(self,e:Exception):
        if self.is_err():
            raise e
    def ok_or_raise(self,e:Exception):
        if self.is_err():
            raise e
        return self.value
    
    def __repr__(self) -> str:
        if self.is_ok():
            return f"Ok({self.value})"
        return f"Err({self.error})"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Result):
            return False
        if self.is_ok() and other.is_ok():
            return self.value == other.value
        if self.is_err() and other.is_err():
            return self.error == other.error
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @staticmethod
    def ok(value: T = ValueDefiend) -> "Result[T, E]":
        return Result(value=value)

    @staticmethod
    def err(error: E=ValueDefiend) -> "Result[T, E]": 
        return Result(error=error)


class File(BaseModel):
    id: str
    name: str
    expires: int
    password: Optional[str]
