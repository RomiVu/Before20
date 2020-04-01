class Parent:
    def __init__(self):
        self.parent_names = "hello and world"
        print(f"Parent is initiation {self.parent_names}")
    
    def hit_child(self):
         print("winter is coming from parent...")

class Child(Parent):
    def __init__(self, name):
        #super(Parent, self).__init__(self)
        self.child_names = "child_name : " + name
        print(f"child is initixaiton {self.child_names}  ")
    
    def hit_child(self):
        #super(Parent, self).hit_child()
        super().hit_child()
        print(f"fuck... {self.child_names} ")


class A:
    def __init__(self):
        print("A")



class B(A):
    def __init__(self):
        print("B")
        super().__init__()

class C(A):
    def __init__(self):
        print("C")
        super(C, self).__init__()

import collections, logging
from pprint import pprint as pp

class LoggingDict(dict):
    def __setitem__(self, k, v):
        logging.info(f"inserting {k} : {v}")
        super().__setitem__(k, v)

class LoggingOD(LoggingDict, collections.OrderedDict):
    pass


class S:
    def __init__(self, s, **kw):
        self.s = s
        super().__init__(**kw)


class SC(S):
    def __init__(self, c, **kw):
        self.c = c
        super().__init__(**kw)


class Root: pass
    #def draw(self):
    #    print("fuck. this draw is stopped here.")
        # the delegation chain stops here
    #    assert not hasattr(super(), 'draw')


class Shape(Root):
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super().__init__(**kwds)

    def draw(self):
        print('Drawing.  Setting shape to:', self.shapename)
        #super().draw()
        assert not hasattr(super(), "draw")


class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super().__init__(**kwds)

    def draw(self):
        print('Drawing.  Setting color to:', self.color)
        super().draw()

cs = ColoredShape(color='blue', shapename='square')
cs.draw()


if __name__ == "__main__":
    pass
