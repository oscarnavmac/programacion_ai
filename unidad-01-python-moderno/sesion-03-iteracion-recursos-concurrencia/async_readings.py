"""Collect station readings with explicit asynchronous resource ownership."""

import asyncio
from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from math import isfinite

STATION_VALUES = {"north": 18.0, "south": 27.0, "west": 32.0}


class ReadingClient:
    """Model an asynchronous client using in-memory readings and simulated latency."""

    def __init__(self, delay: float = 0.1) -> None:
        if not isfinite(delay) or delay < 0:
            raise ValueError("Delay must be finite and nonnegative")
        self.delay = delay
        self.closed = True
        self.active = 0
        self.peak_active = 0

    async def connect(self) -> None:
        await asyncio.sleep(0)
        self.closed = False

    async def fetch(self, station: str) -> tuple[str, float]:
        if self.closed:
            raise RuntimeError("Client is closed")
        self.active += 1
        self.peak_active = max(self.peak_active, self.active)
        try:
            await asyncio.sleep(self.delay)
            return station, STATION_VALUES[station]
        finally:
            self.active -= 1

    async def close(self) -> None:
        await asyncio.sleep(0)
        self.closed = True


@asynccontextmanager
async def open_reading_client(delay: float = 0.1) -> AsyncIterator[ReadingClient]:
    client = ReadingClient(delay)
    await client.connect()
    try:
        yield client
    finally:
        await client.close()


async def collect_readings(
    client: ReadingClient, stations: Sequence[str], limit: int = 2
) -> list[tuple[str, float]]:
    """Preserve input order and bound active requests for a small batch."""
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("Limit must be a positive integer")
    semaphore = asyncio.Semaphore(limit)

    async def fetch_limited(station: str) -> tuple[str, float]:
        async with semaphore:
            return await client.fetch(station)

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(fetch_limited(station)) for station in stations]
    return [task.result() for task in tasks]


async def main() -> None:
    async with open_reading_client() as client:
        readings = await collect_readings(client, ["north", "south", "west"])
        print(readings)
        print(f"Peak active requests: {client.peak_active}")
    print(f"Client closed: {client.closed}")


if __name__ == "__main__":
    asyncio.run(main())
