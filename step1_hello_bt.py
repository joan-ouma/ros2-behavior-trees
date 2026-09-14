"""
Step 1: The simplest possible behavior tree.

One single node. We tick it once and print what comes back.
"""
import py_trees


class SaySuccess(py_trees.behaviour.Behaviour):
    """A leaf node that does nothing except always report SUCCESS."""

    def update(self):
        print("SaySuccess: doing my one job")
        return py_trees.common.Status.SUCCESS


# Build the tree -- here it's just a single node, no parent needed yet.
root = SaySuccess(name="SaySuccess")

# Tick it once. This is the same "tick" concept from the diagram --
# the tree runs one full pass and reports back a status.
root.tick_once()

print("Final status:", root.status)