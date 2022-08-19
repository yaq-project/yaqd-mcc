__all__ = ["Mcc152AOut"]

import asyncio
from typing import Dict, Any, List
from yaqd_core import IsDaemon, HasPosition, HasLimits


class Mcc152AOut(HasLimits, HasPosition, IsDaemon):
    _kind = "mcc-152-aout"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Set up board communication address
        self.address = self._config["address"]
        self.terminal = self._config["terminal"]

        # Set up initiation of board and outputs
        import daqhats  # type: ignore

        self.d = daqhats.mcc152(self.address)
        self._state["hw_limits"] = [0, 5]

    def get_address(self):
        return self.address

    def _set_position(self, v):
        """
        voltage is float 0.0-5.0
        """

        async def _setter(self, v):
            self.d.a_out_write(self.terminal, v)
            self._state["position"] = v
            await asyncio.sleep(5)
            self._busy = False

        for task in asyncio.all_tasks():
            if task.get_name() == "setting position":
                task.cancel()
        asyncio.create_task(_setter(self, v), name="setting position")
