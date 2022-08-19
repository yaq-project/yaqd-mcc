__all__ = ["Mcc118"]

import asyncio
from typing import Dict, Any, List

from yaqd_core import HasMeasureTrigger, IsSensor, IsDaemon


class Mcc118(HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "mcc-118"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._channel_names = [f"ch{i}" for i in range(8)]
        self._channel_units = {k: "V" for k in self._channel_names}
        import daqhats  # type: ignore

        self._hat = daqhats.mcc118()

    async def _measure(self):
        out = dict()
        for i in range(8):
            out[f"ch{i}"] = self._hat.a_in_read(i)
        return out
