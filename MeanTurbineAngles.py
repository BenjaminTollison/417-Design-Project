import numpy as np

from AnnulusDimension import (
    annulus_dimensions,
    total_rotor_velocity_hub,
    total_rotor_velocity_tip,
)

### variables that change the entire solution
stage_temperature_change = 150  # K
# mean_rotational_velocity = (total_rotor_velocity_tip + total_rotor_velocity_hub) / 2
# mean_rotational_velocity = 340
mean_rotational_velocity = annulus_dimensions["U_t"][0]
flow_coefficient = 0.8
###
specific_heat_ratio_gas = 1.333
specific_heat_gas_pressure = (specific_heat_ratio_gas * 287) / (
    specific_heat_ratio_gas - 1
)
axial_velocity = annulus_dimensions["C_a"][0]
work_coefficient = (
    2 * specific_heat_gas_pressure * stage_temperature_change
) / mean_rotational_velocity**2

### I will be using the same naming scheme as the example problem
inlet_angle = np.radians(0)
alpha_3 = np.radians(12)
beta_3 = np.arctan(np.tan(alpha_3) + 1 / flow_coefficient)
degree_of_reaction = (
    2 * flow_coefficient * np.tan(beta_3) - 0.5 * work_coefficient
) / 2
beta_2 = np.arctan(
    (1 / (2 * flow_coefficient)) * (0.5 * work_coefficient - 2 * degree_of_reaction)
)
alpha_2 = np.arctan(np.tan(beta_2) + 1 / flow_coefficient)

velocity_angles_dict = {
    r"$\psi$": [work_coefficient, np.nan, np.nan],
    r"$\Lambda$": [degree_of_reaction, np.nan, np.nan],
    r"$\alpha$": [0, np.degrees(alpha_2), np.degrees(alpha_3)],
    r"$\beta$": [0, np.degrees(beta_2), np.degrees(beta_3)],
}

if __name__ == "__main__":
    print(np.degrees(alpha_2))
    print(np.degrees(beta_2))
    print(np.degrees(alpha_3))
    print(np.degrees(beta_3))
