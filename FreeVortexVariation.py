import matplotlib.pyplot as plt
import numpy as np

from AnnulusDimension import annulus_dimensions
from DesignConstants import (
    inlet_stagnation_pressure,
    inlet_stagnation_temperature,
    rotational_speed,
)
from MeanVelocityTriangles import HubRadius

x, hub_radii = HubRadius(
    radius_hub_inlet=annulus_dimensions["inlet_radii"][0],
    radius_hub_outlet=annulus_dimensions["outlet_radii"][0],
    compressor_length=1,
    number_of_points=100,
)
tip_radii = [annulus_dimensions["inlet_radii"][-1] for i in range(len(hub_radii))]
mean_radii = (np.array(hub_radii) + np.array(tip_radii)) / 2

from math import atan, cos, pi, tan

# We will now vary the air angles from root to tip by taking into account the various distributions of the whirl velocity with radius.
# For this design we will use the Free Vortex constraint
# For the first stage, the design choice is limited due to the lack of inlet guide vanes (IGVs), resulting in no whirl component as
# the airflow enters the compressor. Consequently, the inlet velocity remains uniform across the annular area.
#
# In subsequent stages, the whirl velocity as the airflow enters the rotor blades is influenced by the axial velocity and the outlet
# angle from the previous stage's stator. The allows greater flexibility in the aerodynamic design for these stages.
# For this design we will use a Free Vortex approach to analyze the first stage with the condition V_U = constant holding true when V_U = 0
# The focus will then shift to designing the third stage, taking into account that the mean radius design assumed Lambda_mean = 0.50
#
from MeanVelocityTriangles import velocity_triangles_table

c_p = 1.005e3  # J/K kg Specific heat at constant pressure
gamma = 1.4
R = 287  # J/kgK
#
# From the preliminary mean radius design inlet conditions give us
r_tip_inlet = tip_radii[0]
r_mean_inlet = mean_radii[0]
r_hub_inlet = (2 * r_mean_inlet) - r_tip_inlet
height_inlet = r_tip_inlet - r_hub_inlet
P_01_inlet = inlet_stagnation_pressure / (1e5)  # bar
T_01_inlet = inlet_stagnation_temperature
beta_mean_inlet = velocity_triangles_table[r"$ \beta_1 $"][0]
alpha_15_mean = velocity_triangles_table[r"$ \alpha_1 $"][0]

V_U_inlet = 0  # because no IGV

lengths = np.linspace(0, len(mean_radii) - 1, 11, dtype=int)

r_mean_stage_vals = [mean_radii[i] for i in lengths]
r_mean_intermediate_stages = []
r_mean_inlet_stages = []
for i in range(len(r_mean_stage_vals)):
    if i % 2 == 0:
        r_mean_inlet_stages += [r_mean_stage_vals[i]]
    else:
        r_mean_intermediate_stages += [r_mean_stage_vals[i]]
P_0_stages = velocity_triangles_table[r"$P_{0S}$"]
T_0_stages = velocity_triangles_table[r"$T_{0S}$"]
T_02_stage1 = T_0_stages[0]

# Inlet Conditions
del_T0_stage1 = T_02_stage1 - T_01_inlet
U_mean_inlet = r_mean_inlet_stages[0] * rotational_speed * 2 * pi / 60
del_V_U_stage1 = (c_p * del_T0_stage1) / (0.98 * U_mean_inlet)
VU_15_mean_stage1 = V_U_inlet + del_V_U_stage1
U_inlet_vals = []
r_inlet_vals = np.linspace(r_hub_inlet, r_tip_inlet, 98)
for i in r_inlet_vals:
    U_inlet_vals += [i * rotational_speed * 2 * pi / 60]
V_a = U_mean_inlet / (tan(beta_mean_inlet * pi / 180))
beta_inlet_vals = []
for i in U_inlet_vals:
    beta_inlet_vals += [atan(i / V_a) * 180 / pi]
alpha_inlet_vals = np.zeros(len(beta_inlet_vals))
# To determine the air angles, it's necessary to assess the radial variation of V_U. Under the free vortex condition, V_U*r = constant,
# with the value of V_U previously established in the mean design calculation
const2 = VU_15_mean_stage1 * r_mean_intermediate_stages[0]
del r_mean_inlet_stages[0]


r_tip = tip_radii[0]
alpha_15_mean_vals = velocity_triangles_table[r"$ \alpha_1 $"]
VU_15_mean_vals = velocity_triangles_table[r"$C_{w1}$"]
VU_1_mean_vals = velocity_triangles_table[r"$C_{w2}$"]
beta_1_vals = [beta_inlet_vals]
beta_15_vals = []
alpha_1_vals = [alpha_inlet_vals]
alpha_15_vals = []
r_15_vals = []
r_1_vals = []

for stage_number in range(0, 5):
    r_15_hub = 2 * r_mean_intermediate_stages[stage_number] - r_tip
    r_1_hub = 2 * r_mean_inlet_stages[stage_number] - r_tip
    const2 = VU_15_mean_vals[stage_number] * r_mean_intermediate_stages[stage_number]
    const = VU_1_mean_vals[stage_number] * r_mean_inlet_stages[stage_number]
    r_15_stage_vals = np.linspace(r_15_hub, r_tip, 98)
    r_1_stage_vals = np.linspace(r_1_hub, r_tip, 98)
    beta_1_stage_vals = []
    beta_15_stage_vals = []
    alpha_15_stage_vals = []
    for i in range(len(r_15_stage_vals)):
        VU_15 = const2 / r_15_stage_vals[i]
        VU_1 = const / r_1_stage_vals[i]
        U_15 = r_15_stage_vals[i] * rotational_speed * 2 * pi / 180
        U_1 = r_1_stage_vals[i] * rotational_speed * 2 * pi / 180
        beta_1 = atan((U_1 - VU_1) / V_a) * 180 / pi
        beta_1_stage_vals += [beta_1]
        beta_15 = atan((U_15 - VU_15) / V_a) * 180 / pi
        beta_15_stage_vals += [beta_15]
        alpha_15 = atan(VU_15 / V_a) * 180 / pi
        alpha_15_stage_vals += [alpha_15]
    beta_1_vals += [beta_1_stage_vals]
    beta_15_vals += [beta_15_stage_vals]
    alpha_15_vals += [alpha_15_stage_vals]
    alpha_1_vals += [beta_15_stage_vals]  # because alpha_1 = beta_1.5
    r_15_vals += [r_15_stage_vals]
    r_1_vals += [r_1_stage_vals]
    # print(r_15_hub)

fig, axs = plt.subplots(1, 5, figsize=(20, 5))
axs[0].plot(r_inlet_vals, beta_1_vals[0], label=r"$\beta_{1}$")
axs[0].plot(r_15_vals[0], beta_15_vals[0], label=r"$\beta_{1.5}$")
axs[0].plot(r_15_vals[0], alpha_15_vals[0], label=r"$\alpha_{1.5}$")
axs[0].plot(r_inlet_vals, alpha_1_vals[0], label=r"$\alpha_{1}$")
axs[0].set_title("Stage 1 angles")
axs[0].legend()


axs[1].plot(r_1_vals[0], beta_1_vals[1], label=r"$\beta_{1}$")
axs[1].plot(r_15_vals[1], beta_15_vals[1], label=r"$\beta_{1.5}$")
axs[1].plot(r_15_vals[1], alpha_15_vals[1], label=r"$\alpha_{1.5}$")
axs[1].plot(r_1_vals[0], alpha_1_vals[1], label=r"$\alpha_{1}$")
axs[1].set_title("Stage 2 angles")
axs[1].legend()

axs[2].plot(r_1_vals[1], beta_1_vals[2], label=r"$\beta_{1}$")
axs[2].plot(r_15_vals[2], beta_15_vals[2], label=r"$\beta_{1.5}$")
axs[2].plot(r_1_vals[2], alpha_15_vals[2], label=r"$\alpha_{1.5}$")
axs[2].plot(r_1_vals[1], alpha_1_vals[2], label=r"$\alpha_{1}$")
axs[2].set_title("Stage 3 angles")
axs[2].legend()

axs[3].plot(r_1_vals[2], beta_1_vals[3], label=r"$\beta_{1}$")
axs[3].plot(r_15_vals[3], beta_15_vals[3], label=r"$\beta_{1.5}$")
axs[3].plot(r_15_vals[3], alpha_15_vals[3], label=r"$\alpha_{1.5}$")
axs[3].plot(r_1_vals[2], alpha_1_vals[3], label=r"$\alpha_{1}$")
axs[3].set_title("Stage 4 angles")
axs[3].legend()

axs[4].plot(r_1_vals[3], beta_1_vals[4], label=r"$\beta_{1}$")
axs[4].plot(r_15_vals[4], beta_15_vals[4], label=r"$\beta_{1.5}$")
axs[4].plot(r_15_vals[4], alpha_15_vals[4], label=r"$\alpha_{1.5}$")
axs[4].plot(r_1_vals[3], alpha_1_vals[4], label=r"$\alpha_{1}$")
axs[4].set_title("Stage 5 angles")
axs[4].legend()
plt.show()
