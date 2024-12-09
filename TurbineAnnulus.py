import numpy as np
from DesignConstants import maximum_cycle_temperature
from AnnulusDimension import annulus_dimensions
from DesignConstants import (
    mass_flow_rate,
    turbine_efficiency,
    turbine_power,
    turbine_pressure_ratio,
    maximum_cycle_temperature,
    rotational_speed,
    combustion_chamber_pressure_loss,
    compressor_pressure_ratio,
    inlet_stagnation_pressure,
)
from MeanTurbineAngles import (
    stage_temperature_change,
    flow_coefficient,
    alpha_2,
    alpha_3,
    specific_heat_gas_pressure,
    specific_heat_ratio_gas,
)

mean_rotational_velocity = annulus_dimensions["U_t"][0]
axial_velocity_station_2 = mean_rotational_velocity * flow_coefficient
absolute_velocity_station_2 = axial_velocity_station_2 / np.cos(alpha_2)
stagnation_temperature_station_2 = maximum_cycle_temperature
loss_coefficient = 0.06
temperature_station_2 = stagnation_temperature_station_2 - (
    absolute_velocity_station_2**2 / (2 * specific_heat_gas_pressure)
) * (1 + loss_coefficient)
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

axial_velocity_station_3 = axial_velocity_station_2 / np.cos(alpha_3)
axial_velocity_station_1 = axial_velocity_station_3

temperature_station_1 = maximum_cycle_temperature - axial_velocity_station_1**2 / (2*specific_heat_gas_pressure)
stagnation_pressure_station_1 = (
    inlet_stagnation_pressure
    * compressor_pressure_ratio
    * (1 - combustion_chamber_pressure_loss)
)
pressure_station_1 = stagnation_pressure_station_1*(temperature_station_1/maximum_cycle_temperature)**(specific_heat_ratio_gas/(specific_heat_ratio_gas-1))
density_station_1 = pressure_station_1 / (287 * temperature_station_1)
area_station_1 = mass_flow_rate / (density_station_1 * axial_velocity_station_1)
stagnation_temperature_station_3 = maximum_cycle_temperature - stage_temperature_change
temperature_station_3 = stagnation_temperature_station_3 - axial_velocity_station_3**2 / (2*specific_heat_gas_pressure)
stagnation_pressure_station_3 = stagnation_pressure_station_1*turbine_pressure_ratio**-1
pressure_station_3 = stagnation_pressure_station_3*(temperature_station_3/maximum_cycle_temperature)**(specific_heat_ratio_gas/(specific_heat_ratio_gas-1))
density_station_3 = pressure_station_3 / (287 * temperature_station_3)
area_station_3 = mass_flow_rate / (density_station_3 * axial_velocity_station_3)

if __name__ == "__main__":
    print(area_station_1)
    print(area_station_2)
    print(area_station_3)