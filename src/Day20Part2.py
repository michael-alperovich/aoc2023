import abc
import math
import pathlib
from collections import deque
from enum import Enum, auto
from typing import List, Dict

CURRENT_PATH = pathlib.Path(__file__)
IN_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_in.txt'
OUT_FILE = CURRENT_PATH.parent.parent / f'resources/{CURRENT_PATH.stem}_out.txt'


class Pulse(Enum):
    HIGH = auto()
    LOW = auto()


class Module(abc.ABC):
    press_counter = 0
    _queue = deque()

    def __init__(self, name: str, subscriber_names: List[str]) -> None:
        self.name = name
        self._subscriber_names = subscriber_names
        self._subscribers = []
        self.first_high = -1

    def init_subscribers(self, modules: Dict[str, 'Module']) -> None:
        for sn in self._subscriber_names:
            m = modules.get(sn, EmptyModule(name=sn))
            self._subscribers.append(m)
            m.register_input(self)

    def register_input(self, module: 'Module') -> None:
        pass

    def receive(self, pulse: Pulse, module: 'Module') -> None:
        Module._queue.append(lambda: self.process(pulse, module))

    def is_activator(self) -> bool:
        return 'rx' in self._subscriber_names

    def is_key(self, activator_module: 'Module') -> bool:
        return activator_module in self._subscribers

    @abc.abstractmethod
    def process(self, pulse: Pulse, module: 'Module') -> None:
        pass

    def _send(self, pulse: Pulse) -> None:
        if pulse == Pulse.HIGH and self.first_high == -1:
            self.first_high = Module.press_counter
        for s in self._subscribers:
            s.receive(pulse=pulse, module=self)

    @classmethod
    def process_queue(cls) -> None:
        while len(cls._queue) > 0:
            func = cls._queue.popleft()
            func()


class FlipFlopModule(Module):

    def __init__(self, name: str, subscriber_names: List[str]):
        super().__init__(name, subscriber_names)
        self.state_on = False

    def process(self, pulse: Pulse, module: Module) -> None:
        super().process(pulse, module)
        if pulse == Pulse.LOW:
            new_pulse = Pulse.HIGH if not self.state_on else Pulse.LOW
            self.state_on = not self.state_on
            self._send(pulse=new_pulse)


class ConjunctionModule(Module):

    def __init__(self, name: str, subscriber_names: List[str]):
        super().__init__(name, subscriber_names)
        self._pulse_memory: Dict[str, Pulse] = {}

    def register_input(self, module: 'Module') -> None:
        self._pulse_memory[module.name] = Pulse.LOW

    def process(self, pulse: Pulse, module: Module) -> None:
        super().process(pulse, module)
        self._pulse_memory[module.name] = pulse
        new_pulse = Pulse.LOW if all((p == Pulse.HIGH for p in self._pulse_memory.values())) else Pulse.HIGH
        self._send(new_pulse)


class BroadcastModule(Module):

    def process(self, pulse: Pulse, module: Module) -> None:
        super().process(pulse, module)
        self._send(pulse)


class ButtonModule(Module):

    def __init__(self):
        super().__init__(name='button', subscriber_names=['broadcaster'])

    def process(self, pulse: Pulse, module: 'Module') -> None:
        pass

    def push(self) -> None:
        Module.press_counter += 1
        self._send(Pulse.LOW)


class EmptyModule(Module):

    def __init__(self, name: str):
        super().__init__(name, subscriber_names=[])

    def process(self, pulse: Pulse, module: 'Module') -> None:
        pass


class ModuleFactory:

    @classmethod
    def parse(cls, config: str) -> Module:
        module_config, subscribers_config = config.split(' -> ')
        if module_config.startswith('%'):
            module_cls = FlipFlopModule
            module_name = module_config.strip()[1:]
        elif module_config.startswith('&'):
            module_cls = ConjunctionModule
            module_name = module_config.strip()[1:]
        else:
            module_cls = BroadcastModule
            module_name = module_config.strip()
        subscribers = subscribers_config.strip().split(', ')
        return module_cls(name=module_name, subscriber_names=subscribers)


def main():
    lines = IN_FILE.read_text().split('\n')
    modules = {'button': ButtonModule()}
    for line in lines:
        module = ModuleFactory.parse(config=line)
        modules[module.name] = module
    for module in modules.values():
        module.init_subscribers(modules=modules)

    activator_module = [m for m in modules.values() if m.is_activator()][0]
    key_modules = [m for m in modules.values() if m.is_key(activator_module)]
    flag = True
    while flag:
        modules['button'].push()
        Module.process_queue()
        for module in key_modules:
            if module.first_high == -1:
                break
        else:
            flag = False

    ans = math.lcm(*[m.first_high for m in key_modules])
    OUT_FILE.write_text(str(ans))


if __name__ == '__main__':
    main()
