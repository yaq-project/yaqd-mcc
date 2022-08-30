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
        
        # Set up initiation of board and input terminals
        self.d = daqhats.mcc152(self.address)
        try: 
            self._channel_names = [str(n) for n in self._config["terminals"]]
        except: 
            self._channel_names = [str(n) for n in range(self.d.info()[0])]
        self._channel_units = {k: None for k in self._channel_names}        
        asyncio.get_event_loop().create_task(self._update_measurements())
        
    def get_address(self):
        return self.address

    async def _update_measurements(self):
        while True: 
            out = dict()
            for name in self._channel_names:
                out[name] = self.d.dio_input_read_tuple()[int(name)]
            self._measurement_id+=1
            out["measurement_id"] = self._measurement_id
            self._measured = out
            await asyncio.sleep(self._config["update_period"])
        
