
import pandapower as pp

# ==================================================
# 1. INITIALISE NETWORK
# ==================================================

net = pp.create_empty_network(
    name="Introductory Distribution Network",
    f_hz=50.0
)

# ==================================================
# 2. CREATE BUSES
# ==================================================

b1 = pp.create_bus(net, vn_kv=20.0, name="HV Bus")
b2 = pp.create_bus(net, vn_kv=0.4, name="LV Bus")
b3 = pp.create_bus(net, vn_kv=0.4, name="Residential Bus")

# ==================================================
# 3. CREATE EXTERNAL GRID
# ==================================================

pp.create_ext_grid(
    net,
    bus=b1,
    vm_pu=1.02,
    name="Grid Connection"
)

# ==================================================
# 4. CREATE TRANSFORMER
# ==================================================

pp.create_transformer(
    net,
    hv_bus=b1,
    lv_bus=b2,
    std_type="0.4 MVA 20/0.4 kV",
    name="Distribution Transformer"
)

# ==================================================
# 5. CREATE DISTRIBUTION LINE
# ==================================================

pp.create_line(
    net,
    from_bus=b2,
    to_bus=b3,
    length_km=0.1,
    std_type="NAYY 4x50 SE",
    name="LV Cable"
)

# ==================================================
# 6. CREATE RESIDENTIAL LOAD
# ==================================================

pp.create_load(
    net,
    bus=b3,
    p_mw=0.1,
    q_mvar=0.05,
    name="Residential Load"
)

# ==================================================
# 7. INSPECT NETWORK
# ==================================================

print("\n--- NETWORK COMPONENTS ---")

print("Buses:", len(net.bus))
print("External grids:", len(net.ext_grid))
print("Transformers:", len(net.trafo))
print("Lines:", len(net.line))
print("Loads:", len(net.load))

# Rooftop PV generation assumption
# Rooftop PV generation assumption
pv_kw = 60

pv = pp.create_sgen(
    net,
    bus=b3,
    p_mw=pv_kw / 1000,
    q_mvar=0.0,
    name="Rooftop PV"
)

# ==================================================
# 8. RUN AC POWER FLOW
# ==================================================

pp.runpp(net, algorithm="nr", numba=False)

print("\n--- POWER FLOW STATUS ---")
print("Converged:", net.converged)

# ==================================================
# 9. DISPLAY RESULTS
# ==================================================

print("\n--- BUS VOLTAGES ---")
print(net.res_bus[["vm_pu", "va_degree"]])

print("\n--- LINE RESULTS ---")
print(net.res_line[["i_ka", "loading_percent", "pl_mw"]])

print("\n--- TRANSFORMER RESULTS ---")
print(net.res_trafo[["loading_percent", "pl_mw"]])

print("\n--- RESIDENTIAL LOAD ---")
print(net.res_load[["p_mw", "q_mvar"]])

print("\n--- GRID SUPPLY ---")
print(net.res_ext_grid)

# ==================================================
# 10. CALCULATE POWER BALANCE
# ==================================================

p_grid = net.res_ext_grid.p_mw.sum()
p_load = net.res_load.p_mw.sum()
p_pv = net.res_sgen.p_mw.sum()

p_line_loss = net.res_line.pl_mw.sum()
p_trafo_loss = net.res_trafo.pl_mw.sum()

p_total_loss = p_line_loss + p_trafo_loss

p_balance_error = p_grid + p_pv - p_load - p_total_loss

print("\n--- ACTIVE POWER BALANCE ---")

print(f"Grid import: {p_grid * 1000:.3f} kW")
print(f"Residential demand: {p_load * 1000:.3f} kW")
print(f"Line losses: {p_line_loss * 1000:.3f} kW")
print(f"Transformer losses: {p_trafo_loss * 1000:.3f} kW")
print(f"Total losses: {p_total_loss * 1000:.3f} kW")
print(f"Power balance error: {p_balance_error * 1000:.6f} kW")
print(f"PV generation: {p_pv * 1000:.3f} kW")
# ==================================================
# 11. VALIDATION
# ==================================================

assert net.converged, "Power flow did not converge"

assert net.res_bus.vm_pu.notna().all(), \
    "Unsupplied buses detected"

assert len(net.load) == 1, \
    "Incorrect number of loads"

assert abs(p_load - 0.1) < 1e-6, \
    "Incorrect active power demand"

assert abs(net.res_load.q_mvar.sum() - 0.05) < 1e-6, \
    "Incorrect reactive power demand"

assert abs(p_balance_error) < 1e-6, \
    "Active power balance failed"
assert abs(p_pv - pv_kw / 1000) < 1e-6, \
    "Incorrect PV generation"
print("\nAll validation checks passed.")


# ==================================================
# 12. OPERATIONAL CONSTRAINTS
# ==================================================

print("\n--- OPERATIONAL CONSTRAINTS ---")

voltage_min = 0.95
voltage_max = 1.05

voltage_ok = net.res_bus.vm_pu.between(
    voltage_min, voltage_max
).all()

line_ok = (net.res_line.loading_percent <= 100).all()

trafo_ok = (net.res_trafo.loading_percent <= 100).all()

print("Voltage limits satisfied:", voltage_ok)
print("Line thermal limits satisfied:", line_ok)
print("Transformer limits satisfied:", trafo_ok)

print(
    "Operating point feasible:",
    bool(voltage_ok and line_ok and trafo_ok)
)
