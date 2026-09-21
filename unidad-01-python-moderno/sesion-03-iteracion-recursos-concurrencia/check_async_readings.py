"""Check concurrency and cleanup without timing-based speed assertions."""
import asyncio
import unittest
from async_readings import ReadingClient, collect_readings, open_reading_client


class AsyncReadingTests(unittest.IsolatedAsyncioTestCase):
    async def test_results_and_duplicates(self):
        async with open_reading_client(delay=0) as client:
            result = await collect_readings(client, ["west", "north", "west"])
        self.assertEqual(result, [("west", 32.0), ("north", 18.0), ("west", 32.0)])
        self.assertTrue(client.closed)
        self.assertEqual(client.active, 0)

    async def test_empty(self):
        async with open_reading_client(delay=0) as client:
            self.assertEqual(await collect_readings(client, []), [])
            self.assertEqual(client.peak_active, 0)

    async def test_limit_and_overlap(self):
        class GatedClient(ReadingClient):
            def __init__(self):
                super().__init__(delay=0)
                self.entered = 0
                self.gate = asyncio.Event()

            async def fetch(self, station):
                self.entered += 1
                if self.entered == 2:
                    self.gate.set()
                await self.gate.wait()
                return await super().fetch(station)

        client = GatedClient()
        await client.connect()
        try:
            async with asyncio.timeout(2):
                result = await collect_readings(client, ["north", "south", "west"], 2)
            self.assertEqual(len(result), 3)
            self.assertEqual(client.peak_active, 2)
        finally:
            await client.close()

    async def test_limit_one(self):
        async with open_reading_client(delay=0) as client:
            await collect_readings(client, ["north", "south", "west"], 1)
            self.assertEqual(client.peak_active, 1)

    async def test_invalid_limit(self):
        async with open_reading_client(delay=0) as client:
            for limit in (0, -1, True, 1.5):
                with self.subTest(limit=limit), self.assertRaises(ValueError):
                    await collect_readings(client, ["north"], limit)
            self.assertEqual(client.peak_active, 0)

    async def test_failure(self):
        with self.assertRaises(ExceptionGroup) as caught:
            async with open_reading_client(delay=0) as client:
                await collect_readings(client, ["unknown", "north", "south"])
        self.assertTrue(any(isinstance(e, KeyError) for e in caught.exception.exceptions))
        self.assertTrue(client.closed)
        self.assertEqual(client.active, 0)

    async def test_cancellation(self):
        started = asyncio.Event()
        clients = []

        async def operation():
            async with open_reading_client(delay=0) as client:
                clients.append(client)
                started.set()
                await asyncio.Event().wait()

        task = asyncio.create_task(operation())
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(clients[0].closed)

    async def test_timeout(self):
        with self.assertRaises(TimeoutError):
            async with asyncio.timeout(0.01):
                async with open_reading_client(delay=0) as client:
                    await asyncio.Event().wait()
        self.assertTrue(client.closed)

    async def test_closed_client(self):
        client = ReadingClient(delay=0)
        with self.assertRaises(RuntimeError):
            await client.fetch("north")
        async with open_reading_client(delay=0) as client:
            await client.fetch("north")
        with self.assertRaises(RuntimeError):
            await client.fetch("north")

    def test_invalid_delay(self):
        for delay in (-1, float("nan"), float("inf")):
            with self.subTest(delay=delay), self.assertRaises(ValueError):
                ReadingClient(delay=delay)


if __name__ == "__main__":
    unittest.main()
