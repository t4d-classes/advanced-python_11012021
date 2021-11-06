from __future__ import annotations
from typing import Any, Iterator


# arr = np.array([1,2,3,4,5,6])

# # overload the greater than operator
# exp = arr > 3 # [ False, False, False, True, True, True ]

# # overload the indexer
# arr[exp] # [4,5,6]

# arr[arr > 3]

class ItemList:

    def __init__(self) -> None:
        self.__items: list[Any] = []

    def __add__(self, new_item: Any) -> ItemList:
        self.__items.append(new_item)
        return self

    def __sub__(self, item_to_remove: Any) -> ItemList:
        self.__items.remove(item_to_remove)
        return self

    def __iter__(self) -> Iterator[Any]:
        self.__current_iter = iter(self.__items)
        return self.__current_iter

    def __next__(self) -> Any:
        return next(self.__current_iter)

nums = ItemList()
nums = nums + 2
nums += 4
nums += 6

for num in nums:
    print(num)

nums -= 4

for num in nums:
    print(num)


# class MyObj:
#     ...

# t = MyObj()

# for x in t:
#     print(x)