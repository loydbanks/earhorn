from datetime import datetime
from pathlib import Path
from queue import Empty, Queue
from subprocess import CalledProcessError, run
from threading import Event as ThreadEvent
from threading import Thread
from typing import List, Optional, Union

from loguru import logger
from pydantic import BaseModel, Field
from typing_extensions import Literal, Protocol, TypeAlias

from .prometheus import stream_silence, stream_status, unhandled_errors


def now():
    return datetime.now()


class Event(BaseModel):
    # pylint: disable=unnecessary-lambda
    when: datetime = Field(default_factory=lambda: now())


class SilenceEvent(Event):
    name = "silence"
    kind: Literal["start", "end"]
    seconds: Optional[float]
    duration: Optional[float]


class StatusEvent(Event):
    name = "status"
    kind: Literal["up", "down"]


class ErrorEvent(Event):
    name = "error"
    message: str


AnyEvent: TypeAlias = Union[SilenceEvent, StatusEvent, ErrorEvent]


class Hook(Protocol):  # pylint: disable=too-few-public-methods
    def __call__(self, event: AnyEvent):
        pass


class HookError(Exception):
    """An error that occurred inside a hook"""


class FileHook:  # pylint: disable=too-few-public-methods
    filepath: Path

    def __init__(self, filepath: str) -> None:
        self.filepath = Path(filepath)
        if not self.filepath.is_file():
            raise ValueError(f"hook '{self.filepath}' is not a file!")

    def __call__(self, event: AnyEvent):
        try:
            run((self.filepath, event.json()), check=True)
        except CalledProcessError as exception:
            logger.error(exception)
            raise HookError(exception)


class PrometheusHook:  # pylint: disable=too-few-public-methods
    def __call__(self, event: AnyEvent):
        if isinstance(event, StatusEvent):
            stream_status.state(event.kind)  # pylint: disable=no-member
        elif isinstance(event, SilenceEvent):
            state_map = {"start": "up", "end": "down"}
            stream_silence.state(state_map[event.kind])  # pylint: disable=no-member
        elif isinstance(event, ErrorEvent):
            unhandled_errors.info(event.dict())


class Handler(Thread):
    name = "handler"
    queue: Queue
    stop: ThreadEvent
    hooks: List[Hook] = []

    def __init__(
        self,
        queue: Queue,
        stop: ThreadEvent,
    ):
        Thread.__init__(self)
        self.queue = queue
        self.stop = stop

    def run(self):
        logger.info("starting event handler")

        while not self.stop.is_set() or not self.queue.empty():
            try:
                event: AnyEvent = self.queue.get(timeout=5)
                logger.debug(f"{event.name}: {event.json()}")
                for hook in self.hooks:
                    try:
                        hook(event)
                    except HookError as exception:
                        self.queue.put(ErrorEvent(message=str(exception)))
                self.queue.task_done()
            except Empty:
                pass

        logger.info("stopped event handler")
