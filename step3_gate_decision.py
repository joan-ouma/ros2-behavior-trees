"""
Step 3: Fallback + Condition, matching the tree you saw in the diagram.

Structure:

Sequence "Navigate to offload zone"
  |-- Fallback "Choose route"
  |     |-- Sequence "Take path 2"
  |     |     |-- Condition "GateOpen"
  |     |     `-- Action "DrivePath2"
  |     `-- Action "DrivePath1" (always succeeds -- always open)
  `-- Action "Arrive"

We tick this tree twice: once with the gate closed, once with it open,
so you can see the SAME tree take a different path depending on one
condition -- no new code, just a different runtime outcome.
"""
import py_trees


class PrintAndSucceed(py_trees.behaviour.Behaviour):
    def __init__(self, name, message):
        super().__init__(name=name)
        self.message = message

    def update(self):
        print(f"  [{self.name}] {self.message}")
        return py_trees.common.Status.SUCCESS


class GateOpen(py_trees.behaviour.Behaviour):
    """A Condition node. Conditions only ever return SUCCESS or FAILURE,
    never RUNNING -- they're an instant check, not an ongoing action."""

    def __init__(self, name, gate_state_fn):
        super().__init__(name=name)
        self.gate_state_fn = gate_state_fn

    def update(self):
        if self.gate_state_fn():
            print(f"  [{self.name}] gate is open -> SUCCESS")
            return py_trees.common.Status.SUCCESS
        else:
            print(f"  [{self.name}] gate is closed -> FAILURE")
            return py_trees.common.Status.FAILURE


def build_tree(gate_state_fn):
    take_path_2 = py_trees.composites.Sequence(name="Take path 2", memory=True)
    take_path_2.add_children([
        GateOpen(name="GateOpen?", gate_state_fn=gate_state_fn),
        PrintAndSucceed(name="DrivePath2", message="driving the flat, gated route"),
    ])

    drive_path_1 = PrintAndSucceed(name="DrivePath1", message="driving the always-open ramps route")

    choose_route = py_trees.composites.Selector(name="Choose route", memory=True)
    choose_route.add_children([take_path_2, drive_path_1])

    root = py_trees.composites.Sequence(name="Navigate to offload zone", memory=True)
    root.add_children([
        choose_route,
        PrintAndSucceed(name="Arrive", message="arrived at the offload zone"),
    ])
    return root


def run_once(gate_is_open):
    label = "OPEN" if gate_is_open else "CLOSED"
    print(f"\n=== Tick with gate {label} ===")
    tree = build_tree(gate_state_fn=lambda: gate_is_open)
    tree.tick_once()
    print(f"Root status: {tree.status}")


if __name__ == "__main__":
    print("--- Tree structure ---")
    print(py_trees.display.ascii_tree(build_tree(gate_state_fn=lambda: True)))

    run_once(gate_is_open=False)  # gate closed -> falls back to path 1
    run_once(gate_is_open=True)   # gate open   -> takes path 2