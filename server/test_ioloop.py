

class A:
    __a = None
    __b = None

    def __new__(cls, *args, **kwargs):
        print(f"fuck ... A is __new__{args} {kwargs}")

    @classmethod
    def init(cls, *args, **kwargs):
        raise NotImplementedError()

class B(A):
#    def init(self, *args, **kwargs):
#        print(f"fuck ... B is init")
    @staticmethod
    def _print():
        print("B.print...")
        return 0

if __name__ == "__main__":
    a = B._print()
