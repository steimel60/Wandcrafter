class A:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2

class B(A):
    def __init__(self, p3, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.p3 = p3

b = B(p3 = 3, p1 = 1, p2 =2)

print(b.p1, b.p2, b.p3)