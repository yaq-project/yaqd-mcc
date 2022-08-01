__all__ = ["Mcc152"]

import asyncio
from typing import Dict, Any, List
import daqhats
from yaqd_core import IsDaemon, HasPosition, HasLimits


class Mcc152(HasLimits, HasPosition, IsDaemon):
    _kind = "mcc-152"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Set up board communication address
        self.address = self._config["address"]
        self.terminal = (self._config["terminal"][:-1], int(self._config["terminal"][-1]))
        
        # Set up initiation of board and outputs
        self.busy=True
        self.d = daqhats.mcc152(self.address)
        if self.terminal[0]=="ao" and 0<=self.terminal[1]<=1:
            self.d.a_out_write(self.terminal[1], 0)
        elif self.terminal[0]=="dio" and 0<=self.terminal[1]<=7:
            pass #implement dio reseting here
        else: 
            pass #implement error here
        self._set_position(0)
        self._state["destination"]=0
        self.busy=False  
        print(config_filepath)      
        
        self._state["hw_limits"] = [0,5]
                

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
        
        
        if self.terminal[0]=="ao" and 0<=self.terminal[1]<=1:
            try:
                self.busy=True
                self.d.a_out_write(self.terminal[1], float(v)) 
                self._state["position"] = v
                self.busy=False
            except:
                raise TypeError("The given voltage is not a number")
        elif self.terminal[0]=="dio" and 0<=self.terminal[1]<=7:
            pass #implement digital io terminal writing 
        else:
            pass #implement appropriate error
            
    
