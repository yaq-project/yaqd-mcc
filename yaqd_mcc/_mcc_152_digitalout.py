__all__ = ["Mcc152DigitalOut"]

import asyncio
from typing import Dict, Any, List
import daqhats # type: ignore
from yaqd_core import IsDaemon, HasPosition, HasLimits


class Mcc152DigitalOut(HasLimits, HasPosition, IsDaemon):
    _kind = "mcc-152-digitalout"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Set up board communication address
        self.address = self._config["address"]
        self.terminal = self._config["terminal"]

        # Set up initiation of board and outputs
        self.d = daqhats.mcc152(self.address)
        self._state["hw_limits"] = [0, 1]

    def get_address(self):
        return self.address

    def _set_position(self, b):
        """
        the b argument is a bit integer
        """
        async def _setter(self, b):
            self.d.dio_output_write_bit(self.terminal, b)
            self._state["position"] = self.d.dio_output_read_bit(self.terminal)
            await asyncio.sleep(1)
            self._busy = False
        for task in asyncio.all_tasks():
            if task.get_name()=="setting position": task.cancel()
        asyncio.create_task(_setter(self, b), name="setting position")
