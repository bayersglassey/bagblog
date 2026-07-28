# How do Python's asyncio and async/await work?

I think most programmers these days are at least somewhat familiar with
Javascript's promises, and maybe even know that its async/await keywords
are a kind of syntactic sugar for promises.

Well, the same is true of Python, except instead of a Promise class, there's
a Future class.
There are explanations of this out there on the Internet, but I have yet to
see a really nice minimalist example you can play with yourself at the REPL.
So, here it is!..

```python
import asyncio
from typing import Awaitable


# We need an event loop so we can create asyncio.Future instances.
# But we're going to simulate the event loop's behaviour, so we're never
# going to actually ask the loop object to do anything.
loop = asyncio.new_event_loop()


# We're going to simulate some kind of async I/O library, without using the
# async or await keywords!
# When some async code kicks off an I/O request, we're going to add it to
# this list.
# Then, when our I/O library has a chance to do some work, it'll process the
# requests in this list.
# Each request has an associated Future, and when we set its result, that'll
# wake up the async code awaiting on it.
Request = str
Response = str
pending_io_requests: list[tuple[Request, asyncio.Future[Response]]] = []

# NOTE: this function behaves like it was defined using "async def"!
def do_some_io(request: Request) -> Awaitable[Response]:
    print(f"Sending request: {request}")
    future = asyncio.Future(loop=loop)
    pending_io_requests.append((request, future))
    return future

def handle_io_requests():
    for request, future in pending_io_requests:
        response = f"Response for {request}"
        future.set_result(response)
    pending_io_requests.clear()

    # Do some low-level stuff the loop would usually do for itself...
    # Specifically, we need to do this in order for the futures returned by
    # asyncio.gather() to realize that the futures they're waiting on have
    # completed.
    while loop._ready:
        handle = loop._ready.popleft()
        handle._run()


# Okay, now let's test our I/O library.
# We'll use an async function, but we're not going to await it!..
# We're going to create a coroutine from it, and manually run the coroutine
# a little bit at a time...

async def main():
    print("Start!")

    response = await do_some_io("request A")
    print(f"Got response: {response}")

    responses = await asyncio.gather(
        do_some_io("request B"),
        do_some_io("request C"),
    )
    print(f"Got gathered responses: {responses}")


# Since f was defined with "async def", it returns a coroutine.
coro = main()

# Run the coroutine for a bit...
coro.send(None)

# Handle any pending IO requests...
handle_io_requests()

# Run the coroutine for a bit more...
coro.send(None)

# Handle any pending IO requests...
handle_io_requests()

# Run the coroutine to completion
try: coro.send(None)
except StopIteration: pass
```

The output is:
```
Start!
Sending request: request A
Got response: Response for request A
Sending request: request B
Sending request: request C
Got gathered responses: ['Response for request B', 'Response for request C']
```
