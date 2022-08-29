__all__ = ["Mcc152DigitalIn"]

import asyncio
from typing import Dict, Any, List
import daqhats # type: ignore
from yaqd_core import IsDaemon, IsSensor


class Mcc152DigitalIn(IsSensor, IsDaemon):
    _kind = "mcc-152-digitalin"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Set up board communication address
        self.address = self._config["address"]
        self.terminal = self._config["terminal"]

        # Set up initiation of board and outputs
        self.d = daqhats.mcc152(self.address)

    def get_address(self):
        return self.address

    def _measured(self):
        """
        the b argument is a bit integer
        """
        self.d.dio_output_read_bit(self.terminal)
        self._busy = False
