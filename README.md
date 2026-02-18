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
r ≤ 15        → Bone
15 < r ≤ 38   → Muscle
38 < r ≤ 42   → Skin
r > 42        → Empty
Initial vessel density in muscle: p=0.08

---

## Evolution Rules
---

### Rule 1 — Tissue Regrowth

If a neighboring site is non-empty:

$$
C_{t+1}(x,y) = Tissue \quad \text{if} \quad R < P_{growth}
$$

Parameter: $P_{growth}= 0.55$
Cells differentiate by radial position.

---

### Rule 2 — Angiogenesis

If neighbor is Vessel:

$$
C_{t+1}(x,y) = Vessel \quad \text{if} \quad R < P_{vessel}
$$

Parameter: $P_{vessel}=0.10$
Vessel sprouting is ~5× slower than tissue proliferation.

This temporal lag drives pathology.

---

### Rule 3 — Necrosis

If Muscle lacks vascular neighbor:

$$
C_{t+1}(x,y) = Necrosis \quad \text{if} \quad R < P_{necrosis}
$$

Parameter: $P_{necrosis}=0.04$
Prolonged ischemia almost guarantees tissue death.

---

### Rule 4 — Scar Formation
Necrosis → Scar with $P_{scar} = 0.20$
Scar is irreversible.

---

## Injury Event

At timestep: t=30
A wedge-shaped region is removed, resetting cells to Empty.

This creates:

- Moving boundary
- Hypoxic gap
- Competition between growth and perfusion

---

# Emergent Dynamics

Because: $P_{vessel} << P_{growth}$
The regeneration front advances faster than oxygen delivery.

This mismatch generates:

- Patchy scar regions
- Isolated necrotic islands
- Nonuniform vessel penetration

Regenerative failure is therefore a:

> Spatio-temporal synchronization problem.

Increasing `P_vessel` (analogous to VEGF enhancement) improves healing.

---

# Visual Results

## Initial Configuration

<p align="center">
  <img src=""CA Files/Step 29.png" width="450">
  
</p>

---

## Injury Applied

<p align="center">
  <img src="assets/injury.png" width="450">
</p>

---

## Healing Progression

<p align="center">
  <img src="assets/healing.gif" width="600">
</p>

---

## Simulation Phases

| Phase | Behavior |
|-------|----------|
| Early | Rapid regrowth into wound |
| Mid | Vessel lag → hypoxia |
| Late | Necrotic transition |
| Final | Scar-dominated closure |

---

