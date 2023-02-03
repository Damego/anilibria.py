import asyncio
from collections import defaultdict
from logging import getLogger
from typing import Callable, Coroutine, Dict, List

log = getLogger("anilibria.dispatch")
__all__ = ("Dispatch",)


class Dispatch:
    def __init__(self) -> None:
        self._registered_events: Dict[str, List[Callable[..., Coroutine]]] = defaultdict(list)

    @staticmethod
    async def _call(coro: Callable[..., Coroutine], *args):
        try:
            await coro(*args)
        except Exception:  # noqa
            log.exception("")

    def call(self, name: str, *args):
        log.debug(f"Dispatching event {name}")

        for coro in self._registered_events.get(name, []):
            asyncio.create_task(self._call(coro, *args))

    def register(self, name: str, coro: Callable[..., Coroutine]):
        self._registered_events[name].append(coro)

        log.debug(
            f"Added coro to {name} event. Total coros for this event: {self._registered_events[name]}"
        )
