from threading import Thread as _Thread
from listeners import tick_listener_manager
from core import AutoUnload

class Thread(_Thread, AutoUnload):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tick_listener_manager.register_listener(self._tick)

    def _tick(self):
        pass

    def _unload_instance(self):
        self._stop()
        tick_listener_manager.unregister_listener(self._tick)
