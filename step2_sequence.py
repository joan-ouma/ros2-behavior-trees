"""
Step 2: A Sequence with two children.

Sequence runs children left to right. If either one fails, the whole
Sequence fails immediately and stops -- it never ticks the remaining
children. It only succeeds if every child succeeds.
"""
import py_trees


class PrintAndSucceed(py_trees.behaviour.Behaviour):
    """A reusable leaf: prints a message, always succeeds."""

    def __init__(self, name, message):
        super().__init__(name=name)
        self.message = message

    def update(self):
        print(f"[{self.name}] {self.message}")
        return py_trees.common.Status.SUCCESS


# Build a Sequence with two children.
root = py_trees.composites.Sequence(name="Deliver package", memory=True)
root.add_children([
    PrintAndSucceed(name="DriveToDoor", message="driving to the front door..."),
    PrintAndSucceed(name="DropPackage", message="dropping the package..."),
])

print("--- Tree structure ---")
print(py_trees.display.ascii_tree(root))

print("--- Ticking the tree ---")
root.tick_once()

print("--- Final status ---")
print(root.status)