# Experiment 001: Impact of Distributed PV on a Radial Distribution Network

**Date:** 25 November 2026

## Research Question

Can distributed photovoltaic generation relieve distribution cable congestion while maintaining residential electricity demand?

## Methodology

A balanced three-bus radial distribution network was developed using pandapower 3.5.6. The network consists of a 20 kV external grid, a 400 kVA distribution transformer, a 100 m LV distribution cable and an aggregated residential load of 100 kW and 50 kvar.

Three PV generation scenarios were evaluated: 0 kW, 30 kW and 60 kW. PV generation was connected at the residential bus and operated at unity power factor. All other network parameters were held constant.

AC power flow was performed using the Newton–Raphson algorithm.

## Results

| Metric | Baseline | 30 kW PV | 60 kW PV |
|---|---:|---:|---:|
| Residential voltage (p.u.) | 0.964431 | 0.978597 | 0.992313 |
| Cable loading (%) | 117.835 | 89.352 | 65.590 |
| Transformer loading (%) | 29.290 | 22.258 | 16.352 |
| Grid import (kW) | 107.265 | 74.770 | 43.214 |
| Network losses (kW) | 7.265 | 4.770 | 3.214 |
| Operational feasibility | No | Yes | Yes |

## Discussion

The baseline network experienced a thermal overload on the LV distribution cable despite substantial spare transformer capacity. Both PV scenarios eliminated the cable overload without reducing residential demand.

The 60 kW PV scenario reduced total active power losses by approximately 55.76% relative to the baseline. Residential bus voltage increased towards its nominal value.

## Validation

Power flow convergence, electrical connectivity, demand consistency and active power balance were checked. Operational feasibility was evaluated separately using illustrative voltage limits of 0.95–1.05 p.u. and equipment loading limits of 100%.

## Limitations

The network represents a synthetic balanced steady-state operating condition. PV generation is assumed rather than derived from measured irradiance data. The model does not consider generation uncertainty, phase imbalance, inverter capability constraints or temporal variation in electricity demand.

The results demonstrate congestion relief under the specified operating conditions, rather than guaranteed flexibility availability.

## Future Work

Extend the network to multiple residential buses and investigate the effects of DER location, time-varying demand, EV charging, battery storage and coordinated flexibility optimisation.

## Reference

Thurner et al. (2018). pandapower: An Open-Source Python Tool for Convenient Modeling, Analysis, and Optimization of Electric Power Systems. IEEE Transactions on Power Systems. DOI: 10.1109/TPWRS.2018.2829021.