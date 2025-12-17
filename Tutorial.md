# K‑Means Clustering Game 🎮 (Tutorial)

![screenshot](./Assets/Start.png)

## What this project is

An interactive K‑Means clustering “game” where you can:
- Create / edit datasets in real time
- Run K‑Means step-by-step or automatically
- See **data mining metrics** like **inertia (WCSS)**, convergence history, and the **elbow method**

## Run it

```bash
python Scripts/Kmeans_Game_Debug.py
```

## Controls

### Core gameplay

| Key / Action | What it does |
|---|---|
| `LEFT CLICK` | Add a new point (in the main area) |
| `RIGHT CLICK` | Move the nearest centroid (when close enough) |
| `SPACE` | Run **one** K‑Means iteration |
| `A` | Toggle **Auto** mode |
| `R` | Reset centroids (keeps points) |
| `C` | Clear all points |
| `↑` / `↓` | Increase / decrease **K** quickly |
| `P` | Set number of points (dialog) |
| `K` | Set number of clusters **K** (dialog) |
| `D` | Toggle debug overlay (top-right) |

### Data mining / analysis

| Key | What it does |
|---|---|
| `G` | Toggle **convergence graph** (inertia vs iteration) |
| `S` | Toggle **advanced stats panel** (compactness/separation, per-cluster metrics) |
| `E` | Run the **elbow method** (K vs inertia) |
| `1` | Generate **Blobs** dataset |
| `2` | Generate **Moons** dataset |
| `3` | Generate **Circles** dataset |
| `4` | Generate **Random** dataset |

## What to try (recommended for the report/demo)

- **Best case for K‑Means**: press `1` (Blobs), set `K` equal to the number of visible blobs, press `A`.
- **K‑Means limitation (non‑linear)**: press `2` (Moons) and try `K=2`. You’ll see it doesn’t separate the moons well.
- **Pick K scientifically**: press `E` to run the elbow method, then set `K` and compare results using `S` and `G`.

## Key data mining terms (quick)

- **Inertia / WCSS**: sum of squared distances from points to their assigned centroid. Lower generally means “tighter clusters”.
- **Elbow method**: plot inertia vs K; the “bend” suggests a good K.
- **Convergence**: when assignments stop changing between iterations.


