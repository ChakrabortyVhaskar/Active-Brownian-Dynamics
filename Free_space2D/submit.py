import subprocess
import numpy as np

# Fixed parameters
Dt = 1.0
Dr = 1.0
dt = 0.001
tf = 100.0

# --- Loop over velocities ---
N = 100000
v_vals = np.arange(0.0, 5.5, 0.5)
for v in v_vals:
    print(f"Running simulation with v = {v}, N = {N}")
    cmd = [
        "julia", "ABP.jl",
        "--Dt", str(Dt),
        "--Dr", str(Dr),
        "--dt", str(dt),
        "--tf", str(tf),
        "--N", str(N),
        "--v", str(v)
    ]
    subprocess.run(cmd)

# # --- Loop over N values ---
# dt = 0.001
# v = 2.0
# N_vals = np.logspace(2, 6, 13).astype(int)
# for N in N_vals:
#     print(f"Running simulation with v = {v}, N = {N}")
#     cmd = [
#         "julia", "ABP.jl",
#         "--Dt", str(Dt),
#         "--Dr", str(Dr),
#         "--dt", str(dt),
#         "--tf", str(tf),
#         "--N", str(N),
#         "--v", str(v)
#     ]
#     subprocess.run(cmd)

# ---Loop over dt values ---
# v = 2.0
# N = 100000
# nsteps_default = 100000
# tf_min = 100.0

# # Loop over dt values
# dt_vals = np.logspace(-4, -1, 13)
# for dt in dt_vals:
#     nsteps = nsteps_default
#     tf = dt * nsteps

#     # If tf is too small, increase nsteps to reach tf_min
#     if tf < tf_min:
#         nsteps = int(tf_min / dt) + 1  # +1 to ensure it crosses the threshold
#         tf = dt * nsteps

#     print(f"Running simulation with v = {v}, N = {N}, dt = {dt:.4f}, tf = {tf:.2f}, steps = {nsteps}")
#     cmd = [
#         "julia", "ABP.jl",
#         "--Dt", str(Dt),
#         "--Dr", str(Dr),
#         "--dt", str(dt),
#         "--tf", str(tf),
#         "--N", str(N),
#         "--v", str(v)
#     ]
#     subprocess.run(cmd)