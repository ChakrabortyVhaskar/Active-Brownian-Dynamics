import pandas as pd
import numpy as np

v_val = np.arange(0.0, 5.5, 0.5)
results = []

N_fit = 90000
N = 100000

D_T = 1.0 #change according to the simulation
D_r = 1.0 #change accroding to the simulation

for v in v_val:
    filename = f"msd_data_D_1.0_Dr_1.0_v_{v}_N_{N}_dt_0.0010.csv"
    try:
        df = pd.read_csv(filename)
        time = df['time'].values
        msd = df['msd'].values

        # Compute mean_r(t)
        mean_dx = df['mean_dx'].values
        mean_dy = df['mean_dy'].values
        mean_r = np.sqrt(mean_dx**2 + mean_dy**2)

        # Limit to last N_fit points
        n_points = min(N_fit, len(time))
        t_fit = time[-n_points:]

        # Linear fit for MSD → D_eff
        fit_msd = np.polyfit(t_fit, msd[-n_points:], 1)
        Deff = fit_msd[0] / 4

        # Linear fit for mean_r → U_eff
        fit_mean_r = np.polyfit(t_fit, mean_r[-n_points:], 1)
        Ueff = fit_mean_r[0]

        # Theoretical Deff
        Deff_theory = D_T + (v**2) / (2 * D_r)

        results.append({
            'v': v,
            'D_eff': Deff,
            'U_eff': Ueff,
            'D_eff_theory': Deff_theory
        })
    except FileNotFoundError:
        print(f"File not found: {filename}")

# Save results
df_results = pd.DataFrame(results)
df_results.to_csv(f"Deff_Ueff_vs_v_N{N}.csv", index=False)
print(f"Saved to Deff_Ueff_vs_v_N{N}.csv")
