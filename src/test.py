class Foo:
    def __init__(self) -> None:
        pass
    def test(self):
        print(self.call_me())
    def call_me(self):
        print("I'm Foo")

class Bar(Foo):
    def __init__(self) -> None:
        super().__init__()
    def call_me(self):
        print("I'm Bar.")

Bar().call_me()