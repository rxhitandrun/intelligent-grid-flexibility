# Experiment 002: Five-Bus Residential Distribution Network

**Date:** 25 November 2026

## Objective

Develop and validate a synthetic radial distribution network suitable for investigating the spatial and operational effects of distributed energy resources.

## Network Configuration

- External grid: 11 kV, 1.0 p.u.
- Distribution transformer: 400 kVA, 11/0.4 kV
- Distribution cables: Three 100 m NAYY 4x150 SE sections
- Residential demand: Three 50 kW aggregated load groups
- Residential power factor: 0.95 lagging
- Rooftop PV: Two 30 kW installations at Residential B and Residential C
- PV reactive power: Zero

Transformer parameters and operating conditions are synthetic assumptions. Cable parameters are obtained from the pandapower standard-type library.

## Methodology

Balanced steady-state AC power flow was performed using the Newton–Raphson algorithm in pandapower 3.5.6.

Validation included network component counts, electrical connectivity, active and reactive demand consistency, PV generation consistency, and active and reactive power balance.

Operational feasibility was evaluated using illustrative voltage limits of 0.95–1.05 p.u. and equipment loading limits of 100%.

## Results

| Metric | Result |
|---|---:|
| Residential demand | 150 kW |
| PV generation | 60 kW |
| Grid import | 92.985 kW |
| Grid reactive supply | 52.945 kvar |
| Minimum bus voltage | 0.967521 p.u. |
| Maximum cable loading | 56.354% |
| Transformer loading | 26.750% |
| Cable losses | 1.909 kW |
| Transformer losses | 1.076 kW |
| Total active power losses | 2.985 kW |

All implemented validation checks passed. All modelled voltage and thermal constraints were satisfied.

## Discussion

Residential C exhibited the lowest bus voltage, while Cable 1 experienced the highest thermal loading. These findings agree with analytical expectations based on cumulative downstream demand and feeder impedance.

The network provides a reference operating point for subsequent studies of DER connection location, voltage sensitivity, network congestion and coordinated flexibility.

## Limitations

The network is synthetic and does not represent an identified real distribution feeder. The balanced steady-state formulation excludes phase imbalance, temporal demand variation, PV uncertainty, detailed inverter capability constraints and dynamic behaviour.

The current results establish feasibility for one operating point only. Further comparative experiments are required to quantify the benefits of DER placement and coordination.

## Reproduction

With the project virtual environment activated, execute:

`python residential_network.py`