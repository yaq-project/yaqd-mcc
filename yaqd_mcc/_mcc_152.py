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
        self._state["hw_limits"] = [0,5]
        print(config_filepath)
                

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
        
    def _set_position(self, v): #why this method need _ before but doesnt show as so in messages?
        """
        voltage is float 0.0-5.0
        """
        terminal = (self._config["terminal"][:-1], int(self._config["terminal"][-1]))
        
        if terminal[0]=="ao" and 0<=terminal[1]<=1:
            try:
                self.busy=True
                self.d.a_out_write(terminal[1], float(v)) 
                self._state["position"] = v
                self.busy=False
            except:
                raise TypeError("The given voltage is not a number")
        elif terminal[0]=="dio" and 0<=terminal[1]<=7:
            pass #implement digital io terminal writing 
        else:
            pass #implement appropriate error
            
    
