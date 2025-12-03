# K-Means Clustering Game 🎮

![screenshot](./Assets/Start.png)  

## Features

- Fully interactive visualization of the K-Means algorithm
- Step-by-step or automatic iteration
- Add your own data points with left click
- Manually drag centroids with right click
- Change number of clusters (K) on the fly
- Instant reset with new random centroids
- Clean, commented, educational code (~180 lines)

## How to Play / Controls

| Key / Action          | Function                                      |
|-----------------------|-----------------------------------------------|
| `SPACE`               | Run **one step** of K-Means                   |
| `A`                   | Toggle **auto-iteration** (watch it run)      |
| `R`                   | **Reset** with new random centroids           |
| `↑` / `↓`             | Increase / Decrease number of clusters **K**  |
| `Left Click`          | Add a new data point at mouse position        |
| `Right Click + Drag`  | Manually move a centroid                      |
| `ESC` or close window | Quit the game                                 |

## What You'll See

- **Colored dots** → data points (color = assigned cluster)
- **Larger circles with black borders** → current centroids
- Real-time reassignment and centroid movement as the algorithm converges

## Installation & Running

```bash
# 1. Clone or download this repository
git clone https://github.com/nerkolt/kmeans-game.git
cd kmeans-game

# 2. Install pygame
pip install pygame

# 3. Run the game!
python kmeans_game.py
```
