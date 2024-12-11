import numpy as np

from AnnulusDimension import annulus_dimensions
from DesignConstants import (
    combustion_chamber_pressure_loss,
    compressor_pressure_ratio,
    inlet_stagnation_pressure,
    mass_flow_rate,
    maximum_cycle_temperature,
    rotational_speed,
    turbine_efficiency,
    turbine_power,
    turbine_pressure_ratio,
)
from MeanTurbineAngles import (
    alpha_2,
    alpha_3,
    flow_coefficient,
    specific_heat_gas_pressure,
    specific_heat_ratio_gas,
    stage_temperature_change,
)

stagnation_pressure_station_1 = (
    inlet_stagnation_pressure
    * compressor_pressure_ratio
    * (1 - combustion_chamber_pressure_loss)
)
mean_rotational_velocity = annulus_dimensions["U_t"][0]
axial_velocity_station_2 = mean_rotational_velocity * flow_coefficient

absolute_velocity_station_2 = axial_velocity_station_2 / np.cos(alpha_2)
stagnation_temperature_station_2 = maximum_cycle_temperature
loss_coefficient = 0.06
temperature_station_2 = (
    stagnation_temperature_station_2
    - absolute_velocity_station_2**2 / (2 * specific_heat_gas_pressure)
)
temperature_station_2 = temperature_station_2 - loss_coefficient * (
    absolute_velocity_station_2**2 / (2 * specific_heat_gas_pressure)
)
stagnation_pressure_station_2 = (
    inlet_stagnation_pressure
    * compressor_pressure_ratio
    * (1 - combustion_chamber_pressure_loss)
)
pressure_station_2 = stagnation_pressure_station_2 / (
    stagnation_temperature_station_2 / temperature_station_2
) ** (specific_heat_ratio_gas / (specific_heat_ratio_gas - 1))
critical_pressure_ratio = ((specific_heat_ratio_gas + 1) / 2) ** (
    specific_heat_ratio_gas / (specific_heat_ratio_gas - 1)
)
density_station_2 = pressure_station_2 / (287 * temperature_station_2)
area_station_2 = mass_flow_rate / (density_station_2 * axial_velocity_station_2)
throat_area_station_2 = area_station_2 * np.cos(alpha_2)

axial_velocity_station_3 = axial_velocity_station_2
axial_velocity_station_1 = axial_velocity_station_2
absolute_velocity_station_3 = axial_velocity_station_3 / np.cos(alpha_3)

temperature_station_1 = maximum_cycle_temperature - axial_velocity_station_1**2 / (
    2 * specific_heat_gas_pressure
)
stagnation_pressure_station_1 = (
    inlet_stagnation_pressure
    * compressor_pressure_ratio
    * (1 - combustion_chamber_pressure_loss)
)
pressure_station_1 = stagnation_pressure_station_1 * (
    temperature_station_1 / maximum_cycle_temperature
) ** (specific_heat_ratio_gas / (specific_heat_ratio_gas - 1))
density_station_1 = pressure_station_1 / (287 * temperature_station_1)
area_station_1 = mass_flow_rate / (density_station_1 * axial_velocity_station_1)
stagnation_temperature_station_3 = maximum_cycle_temperature - stage_temperature_change
absolute_velocity_station_3 = axial_velocity_station_1 / np.cos(alpha_3)
temperature_station_3 = (
    stagnation_temperature_station_3
    - absolute_velocity_station_3**2 / (2 * specific_heat_gas_pressure)
)
stagnation_pressure_station_3 = (
    stagnation_pressure_station_1 * turbine_pressure_ratio**-1
)
pressure_station_3 = stagnation_pressure_station_3 * (
    temperature_station_3 / maximum_cycle_temperature
) ** (specific_heat_ratio_gas / (specific_heat_ratio_gas - 1))
density_station_3 = (pressure_station_1 * turbine_pressure_ratio**-1) / (
    287 * temperature_station_3
)
area_station_3 = mass_flow_rate / (density_station_3 * axial_velocity_station_3)

turbine_annulus_dict = {
    "stagnation_pressures": [
        stagnation_pressure_station_1,
        stagnation_pressure_station_2,
        stagnation_pressure_station_3,
    ],
    "pressures": [pressure_station_1, pressure_station_2, pressure_station_3],
    "stagnation_temperatures": [
        maximum_cycle_temperature,
        stagnation_temperature_station_2,
        stagnation_temperature_station_3,
    ],
    "temperatures": [
        temperature_station_1,
        temperature_station_2,
        temperature_station_3,
    ],
    "densities": [density_station_1, density_station_2, density_station_3],
    "area": [area_station_1, area_station_2, area_station_3],
}
turbine_revolutions_per_second = rotational_speed / 60
radius_mean = mean_rotational_velocity / (2 * np.pi * turbine_revolutions_per_second)
Height = lambda area: area * turbine_revolutions_per_second / mean_rotational_velocity
height_station_1 = Height(area_station_1)
height_station_2 = Height(area_station_2)
height_station_3 = Height(area_station_3)
Radius_ratio = lambda height: (radius_mean + height / 2) / (radius_mean - height / 2)
radius_ratio_station_1 = Radius_ratio(height_station_1)
radius_ratio_station_2 = Radius_ratio(height_station_2)
radius_ratio_station_3 = Radius_ratio(height_station_3)
turbine_annulus_dict["heights"] = [height_station_1, height_station_2, height_station_3]
turbine_annulus_dict["radius_ratio"] = [
    radius_ratio_station_1,
    radius_ratio_station_2,
    radius_ratio_station_3,
]
if __name__ == "__main__":
    print(radius_mean)
