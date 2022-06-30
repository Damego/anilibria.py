from asyncio import get_event_loop
from typing import Callable, Dict, List, Union
from logging import getLogger


log = getLogger("anilibria.dispatch")


class EventListener:
    def __init__(self) -> None:
        self.loop = get_event_loop()
        self.events: Dict[str, List[Dict[str, Union[Callable, str]]]] = {}

    def dispatch(self, name: str, *args, **kwargs):
        for event_data in self.events.get(name, []):
            event = event_data["coro"]
            self.loop.create_task(event(*args, **kwargs))
        log.debug(f"Event {name} dispatched")

    def add_event(self, name: str, data: Dict[str, Union[Callable, str]]):
        event = self.events.get(name, [])
        event.append(data)

        self.events[name] = event
        log.debug(f"Added coro to {name} event. Total coros for this event: {self.events[name]}")
