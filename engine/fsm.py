class FlowNode:
    """
    FSM(Finite State Machine)의 State입니다.
    일반적인 상태를 나타내는 State와 헷갈리는 것을 방지하고자 FlowNode라고 이름지었습니다.
    """

    machine: "FlowMachine"

    def __init__(self) -> None:
        pass

    def enter(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def exit(self) -> None:
        pass


class FlowMachine:
    """
    FSM(Finite State Machine)의 StateMachine입니다.
    일반적인 상태를 나타내는 State와 헷갈리는 것을 방지하고자 StateMachine대신 FlowMachine이라고 이름지었습니다.
    """

    _current_node: FlowNode

    def __init__(self) -> None:
        self._current_node = None

    def update(self, dt: float) -> None:
        self._current_node.update()

    @property
    def current_node(self) -> FlowNode:
        return self._current_node

    def transition_to(self, new_node: FlowNode) -> None:
        if self._current_node is not None:
            self._current_node.exit()

        self._current_node = new_node
        self._current_node.machine = self
        self._current_node.enter()
