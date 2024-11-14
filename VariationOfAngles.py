import numpy as np
import matplotlib.pyplot as plt
from MeanVelocityTriangles import (
    HubRadius,
    RotationalVelocity,
    WorkDone,
    DegOfReaction,
    delta_temperature_stage,
)
from AnnulusDimension import annulus_dimensions


def FindAlphaAndBeta(normalized_length: float, radius: float) -> list:
    U = RotationalVelocity(radius)
    axial_velocity = annulus_dimensions["C_a"][0]
    specific_heat = 1005
    b1 = (specific_heat * delta_temperature_stage) / (
        WorkDone(normalized_length) * U * axial_velocity
    )
    b2 = (2 * DegOfReaction(normalized_length) * U) / axial_velocity
    b_vector = np.array([b1, b2])
    system_of_eqns = np.array([[1, -1], [1, 1]])
    beta_vector = np.arctan(np.linalg.inv(system_of_eqns) @ b_vector)
    alpha_vector = np.arctan(U / axial_velocity - np.tan(beta_vector))
    return np.hstack([alpha_vector, b_vector])


def RangeOfRadii(normalized_length: float) -> list:
    x, hub_radii = HubRadius(
        radius_hub_inlet=annulus_dimensions["inlet_radii"][0],
        radius_hub_outlet=annulus_dimensions["outlet_radii"][0],
        compressor_length=1,
        number_of_points=100,
    )
    tip_radii = annulus_dimensions["inlet_radii"][-1]
    closest_index = np.argmin(np.abs(x - normalized_length))
    return np.linspace(hub_radii[closest_index], tip_radii, 50)


def PlotAnglesAtCertainPosition(normalized_length: float):
    alpha_1_values = []
    alpha_2_values = []
    beta_1_values = []
    beta_2_values = []
    r_values = RangeOfRadii(normalized_length)
    for r in r_values:
        angle_vector = FindAlphaAndBeta(normalized_length, r) * 180 / np.pi
        alpha_1_values.append(angle_vector[0])
        alpha_2_values.append(angle_vector[1])
        beta_1_values.append(angle_vector[2])
        beta_2_values.append(angle_vector[3])
    plt.plot(r_values, alpha_1_values, label=r"$\alpha_1$")
    plt.plot(r_values, alpha_2_values, label=r"$\alpha_2$")
    plt.plot(r_values, beta_1_values, label=r"$\beta_1$")
    plt.plot(r_values, beta_2_values, label=r"$\beta_2$")
    plt.legend()
    plt.title(f"At x = {normalized_length}")
    plt.xlabel("Radius from root to tip")
    plt.ylabel("Degrees")
    plt.xlim(r_values[0], r_values[-1])
    # plt.ylim(0,120)
    plt.show()


if __name__ == "__main__":
    stage_locations = np.linspace(0, 1, 5)
    for x in stage_locations:
        PlotAnglesAtCertainPosition(x)
