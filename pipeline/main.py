import functools
import logging
import asyncio
import signal
from typing import Coroutine, List

LOG = logging.getLogger(__name__)


def cancel_all_tasks(loop: asyncio.BaseEventLoop):
    LOG.debug('Cancelling tasks.')
    tasks = asyncio.gather(
        *asyncio.Task.all_tasks(loop=loop),
        loop=loop,
        return_exceptions=True,
    )

    tasks.cancel()


def main(tasks: List[Coroutine]):
    '''
    Main entry point for a task.
    Adds signal handlers and starts the task.
    '''
    loop = asyncio.get_event_loop()

    # connect signal handler for stopping program
    stop_signals = [signal.SIGINT, signal.SIGHUP]
    stop_handler = functools.partial(cancel_all_tasks, loop)
    for value in stop_signals:
        loop.add_signal_handler(value, stop_handler)

    LOG.debug('Starting loop.')
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except asyncio.CancelledError:
        LOG.debug('Cancelled tasks. Shutting down.')

    LOG.debug('Main finished.')
