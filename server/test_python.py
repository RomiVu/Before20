from typing import (
    Any,
    Optional,
    Dict,
    Mapping,
    List,
    Tuple,
    Match,
    Callable,
    Type,
    Sequence,
)
import sys
from random import random
from collections import deque
from functools import wraps
from time import time


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        rslt = func(*args, **kwargs)
        print(f'{func.__name__} time used {time()-start}')
        return rslt
    return wrapper


class ObjectDict(Dict[str, Any]):
    """Makes a dictionary behave like an object, with attribute-style access.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

@timeit
def append_list():
    a = [i * random() for i in range(10000)] 
    count = 0
    while count < 10000:
        count += 1
        a.append(random())
        a.insert(0, random())
    return a[0]


@timeit
def append_deque():
    a = deque([i*random() for i in range(10000)])
    count = 0
    while count < 10000:
        count += 1
        a.append(random()) 
        a.appendleft(random())
    
    return a[0]    

if __name__ == "__main__":
    append_list()
    append_deque()
