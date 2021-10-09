from typing import AsyncGenerator, Awaitable, TypeVar

T = TypeVar("T")


def anext(async_generator: AsyncGenerator[T, None]) -> Awaitable[T]:
    return async_generator.__anext__()
