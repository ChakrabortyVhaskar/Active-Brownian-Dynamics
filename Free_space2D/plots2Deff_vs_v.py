import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
plt.rcParams.update(params)

fig, ax = plt.subplots(figsize=(fig_width, fig_height))

# Load data
df2 = pd.read_csv("Deff_Ueff_vs_v_N100000.csv")

v = df2['v']
Deff_sim = df2['D_eff']
Deff_theory = df2['D_eff_theory']

# Plot theoretical Deff
ax.plot(
    v, Deff_theory,
    marker='v',
    markersize=4,
    markerfacecolor='none',
    markeredgecolor='red',
    linewidth=1,
    linestyle='--',
    color='black',
    label='Analytical',
    clip_on=False
)

# Plot simulated Deff
ax.plot(
    v, Deff_sim, 
    marker='^',
    linestyle='None',
    markersize=4,
    color='blue',
    label='Simulated',
    markerfacecolor='none',
    clip_on=False
)




# Set axis properties
xticks = np.arange(0.0, 5.5, 0.5)
ax.set_xticks(xticks)
ax.set_xlabel(r"$v_0$")
ax.set_ylabel(r"$D_{\mathrm{eff}}$")

# Tick customization
ax.tick_params(axis="x", which="both", direction="in", top=True, labeltop=False, length=2, width=0.8)
ax.tick_params(axis="y", which="both", direction="in", right=True, labelright=False, length=2, width=0.8)
ax.tick_params(axis="x", which="minor", direction="in", top=True, length=2, width=0.8, color='black')
ax.set_xlim([xticks.min(), xticks.max()])

# Turn off clipping for all markers
for artist in ax.get_children():
    if hasattr(artist, 'set_clip_on'):
        artist.set_clip_on(False)

# Legend
plt.subplots_adjust(left=0.16, bottom=0.2, right=0.95, top=0.9)  # increased right to make room if needed
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles[::-1], labels[::-1], 
    fontsize=6, 
    frameon=False,
    markerfirst=False,
    loc='upper left'  # now inside the plot
)


# Save and show
plt.savefig("Deff_vs_v_N100000_new.pdf")
plt.show()
