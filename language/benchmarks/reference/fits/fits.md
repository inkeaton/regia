# Benchmark fits

Time: compilation only; each point is the mean of the runs of one configuration.

## Fits

| Analysis | Size | Model | Result | R² | Points |
|---|---|---|---|---|---|
| Pooled sweeps | input_loc | power | k = 1.033 [1.005, 1.062] | 0.989 | 62 |
| Pooled sweeps | input_loc | linear | 17.6 ms/kLOC, overhead -1.1 ms | 0.981 | 62 |
| Pooled sweeps | output_loc | power | k = 0.807 [0.700, 0.913] | 0.792 | 62 |
| Pooled sweeps | output_loc | linear | 2.9 ms/kLOC, overhead 4.0 ms | 0.759 | 62 |
| Roles | input_loc | power | k = 1.051 [1.013, 1.090] | 0.998 | 9 |
| Roles | input_loc | linear | 18.8 ms/kLOC, overhead -0.5 ms | 1.000 | 9 |
| Roles | output_loc | power | k = 0.850 [0.786, 0.914] | 0.993 | 9 |
| Roles | output_loc | linear | 3.3 ms/kLOC, overhead 0.8 ms | 1.000 | 9 |
| Phases | input_loc | power | k = 0.985 [0.923, 1.047] | 0.996 | 8 |
| Phases | input_loc | linear | 14.5 ms/kLOC, overhead -0.2 ms | 0.999 | 8 |
| Phases | output_loc | power | k = 1.439 [1.280, 1.597] | 0.988 | 8 |
| Phases | output_loc | linear | 18.2 ms/kLOC, overhead -3.4 ms | 0.999 | 8 |
| Playbooks | input_loc | power | k = 1.038 [1.000, 1.077] | 0.999 | 8 |
| Playbooks | input_loc | linear | 16.2 ms/kLOC, overhead -0.2 ms | 1.000 | 8 |
| Playbooks | output_loc | power | k = 1.141 [1.088, 1.194] | 0.998 | 8 |
| Playbooks | output_loc | linear | 8.7 ms/kLOC, overhead -0.7 ms | 1.000 | 8 |
| Plans per Playbook | input_loc | power | k = 1.066 [1.012, 1.119] | 0.997 | 8 |
| Plans per Playbook | input_loc | linear | 17.5 ms/kLOC, overhead -0.4 ms | 1.000 | 8 |
| Plans per Playbook | output_loc | power | k = 1.237 [1.140, 1.333] | 0.994 | 8 |
| Plans per Playbook | output_loc | linear | 11.6 ms/kLOC, overhead -1.4 ms | 1.000 | 8 |
| Branches per Plan | input_loc | power | k = 1.170 [1.060, 1.281] | 0.993 | 7 |
| Branches per Plan | input_loc | linear | 19.8 ms/kLOC, overhead -0.7 ms | 0.999 | 7 |
| Branches per Plan | output_loc | power | k = 1.387 [1.247, 1.527] | 0.992 | 7 |
| Branches per Plan | output_loc | linear | 11.9 ms/kLOC, overhead -1.6 ms | 0.999 | 7 |
| Statements per Branch | input_loc | power | k = 1.092 [1.027, 1.157] | 0.996 | 8 |
| Statements per Branch | input_loc | linear | 18.3 ms/kLOC, overhead -0.6 ms | 1.000 | 8 |
| Statements per Branch | output_loc | power | k = 1.488 [1.281, 1.695] | 0.981 | 8 |
| Statements per Branch | output_loc | linear | 18.3 ms/kLOC, overhead -3.4 ms | 1.000 | 8 |
| Subplot Breadth | input_loc | power | k = 0.934 [0.806, 1.062] | 0.986 | 7 |
| Subplot Breadth | input_loc | linear | 12.3 ms/kLOC, overhead 0.1 ms | 0.999 | 7 |
| Subplot Breadth | output_loc | power | k = 0.574 [0.410, 0.737] | 0.942 | 7 |
| Subplot Breadth | output_loc | linear | 1.4 ms/kLOC, overhead 1.3 ms | 0.999 | 7 |
| Subplot Depth | input_loc | power | k = 0.946 [0.865, 1.028] | 0.994 | 7 |
| Subplot Depth | input_loc | linear | 12.2 ms/kLOC, overhead 0.1 ms | 1.000 | 7 |
| Subplot Depth | output_loc | power | k = 0.691 [0.526, 0.856] | 0.959 | 7 |
| Subplot Depth | output_loc | linear | 1.6 ms/kLOC, overhead 1.2 ms | 1.000 | 7 |
| Realistic project | input_loc | power | k = 1.092 [1.020, 1.164] | 0.999 | 5 |
| Realistic project | input_loc | linear | 28.1 ms/kLOC, overhead -64.5 ms | 0.996 | 5 |
| Realistic project | output_loc | power | k = 1.156 [1.122, 1.191] | 1.000 | 5 |
| Realistic project | output_loc | linear | 19.1 ms/kLOC, overhead -73.5 ms | 0.996 | 5 |
| Narrative-heavy | input_loc | power | k = 1.074 [0.999, 1.149] | 0.997 | 6 |
| Narrative-heavy | input_loc | linear | 19.7 ms/kLOC, overhead -1.2 ms | 1.000 | 6 |
| Narrative-heavy | output_loc | power | k = 1.268 [1.150, 1.386] | 0.996 | 6 |
| Narrative-heavy | output_loc | linear | 16.8 ms/kLOC, overhead -4.9 ms | 0.998 | 6 |
| Reactive-heavy | input_loc | power | k = 1.058 [1.017, 1.099] | 0.999 | 6 |
| Reactive-heavy | input_loc | linear | 20.5 ms/kLOC, overhead -2.5 ms | 1.000 | 6 |
| Reactive-heavy | output_loc | power | k = 1.144 [1.064, 1.223] | 0.998 | 6 |
| Reactive-heavy | output_loc | linear | 13.1 ms/kLOC, overhead -3.9 ms | 1.000 | 6 |

## Cost per thousand lines at the top of each sweep

| Dimension | Source lines | ms per kLOC (source) | ms per kLOC (output) |
|---|---|---|---|
| Roles | 7103 | 18.8 | 3.3 |
| Phases | 3087 | 14.6 | 17.0 |
| Playbooks | 3589 | 16.1 | 8.6 |
| Plans per Playbook | 2493 | 17.2 | 11.2 |
| Branches per Plan | 705 | 18.8 | 10.6 |
| Statements per Branch | 2109 | 18.1 | 16.9 |
| Subplot Breadth | 1028 | 12.4 | 1.5 |
| Subplot Depth | 2768 | 12.3 | 1.6 |

## Sweep endpoints

| Dimension | Range | Source lines | Output lines | Time (ms) |
|---|---|---|---|---|
| Roles | 1 -> 1000 | 110 -> 7103 | 229 -> 40189 | 1.9 -> 133.5 |
| Phases | 1 -> 200 | 102 -> 3087 | 257 -> 2645 | 1.7 -> 45.1 |
| Playbooks | 0 -> 250 | 64 -> 3589 | 191 -> 6717 | 1.0 -> 57.6 |
| Plans per Playbook | 1 -> 200 | 105 -> 2493 | 251 -> 3833 | 1.7 -> 42.9 |
| Branches per Plan | 0 -> 50 | 105 -> 705 | 253 -> 1249 | 1.6 -> 13.2 |
| Statements per Branch | 1 -> 500 | 113 -> 2109 | 265 -> 2261 | 1.8 -> 38.1 |
| Subplot Breadth | 0 -> 50 | 117 -> 1028 | 269 -> 8421 | 1.9 -> 12.8 |
| Subplot Depth | 0 -> 6 | 117 -> 2768 | 269 -> 20933 | 1.9 -> 34.1 |

## Default configuration (mean over the sweeps containing it)

- Source lines: 117; output lines: 269; files: 5; ratio: 2.30
- Time: 1.56 ms (range 1.52 to 1.61 across 6 sweeps); peak RAM: 0.13 MB

## Realistic project

| Source lines | Output lines | Files | Time (ms) | ms per kLOC | Peak RAM (MB) |
|---|---|---|---|---|---|
| 433 | 877 | 16 | 7.1 | 16.5 | 0.7 |
| 1284 | 2238 | 29 | 20.9 | 16.3 | 2.3 |
| 7041 | 10965 | 68 | 125.5 | 17.8 | 13.3 |
| 27316 | 40990 | 133 | 568.0 | 20.8 | 52.6 |
| 107916 | 159090 | 263 | 3000.5 | 27.8 | 209.1 |

## Construct mix at matched source size

- Overlap: 100 to 8085 source lines
- Gap between the curves: 0.8% to 10.9%
- Same order throughout: False
- Rise in cost per kLOC across the overlap: Narrative-heavy x1.24, Reactive-heavy x1.19

| Source lines | Narrative-heavy (ms/kLOC) | Reactive-heavy (ms/kLOC) |
|---|---|---|
| 300 | 15.9 | 16.3 |
| 1000 | 17.8 | 17.3 |
| 4000 | 18.9 | 18.5 |

- Curves cross near: 351 source lines
