from asyncio import get_event_loop
from typing import Coroutine

# TODO: Использовать logger


class EventListener:
    def __init__(self) -> None:
        self.loop = get_event_loop()
        self.events = {}

    def dispatch(self, name: str, *args, **kwargs):
        for event in self.events.get(name, []):
            self.loop.create_task(event(*args, **kwargs))
            print(f"event {name} was dispatched")

    def add_event(self, coro: Coroutine, name: str = None):
        _name = name or coro.__name__
        event = self.events.get(_name, [])
        event.append(coro)

        self.events[_name] = event
        print(f"Event {_name} added")
        print(f"Coros for {_name}:", self.events[_name])
