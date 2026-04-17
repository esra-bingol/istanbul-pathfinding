import heapq
import math
import random
import datetime
from collections import deque
from pathlib import Path
 
try:
    from fpdf import FPDF
except ImportError:
    print("fpdf2 kurulu değil. Kurmak için: pip install fpdf2")
    raise
 
 
# ── Sabitler ──────────────────────────────────────────────────────────────────
 
GRID_COLS   = 30
GRID_ROWS   = 20
WALL_DENSITY = 0.22   # %22 engel
NUM_SCENARIOS = 12    # kaç senaryo çalıştırılacak
RANDOM_SEED   = 42
 
# Renkler (RGB)
C_DARK    = (15,  20,  40)
C_ACCENT  = (0,  180, 140)
C_BFS     = (59, 130, 246)
C_DFS     = (168, 85, 247)
C_DIJ     = (34, 197,  94)
C_GOLD    = (245, 180,  30)
C_LIGHT   = (220, 228, 245)
C_GRAY    = (100, 112, 145)
C_RED     = (220,  60,  60)
C_WHITE   = (255, 255, 255)
C_PANEL   = (22,  30,  52)
C_PANEL2  = (30,  40,  65)
C_GREEN_B = (20,  60,  35)
C_BORDER  = (45,  60,  95)
 
 
# ── Grid & Algoritmalar ────────────────────────────────────────────────────────
 
def make_grid(cols, rows, density, seed):
    rng = random.Random(seed)
    grid = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if rng.random() < density:
                grid[r][c] = 1
    return grid
 
 
def neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0:
            yield nr, nc
 
 
def reconstruct(came, end):
    path, cur = [], end
    while cur:
        path.append(cur)
        cur = came.get(cur)
    path.reverse()
    return path
 
 
def bfs(grid, start, end):
    q = deque([start]); came = {start: None}; visited = []
    while q:
        cur = q.popleft(); visited.append(cur)
        if cur == end: return visited, reconstruct(came, end)
        for nb in neighbors(grid, *cur):
            if nb not in came:
                came[nb] = cur; q.append(nb)
    return visited, []
 
 
def dfs(grid, start, end):
    stack = [start]; came = {start: None}; seen = set(); visited = []
    while stack:
        cur = stack.pop()
        if cur in seen: continue
        seen.add(cur); visited.append(cur)
        if cur == end: return visited, reconstruct(came, end)
        for nb in neighbors(grid, *cur):
            if nb not in came:
                came[nb] = cur; stack.append(nb)
    return visited, []
 
 
def dijkstra(grid, start, end):
    h = lambda r,c: abs(r-end[0]) + abs(c-end[1])
    dist = {start: 0}; pq = [(h(*start), 0, start)]
    came = {start: None}; closed = set(); visited = []
    while pq:
        _, d, cur = heapq.heappop(pq)
        if cur in closed: continue
        closed.add(cur); visited.append(cur)
        if cur == end: return visited, reconstruct(came, end)
        for nb in neighbors(grid, *cur):
            nd = d + 1
            if nd < dist.get(nb, 1e9):
                dist[nb] = nd; came[nb] = cur
                heapq.heappush(pq, (nd + h(*nb), nd, nb))
    return visited, []
 
 
def run_scenario(seed):
    grid  = make_grid(GRID_COLS, GRID_ROWS, WALL_DENSITY, seed)
    rng   = random.Random(seed + 1000)
    start = (0, 0); end = (GRID_ROWS-1, GRID_COLS-1)
    grid[start[0]][start[1]] = 0
    grid[end[0]][end[1]]     = 0
 
    results = {}
    for name, fn in [("BFS", bfs), ("DFS", dfs), ("Dijkstra", dijkstra)]:
        visited, path = fn(grid, start, end)
        results[name] = {
            "visited":  len(visited),
            "path_len": len(path),
            "found":    len(path) > 0,
            "optimal":  False,
        }
 
    # Optimal işaretle (en kısa yol)
    found = [k for k,v in results.items() if v["found"]]
    if found:
        min_p = min(results[k]["path_len"] for k in found)
        for k in found:
            if results[k]["path_len"] == min_p:
                results[k]["optimal"] = True
 
    return results
 
 
def aggregate(all_results):
    stats = {}
    for algo in ["BFS", "DFS", "Dijkstra"]:
        vals = [r[algo] for r in all_results if algo in r]
        found = [v for v in vals if v["found"]]
        stats[algo] = {
            "avg_visited":  sum(v["visited"]  for v in vals)  / max(1,len(vals)),
            "avg_path":     sum(v["path_len"] for v in found) / max(1,len(found)),
            "success_rate": len(found) / max(1,len(vals)) * 100,
            "optimal_rate": sum(1 for v in vals if v["optimal"]) / max(1,len(vals)) * 100,
        }
    return stats
 
 
# ── PDF ───────────────────────────────────────────────────────────────────────
 
class ReportPDF(FPDF):
 
    def __init__(self):
        super().__init__()
        self.set_margins(16, 16, 16)
        self.set_auto_page_break(True, margin=18)
 
    # ── Arka plan ─────────────────────────────────────────────────────────────
 
    def _bg(self):
        self.set_fill_color(*C_DARK)
        self.rect(0, 0, 210, 297, 'F')
 
    def header(self):
        self._bg()
 
    # ── Yardımcılar ───────────────────────────────────────────────────────────
 
    def _color(self, rgb):
        self.set_text_color(*rgb)
 
    def _fill(self, rgb):
        self.set_fill_color(*rgb)
 
    def _draw_color(self, rgb):
        self.set_draw_color(*rgb)
 
    def _rect(self, x, y, w, h, color, style='F'):
        self._fill(color)
        self.rect(x, y, w, h, style)
 
    def _line(self, x1, y1, x2, y2, color, width=0.3):
        self._draw_color(color)
        self.set_line_width(width)
        self.line(x1, y1, x2, y2)
 
    def _text(self, x, y, txt, size=10, bold=False, color=C_LIGHT, align='L'):
        self.set_font("Helvetica", "B" if bold else "", size)
        self._color(color)
        self.set_xy(x, y)
        self.cell(0, 5, txt, align=align)
 
    # ── Kapak sayfası ─────────────────────────────────────────────────────────
 
    def cover_page(self, stats, num_scenarios):
        self.add_page()
        self._bg()
 
        # Üst dekoratif şerit
        self._rect(0, 0, 210, 4, C_ACCENT)
 
        # Başlık bloğu
        self._rect(16, 22, 178, 58, C_PANEL, 'F')
        self._rect(16, 22, 4, 58, C_ACCENT, 'F')
 
        self.set_font("Helvetica", "B", 22)
        self._color(C_ACCENT)
        self.set_xy(24, 30)
        self.cell(0, 10, "ISTANBUL PATHFINDING")
 
        self.set_font("Helvetica", "B", 14)
        self._color(C_LIGHT)
        self.set_xy(24, 43)
        self.cell(0, 8, "Algoritma Performans Analiz Raporu")
 
        self.set_font("Helvetica", "", 9)
        self._color(C_GRAY)
        self.set_xy(24, 55)
        self.cell(0, 5, f"Pikachu Edition  -  {num_scenarios} Senaryo  -  {GRID_COLS}x{GRID_ROWS} Grid")
 
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        self.set_xy(24, 65)
        self.cell(0, 5, f"Olusturulma: {now}")
 
        # Özet kartlar
        y0 = 92
        card_w = 54
        card_data = [
            ("BFS",      C_BFS,  f'{stats["BFS"]["avg_visited"]:.0f}',     "ort. ziyaret"),
            ("DFS",      C_DFS,  f'{stats["DFS"]["avg_visited"]:.0f}',      "ort. ziyaret"),
            ("Dijkstra", C_DIJ,  f'{stats["Dijkstra"]["optimal_rate"]:.0f}%',"optimal oran"),
        ]
        for i, (name, col, val, sub) in enumerate(card_data):
            cx = 16 + i * (card_w + 7)
            self._rect(cx, y0, card_w, 40, C_PANEL2)
            self._rect(cx, y0, card_w, 3, col)
 
            self.set_font("Helvetica", "B", 8)
            self._color(col)
            self.set_xy(cx+4, y0+6)
            self.cell(card_w-8, 5, name)
 
            self.set_font("Helvetica", "B", 20)
            self._color(C_LIGHT)
            self.set_xy(cx+4, y0+14)
            self.cell(card_w-8, 10, val)
 
            self.set_font("Helvetica", "", 7)
            self._color(C_GRAY)
            self.set_xy(cx+4, y0+27)
            self.cell(card_w-8, 5, sub)
 
        # Açıklama kutusu
        self._rect(16, 145, 178, 32, C_PANEL)
        self.set_font("Helvetica", "B", 9)
        self._color(C_ACCENT)
        self.set_xy(20, 149)
        self.cell(0, 5, "Bu Rapor Hakkinda")
        self.set_font("Helvetica", "", 8)
        self._color(C_GRAY)
        self.set_xy(20, 156)
        self.multi_cell(170, 4.5,
            f"Bu rapor, BFS, DFS ve Dijkstra algoritmalarinin {num_scenarios} farkli "
            f"rastgele labirent senaryosundaki performansini karsilastirmaktadir. "
            f"Her senaryo {GRID_COLS}x{GRID_ROWS} boyutunda, %{int(WALL_DENSITY*100)} engel yogunlugunda "
            f"bir grid uzerinde calistirilmistir.")
 
        # Alt çizgi
        self._line(16, 280, 194, 280, C_BORDER, 0.3)
        self.set_font("Helvetica", "", 7)
        self._color(C_GRAY)
        self.set_xy(16, 283)
        self.cell(0, 4, "Istanbul Pathfinding - Pikachu Edition  |  Yapay Zeka Dersi Odevi")
 
    # ── Algoritma karşılaştırma sayfası ───────────────────────────────────────
 
    def comparison_page(self, stats, all_results):
        self.add_page()
        self._bg()
        self._rect(0, 0, 210, 3, C_ACCENT)
 
        self._text(16, 12, "ALGORITMA KARSILASTIRMASI", 13, True, C_ACCENT)
        self._line(16, 20, 194, 20, C_BORDER, 0.3)
 
        # Tablo
        y = 26
        cols_w = [42, 32, 32, 32, 40]
        headers = ["Algoritma", "Ort. Ziyaret", "Ort. Yol", "Basari %", "Optimal %"]
        algos   = [("BFS", C_BFS), ("DFS", C_DFS), ("Dijkstra", C_DIJ)]
 
        # Header
        self._rect(16, y, 178, 9, C_PANEL2)
        x = 16
        for i, h in enumerate(headers):
            self.set_font("Helvetica", "B", 8)
            self._color(C_ACCENT)
            self.set_xy(x+2, y+2)
            self.cell(cols_w[i]-2, 5, h)
            x += cols_w[i]
        y += 9
 
        # Satırlar
        for algo, col in algos:
            s = stats[algo]
            row_bg = C_PANEL if (algos.index((algo,col)) % 2 == 0) else C_DARK
            self._rect(16, y, 178, 9, row_bg)
            self._rect(16, y, 3, 9, col)
 
            vals = [
                algo,
                f'{s["avg_visited"]:.1f}',
                f'{s["avg_path"]:.1f}',
                f'{s["success_rate"]:.0f}%',
                f'{s["optimal_rate"]:.0f}%',
            ]
            x = 16
            for i, v in enumerate(vals):
                fc = col if i == 0 else C_LIGHT
                self.set_font("Helvetica", "B" if i==0 else "", 8)
                self._color(fc)
                self.set_xy(x+4, y+2)
                self.cell(cols_w[i]-4, 5, v)
                x += cols_w[i]
            y += 9
 
        y += 8
 
        # Bar grafikleri
        self._text(16, y, "ZIYARET EDILEN HUCRE KARSILASTIRMASI", 10, True, C_ACCENT)
        y += 10
 
        max_v = max(stats[a]["avg_visited"] for a in ["BFS","DFS","Dijkstra"])
        bar_max_w = 140
 
        for algo, col in algos:
            v = stats[algo]["avg_visited"]
            bw = int((v / max_v) * bar_max_w)
 
            self.set_font("Helvetica", "B", 8)
            self._color(col)
            self.set_xy(16, y+1)
            self.cell(28, 5, algo)
 
            self._rect(46, y, bw, 7, col)
            # Gri arka plan
            self._rect(46+bw, y, bar_max_w-bw, 7, C_PANEL2)
 
            self.set_font("Helvetica", "", 7)
            self._color(C_LIGHT)
            self.set_xy(48+bw, y+1)
            self.cell(0, 5, f" {v:.1f}")
            y += 12
 
        y += 6
 
        # Optimal oran pasta benzeri gösterim
        self._text(16, y, "OPTIMAL YOL BULMA ORANI", 10, True, C_ACCENT)
        y += 10
 
        for algo, col in algos:
            rate = stats[algo]["optimal_rate"]
            self._rect(16, y, 160, 7, C_PANEL2)
            self._rect(16, y, int(rate/100*160), 7, col)
            self.set_font("Helvetica", "B", 8)
            self._color(C_LIGHT)
            self.set_xy(18, y+1)
            self.cell(0, 5, f"{algo}  {rate:.0f}%")
            y += 11
 
        y += 8
        self._text(16, y, "SENARYO BAZLI SONUCLAR (ilk 6)", 10, True, C_ACCENT)
        y += 10
 
        # Mini tablo - senaryo bazlı
        mini_cols = [14, 28, 28, 28, 28, 28, 24]
        mini_h = ["#", "BFS-Ziyaret", "BFS-Yol", "DFS-Ziyaret", "DFS-Yol", "Dij-Ziyaret", "Dij-Yol"]
 
        self._rect(16, y, 178, 8, C_PANEL2)
        x = 16
        for i, h in enumerate(mini_h):
            self.set_font("Helvetica", "B", 7)
            self._color(C_ACCENT)
            self.set_xy(x+1, y+2)
            self.cell(mini_cols[i]-1, 4, h)
            x += mini_cols[i]
        y += 8
 
        for idx, row in enumerate(all_results[:6]):
            bg = C_PANEL if idx%2==0 else C_DARK
            self._rect(16, y, 178, 7, bg)
            row_vals = [
                str(idx+1),
                str(row["BFS"]["visited"]),
                str(row["BFS"]["path_len"]) if row["BFS"]["found"] else "-",
                str(row["DFS"]["visited"]),
                str(row["DFS"]["path_len"]) if row["DFS"]["found"] else "-",
                str(row["Dijkstra"]["visited"]),
                str(row["Dijkstra"]["path_len"]) if row["Dijkstra"]["found"] else "-",
            ]
            x = 16
            for i, v in enumerate(row_vals):
                self.set_font("Helvetica", "", 7)
                self._color(C_LIGHT)
                self.set_xy(x+2, y+1.5)
                self.cell(mini_cols[i]-2, 4, v)
                x += mini_cols[i]
            y += 7
 
    # ── Algoritma açıklama sayfası ────────────────────────────────────────────
 
    def algo_theory_page(self):
        self.add_page()
        self._bg()
        self._rect(0, 0, 210, 3, C_ACCENT)
 
        self._text(16, 12, "ALGORITMA TEORISI", 13, True, C_ACCENT)
        self._line(16, 20, 194, 20, C_BORDER, 0.3)
 
        algos_info = [
            {
                "name":    "BFS - Breadth First Search",
                "color":   C_BFS,
                "complexity": "Zaman: O(V+E)  |  Alan: O(V)",
                "optimal": "EVET - agirliksiz graflarda",
                "complete":"EVET",
                "desc": (
                    "BFS, baslangic dugumunden itibaren tum komsulari katman katman "
                    "kesfeder. Kuyruk (queue) veri yapisi kullanir. Agirliksiz "
                    "graflarda her zaman en kisa yolu bulur. Genis grafiklerde "
                    "bellekte cok yer kaplar cunku tum kesfedilen dugumleri saklar."
                ),
                "pros":  ["Agirliksiz grafta optimal", "Her zaman yolu bulur (varsa)", "Tahmin edilebilir davranis"],
                "cons":  ["Yuksek bellek kullanimi", "Derin grafiklerde yavas", "A* kadar akilli degil"],
            },
            {
                "name":    "DFS - Depth First Search",
                "color":   C_DFS,
                "complexity": "Zaman: O(V+E)  |  Alan: O(V)",
                "optimal": "HAYIR - uzun yollar bulabilir",
                "complete":"HAYIR - sonsuz yollarda takilabilir",
                "desc": (
                    "DFS, bir koldan sonuna kadar giderek arama yapar. Yigin (stack) "
                    "veri yapisi kullanir (veya oz-yineleme). Optimal degildir; "
                    "cok daha uzun bir yol bulabilir. Bellek kullanimi BFS'e gore "
                    "daha dusuktur cunku sadece aktif yolu saklar."
                ),
                "pros":  ["Dusuk bellek kullanimi", "Hizli baslar", "Labirentlerde etkili"],
                "cons":  ["Optimal degil", "Uzun yollar bulabilir", "Dongusel grafiklerde sorunlu"],
            },
            {
                "name":    "Dijkstra / A*",
                "color":   C_DIJ,
                "complexity": "Zaman: O((V+E) log V)  |  Alan: O(V)",
                "optimal": "EVET - agirlikli graflar dahil",
                "complete":"EVET",
                "desc": (
                    "Dijkstra, her dugume olan minimum mesafeyi hesaplayarak ilerler. "
                    "Oncelik kuyrugu (min-heap) kullanir. Bu uygulamada A* heuristigi "
                    "(Manhattan mesafesi) ile guclendirilmistir. Hem agirliksiz hem "
                    "agirlikli grafiklerde optimal sonuc verir."
                ),
                "pros":  ["Her zaman optimal", "Agirlikli grafiklerde mukemmel", "A* ile cok hizli"],
                "cons":  ["BFS/DFS'den daha karmasik", "Negatif agirliklarla calismiyor"],
            },
        ]
 
        y = 26
        for info in algos_info:
            col = info["color"]
            box_h = 68
 
            self._rect(16, y, 178, box_h, C_PANEL)
            self._rect(16, y, 4, box_h, col)
            self._rect(16, y, 178, 10, C_PANEL2)
 
            # Başlık
            self.set_font("Helvetica", "B", 10)
            self._color(col)
            self.set_xy(24, y+3)
            self.cell(0, 5, info["name"])
 
            # Karmaşıklık
            self.set_font("Helvetica", "", 7)
            self._color(C_GRAY)
            self.set_xy(130, y+3)
            self.cell(0, 5, info["complexity"])
 
            # Açıklama
            self.set_font("Helvetica", "", 8)
            self._color(C_LIGHT)
            self.set_xy(24, y+13)
            self.multi_cell(106, 4, info["desc"])
 
            # Optimal / Complete
            tx = 140
            for label, val in [("Optimal:", info["optimal"]),("Eksiksiz:", info["complete"])]:
                self.set_font("Helvetica", "B", 7)
                self._color(C_GRAY)
                self.set_xy(tx, y+13)
                self.cell(0, 4, label)
                self.set_font("Helvetica", "", 7)
                color = C_DIJ if "EVET" in val else C_RED
                self._color(color)
                self.set_xy(tx, y+19)
                self.cell(0, 4, val)
                y += 0
 
            # Artılar
            self.set_font("Helvetica", "B", 7)
            self._color((100, 220, 120))
            self.set_xy(140, y+27)
            self.cell(0, 4, "Avantajlar:")
            for i, pro in enumerate(info["pros"]):
                self.set_font("Helvetica", "", 7)
                self._color(C_LIGHT)
                self.set_xy(140, y+33+i*5)
                self.cell(0, 4, f"+ {pro}")
 
            # Eksiler
            self.set_font("Helvetica", "B", 7)
            self._color(C_RED)
            self.set_xy(140, y+51)
            self.cell(0, 4, "Dezavantajlar:")
            for i, con in enumerate(info["cons"][:2]):
                self.set_font("Helvetica", "", 7)
                self._color(C_GRAY)
                self.set_xy(140, y+57+i*5)
                self.cell(0, 4, f"- {con}")
 
            y += box_h + 7
 
    # ── Sonuç sayfası ─────────────────────────────────────────────────────────
 
    def conclusion_page(self, stats):
        self.add_page()
        self._bg()
        self._rect(0, 0, 210, 3, C_ACCENT)
 
        self._text(16, 12, "SONUC VE DEGERLENDIRME", 13, True, C_ACCENT)
        self._line(16, 20, 194, 20, C_BORDER, 0.3)
 
        # Kazanan kutucukları
        categories = [
            ("En Az Ziyaret (Verimlilik)",
             min(["BFS","DFS","Dijkstra"], key=lambda a: stats[a]["avg_visited"]),
             "Daha az hucre tarayarak hedefe ulasti"),
            ("En Kisa Yol (Optimallik)",
             min(["BFS","DFS","Dijkstra"], key=lambda a: -stats[a]["optimal_rate"]),
             "En yuksek optimal yol bulma orani"),
            ("En Yuksek Basari",
             min(["BFS","DFS","Dijkstra"], key=lambda a: -stats[a]["success_rate"]),
             "Her senaryoda yolu en cok bulan"),
        ]
 
        algo_cols = {"BFS": C_BFS, "DFS": C_DFS, "Dijkstra": C_DIJ}
        y = 28
        for cat, winner, reason in categories:
            col = algo_cols[winner]
            self._rect(16, y, 178, 22, C_PANEL)
            self._rect(16, y, 4, 22, col)
            self._rect(16, y, 178, 1, col)
 
            self.set_font("Helvetica", "B", 8)
            self._color(C_GRAY)
            self.set_xy(24, y+3)
            self.cell(0, 4, cat.upper())
 
            self.set_font("Helvetica", "B", 14)
            self._color(col)
            self.set_xy(24, y+9)
            self.cell(0, 7, winner)
 
            self.set_font("Helvetica", "", 8)
            self._color(C_LIGHT)
            self.set_xy(90, y+11)
            self.cell(0, 5, reason)
 
            y += 27
 
        # Genel yorum
        y += 5
        self._rect(16, y, 178, 55, C_PANEL)
        self._rect(16, y, 4, 55, C_GOLD)
 
        self.set_font("Helvetica", "B", 10)
        self._color(C_GOLD)
        self.set_xy(24, y+5)
        self.cell(0, 6, "Genel Degerlendirme")
 
        self.set_font("Helvetica", "", 8.5)
        self._color(C_LIGHT)
        self.set_xy(24, y+14)
        self.multi_cell(166, 5,
            f"Bu analiz, {NUM_SCENARIOS} farkli labirent senaryosunda uc algoritmanin "
            f"guclu ve zayif yonlerini ortaya koymaktadir.\n\n"
            f"Dijkstra/A* algoritmasi {stats['Dijkstra']['optimal_rate']:.0f}% optimal oran ile "
            f"en guvenilir sonuclari vermistir. BFS, agirliksiz grafiklerde garantili optimal "
            f"yol bulurken, DFS en az bellek kullanan ancak optimal olmayan secenektir.\n\n"
            f"Gercek sehir navigasyonu icin Dijkstra veya A* onerilir.")
 
        # Footer
        self._line(16, 278, 194, 278, C_BORDER, 0.3)
        self.set_font("Helvetica", "", 7)
        self._color(C_GRAY)
        self.set_xy(16, 281)
        now = datetime.datetime.now().strftime("%d.%m.%Y")
        self.cell(0, 4, f"Istanbul Pathfinding Raporu  -  {now}  -  Sayfa {{page}}")
 
 
# ── Ana fonksiyon ──────────────────────────────────────────────────────────────
 
RESET  = "\033[0m"; BOLD = "\033[1m"; CYAN = "\033[96m"
GREEN  = "\033[92m"; YELLOW = "\033[93m"; GRAY = "\033[90m"
 
def main():
    print()
    print(f"  {CYAN}{BOLD}PDF Rapor Uretici{RESET}")
    print(f"  {GRAY}Istanbul Pathfinding - Algoritma Analizi{RESET}")
    print()
 
    # Senaryoları çalıştır
    print(f"  {YELLOW}▸{RESET} {NUM_SCENARIOS} senaryo calistiriliyor...")
    all_results = []
    for i in range(NUM_SCENARIOS):
        res = run_scenario(RANDOM_SEED + i * 17)
        all_results.append(res)
        bar = "█" * (i+1) + "░" * (NUM_SCENARIOS-i-1)
        print(f"    [{bar}] {i+1}/{NUM_SCENARIOS}", end="\r")
    print(f"    {GREEN}✓{RESET}  Tum senaryolar tamamlandi{' '*20}")
    print()
 
    # İstatistikleri hesapla
    stats = aggregate(all_results)
 
    print(f"  {YELLOW}▸{RESET} Sonuclar:")
    for algo, col_code in [("BFS","\033[94m"),("DFS","\033[95m"),("Dijkstra","\033[92m")]:
        s = stats[algo]
        print(f"    {col_code}{BOLD}{algo:<10}{RESET} "
              f"ort.ziyaret={s['avg_visited']:.0f}  "
              f"ort.yol={s['avg_path']:.0f}  "
              f"optimal={s['optimal_rate']:.0f}%")
    print()
 
    # PDF oluştur
    print(f"  {YELLOW}▸{RESET} PDF olusturuluyor...")
    pdf = ReportPDF()
    pdf.cover_page(stats, NUM_SCENARIOS)
    pdf.comparison_page(stats, all_results)
    pdf.algo_theory_page()
    pdf.conclusion_page(stats)
 
    out = Path("pathfinding_rapor.pdf")
    pdf.output(str(out))
 
    size_kb = out.stat().st_size // 1024
    print(f"    {GREEN}✓{RESET}  {out}  ({size_kb} KB, {pdf.page} sayfa)")
    print()
    print(f"  {GRAY}Rapor hazir! pathfinding_rapor.pdf dosyasini acin.{RESET}")
    print()
 
 
if __name__ == "__main__":
    main()