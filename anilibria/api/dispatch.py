from asyncio import get_event_loop
from typing import Callable, Dict, List, Coroutine, Optional
from logging import getLogger

from .models.attrs_utils import define, field, DictSerializer


log = getLogger("anilibria.dispatch")
__all__ = ["Event", "EventDispatcher"]


@define()
class Event(DictSerializer):
    coro: Callable = field()
    data: Optional[dict] = field(factory=dict)  # Extra data


class EventDispatcher:
    def __init__(self) -> None:
        self.loop = get_event_loop()
        self.events: Dict[str, List[Event]] = {}

    def _dispatch(self, coro: Coroutine):
        self.loop.create_task(coro)

    def dispatch(self, name: str, *args, **kwargs):
        log.debug(f"Dispatching event {name}")
        for event_data in self.events.get(name, []):
            self._dispatch(event_data.coro(*args, **kwargs))

    def add_event(self, name: str, event: Event):
        events = self.events.get(name, [])
        events.append(event)

        self.events[name] = events
        log.debug(f"Added coro to {name} event. Total coros for this event: {self.events[name]}")
