from time import sleep
from typing import Callable
from rich.console import Console
import functools

console = Console(log_path=False)

def spinner(console: Console, msg: str, spinner: str="dots") -> Callable:
    def decorator_spinner(func):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            with console.status(msg, spinner=spinner):
                value = func(*args, **kwargs)
            return value

        return wrapper_decorator

    return decorator_spinner

if __name__ == '__main__':
    @spinner(console, "hallo!")
    def wait(x):
        sleep(x)

    wait(10)