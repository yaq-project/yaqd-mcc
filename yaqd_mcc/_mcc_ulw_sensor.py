__all__ = ["Mcc118"]

import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass

from yaqd_core import HasMeasureTrigger, IsSensor, IsDaemon


@dataclass
class Channel:
    name: str
    enabled: bool
    invert: bool
    index: int


class MccUlwSensor(HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "mcc-ulw-sensor"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._channels = list()
        for k, d in self._config["channels"].items():
            channel = Channel(**d, name=k)
            self._channels.append(channel)
        self._channel_names = [c.name for c in self._channels]
        self._channel_units = {k: "V" for k in self._channel_names}
        from mcculw import ul  # type: ignore
        from mcculw.enums import InterfaceType  # type: ignore

        ul.ignore_instacal()
        devices = ul.get_daq_device_inventory(InterfaceType.ANY)
        if self._config["serial"]:
            for device in devices:
                if device.unique_id == self._config["serial"]:
                    ul.create_daq_device(0, device)
                    break
            else:
                raise Exception("no device with that serial found")
        else:
            ul.create_daq_device(0, devices[0])
        from mcculw.device_info import DaqDeviceInfo  # type: ignore

        info = DaqDeviceInfo(0)
        self._ai_info = info.get_ai_info()

    async def _measure(self):
        from mcculw import ul  # type: ignore

        out = dict()
        for c in self._channels:
            ai_range = self._ai_info.supported_ranges[c.index]
            if self._ai_info.resolution <= 16:
                value = ul.a_in(0, c.index, ai_range)
                voltage = ul.to_eng_units(0, ai_range, value)
            else:
                value = ul.a_in_32(0, c.index, ai_range)
                voltage = ul.to_eng_units_32(0, ai_range, value)
            if c.invert:
                voltage *= -1
            out[c.name] = voltage
        return out
