from enum import Enum


class DuetBand(str, Enum):
    FUEL_DEPTH_GRASS = "fuel_depth.grass"
    FUEL_DEPTH_LITTER = "fuel_depth.litter"
    FUEL_DEPTH_LITTER_CONIFEROUS = "fuel_depth.litter.coniferous"
    FUEL_DEPTH_LITTER_DECIDUOUS = "fuel_depth.litter.deciduous"
    FUEL_DEPTH_TOTAL = "fuel_depth.total"
    FUEL_LOAD_GRASS = "fuel_load.grass"
    FUEL_LOAD_LITTER = "fuel_load.litter"
    FUEL_LOAD_LITTER_CONIFEROUS = "fuel_load.litter.coniferous"
    FUEL_LOAD_LITTER_DECIDUOUS = "fuel_load.litter.deciduous"
    FUEL_LOAD_TOTAL = "fuel_load.total"
    FUEL_MOISTURE_GRASS = "fuel_moisture.grass"
    FUEL_MOISTURE_LITTER = "fuel_moisture.litter"
    FUEL_MOISTURE_LITTER_CONIFEROUS = "fuel_moisture.litter.coniferous"
    FUEL_MOISTURE_LITTER_DECIDUOUS = "fuel_moisture.litter.deciduous"
    FUEL_MOISTURE_TOTAL = "fuel_moisture.total"

    def __str__(self) -> str:
        return str(self.value)
