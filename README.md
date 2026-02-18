# Stochastic Tissue Regeneration on a Cellular Lattice
**From Local Hypoxia to Global Scarring**

This model is a high-resolution stochastic simulation framework that models vascularized tissue regeneration as a **Coupled Cellular Automaton**.  

Instead of solving global reaction–diffusion equations, the model demonstrates how complex regenerative outcomes emerge from **localized nearest-neighbor interaction rules** governing proliferation, angiogenesis, ischemia, and fibrosis.

Built using **NumPy + Matplotlib**, the engine simulates anatomical cross-sections and visualizes emergent spatial heterogeneity during healing.

---

## Key Features

* **Anatomically Constrained Geometry:** Radially encoded Bone–Muscle–Skin layers.
* **Stochastic Local Dynamics:** Each cell updates using probabilistic local rules.
* **Angiogenesis Lag Modeling:** Explicit separation between proliferation and vascular expansion speeds.
* **Emergent Pathology:** Naturally produces necrotic islands and scar clusters.
* **Injury Simulation:** Supports dynamic removal of tissue mid-simulation.
* **Parameter Tunable:** Modify growth, vessel, necrosis, and scarring probabilities.

---

## The Core Idea: Healing as a Local Competition

Most biological models use smooth differential equations.  
This model treats tissue as a **100×100 discrete lattice** where each site evolves using only neighbor information.

Each cell $(x, y)$ belongs to one of the states:
| State | Meaning |
|--------|----------|
| B | Bone |
| M | Muscle |
| S | Skin |
| V | Vessel |
| N | Necrosis |
| Sc | Scar |
| ∅ | Empty |

---

## Mathematical Framework

### 1. Lattice

Grid size: 100x100
Von Neumann neighborhood:

$$
N(x,y) = \{ C(x\pm1,y), C(x,y\pm1) \}
$$

Each cell interacts only with its 4 orthogonal neighbors.

---

## Initial Geometry

Radial coordinate:

$$
r = \sqrt{(x - x_c)^2 + (y - y_c)^2}
$$

Layer definition:
