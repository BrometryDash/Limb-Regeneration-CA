import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# -------- PARAMETERS --------
GRID_SIZE = 100
CENTER = GRID_SIZE // 2
STEPS = 250
INJURY_FRAME = 30

PROB_TISSUE_GROWTH = 0.55
PROB_VESSEL_GROWTH = 0.10
PROB_NECROSIS = 0.04
PROB_SCAR_FORMATION = 0.20

EMPTY, BONE, MUSCLE, SKIN, VESSEL, NECROSIS, SCAR = range(7)

RAD_BONE = 15
RAD_MUSCLE = 38
RAD_SKIN = 42
# ----------------------------


class VascularModel:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.injury_mask = np.zeros((size, size), dtype=bool)

        y, x = np.ogrid[:size, :size]
        self.dist = np.sqrt((x - CENTER) ** 2 + (y - CENTER) ** 2)

        # Layered tissue
        self.grid[self.dist <= RAD_SKIN] = SKIN
        self.grid[self.dist <= RAD_MUSCLE] = MUSCLE
        self.grid[self.dist <= RAD_BONE] = BONE
        self.grid[self.dist > RAD_SKIN] = EMPTY

        # Initial vessels in muscle
        muscle_mask = self.grid == MUSCLE
        vessels = (np.random.random((size, size)) < 0.08) & muscle_mask
        self.grid[vessels] = VESSEL

    def amputate(self):
        y, x = np.ogrid[:self.size, :self.size]
        angle = np.arctan2(y - CENTER, x - CENTER)
        cut = (np.abs(angle) < 0.5) & (self.dist < 50)

        self.grid[cut] = EMPTY
        self.injury_mask[cut] = True

    def neighbors(self):
        g = self.grid
        up = np.roll(g, -1, 0)
        down = np.roll(g, 1, 0)
        left = np.roll(g, -1, 1)
        right = np.roll(g, 1, 1)
        return up, down, left, right

    def update(self):
        g = self.grid
        new = g.copy()
        up, down, left, right = self.neighbors()

        has_neighbor = (up > 0) | (down > 0) | (left > 0) | (right > 0)
        near_vessel = (up == VESSEL) | (down == VESSEL) | \
                      (left == VESSEL) | (right == VESSEL)

        dice = np.random.random(g.shape)

        # -------- Tissue Regrowth --------
        grow = (g == EMPTY) & has_neighbor & self.injury_mask & (dice < PROB_TISSUE_GROWTH)

        new[grow & (self.dist <= RAD_BONE)] = BONE
        new[grow & (self.dist <= RAD_MUSCLE) & (self.dist > RAD_BONE)] = MUSCLE
        new[grow & (self.dist <= RAD_SKIN) & (self.dist > RAD_MUSCLE)] = SKIN
        new[(new != EMPTY) & (self.dist > RAD_SKIN)] = EMPTY

        # -------- Vessel Sprouting --------
        vessel_grow = (g == EMPTY) & near_vessel & self.injury_mask & (dice < PROB_VESSEL_GROWTH)
        new[vessel_grow] = VESSEL

        # -------- Necrosis --------
        death = (g == MUSCLE) & (~near_vessel) & self.injury_mask & \
                (np.random.random(g.shape) < PROB_NECROSIS)
        new[death] = NECROSIS

        # -------- Scar Formation --------
        scar = (g == NECROSIS) & (np.random.random(g.shape) < PROB_SCAR_FORMATION)
        new[scar] = SCAR

        self.grid = new

# -------- Visualization --------
model = VascularModel(GRID_SIZE)

colors = [
    '#2b2b2b', '#f4f1e8', '#c14953', '#e6c9a8',
    '#7a1e1e', '#4d3b2f', '#d6cfc7'
]

cmap = ListedColormap(colors)

fig, ax = plt.subplots(figsize=(7, 7))
ax.axis('off')
fig.patch.set_facecolor('#1e1e1e')

img = ax.imshow(model.grid, cmap=cmap, vmin=0, vmax=6)

legend_elements = [
    Patch(facecolor=colors[BONE], label='Bone'),
    Patch(facecolor=colors[MUSCLE], label='Muscle'),
    Patch(facecolor=colors[SKIN], label='Skin'),
    Patch(facecolor=colors[VESSEL], label='Vessel'),
    Patch(facecolor=colors[SCAR], label='Scar')
]

legend = ax.legend(handles=legend_elements, loc='lower left',
                   fontsize=9, frameon=True)

legend.get_frame().set_facecolor('#1e1e1e')
legend.get_frame().set_edgecolor('white')
plt.setp(legend.get_texts(), color='white')


# -------- Animation --------
def animate(frame):
    if frame == INJURY_FRAME:
        model.amputate()
        title = "Injury Applied"
    else:
        scar_count = np.sum(model.grid == SCAR)
        title = f"Step {frame} | Scar Area: {scar_count}"

    ax.set_title(title, color='white', fontsize=12)
    model.update()
    img.set_data(model.grid)
    return [img]


ani = animation.FuncAnimation(fig, animate,
                              frames=STEPS,
                              interval=50)
# --------------------------
ani.save("vascular_CA67.gif",
         writer="pillow",
         fps=18)
