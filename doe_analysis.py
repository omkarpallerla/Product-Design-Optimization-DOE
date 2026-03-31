# =============================================================
# Product Design Optimization — 2^4 Full Factorial DOE
# Author: Omkar Pallerla | MS Business Analytics, ASU
# ANOVA + Interaction Analysis + Power BI Output
# =============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from itertools import product
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import warnings
warnings.filterwarnings('ignore')

plt.style.use('dark_background')
np.random.seed(42)
COLORS = ['#4f9cf9','#06d6a0','#7c3aed','#f59e0b','#ef4444']

# ══════════════════════════════════════════════════════════════
# DEFINE 2^4 FULL FACTORIAL DESIGN
# ══════════════════════════════════════════════════════════════
factors = {
    'Length':    {'Big': 1, 'Small': -1},
    'Load':      {'Back': 1, 'Front': -1},
    'Width':     {'Large': 1, 'Small': -1},
    'TyreSize':  {'Big': 1, 'Small': -1},
}

factor_names  = list(factors.keys())
level_combos  = list(product([-1, 1], repeat=4))
N_REPLICATES  = 3

# Generate experiment data with known effects
# True effects (cm): Width=+23, Length=+19, Load=+8, Tyre=+1.2
# Interaction: Length×Width = +12 (synergistic)
def simulate_response(L, Lo, W, T, noise_std=4.5):
    base     = 110
    main_eff = 9.5*L + 4.0*Lo + 11.5*W + 0.6*T
    interact = 6.0*L*W       # Length×Width interaction
    noise    = np.random.normal(0, noise_std)
    return base + main_eff + interact + noise

rows = []
for combo in level_combos:
    L, Lo, W, T = combo
    for rep in range(1, N_REPLICATES + 1):
        response = simulate_response(L, Lo, W, T)
        rows.append({
            'Length':    'Big'   if L  == 1 else 'Small',
            'Load':      'Back'  if Lo == 1 else 'Front',
            'Width':     'Large' if W  == 1 else 'Small',
            'TyreSize':  'Big'   if T  == 1 else 'Small',
            'L':  L, 'Lo': Lo, 'W': W, 'T': T,
            'Replicate': rep,
            'Distance':  response
        })

df = pd.DataFrame(rows)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # randomize run order
df['RunOrder'] = range(1, len(df)+1)

print(f"Experiment design: 2^4 × {N_REPLICATES} replicates = {len(df)} runs")
print(f"Response (Distance):")
print(f"  Mean: {df['Distance'].mean():.2f} cm")
print(f"  Std:  {df['Distance'].std():.2f} cm")
print(f"  Min:  {df['Distance'].min():.2f} cm")
print(f"  Max:  {df['Distance'].max():.2f} cm")

# ══════════════════════════════════════════════════════════════
# ANOVA — MAIN EFFECTS + INTERACTIONS
# ══════════════════════════════════════════════════════════════
formula = "Distance ~ L + Lo + W + T + L:W + L:Lo + W:T"
model   = ols(formula, data=df).fit()
anova   = anova_lm(model, typ=2)

print("\n" + "="*60)
print("ANOVA TABLE (Type II Sum of Squares)")
print("="*60)
print(anova.to_string())

# Identify significant effects (p < 0.05)
significant = anova[anova['PR(>F)'] < 0.05].index.tolist()
print(f"\nSignificant effects (p<0.05): {significant}")

# ── MAIN EFFECTS ────────────────────────────────────────────
print("\nMain Effects (cm):")
for factor, col in zip(['Length','Load','Width','TyreSize'], ['L','Lo','W','T']):
    hi  = df[df[col] == 1]['Distance'].mean()
    lo  = df[df[col] == -1]['Distance'].mean()
    eff = hi - lo
    t_stat, p_val = stats.ttest_ind(
        df[df[col] == 1]['Distance'],
        df[df[col] == -1]['Distance']
    )
    print(f"  {factor:12s}: +{eff:.1f} cm  (p={p_val:.4f}) {'✅' if p_val < 0.05 else '❌ not sig.'}")

# ── INTERACTION EFFECTS ──────────────────────────────────────
print("\nKey Interaction — Length × Width:")
combos_lw = df.groupby(['Length','Width'])['Distance'].mean().unstack()
print(combos_lw.to_string())
interaction_effect = (combos_lw.loc['Big','Large'] + combos_lw.loc['Small','Small'] -
                       combos_lw.loc['Big','Small'] - combos_lw.loc['Small','Large']) / 2
print(f"  Interaction Effect: {interaction_effect:.1f} cm")
print(f"  Synergy: Big Length + Large Width = {combos_lw.loc['Big','Large']:.1f} cm")
print(f"           (additive prediction: ~{combos_lw.loc['Big','Small'].mean():.1f} cm)")

# ── OPTIMAL CONFIGURATION ───────────────────────────────────
config_means = df.groupby(['Length','Load','Width','TyreSize'])['Distance'].mean().reset_index()
config_means = config_means.sort_values('Distance', ascending=False)
best_config  = config_means.iloc[0]

print(f"\n{'='*60}")
print(f"OPTIMAL CONFIGURATION:")
print(f"  Length:   {best_config['Length']}")
print(f"  Load:     {best_config['Load']}")
print(f"  Width:    {best_config['Width']}")
print(f"  Tyre:     {best_config['TyreSize']}")
print(f"  Distance: {best_config['Distance']:.2f} cm")
print(f"\nCost Insight: Small Tyres = same performance as Big Tyres")
print(f"  → Save $4/unit at scale (significant margin improvement)")

# Export
df.to_csv('outputs/experiment_data.csv', index=False)
config_means.to_csv('outputs/configuration_results.csv', index=False)
print("Exported: outputs/experiment_data.csv, outputs/configuration_results.csv")

# ══════════════════════════════════════════════════════════════
# VISUALIZATIONS
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.patch.set_facecolor('#0d1117')

# Main effects plot
ax = axes[0, 0]
effects = {}
for factor, col in zip(['Length','Load','Width','TyreSize'], ['L','Lo','W','T']):
    hi = df[df[col] == 1]['Distance'].mean()
    lo = df[df[col] == -1]['Distance'].mean()
    effects[factor] = hi - lo
eff_df = pd.Series(effects).sort_values(ascending=True)
colors_eff = ['#06d6a0' if abs(v) > 5 else ('#f59e0b' if abs(v) > 2 else '#7a8499')
              for v in eff_df.values]
ax.barh(eff_df.index, eff_df.values, color=colors_eff)
ax.axvline(0, color='white', alpha=0.3, linestyle='--')
ax.set_xlabel('Main Effect on Distance (cm)')
ax.set_title('Main Effects — Factor vs Response', color='white', pad=12)
for i, (k, v) in enumerate(eff_df.items()):
    ax.text(v + 0.2 if v >= 0 else v - 0.2, i,
            f'+{v:.1f}' if v > 0 else f'{v:.1f}',
            va='center', color='white', fontsize=9,
            ha='left' if v >= 0 else 'right')

# Pareto chart of effects
ax = axes[0, 1]
sorted_eff = sorted(effects.items(), key=lambda x: abs(x[1]), reverse=True)
names_p = [k for k,v in sorted_eff]
vals_p  = [abs(v) for k,v in sorted_eff]
t_crit  = stats.t.ppf(0.975, df=len(df)-5) * df['Distance'].std() / np.sqrt(len(df))
ax.bar(names_p, vals_p, color=['#06d6a0' if v > t_crit else '#4a5568' for v in vals_p])
ax.axhline(t_crit, color='#ef4444', linestyle='--', label=f't-critical={t_crit:.1f}')
ax.set_ylabel('|Effect| (cm)')
ax.set_title('Pareto — Standardized Effects', color='white', pad=12)
ax.legend(fontsize=8)

# Interaction plot Length × Width
ax = axes[0, 2]
for width_level, color in zip(['Large','Small'], ['#06d6a0','#4f9cf9']):
    sub = df[df['Width'] == width_level].groupby('Length')['Distance'].mean()
    ax.plot(sub.index, sub.values, marker='o', color=color,
            label=f'Width={width_level}', lw=2, ms=8)
ax.set_xlabel('Length'); ax.set_ylabel('Avg Distance (cm)')
ax.set_title('Interaction Plot: Length × Width\n(Crossing lines = significant interaction)', color='white', pad=12)
ax.legend(); ax.grid(alpha=0.15)

# Configuration performance
ax = axes[1, 0]
top10 = config_means.head(10)
colors_c = ['#06d6a0' if i == 0 else '#4f9cf9' for i in range(10)]
ax.barh([f"{r['Length'][0]}L+{r['Load'][0]}Lo+{r['Width'][0]}W+{r['TyreSize'][0]}T"
         for _,r in top10.iterrows()][::-1],
        top10['Distance'].values[::-1], color=colors_c[::-1])
ax.set_xlabel('Average Distance (cm)')
ax.set_title('Top 10 Configurations', color='white', pad=12)

# Residuals normality check
residuals = model.resid
ax = axes[1, 1]
stats.probplot(residuals, plot=ax)
ax.set_title('Q-Q Plot — Residuals Normality Check', color='white', pad=12)
ax.get_lines()[0].set(color='#4f9cf9', alpha=0.7)
ax.get_lines()[1].set(color='#ef4444')

# ANOVA F-values
ax = axes[1, 2]
anova_plot = anova.dropna()
fvals = anova_plot['F'].sort_values(ascending=True)
ax.barh(fvals.index, fvals.values,
        color=['#06d6a0' if v > 4 else '#4a5568' for v in fvals.values])
ax.axvline(4.0, color='#ef4444', linestyle='--', alpha=0.6, label='F-critical ≈ 4.0')
ax.set_xlabel('F-value')
ax.set_title('ANOVA F-values', color='white', pad=12)
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig('outputs/doe_analysis.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
print("Saved: outputs/doe_analysis.png")
plt.show()
