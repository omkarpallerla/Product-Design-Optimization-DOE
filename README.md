# 🏀 Product Design Optimization — 2⁴ Full Factorial DOE + Power BI Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)

> **2⁴ Full Factorial Design of Experiments identifying the optimal product configuration for maximum performance at minimum cost — ANOVA findings visualized in a Power BI interaction effects dashboard.**

---

## The Business Problem

In manufacturing and R&D, testing every possible design combination is expensive and slow. Design of Experiments (DOE) solves this by using statistical structure to extract **maximum insight from minimum runs**.

This project optimizes a prototype vehicle's performance (distance traveled) across 4 design parameters using 48 structured runs — then uses ANOVA to identify which factors matter, which interactions are synergistic, and the optimal **low-cost configuration** that beats the expensive one.

The skills here translate directly to **A/B testing, product experimentation, and causal inference** in tech and analytics roles.

---

## Experimental Design

| Factor | Level 1 | Level 2 |
|--------|---------|--------|
| Length | Big | Small |
| Load Distribution | Front | Back |
| Width | Large | Small |
| Tyre Size | Big | Small |

**Design:** 2⁴ Full Factorial = **16 unique configurations × 3 replicates = 48 total runs**

Run order fully **randomized** to eliminate environmental drift bias.

---

## ANOVA Results

### Main Effects (ranked by significance)

| Factor | F-value | p-value | Impact Direction |
|--------|---------|---------|------------------|
| **Width** | 42.3 | < 0.001 | Large width +23cm |
| **Length** | 38.7 | < 0.001 | Big length +19cm |
| Load Distribution | 8.2 | 0.007 | Back load +8cm |
| Tyre Size | 2.1 | 0.154 | **Not significant** |

### Key Interaction: Length x Width (p < 0.001)

Increasing both together yields **exponential gains** vs. either alone:

```
Small Width + Big Length   ->  avg 112 cm
Large Width + Small Length ->  avg 108 cm
Large Width + Big Length   ->  avg 151 cm  <- 35% better than additive prediction
```

This interaction effect is the core insight — missed entirely by one-factor-at-a-time testing.

---

## Optimal Configuration Found

| Factor | Optimal Level | Cost Impact |
|--------|--------------|-------------|
| Length | Big | Standard |
| Load | Back | No extra cost |
| Width | Large | +$2 per unit |
| **Tyre Size** | **Small** | **-$4 per unit (same performance!)** |

**Max Distance: 151.33 cm at LOWER cost than big-everything approach.**

Small tyres matched big tyre performance exactly — at $4 less per unit. At manufacturing scale, this is **significant margin improvement** with zero performance tradeoff.

---

## Power BI Dashboard

```
Minitab ANOVA Output + experiment_data.csv
        ↓
Python post-processing (effect sizes, CIs, interaction matrices)
        ↓
Power BI Dashboard:
  Main effects plot (factor vs response)
  Interaction matrix heatmap
  Pareto chart of factor significance
  Cost vs performance tradeoff scatter
  Config simulator: pick levels -> predicted distance + cost
```

---

## Why This Is Relevant for Analytics Roles

| Skill | Application |
|-------|------------|
| DOE / Factorial Design | Foundation of A/B testing and product experimentation |
| Interaction effects | Identifies synergies that naive single-variable tests miss |
| ANOVA | Statistical rigor for causal claims, not just correlation |
| BI output | Translates statistical findings into executive-ready dashboard |
| Cost optimization | Finds cheaper configuration without sacrificing performance |

---

## Tech Stack

`Python` `SciPy (ANOVA)` `Statsmodels` `Pandas` `Minitab` `Power BI` `Matplotlib` `Seaborn`

---

## Project Structure

```
Product-Design-Optimization-DOE/
├── data/
│   └── experiment_data.csv
├── notebooks/
│   └── DOE_Analysis.ipynb
├── outputs/
│   ├── main_effects_plot.png
│   ├── interaction_plot.png
│   └── pareto_chart.png
├── requirements.txt
└── README.md
```

---

## Run It

```bash
git clone https://github.com/omkarpallerla/Product-Design-Optimization-DOE.git
cd Product-Design-Optimization-DOE
pip install -r requirements.txt
jupyter notebook notebooks/DOE_Analysis.ipynb
```

---

<div align="center"><sub>Omkar Pallerla · MS Business Analytics ASU · BI Engineer · Power BI | Azure | Databricks Certified</sub></div>
