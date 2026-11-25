
import pandapower as pp
import numpy as np

# ==================================================
# 1. INITIALISE NETWORK
# ==================================================

net = pp.create_empty_network(
    name="Residential Distribution Network",
    f_hz=50.0
)

# ==================================================
# 2. CREATE BUSES
# ==================================================

b0 = pp.create_bus(net, vn_kv=11.0, name="HV Grid")
b1 = pp.create_bus(net, vn_kv=0.4, name="LV Substation")
b2 = pp.create_bus(net, vn_kv=0.4, name="Residential A")
b3 = pp.create_bus(net, vn_kv=0.4, name="Residential B")
b4 = pp.create_bus(net, vn_kv=0.4, name="Residential C")

# ==================================================
# 3. EXTERNAL GRID
# ==================================================

pp.create_ext_grid(
    net,
    bus=b0,
    vm_pu=1.0,
    name="External Grid"
)

# ==================================================
# 4. DISTRIBUTION TRANSFORMER
# ==================================================

# Synthetic transformer parameters
pp.create_transformer_from_parameters(
    net,
    hv_bus=b0,
    lv_bus=b1,
    sn_mva=0.4,
    vn_hv_kv=11.0,
    vn_lv_kv=0.4,
    vk_percent=4.0,
    vkr_percent=1.0,
    pfe_kw=0.8,
    i0_percent=0.5,
    shift_degree=30,
    name="Distribution Transformer"
)

# ==================================================
# 5. DISTRIBUTION CABLES
# ==================================================

cable_type = "NAYY 4x150 SE"
cable_length_km = 0.1

pp.create_line(
    net,
    from_bus=b1,
    to_bus=b2,
    length_km=cable_length_km,
    std_type=cable_type,
    name="Cable 1"
)

pp.create_line(
    net,
    from_bus=b2,
    to_bus=b3,
    length_km=cable_length_km,
    std_type=cable_type,
    name="Cable 2"
)

pp.create_line(
    net,
    from_bus=b3,
    to_bus=b4,
    length_km=cable_length_km,
    std_type=cable_type,
    name="Cable 3"
)

# ==================================================
# 6. RESIDENTIAL LOADS
# ==================================================

p_load_kw = 50
power_factor = 0.95

# Reactive demand calculated from power factor
q_load_kvar = p_load_kw * np.tan(
    np.arccos(power_factor)
)

residential_buses = [b2, b3, b4]
residential_names = ["A", "B", "C"]

for bus, name in zip(
    residential_buses, residential_names
):
    pp.create_load(
        net,
        bus=bus,
        p_mw=p_load_kw / 1000,
        q_mvar=q_load_kvar / 1000,
        name=f"Residential Load {name}"
    )

# ==================================================
# 7. ROOFTOP PV GENERATION
# ==================================================

# Assumed PV output per installation
pv_kw = 30

pp.create_sgen(
    net,
    bus=b3,
    p_mw=pv_kw / 1000,
    q_mvar=0.0,
    name="PV Residential B"
)

pp.create_sgen(
    net,
    bus=b4,
    p_mw=pv_kw / 1000,
    q_mvar=0.0,
    name="PV Residential C"
)

# ==================================================
# 8. NETWORK COMPONENT SUMMARY
# ==================================================

print("\n--- NETWORK COMPONENTS ---")

print("Buses:", len(net.bus))
print("External grids:", len(net.ext_grid))
print("Transformers:", len(net.trafo))
print("Lines:", len(net.line))
print("Residential loads:", len(net.load))
print("PV installations:", len(net.sgen))

print(f"\nActive demand per group: {p_load_kw} kW")
print(f"Reactive demand per group: {q_load_kvar:.3f} kvar")
print(f"Residential power factor: {power_factor}")

# ==================================================
# 9. RUN AC POWER FLOW
# ==================================================

pp.runpp(
    net,
    algorithm="nr",
    numba=False
)

print("\n--- POWER FLOW STATUS ---")
print("Converged:", net.converged)

# ==================================================
# 10. BUS VOLTAGE RESULTS
# ==================================================

bus_results = net.res_bus[
    ["vm_pu", "va_degree"]
].copy()

bus_results.insert(0, "name", net.bus.name)

bus_results["voltage_kv"] = (
    net.res_bus.vm_pu * net.bus.vn_kv
)

print("\n--- BUS VOLTAGES ---")
print(bus_results.to_string())

# ==================================================
# 11. LINE RESULTS
# ==================================================

line_results = net.res_line[
    ["p_from_mw", "q_from_mvar",
     "i_ka", "loading_percent", "pl_mw"]
].copy()

line_results.insert(0, "name", net.line.name)

print("\n--- LINE RESULTS ---")
print(line_results.to_string())

# ==================================================
# 12. TRANSFORMER RESULTS
# ==================================================

print("\n--- TRANSFORMER RESULTS ---")

print(
    net.res_trafo[
        ["loading_percent", "pl_mw", "ql_mvar"]
    ]
)

# ==================================================
# 13. LOAD AND PV RESULTS
# ==================================================

print("\n--- RESIDENTIAL LOAD RESULTS ---")

print(net.res_load[["p_mw", "q_mvar"]])

print("\n--- PV GENERATION RESULTS ---")

print(net.res_sgen[["p_mw", "q_mvar"]])

print("\n--- EXTERNAL GRID RESULTS ---")

print(net.res_ext_grid)

# ==================================================
# 14. ACTIVE POWER BALANCE
# ==================================================

p_grid = net.res_ext_grid.p_mw.sum()
p_load = net.res_load.p_mw.sum()
p_pv = net.res_sgen.p_mw.sum()

p_line_loss = net.res_line.pl_mw.sum()
p_trafo_loss = net.res_trafo.pl_mw.sum()

p_total_loss = p_line_loss + p_trafo_loss

p_balance_error = (
    p_grid + p_pv - p_load - p_total_loss
)

print("\n--- ACTIVE POWER BALANCE ---")

print(f"Grid import: {p_grid * 1000:.3f} kW")
print(f"Residential demand: {p_load * 1000:.3f} kW")
print(f"PV generation: {p_pv * 1000:.3f} kW")
print(f"Line losses: {p_line_loss * 1000:.3f} kW")
print(f"Transformer losses: {p_trafo_loss * 1000:.3f} kW")
print(f"Total losses: {p_total_loss * 1000:.3f} kW")

print(
    f"Power balance error: "
    f"{p_balance_error * 1000:.6f} kW"
)

# ==================================================
# 15. REACTIVE POWER BALANCE
# ==================================================

q_grid = net.res_ext_grid.q_mvar.sum()
q_load = net.res_load.q_mvar.sum()
q_pv = net.res_sgen.q_mvar.sum()

q_line = net.res_line.ql_mvar.sum()
q_trafo = net.res_trafo.ql_mvar.sum()

q_balance_error = (
    q_grid + q_pv - q_load - q_line - q_trafo
)

print("\n--- REACTIVE POWER BALANCE ---")

print(f"Grid reactive supply: {q_grid * 1000:.3f} kvar")
print(f"Residential demand: {q_load * 1000:.3f} kvar")
print(f"PV reactive generation: {q_pv * 1000:.3f} kvar")
print(f"Net line absorption: {q_line * 1000:.3f} kvar")
print(f"Transformer absorption: {q_trafo * 1000:.3f} kvar")

print(
    f"Reactive balance error: "
    f"{q_balance_error * 1000:.6f} kvar"
)

# ==================================================
# 16. MODEL VALIDATION
# ==================================================

assert net.converged, "Power flow did not converge"

assert net.res_bus.vm_pu.notna().all(), \
    "Unsupplied buses detected"

assert len(net.bus) == 5, "Incorrect bus count"
assert len(net.ext_grid) == 1, "Incorrect grid count"
assert len(net.trafo) == 1, "Incorrect transformer count"
assert len(net.line) == 3, "Incorrect line count"
assert len(net.load) == 3, "Incorrect load count"
assert len(net.sgen) == 2, "Incorrect PV count"

expected_p_load = 3 * p_load_kw / 1000
expected_q_load = 3 * q_load_kvar / 1000
expected_p_pv = 2 * pv_kw / 1000

tolerance = 1e-6

assert abs(p_load - expected_p_load) < tolerance, \
    "Incorrect active demand"

assert abs(q_load - expected_q_load) < tolerance, \
    "Incorrect reactive demand"

assert abs(p_pv - expected_p_pv) < tolerance, \
    "Incorrect PV generation"

assert abs(q_pv) < tolerance, \
    "Unexpected PV reactive generation"

assert abs(p_balance_error) < tolerance, \
    "Active power balance failed"

assert abs(q_balance_error) < tolerance, \
    "Reactive power balance failed"

print("\nAll validation checks passed.")

# ==================================================
# 17. OPERATIONAL CONSTRAINTS
# ==================================================

# Illustrative research limits
voltage_min = 0.95
voltage_max = 1.05
loading_max = 100

voltage_ok = net.res_bus.vm_pu.between(
    voltage_min, voltage_max
).all()

line_ok = (
    net.res_line.loading_percent <= loading_max
).all()

trafo_ok = (
    net.res_trafo.loading_percent <= loading_max
).all()

feasible = bool(
    voltage_ok and line_ok and trafo_ok
)

print("\n--- OPERATIONAL CONSTRAINTS ---")

print("Voltage limits satisfied:", voltage_ok)
print("Line thermal limits satisfied:", line_ok)
print("Transformer limits satisfied:", trafo_ok)
print("Operating point feasible:", feasible)

# ==================================================
# 18. RESEARCH SUMMARY
# ==================================================

min_voltage_bus = net.res_bus.vm_pu.idxmin()
max_loading_line = net.res_line.loading_percent.idxmax()

print("\n--- RESEARCH SUMMARY ---")

print(
    f"Minimum bus voltage: "
    f"{net.res_bus.vm_pu.min():.6f} p.u."
)

print(
    f"Lowest voltage bus: "
    f"{net.bus.at[min_voltage_bus, 'name']}"
)

print(
    f"Maximum cable loading: "
    f"{net.res_line.loading_percent.max():.3f}%"
)

print(
    f"Most heavily loaded cable: "
    f"{net.line.at[max_loading_line, 'name']}"
)

print(f"Total network losses: {p_total_loss * 1000:.3f} kW")

print("\nSimulation completed successfully.")
