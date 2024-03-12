import asyncio


class Loop:
    def __init__(self, interval, execute, *args, **kwargs):
        self.loop = asyncio.get_event_loop()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        self.stopped = False
        self.task = self.loop.create_task(self._periodic())

    def stop(self):
        self.stopped = True
        self.task.cancel()

    def start(self):
        try:
            self.loop.run_until_complete(self.task)
        except asyncio.CancelledError:
            pass

    async def _periodic(self):
        while True:
            timer = 0
            await self.execute(*self.args, **self.kwargs)
            while not self.stopped and timer != self.interval:
                await asyncio.sleep(1)
                timer += 1
