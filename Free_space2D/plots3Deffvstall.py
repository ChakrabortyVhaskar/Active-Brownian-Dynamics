import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator

# Plot Parameters
cm_to_inch = 1 / 2.54
fig_width = 8.6 * cm_to_inch
fig_height = 6.45 * cm_to_inch

a = 8
plt.rcParams["text.usetex"] = True
params = {
    "text.latex.preamble": r"\usepackage{amsmath}",
    "font.size": a,
    "font.family": "Computer Modern",
}

fig, ax = plt.subplots(figsize=(fig_width, fig_height))

plt.rcParams.update(params)

# Velocity values
v_val = np.arange(0.0, 5.5, 0.5)  # from 0.5 to 5.0 inclusive
N = 100000

# Plot settings
for v in v_val:
    filename = f"msd_data_D_1.0_Dr_1.0_v_{v}_N_{N}_dt_0.0010.csv"
    try:
        # Read the data
        df = pd.read_csv(filename)
        time = df['time'].values
        msd = df['msd'].values
        
        # Plot MSD vs Time for this v value
        ax.loglog(time[1:], msd[1:], 
                  label=f'v = {v:.1f}',
                  linewidth=0.25,
                 )

    except FileNotFoundError:
        print(f"File not found: {filename}")

# Set labels, title, and legend
xticks = np.logspace(-3, 2, 6)
ax.set_xscale("log")
ax.set_xticks(xticks)
ax.set_xticklabels([f"$10^{{{int(np.log10(x))}}}$" for x in xticks], fontsize=8)
ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(1.0, 10.0) * 0.1, numticks=10))

# Tick customization
ax.tick_params(axis="x", which="both", direction="in", top=True, labeltop=False, length=2, width=0.8)
ax.tick_params(axis="y", which="both", direction="in", right=True, labelright=False, length=2, width=0.8)

ax.tick_params(axis="x", which="minor", direction="in", top=True,
               length=2, width=0.8, color='black')  # Minor ticks
ax.set_xlim([xticks.min(), xticks.max()])

plt.xlabel('Time')
plt.ylabel(' Total MSD ')
# plt.title(f"MSD vs Time for N={N}")

# Adjust the legend to be placed properly within the figure
# Reverse the legend order
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], 
          fontsize=6, 
          frameon=False,
          markerfirst=False,
          loc='upper left',  # Adjust location if needed
          bbox_to_anchor=(1, 1))  # If you want it outside the plot area


plt.tight_layout()  # Adjust the layout to avoid clipping
plt.savefig("Deff_vs_time_N100000_diffv_D1.0_Dr1.0_dt_0.0010.pdf")
plt.show()
