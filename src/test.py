def action(func):
    """Decorator to mark methods as an action and register them."""
    if not hasattr(func, '__action__'):
        func.__action__ = []  # Initialize once
    func.__action__.append(func.__name__)
    return func

def quick_action(func):
    """Decorator to mark methods as quick actions and register them.
    
    All quick actions are also registered as actions.
    """
    action(func)
    if not hasattr(func, '__quick_action__'):
        func.__quick_action__ = []  # Initialize once
    func.__quick_action__.append(func.__name__)
    return func

class Tree:
    def __init__(self) -> None:
        pass
    
    def get_actions(self):
        methods = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        return [(m, getattr(self,m)) for m in methods if hasattr(getattr(self,m), "__action__")]
    
    def get_quick_actions(self):
        methods = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        return [(m, getattr(self,m)) for m in methods if hasattr(getattr(self,m), "__quick_action__")]

    @quick_action
    def shake(self):
        print("You shook the tree")

    @action
    def ztest(self):
        print("Check if it sorts alphabetically.")

    @action
    def inspect(self):
        print("It's an oak tree.")


print("Tree actions:", Tree().get_actions())
print("Tree quick actions:", Tree().get_quick_actions())
Tree().get_actions()[0][1]() # Call 1st action in list