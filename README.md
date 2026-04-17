# 🗺️ Istanbul Pathfinding Visualizer — Pikachu Edition

An interactive pathfinding visualizer built on a **real Istanbul map**, where Pikachu navigates through the city using BFS, DFS, and Dijkstra algorithms. Place obstacles in real time and watch Pikachu reroute dynamically.

> Built as an AI course project — *Principles of Artificial Intelligence, Applied Programming Project*

---

## ✨ Features

- **Real map** — Carto Voyager tile layer with the actual streets of Istanbul
- **3 algorithms** — BFS, DFS, and Dijkstra/A* with live color-coded visualization
- **Compare mode** — Run all three algorithms simultaneously, side-by-side stats
- **Dynamic rerouting** — Place an obstacle while Pikachu is walking and watch it recalculate
- **Particle effects** — Sparkle trail, burst on collision, victory explosion
- **Sound effects** — Web Audio API: footsteps, alert, victory melody, spark
- **Night / Day theme** — Toggle with `G`, animated stars and crescent moon
- **Python launcher** — Local HTTP server with a colorful terminal startup screen
- **PDF report generator** — Benchmarks all 3 algorithms across 12 scenarios
- **Interactive quiz** — 20-question terminal quiz on algorithm theory

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/istanbul-pathfinding.git
cd istanbul-pathfinding

# Install the only dependency (for PDF report)
pip install fpdf2

# Launch the app
python3 launcher.py
```

> Requires Python 3.8+ and a modern browser. Internet connection needed for map tiles.

---

## 📁 Project Structure

```
istanbul-pathfinding/
├── istanbul_v4_final.html   # Main app — real map + Pikachu + algorithms
├── launcher.py              # Python entry point — starts server, opens browser
├── report_generator.py      # Benchmark runner + PDF report generator
├── quiz.py                  # Interactive terminal quiz (no dependencies)
├── requirements.txt
└── README.md
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| Click map | Place start / end / obstacle |
| `Space` | Run selected algorithm |
| `C` | Compare all 3 algorithms |
| `G` | Toggle night / day |
| `R` | Reset |
| `Delete` | Clear all |
| Scroll | Zoom map |

---

## 🧠 Algorithms

| Algorithm | Data Structure | Optimal | Time Complexity |
|-----------|---------------|---------|-----------------|
| BFS | Queue (FIFO) | ✅ (unweighted) | O(V + E) |
| DFS | Stack (LIFO) | ❌ | O(V + E) |
| Dijkstra / A* | Min-Heap | ✅ | O((V+E) log V) |

---

## 📊 Benchmark Results

Averaged over 12 random 30×20 grid scenarios (22% wall density):

| Algorithm | Avg. Cells Visited | Avg. Path Length | Optimal Rate |
|-----------|--------------------|-----------------|--------------|
| BFS | 459 | 49 | 83% |
| DFS | 274 | 73 | 0% |
| Dijkstra/A* | 314 | 49 | 83% |

Run `python3 report_generator.py` to generate a full PDF report.

---

## 🛠️ Tech Stack

- **Frontend** — HTML5 Canvas, Leaflet.js, Web Audio API, Carto tile layers
- **Backend / Tooling** — Python 3 (standard library only for launcher & quiz)
- **Report** — fpdf2

---

## 📄 License

MIT
