import os
import sys
import time
import socket
import threading
import webbrowser
import http.server
import urllib.request
from pathlib import Path

RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RED    = "\033[91m"
GRAY   = "\033[90m"
BLUE   = "\033[94m"
MAGENTA= "\033[95m"

def banner():
    print()
    print(f"{YELLOW}{BOLD}  ██████╗ ██╗██╗  ██╗ █████╗ {CYAN} ██████╗  █████╗ ████████╗██╗  ██╗{RESET}")
    print(f"{YELLOW}{BOLD}  ██╔══██╗██║██║ ██╔╝██╔══██╗{CYAN} ██╔══██╗██╔══██╗╚══██╔══╝██║  ██║{RESET}")
    print(f"{YELLOW}{BOLD}  ██████╔╝██║█████╔╝ ███████║{CYAN} ██████╔╝███████║   ██║   ███████║{RESET}")
    print(f"{YELLOW}{BOLD}  ██╔═══╝ ██║██╔═██╗ ██╔══██║{CYAN} ██╔═══╝ ██╔══██║   ██║   ██╔══██║{RESET}")
    print(f"{YELLOW}{BOLD}  ██║     ██║██║  ██╗██║  ██║{CYAN} ██║     ██║  ██║   ██║   ██║  ██║{RESET}")
    print(f"{YELLOW}{BOLD}  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{CYAN} ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝{RESET}")
    print()
    print(f"  {MAGENTA}{BOLD}Istanbul Pathfinding{RESET}  {GRAY}—{RESET}  {CYAN}Pikachu Edition{RESET}")
    print(f"  {GRAY}BFS  •  DFS  •  Dijkstra  •  Gece/Gunduz  •  Parcacik Efektleri{RESET}")
    print()

def section(title: str):
    print(f"  {CYAN}▸{RESET} {BOLD}{title}{RESET}")

def ok(msg: str):
    print(f"    {GREEN}✓{RESET}  {msg}")

def warn(msg: str):
    print(f"    {YELLOW}⚠{RESET}  {msg}")

def err(msg: str):
    print(f"    {RED}✗{RESET}  {msg}")

def info(msg: str):
    print(f"    {GRAY}{msg}{RESET}")


HTML_FILE = "istanbul_v4_final.html"

def check_files() -> bool:
    section("Dosya kontrolu")
    html = Path(HTML_FILE)
    if html.exists():
        size_kb = html.stat().st_size // 1024
        ok(f"{HTML_FILE}  ({size_kb} KB)")
        return True
    else:
        err(f"{HTML_FILE} bulunamadi!")
        info("Lutfen HTML dosyasini bu klasore koyun.")
        return False

def check_internet() -> bool:
    section("Baglanti kontrolu")
    try:
        urllib.request.urlopen("https://a.basemaps.cartocdn.com", timeout=4)
        ok("Carto harita sunucusuna ulasildi")
        return True
    except Exception:
        warn("Internet baglantisi yok — harita yuklenemeyebilir")
        return False

def find_free_port(start: int = 8765) -> int:
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    return start


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Sessiz HTTP handler — log satirlarini gizler."""

    def log_message(self, fmt, *args):
        pass   # terminal kirlenmesi olmasin

    def log_error(self, fmt, *args):
        pass


def start_server(port: int) -> http.server.HTTPServer:
    server = http.server.HTTPServer(("", port), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

def algo_info():
    section("Uygulanan Algoritmalar")
    algos = [
        ("BFS",      "Breadth-First Search",  "En kisa yolu garanti eder (agirliksiz)"),
        ("DFS",      "Depth-First Search",    "Derin arama, optimal degildir"),
        ("Dijkstra", "Dijkstra / A*",         "Agirlikli graf icin optimal yol"),
    ]
    for short, full, desc in algos:
        print(f"    {CYAN}{short:<10}{RESET} {BOLD}{full:<28}{RESET} {GRAY}{desc}{RESET}")
    print()


def controls():
    section("Kisayollar")
    keys = [
        ("Space",  "Algoritmay calistir"),
        ("R",      "Sifirla"),
        ("C",      "Tum algoritmalari karsilastir"),
        ("G",      "Gece / Gunduz gecisi"),
        ("Delete", "Haritayi temizle"),
    ]
    for key, desc in keys:
        print(f"    {YELLOW}{key:<10}{RESET} {desc}")
    print()


def main():
    banner()

    
    if not check_files():
        sys.exit(1)
    print()
    check_internet()
    print()

    
    algo_info()
    controls()

    
    port = find_free_port()
    section("Sunucu baslatiliyor")
    server = start_server(port)
    url    = f"http://localhost:{port}/{HTML_FILE}"
    ok(f"Sunucu calisiyor  →  {CYAN}{url}{RESET}")
    print()

   
    section("Tarayici aciliyor")
    time.sleep(0.6)
    webbrowser.open(url)
    ok("Tarayici acildi")
    print()

    
    print(f"  {GRAY}{'─'*54}{RESET}")
    print(f"  {BOLD}Uygulamayi kapatmak icin {RED}Ctrl+C{RESET}{BOLD} tuslayın.{RESET}")
    print(f"  {GRAY}{'─'*54}{RESET}")
    print()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        section("Kapatiliyor")
        server.shutdown()
        ok("Sunucu durduruldu")
        print()
        print(f"  {GRAY}Gorusuruz! ⚡{RESET}")
        print()


if __name__ == "__main__":
    main()