__all__ = ["Mcc152"]

import asyncio
from typing import Dict, Any, List
import daqhats
from yaqd_core import IsDaemon, HasPosition, HasLimits


class Mcc152(HasLimits, HasPosition, IsDaemon):
    _kind = "mcc-152"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Perform any unique initialization
        self.address = self._config["address"]
        self.d = daqhats.mcc152(self.address)
                

    async def update_state(self):
        """Continually monitor and update the current daemon state."""
        # If there is no state to monitor continuously, delete this function
        while True:
            # Perform any updates to internal state
            self._busy = False
            # There must be at least one `await` in this loop
            # This one waits for something to trigger the "busy" state
            # (Setting `self._busy = True)
            # Otherwise, you can simply `await asyncio.sleep(0.01)`
            #await self._busy_sig.wait()
            await asyncio.sleep(0.01)
            
    def get_address(self):
        return self.address

    def set_voltage0(self, v0):
        """
        voltage is float 0.0-5.0
        """
        try:
            self.busy=True
            self.d.a_out_write(0, float(v0))
            self.voltage0 = float(v0)
            print(self.voltage0)
            self.busy=False
        except:
            raise TypeError("The given voltage is not a number")

    def get_voltage0(self) -> float:
        try:
            return self.voltage0
        except:
            print("voltage0 has not been set.")
            return

    def set_voltage1(self, v1):
        """
        voltage is float 0.0-5.0
        """
        try:
            self.busy=True
            self.d.a_out_write(1, float(v1))
            self.voltage1 = float(v1)
            print(self.voltage1)
            self.busy=False
        except:
            raise TypeError("The given voltage is not a number")

    def get_voltage1(self) -> float:
        try:
            return self.voltage1
        except:
            print("voltage1 has not been set.")
            return

    def _set_position(self, pos):
        pass
        
