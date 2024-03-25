# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

import sys
import subprocess
import random
from dataclasses import dataclass, field
from typing import types, Optional, Union, Any, List, Tuple, Dict  # type: ignore[attr-defined]

from farr.parser.nodes import BlockNode, ItemizedExpressionNode
from farr.interpreter.base import Environment


class FarrObject:
    pass


class ExpressionObject(FarrObject):
    pass


class PassObject(ExpressionObject):
    def __str__(self) -> str:
        """Returns a text as object equivalent."""
        return 'ellipsis'

    def __bool__(self) -> bool:
        """Returns the boolean equivalent of the pass."""
        return False

    def __hash__(self) -> int:
        """Returns zero as the object hash."""
        return 0


class NullObject(ExpressionObject):
    def __str__(self) -> str:
        """Returns `null`."""
        return 'null'

    def __bool__(self) -> bool:
        """Returns the essence of `NullObject`."""
        return False

    def __hash__(self) -> int:
        """Returns zero as the object hash."""
        return 0

    def __eq__(self, other: FarrObject) -> 'BooleanObject':  # type: ignore[override]
        """Compares the equality of nothing with another object."""
        return BooleanObject(value=False == other)  # noqa: E712

    def __ne__(self, other: FarrObject) -> 'BooleanObject':  # type: ignore[override]
        """Compares the inequality of nothing with another object."""
        return BooleanObject(value=False != other)  # noqa: E712


@dataclass
class HeterogeneousLiteralObject(ExpressionObject):
    value: Any = field(kw_only=True)

    def __str__(self) -> str:
        """Returns the value as a `str`."""
        return str(self.value)

    def __bool__(self) -> bool:
        """Returns the value status as `bool`."""
        return bool(self.value)

    def __hash__(self) -> int:
        """Calculates the hash of the object."""
        return hash(self.value)

    def __eq__(self, other: FarrObject) -> 'BooleanObject':  # type: ignore[override]
        """Checks whether the two values are equal or not."""
        return BooleanObject(value=self.value == other)

    def __ne__(self, other: FarrObject) -> 'BooleanObject':  # type: ignore[override]
        """Checks if the two values are not equal."""
        return BooleanObject(value=self.value != other)

    def __lt__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'BooleanObject':
        """Checks if it is a smaller value or not."""
        if not isinstance(self, (IntegerObject, FloatObject)) or not isinstance(
            other, (IntegerObject, FloatObject)
        ):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `<` with type `{other.__class__.__name__}`!'
            )
        return BooleanObject(value=self.value < other.value)

    def __gt__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'BooleanObject':
        """Checks if the value is greater than or not."""
        if not isinstance(self, (IntegerObject, FloatObject)) or not isinstance(
            other, (IntegerObject, FloatObject)
        ):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `>` with type `{other.__class__.__name__}`!'
            )
        return BooleanObject(value=self.value > other.value)

    def __le__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'BooleanObject':
        """Checks if the value is less than or equal to or not."""
        if not isinstance(self, (IntegerObject, FloatObject)) or not isinstance(
            other, (IntegerObject, FloatObject)
        ):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `<=` with type `{other.__class__.__name__}`!'
            )
        return BooleanObject(value=self.value <= other.value)

    def __ge__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'BooleanObject':
        """Checks if the value is greater than or equal to or not."""
        if not isinstance(self, (IntegerObject, FloatObject)) or not isinstance(
            other, (IntegerObject, FloatObject)
        ):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `>=` with type `{other.__class__.__name__}`!'
            )
        return BooleanObject(value=self.value >= other.value)

    def isin(self, list_: 'ListObject') -> 'BooleanObject':
        """Checks the existence of the object value in the list."""
        return BooleanObject(value=self.value in list_)


class BooleanObject(HeterogeneousLiteralObject):
    def __str__(self) -> str:
        """Converts the value to lowercase letters."""
        return str(self.value).lower()


class IntegerObject(HeterogeneousLiteralObject):
    def __add__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Adds the two values together."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `+` with type `{other.__class__.__name__}`!'
            )
        return other.__class__(value=self.value + other.value)

    def __sub__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Subtracts two existing values."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `-` with type `{other.__class__.__name__}`!'
            )
        return other.__class__(value=self.value - other.value)

    def __mul__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Multiplies two existing values together."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `*` with type `{other.__class__.__name__}`!'
            )
        return other.__class__(value=self.value * other.value)

    def __truediv__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Divides the existing values."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `/` with type `{other.__class__.__name__}`!'
            )
        return FloatObject(value=self.value / other.value)

    def __mod__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Calculates the remainder of the division."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `%` with type `{other.__class__.__name__}`!'
            )
        return other.__class__(value=self.value % other.value)

    def __pow__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> Union['IntegerObject', 'FloatObject']:
        """Calculates the exponentiation."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `^` with type `{other.__class__.__name__}`!'
            )
        return other.__class__(value=self.value**other.value)

    def tostring(self) -> 'StringObject':
        """Converts the value of the object to a string."""
        return StringObject(value=str(self))


class FloatObject(HeterogeneousLiteralObject):
    def __add__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Adds the two values together."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `+` with type `{other.__class__.__name__}`!'
            )
        return FloatObject(value=self.value + other.value)

    def __sub__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Subtracts two existing values."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `-` with type `{other.__class__.__name__}`!'
            )
        return FloatObject(value=self.value - other.value)

    def __mul__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Multiplies two existing values together."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `*` with type `{other.__class__.__name__}`!'
            )
        return FloatObject(value=self.value * other.value)

    def __truediv__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Divides the existing values."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `/` with type `{other.__class__.__name__}`!'
            )
        return FloatObject(value=self.value / other.value)

    def __mod__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Calculates the remainder of the division."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `%` with type `{other.__class__.__name__}`!'
            )
        return FloatObject(value=self.value % other.value)

    def __pow__(
        self,
        other: Union['IntegerObject', 'FloatObject'],
    ) -> 'FloatObject':
        """Calculates the exponentiation."""
        if not isinstance(other, (IntegerObject, FloatObject)):
            raise TypeError(
                f'Type `{self.__class__.__name__}` does not support '
                f'operator `^` with type `{other.__class__.__name__}`!'
            )
        return FloatObject(value=self.value**other.value)

    def toint(self) -> IntegerObject:
        """Removes the decimal part and returns an integer."""
        return IntegerObject(value=int(self.value))

    def tostring(self) -> 'StringObject':
        """Converts the value of the object to a string."""
        return StringObject(value=str(self))


class StringObject(HeterogeneousLiteralObject):
    def __getitem__(self, key: 'RangeObject') -> 'StringObject':
        """Returns the characters in the string based on range."""
        if key.from_.value <= 0 or key.by is not None and key.by.value <= 0:  # type: ignore[union-attr]
            raise IndexError('Non-positive indexes are not allowed!')
        return (
            StringObject(value=self.value[key.from_.value - 1])  # type: ignore[union-attr]
            if key.to is None and key.by is None
            else StringObject(
                value=self.value[
                    key.from_.value  # type: ignore[union-attr]
                    - 1 : key.to.value if key.to is not None else None : (
                        key.by.value if key.by is not None else None
                    )
                ]
            )
        )

    def __iter__(self) -> 'StringObject':
        """Iterates over the characters of the string."""
        self._index = 0
        return self

    def __next__(self) -> 'StringObject':
        """Returns the next character."""
        if self._index >= len(self.value):
            raise StopIteration
        char = self.value[self._index]
        self._index += 1
        return char

    def toint(self) -> IntegerObject:
        """Converts the value to an integer."""
        return IntegerObject(value=int(self.value))

    def tofloat(self) -> FloatObject:
        """Converts the value to a decimal number."""
        return FloatObject(value=float(self.value))

    def tolower(self) -> 'StringObject':
        """Converts the value to lowercase letters."""
        return StringObject(value=self.value.lower())

    def toupper(self) -> 'StringObject':
        """Converts the value to uppercase."""
        return StringObject(value=self.value.upper())

    def concat(self, object_: FarrObject) -> 'StringObject':
        """Merges the string with another object."""
        return StringObject(value=self.value + str(object_))

    def split(self, separator: Optional['StringObject'] = None) -> 'ListObject':
        """Separates the string based on the separator."""
        return ListObject(
            elements=list(
                map(
                    lambda x: StringObject(value=x),
                    (
                        filter(lambda x: x, self.value.split(separator.value))
                        if separator is not None
                        else self.value
                    ),
                )
            )
        )

    def removeprefix(self, prefix: 'StringObject') -> 'StringObject':
        """Removes a prefix from the string if it exists."""
        return StringObject(value=self.value.removeprefix(prefix.value))

    def removesuffix(self, suffix: 'StringObject') -> 'StringObject':
        """Removes a suffix from the string if it exists."""
        return StringObject(value=self.value.removesuffix(suffix.value))

    def count_q(self, subset: 'StringObject') -> IntegerObject:
        """Returns the number of matches by subset."""
        return IntegerObject(value=self.value.count(subset.value))

    def nearest_q(self, subset: 'StringObject') -> IntegerObject:
        """Returns the index of the first matched item."""
        return IntegerObject(
            value=(
                result + 1
                if (result := self.value.find(subset.value)) != -1
                else -1
            )
        )

    def contains_q(self, subset: 'StringObject') -> BooleanObject:
        """Returns whether the given subset exists in the string."""
        return BooleanObject(value=subset.value in self.value)

    def startswith_q(self, prefix: 'StringObject') -> BooleanObject:
        """Returns true if the beginning of the string is the same as the input value."""
        return BooleanObject(value=self.value.startswith(prefix.value))

    def endswith_q(self, suffix: 'StringObject') -> BooleanObject:
        """Returns true if the end of the string is the same as the input value."""
        return BooleanObject(value=self.value.endswith(suffix.value))


@dataclass
class RangeObject(ExpressionObject):
    from_: Optional[IntegerObject] = field(kw_only=True)
    to: Optional[IntegerObject] = field(default=None, kw_only=True)
    by: Optional[IntegerObject] = field(default=None, kw_only=True)

    def __str__(self) -> str:
        """Returns the object as a string."""
        return (
            f'[{self.from_}, {self.by if self.by is not None else 1}'
            f'..{self.to if self.to is not None else "undefined"}]'
        )

    def __hash__(self) -> int:
        """Calculates the hash of the object."""
        return hash((self.from_, self.to, self.by))

    def __iter__(self) -> 'RangeObject':
        """Iterates over the range defined by the object."""
        self._number = self.from_
        return self

    def __next__(self) -> int:
        """Returns the next integer in the range."""
        if self.to is not None and self._number > self.to:  # type: ignore[operator]
            raise StopIteration
        result = self._number
        self._number += (  # type: ignore[operator, assignment]
            self.by if self.by is not None else IntegerObject(value=1)
        )
        return result  # type: ignore[return-value]


class DataStructureObject(ExpressionObject):
    pass


@dataclass
class ListObject(DataStructureObject):
    elements: List[Optional[FarrObject]] = field(kw_only=True)

    def __str__(self) -> str:
        """Returns elements separated by a semicolon."""
        return '; '.join(map(str, self.elements))

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    def __getitem__(
        self,
        key: 'RangeObject',
    ) -> FarrObject:
        """Extracts a range of elements."""
        if key.from_.value <= 0 or key.by is not None and key.by.value <= 0:  # type: ignore[union-attr]
            raise IndexError('Non-positive indexes are not allowed!')
        return (
            self.elements[key.from_.value - 1]  # type: ignore[return-value, union-attr]
            if key.to is None and key.by is None
            else ListObject(
                elements=self.elements[
                    key.from_.value  # type: ignore[union-attr]
                    - 1 : key.to.value if key.to is not None else None : (
                        key.by.value if key.by is not None else None
                    )
                ]
            )
        )

    def __setitem__(
        self,
        key: 'RangeObject',
        value: FarrObject,
    ) -> None:
        """Updates the elements based on the given range."""
        if key.from_.value <= 0 or key.by is not None and key.by.value <= 0:  # type: ignore[union-attr]
            raise IndexError('Non-positive indexes are not allowed!')
        elif key.to is None and key.by is None:
            self.elements[key.from_.value - 1] = value  # type: ignore[union-attr]
            return None
        self.elements[  # type: ignore[call-overload]
            key.from_.value  # type: ignore[union-attr]
            - 1 : key.to.value if key.to is not None else None : (
                key.by.value if key.by is not None else None
            )
        ] = value

    def __iter__(self) -> 'ListObject':
        """Iterates the elements in the list."""
        self._index = 0
        return self

    def __next__(self) -> FarrObject:
        """Returns the next element of the list."""
        if self._index >= len(self.elements):
            raise StopIteration
        element = self.elements[self._index]
        self._index += 1
        return element  # type: ignore[return-value]

    @property
    def first(self) -> FarrObject:
        """Returns the first element if the list is not empty."""
        if not self.elements:
            raise IndexError('The list is empty!')
        return self.elements[0]  # type: ignore[return-value]

    @property
    def last(self) -> FarrObject:
        """Returns the last element if the list is not empty."""
        if not self.elements:
            raise IndexError('The list is empty!')
        return self.elements[-1]  # type: ignore[return-value]

    @property
    def length(self) -> IntegerObject:
        """Returns the number of elements in the list."""
        return IntegerObject(value=len(self.elements))

    def isempty_q(self) -> BooleanObject:
        """Returns the status of the list being empty or not."""
        return BooleanObject(value=not bool(self.elements))

    def clear_e(self) -> NullObject:
        """Removes all elements from the list."""
        self.elements = []
        return NullObject()

    def nearest_q(self, element: FarrObject) -> IntegerObject:
        """Returns the index of the closest element found in the list."""
        return IntegerObject(
            value=(
                self.elements.index(element) + 1
                if element in self.elements
                else -1
            )
        )

    def iprepend_e(self, element: FarrObject) -> NullObject:
        """Adds an element to the beginning of the list."""
        self.elements.insert(0, element)
        return NullObject()

    def iappend_e(self, element: FarrObject) -> NullObject:
        """Adds an element to the end of the list"""
        self.elements.append(element)
        return NullObject()

    def pop_e(self, index: IntegerObject) -> FarrObject:
        """Deletes an element based on the index."""
        if index.value <= 0:
            raise IndexError(
                'Using an index smaller than or equal to zero is not allowed!'
            )
        return self.elements.pop(index.value - 1)  # type: ignore[return-value]

    def popitem_e(self, value: FarrObject) -> FarrObject:
        """Discards an element based on the given value."""
        return self.elements.pop(self.elements.index(value))  # type: ignore[return-value]

    def reverse(self) -> 'ListObject':
        """Returns the reversed list."""
        return ListObject(elements=list(reversed(self.elements)))  # type: ignore[type-var]

    def ireverse_e(self) -> 'ListObject':
        """Reverses the list and returns the new state."""
        self.elements = list(reversed(self.elements))  # type: ignore[type-var]
        return self

    def sort(self) -> 'ListObject':
        """Returns the sorted list."""
        return ListObject(elements=sorted(self.elements))  # type: ignore[type-var]

    def isort_e(self) -> 'ListObject':
        """Sorts the list in its own place."""
        self.elements = sorted(self.elements)  # type: ignore[type-var]
        return self

    def shuffle(self) -> 'ListObject':
        """Returns a shuffled list."""
        return ListObject(
            elements=sorted(self.elements, key=lambda _: random.random())
        )

    def ishuffle_e(self) -> 'ListObject':
        """Assigns the shuffled list to the object and then returns it."""
        self.elements = sorted(self.elements, key=lambda _: random.random())
        return self

    def join(self, separator: Optional[StringObject] = None) -> StringObject:
        """Merges elements together."""
        return StringObject(
            value=(separator.value if separator is not None else '').join(
                map(str, self.elements)
            )
        )


@dataclass
class HashMapObject(DataStructureObject):
    pairs: Optional[List['PairObject']] = field(kw_only=True)

    def __post_init__(self) -> None:
        """Tries to ignore duplicate pairs."""
        self._drop_duplicates()

    def __str__(self) -> str:
        """Returns existing pairs separated by a semicolon."""
        return '; '.join(map(str, self.pairs))  # type: ignore[arg-type]

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    def __getitem__(
        self,
        key: 'RangeObject',
    ) -> FarrObject:
        """Extracts a range of pairs."""
        if key.from_.value <= 0 or key.by is not None and key.by.value <= 0:  # type: ignore[union-attr]
            raise IndexError('Non-positive indexes are not allowed!')
        return (
            self.pairs[key.from_.value - 1]  # type: ignore[index, union-attr]
            if key.to is None and key.by is None
            else HashMapObject(
                pairs=self.pairs[  # type: ignore[index]
                    key.from_.value  # type: ignore[union-attr]
                    - 1 : key.to.value if key.to is not None else None : (
                        key.by.value if key.by is not None else None
                    )
                ]
            )
        )

    def __iter__(self) -> 'HashMapObject':
        """iterates over the pairs in the hash map."""
        self._index = 0
        return self

    def __next__(self) -> Tuple[FarrObject, FarrObject]:
        """Returns the next pair."""
        if self.pairs is not None and self._index >= len(self.pairs):
            raise StopIteration
        pair = self.pairs[self._index]  # type: ignore[index]
        self._index += 1
        return pair.key, pair.value

    def _drop_duplicates(self) -> None:
        """Removes duplicate pairs."""
        self.pairs = list({pair.key: pair for pair in self.pairs}.values())  # type: ignore[union-attr]

    @property
    def first(self) -> 'PairObject':
        """Returns the first existing pair."""
        if not self.pairs:
            raise IndexError('No pair found!')
        return self.pairs[0]

    @property
    def last(self) -> 'PairObject':
        """Returns the last existing pair."""
        if not self.pairs:
            raise IndexError('No pair found!')
        return self.pairs[-1]

    @property
    def length(self) -> IntegerObject:
        """Returns the number of existing pairs."""
        return IntegerObject(value=len(self.pairs))  # type: ignore[arg-type]

    @property
    def keys(self) -> ListObject:
        """Returns all available keys."""
        return ListObject(elements=list(map(lambda x: x.key, self.pairs)))  # type: ignore[arg-type]

    @property
    def values(self) -> ListObject:
        """Returns all values."""
        return ListObject(elements=list(map(lambda x: x.value, self.pairs)))  # type: ignore[arg-type]

    def isempty_q(self) -> BooleanObject:
        """Returns whether there is a pair or not."""
        return BooleanObject(value=not bool(self.pairs))

    def clear_e(self) -> NullObject:
        """Makes the object empty of pairs."""
        self.pairs = []
        return NullObject()

    def get(
        self,
        key: FarrObject,
        orelse: Optional[FarrObject] = None,
    ) -> FarrObject:
        """Returns a value based on the key or something else."""
        return {pair.key: pair.value for pair in self.pairs}.get(  # type: ignore[union-attr]
            key, orelse if orelse is not None else NullObject()
        )

    def iupdate_e(self, hash_map: 'HashMapObject') -> 'HashMapObject':
        """Updates the current pairs based on the new values."""
        self.pairs.extend(hash_map.pairs)  # type: ignore[union-attr, arg-type]
        self._drop_duplicates()
        return self

    def pop_e(self, index: IntegerObject) -> 'PairObject':
        """Discards a pair based on its index."""
        if index.value <= 0:
            raise IndexError('Non-positive indexes are not allowed!')
        return self.pairs.pop(index.value - 1)  # type: ignore[union-attr]

    def popitem_e(self, key: FarrObject) -> 'PairObject':
        """Deletes a pair based on the key."""
        return self.pairs.pop(self.pairs.index(key))  # type: ignore[union-attr, arg-type]


@dataclass
class PairObject(DataStructureObject):
    key: FarrObject = field(kw_only=True)
    value: FarrObject = field(kw_only=True)

    def __str__(self) -> str:
        """Returns the key and value along with an arrow."""
        return f'{self.key}->{self.value}'

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Compares the key with another object for equality."""
        return BooleanObject(value=self.key == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Compares the key with another object for inequality."""
        return BooleanObject(value=self.key != other)

    def __hash__(self) -> int:
        """Calculates the hash of the object."""
        return hash((self.key, self.value))


class PythonNativeObject(ExpressionObject):
    pass


@dataclass
class PythonNativeClassMethodObject(PythonNativeObject):
    method: types.MethodType = field(kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks the sameness of two methods."""
        return BooleanObject(value=self.method.__func__.__qualname__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks to see the difference between the two methods."""
        return BooleanObject(value=self.method.__func__.__qualname__ != other)

    def __call__(
        self,
        *args: Tuple[FarrObject, ...],
        **kwargs: Dict[str, FarrObject],
    ) -> FarrObject:
        """Calls the method."""
        return self.method(*args, **kwargs)


class PythonNativePrintObject(PythonNativeObject):
    def __call__(
        self,
        *args: Tuple[FarrObject, ...],
    ) -> NullObject:
        """Prints and stays on the same line."""
        print(*args, end='')
        return NullObject()


class PythonNativePrintLineObject(PythonNativeObject):
    def __call__(
        self,
        *args: Tuple[FarrObject, ...],
    ) -> NullObject:
        """Prints and goes to the next line."""
        print(*args)
        return NullObject()


class PythonNativeReadLineObject(PythonNativeObject):
    def __call__(self, prompt: Optional[StringObject] = None) -> StringObject:
        """Takes an input from the user."""
        return StringObject(value=input(prompt if prompt is not None else ''))


class PythonNativePanicObject(PythonNativeObject):
    def __call__(
        self,
        exception: Optional[BaseException] = None,
    ) -> None:
        """Throws an error."""
        raise exception if exception is not None else BaseException  # type: ignore[misc]


class PythonNativeAssertObject(PythonNativeObject):
    def __call__(
        self,
        condition: FarrObject,
        message: Optional[StringObject] = None,
    ) -> None:
        """Panics if the condition is not correct."""
        assert condition, message if message is not None else ''


class PythonNativeExitObject(PythonNativeObject):
    def __call__(self, code: Optional[IntegerObject] = None) -> None:
        """Comes out based on the given exit code."""
        sys.exit(code)  # type: ignore[arg-type]


class PythonNativeTypeOfObject(PythonNativeObject):
    def __call__(self, object_: FarrObject) -> StringObject:
        """Returns the object type."""
        return StringObject(value=object_.__class__.__name__)


class PythonNativeSimilarTypesObject(PythonNativeObject):
    def __call__(
        self,
        object_: FarrObject,
        target: FarrObject,
    ) -> BooleanObject:
        """Checks whether there are similar types or not."""
        return BooleanObject(value=object_.__class__ == target.__class__)


class PythonNativeShellExecutionObject(PythonNativeObject):
    def __call__(self, cmd: StringObject) -> StringObject:
        """Executes the command in the shell and returns the result."""
        return StringObject(value=subprocess.getoutput(cmd.value))


class PythonNativeBaseErrorObject(BaseException, PythonNativeObject):
    pass


class PythonNativeKeyboardInterruptErrorObject(
    KeyboardInterrupt,
    PythonNativeObject,
):
    pass


class PythonNativeSystemExitErrorObject(SystemExit, PythonNativeObject):
    pass


class PythonNativeArithmeticErrorObject(ArithmeticError, PythonNativeObject):
    pass


class PythonNativeAssertionErrorObject(AssertionError, PythonNativeObject):
    pass


class PythonNativeAttributeErrorObject(AttributeError, PythonNativeObject):
    pass


class PythonNativeImportErrorObject(ImportError, PythonNativeObject):
    pass


class PythonNativeLookupErrorObject(LookupError, PythonNativeObject):
    pass


class PythonNativeNameErrorObject(NameError, PythonNativeObject):
    pass


class PythonNativeOSErrorObject(OSError, PythonNativeObject):
    pass


class PythonNativeRuntimeErrorObject(RuntimeError, PythonNativeObject):
    pass


class PythonNativeNotImplementedErrorObject(
    NotImplementedError,
    PythonNativeObject,
):
    pass


class PythonNativeTypeErrorObject(TypeError, PythonNativeObject):
    pass


class PythonNativeValueErrorObject(ValueError, PythonNativeObject):
    pass


class PythonNativeDeprecatedErrorObject(DeprecationWarning, PythonNativeObject):
    pass


@dataclass
class StructInstanceObject(ExpressionObject):
    environment: Environment = field(repr=False, kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are similar."""
        return BooleanObject(value=self.__dict__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are different or not."""
        return BooleanObject(value=self.__dict__ != other)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    def __getattr__(self, name: str) -> FarrObject:
        """Finds the value from the environment."""
        return self.environment.locate(name)


class StatementObject(FarrObject):
    pass


@dataclass
class ImportSystemObject(StatementObject):
    environment: Environment = field(repr=False, kw_only=True)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)

    def __getattr__(self, name: str) -> FarrObject:
        """Makes the modules available."""
        return self.environment.locate(name)


class ModuleObject(ImportSystemObject):
    pass


class LibraryObject(ImportSystemObject):
    pass


@dataclass
class NonPythonNativeObject(StatementObject):
    environment: Optional[Environment] = field(
        default=None, repr=False, kw_only=True
    )
    body: BlockNode = field(repr=False, kw_only=True)


@dataclass
class FunctionDefinitionObject(NonPythonNativeObject):
    params: ItemizedExpressionNode = field(repr=False, kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are similar."""
        return BooleanObject(value=self.__dict__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are different or not."""
        return BooleanObject(value=self.__dict__ != other)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)


@dataclass
class StructDefinitionObject(NonPythonNativeObject):
    attributes: ItemizedExpressionNode = field(repr=False, kw_only=True)

    def __eq__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are similar."""
        return BooleanObject(value=self.__dict__ == other)

    def __ne__(self, other: FarrObject) -> BooleanObject:  # type: ignore[override]
        """Checks whether the attributes are different or not."""
        return BooleanObject(value=self.__dict__ != other)

    def __hash__(self) -> int:
        """Returns the object ID as a hash."""
        return id(self)
