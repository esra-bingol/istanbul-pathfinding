import sys
import time
import random
import textwrap
 
R  = "\033[0m"
B  = "\033[1m"
CY = "\033[96m"
YE = "\033[93m"
GR = "\033[92m"
RE = "\033[91m"
GY = "\033[90m"
MA = "\033[95m"
BL = "\033[94m"
WH = "\033[97m"
 
def clear():
    print("\033[H\033[J", end="")
 
def divider(char="─", width=58, color=GY):
    print(f"  {color}{char*width}{R}")
 
def slow_print(text, delay=0.018):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()
 
 
 
QUESTIONS = [
    {
        "q": "BFS hangi veri yapısını kullanır?",
        "opts": ["Stack (Yığın)", "Queue (Kuyruk)", "Priority Queue", "Linked List"],
        "ans": 1,
        "exp": "BFS, FIFO (ilk giren ilk çıkar) mantığıyla çalışan Queue kullanır. "
               "Bu sayede her seviyedeki düğümleri sırayla keşfeder.",
        "algo": "BFS",
    },
    {
        "q": "Ağırlıksız bir grafta en kısa yolu hangi algoritma garanti eder?",
        "opts": ["DFS", "Sadece Dijkstra", "BFS ve Dijkstra", "Hiçbiri"],
        "ans": 2,
        "exp": "Ağırlıksız grafta BFS her zaman en az kenarlı yolu bulur. "
               "Dijkstra da doğru çalışır çünkü tüm ağırlıklar eşit (1) kabul edilir.",
        "algo": "BFS",
    },
    {
        "q": "DFS'in zaman karmaşıklığı nedir?",
        "opts": ["O(V²)", "O(E log V)", "O(V + E)", "O(V × E)"],
        "ans": 2,
        "exp": "DFS, her düğümü (V) ve her kenarı (E) en fazla bir kez ziyaret eder. "
               "Bu nedenle zaman karmaşıklığı O(V + E)'dir.",
        "algo": "DFS",
    },
    {
        "q": "Dijkstra algoritması negatif ağırlıklı kenarlarda neden çalışmaz?",
        "opts": [
            "Çok yavaş olduğu için",
            "Negatif döngülerde sonsuz döngüye girer",
            "Sadece tam sayı ağırlıklar desteklenir",
            "Priority queue negatif değerleri sıralayamaz",
        ],
        "ans": 1,
        "exp": "Dijkstra, bir düğüme ulaştığında o düğümün mesafesini kesinleştirir. "
               "Negatif kenarlar bu varsayımı bozar; daha önce kesinleştirilen düğüme "
               "negatif bir kenarla daha kısa yol bulunabilir, bu da sonsuz döngüye yol açar.",
        "algo": "Dijkstra",
    },
    {
        "q": "A* algoritması Dijkstra'dan nasıl farklıdır?",
        "opts": [
            "A* ağırlıkları yok sayar",
            "A* heuristik (sezgisel) fonksiyon kullanır",
            "A* her zaman daha az düğüm ziyaret eder",
            "A* sadece grid grafiklerde çalışır",
        ],
        "ans": 1,
        "exp": "A*, Dijkstra'ya hedef tahmini (heuristik) ekler: f(n) = g(n) + h(n). "
               "g(n) gerçek maliyet, h(n) tahmini kalan maliyettir. "
               "İyi bir heuristik ile çok daha az düğüm keşfeder.",
        "algo": "Dijkstra",
    },
    {
        "q": "BFS'in bellek karmaşıklığı neden O(V)'dir?",
        "opts": [
            "Tüm grafı bellekte saklar",
            "En kötü durumda tüm düğümleri queue'ya ekler",
            "Her kenar için ayrı bellek kullanır",
            "Rekürsif çağrılar stack overflow yaratır",
        ],
        "ans": 1,
        "exp": "BFS en kötü durumda (hedef son seviyedeyse) tüm düğümleri queue'ya "
               "ekleyebilir. Geniş grafiklerde bu çok fazla bellek tüketir. "
               "DFS ise yalnızca aktif dalı saklar, daha az bellek kullanır.",
        "algo": "BFS",
    },
    {
        "q": "Hangisi DFS için YANLIŞ bir ifadedir?",
        "opts": [
            "Stack veri yapısı kullanır",
            "Agırlıksız grafta optimal yol bulur",
            "Rekürsif olarak yazılabilir",
            "O(V+E) zaman karmaşıklığına sahiptir",
        ],
        "ans": 1,
        "exp": "DFS optimal değildir! Hedefe ulaşan ilk yolu döndürür ama bu en kısa yol "
               "olmayabilir. Labirentlerde çok uzun bir yol bulabilirken BFS veya Dijkstra "
               "daha kısa bir yol bulur.",
        "algo": "DFS",
    },
    {
        "q": "Şehir navigasyonu (Google Maps) için en uygun algoritma hangisidir?",
        "opts": ["BFS", "DFS", "Dijkstra / A*", "Hepsi aynı performansı verir"],
        "ans": 2,
        "exp": "Şehir haritaları ağırlıklı grafiktir (yol uzunlukları farklı). "
               "BFS ağırlıkları görmez, DFS optimal değil. "
               "Google Maps, A* ve Dijkstra kombinasyonu kullanır.",
        "algo": "Dijkstra",
    },
    {
        "q": "BFS ile 5×5 grid'de başlangıçtan tüm hücrelere kaç adımda ulaşılır? "
             "(Engel yok, 4-yön hareket)",
        "opts": ["4 adım", "8 adım", "16 adım", "24 adım"],
        "ans": 1,
        "exp": "5×5 grid'de en uzak köşe (4,4) Manhattan mesafesi 4+4=8'dir. "
               "BFS katman katman genişlediği için 8 adımda tüm hücrelere ulaşır. "
               "Toplam 25 hücrenin hepsi keşfedilir.",
        "algo": "BFS",
    },
    {
        "q": "Dijkstra hangi veri yapısıyla en verimli çalışır?",
        "opts": ["Array", "Linked List", "Min-Heap (Priority Queue)", "Hash Table"],
        "ans": 2,
        "exp": "Dijkstra'da her adımda en düşük maliyetli düğümü bulmak gerekir. "
               "Min-Heap bu işlemi O(log V) ile yapar. "
               "Array ile O(V²) olur — büyük grafiklerde çok yavaş.",
        "algo": "Dijkstra",
    },
    {
        "q": "Hangi durumda DFS, BFS'ten daha avantajlıdır?",
        "opts": [
            "En kısa yol aranıyorsa",
            "Grafın çok geniş (wide) olduğu durumlarda",
            "Yol olup olmadığı kontrol ediliyorsa",
            "Negatif ağırlıklar varsa",
        ],
        "ans": 1,
        "exp": "Çok geniş (yüksek branching factor) grafiklerde BFS'in queue'su patlar. "
               "DFS sadece aktif dalı bellekte tuttuğu için avantajlıdır. "
               "Örneğin satranç ağacında DFS daha uygulanabilirdir.",
        "algo": "DFS",
    },
    {
        "q": "Manhattan heuristiği nedir ve A*'da neden kullanılır?",
        "opts": [
            "Öklid mesafesi hesabıdır",
            "h(n) = |x1-x2| + |y1-y2| — grid hareketi için optimal tahmin",
            "Ağırlıkların ortalamasıdır",
            "Dijkstra'nın özel bir versiyonudur",
        ],
        "ans": 1,
        "exp": "Manhattan mesafesi, yatay+dikey hareket sayısıdır. "
               "4-yön grid hareketinde hiçbir zaman gerçek mesafeyi aşmadığı için "
               "'kabul edilebilir' (admissible) bir heuristiktir. "
               "Bu A*'ın optimal kalmasını sağlar.",
        "algo": "Dijkstra",
    },
    {
        "q": "Pikachu bir engele çarptığında hangi algoritma tekrar çalışmalıdır?",
        "opts": [
            "DFS — en hızlısı olduğu için",
            "Seçili olan algoritma, yeni konumdan hedef için tekrar",
            "Her seferinde BFS",
            "Algoritma çalıştırmaya gerek yok",
        ],
        "ans": 1,
        "exp": "Engel konulduğunda mevcut yol geçersiz hale gelir. "
               "Pikachu'nun bulunduğu konum yeni başlangıç noktası olarak alınır "
               "ve seçili algoritma hedefe kadar yeniden hesaplanır.",
        "algo": "BFS",
    },
    {
        "q": "BFS'te tüm kenarlara eşit maliyet atandığında ne olur?",
        "opts": [
            "BFS yanlış sonuç verir",
            "BFS, Dijkstra ile eşdeğer optimal sonuç verir",
            "BFS daha yavaş çalışır",
            "BFS sonsuz döngüye girer",
        ],
        "ans": 1,
        "exp": "Tüm kenarlar eşit ağırlıklı olduğunda BFS en az kenar sayısı = "
               "en kısa mesafe olur. Bu durumda Dijkstra'nın priority queue avantajı "
               "ortadan kalkar ve ikisi aynı optimal yolu bulur.",
        "algo": "BFS",
    },
    {
        "q": "Hangi algoritma 'uninformed' (kör) arama algoritmasıdır?",
        "opts": [
            "Yalnızca A*",
            "Yalnızca Dijkstra",
            "BFS ve DFS",
            "Hiçbiri",
        ],
        "ans": 2,
        "exp": "BFS ve DFS 'uninformed' (bilgisiz/kör) aramalardır — hedefe ne kadar uzak "
               "olduğunu bilmezler. A* ve Greedy Search ise heuristik kullanan "
               "'informed' (bilgili) aramalardır.",
        "algo": "BFS",
    },
    {
        "q": "DFS'in rekürsif implementasyonunda ne riski vardır?",
        "opts": [
            "Çok fazla bellek kullanımı",
            "Yanlış sonuç verme",
            "Stack Overflow (çok derin rekürsyon)",
            "Sonsuz döngü garantisi",
        ],
        "ans": 2,
        "exp": "Python'da rekürsyon limiti ~1000'dir. Çok derin grafiklerde (1000+ düğüm) "
               "RecursionError alınır. Bu yüzden büyük grafiklerde iteratif "
               "(stack kullanarak) DFS tercih edilir.",
        "algo": "DFS",
    },
    {
        "q": "Dijkstra algoritmasının ziyaret ettiği düğümleri nasıl belirler?",
        "opts": [
            "Rastgele sırayla",
            "Alfabetik sırayla",
            "Başlangıçtan en düşük toplam maliyete göre",
            "Hedefe en yakın olana göre (heuristik)",
        ],
        "ans": 2,
        "exp": "Dijkstra'da her adımda priority queue'dan en düşük g(n) değeri "
               "(başlangıçtan toplam maliyet) olan düğüm seçilir. "
               "A*'dan farkı: hedefe olan tahmini mesafeyi (h) dikkate almaz.",
        "algo": "Dijkstra",
    },
    {
        "q": "Bu uygulamada BFS ziyaret ettiği hücreleri hangi renkte gösterir?",
        "opts": ["Yeşil", "Mor", "Mavi", "Sarı"],
        "ans": 2,
        "exp": "Uygulamada: BFS=Mavi (#3b82f6), DFS=Mor (#a855f7), Dijkstra=Yeşil (#22c55e). "
               "Bulunan yol ise her algoritmada altın sarısı (#fbbf24) ile gösterilir.",
        "algo": "BFS",
    },
    {
        "q": "Aşağıdaki grafta A'dan D'ye BFS sırası nedir?\n"
             "     A-B, A-C, B-D, C-D",
        "opts": ["A, B, D", "A, C, D", "A, B, C, D", "A, D"],
        "ans": 2,
        "exp": "BFS önce A'nın komşularını (B ve C) queue'ya ekler. "
               "Sonra B'yi işler (D'yi bulur ama queue'dan önce C var). "
               "C'yi işler, sonra D'yi işler. Sıra: A → B → C → D.",
        "algo": "BFS",
    },
    {
        "q": "Heuristiği h(n)=0 yaparsak A* hangi algoritmaya dönüşür?",
        "opts": ["BFS", "DFS", "Dijkstra", "Greedy Search"],
        "ans": 2,
        "exp": "A*'da f(n) = g(n) + h(n). h(n)=0 olunca f(n)=g(n) kalır. "
               "Bu tam olarak Dijkstra'nın yaptığıdır: sadece gerçek maliyete göre genişler. "
               "Yani Dijkstra, h=0 olan A*'ın özel halidir.",
        "algo": "Dijkstra",
    },
]
 
 
# ── Quiz motoru ────────────────────────────────────────────────────────────────
 
def banner():
    clear()
    print()
    print(f"  {YE}{B}╔══════════════════════════════════════════════════════╗{R}")
    print(f"  {YE}{B}║     ISTANBUL PATHFINDING — ALGORITMA QUIZ  ⚡         ║{R}")
    print(f"  {YE}{B}║     BFS  •  DFS  •  Dijkstra                         ║{R}")
    print(f"  {YE}{B}╚══════════════════════════════════════════════════════╝{R}")
    print()
 
 
def algo_badge(algo):
    colors = {"BFS": BL, "DFS": MA, "Dijkstra": GR}
    return f"{colors.get(algo,CY)}{B}[{algo}]{R}"
 
 
def show_question(idx, total, q_data, score):
    clear()
    banner()
    divider()
    print(f"  {GY}Soru {idx}/{total}   {YE}Puan: {score}{R}   {GY}{algo_badge(q_data['algo'])}{R}")
    divider()
    print()
 
    # Soru metni
    lines = textwrap.wrap(q_data["q"], width=56)
    for line in lines:
        print(f"  {WH}{B}{line}{R}")
    print()
 
    # Seçenekler
    for i, opt in enumerate(q_data["opts"]):
        letter = chr(65 + i)
        print(f"    {CY}{B}{letter}{R}  {opt}")
    print()
 
 
def get_answer(num_opts):
    valid = [chr(65+i) for i in range(num_opts)]
    while True:
        try:
            raw = input(f"  {YE}Cevabınız ({'/'.join(valid)}): {R}").strip().upper()
            if raw in valid:
                return ord(raw) - 65
            print(f"  {RE}Geçersiz! {'/'.join(valid)} harflerinden birini girin.{R}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {GY}Quiz iptal edildi.{R}\n")
            sys.exit(0)
 
 
def show_result(correct, q_data, chosen_idx):
    chosen  = q_data["opts"][chosen_idx]
    correct_opt = q_data["opts"][q_data["ans"]]
 
    print()
    if correct:
        print(f"  {GR}{B}✓  Doğru!{R}")
    else:
        print(f"  {RE}{B}✗  Yanlış!{R}  Doğru cevap: {GR}{B}{chr(65+q_data['ans'])} — {correct_opt}{R}")
 
    print()
    print(f"  {GY}Açıklama:{R}")
    exp_lines = textwrap.wrap(q_data["exp"], width=56)
    for line in exp_lines:
        print(f"  {GY}{line}{R}")
    print()
    input(f"  {GY}Devam etmek için Enter...{R}")
 
 
def final_screen(score, total, wrong_algos, time_taken):
    clear()
    banner()
 
    pct = score / total * 100
    if pct == 100:
        grade, color, emoji = "MÜKEMMEL", GR, "⚡"
    elif pct >= 80:
        grade, color, emoji = "HARİKA",   GR, "🌟"
    elif pct >= 60:
        grade, color, emoji = "İYİ",      YE, "👍"
    elif pct >= 40:
        grade, color, emoji = "ORTA",     YE, "📚"
    else:
        grade, color, emoji = "ÇALIŞMALI",RE, "💪"
 
    print(f"  {color}{B}{'─'*54}{R}")
    print(f"  {color}{B}  {emoji}  {grade}  {emoji}{R}")
    print(f"  {color}{B}{'─'*54}{R}")
    print()
    print(f"  {WH}Puan:     {color}{B}{score}/{total}{R}  {GY}({pct:.0f}%){R}")
 
    m = int(time_taken // 60)
    s = int(time_taken % 60)
    print(f"  {WH}Süre:     {GY}{m}:{s:02d}{R}")
    print()
 
    # Algo bazlı performans
    divider("─", 54)
    print(f"  {CY}{B}Algoritma Bazlı Performans:{R}")
    print()
    for algo, col in [("BFS", BL), ("DFS", MA), ("Dijkstra", GR)]:
        total_q = wrong_algos.get(algo, {}).get("total", 0)
        wrong_q = wrong_algos.get(algo, {}).get("wrong", 0)
        if total_q == 0:
            continue
        correct_q = total_q - wrong_q
        bar = "█" * correct_q + "░" * wrong_q
        print(f"  {col}{B}{algo:<10}{R} {bar}  {GR}{correct_q}/{total_q}{R}")
 
    print()
    if wrong_algos:
        print(f"  {YE}Eksik Konular:{R}")
        for algo, data in wrong_algos.items():
            if data["wrong"] > 0:
                print(f"    {GY}• {algo} konusunu tekrar gözden geçir{R}")
    print()
    divider()
    print()
 
 
def run_quiz(num_questions=10, shuffle=True):
    banner()
    print(f"  {WH}Toplam {len(QUESTIONS)} sorudan {num_questions} tanesi sorulacak.{R}")
    print(f"  {GY}Her sorudan sonra açıklama gösterilir.{R}")
    print()
    input(f"  {YE}Başlamak için Enter...{R}")
 
    questions = QUESTIONS.copy()
    if shuffle:
        random.shuffle(questions)
    questions = questions[:num_questions]
 
    score = 0
    wrong_algos = {a: {"total":0,"wrong":0} for a in ["BFS","DFS","Dijkstra"]}
    start_time  = time.time()
 
    for idx, q_data in enumerate(questions, 1):
        show_question(idx, num_questions, q_data, score)
        chosen = get_answer(len(q_data["opts"]))
        correct = (chosen == q_data["ans"])
 
        algo = q_data["algo"]
        wrong_algos[algo]["total"] += 1
        if correct:
            score += 1
        else:
            wrong_algos[algo]["wrong"] += 1
 
        show_result(correct, q_data, chosen)
 
    elapsed = time.time() - start_time
    final_screen(score, num_questions, wrong_algos, elapsed)
    return score
 
 
def main_menu():
    while True:
        banner()
        divider()
        print(f"  {CY}{B}1{R}  Kısa Quiz  (10 soru)")
        print(f"  {CY}{B}2{R}  Tam Quiz   (20 soru - tüm sorular)")
        print(f"  {CY}{B}3{R}  Sadece BFS soruları")
        print(f"  {CY}{B}4{R}  Sadece DFS soruları")
        print(f"  {CY}{B}5{R}  Sadece Dijkstra soruları")
        print(f"  {CY}{B}6{R}  Çıkış")
        divider()
        print()
 
        try:
            choice = input(f"  {YE}Seçiminiz (1-6): {R}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {GY}Görüşürüz!{R}\n")
            break
 
        if choice == "1":
            run_quiz(10)
        elif choice == "2":
            run_quiz(20, shuffle=False)
        elif choice in ("3","4","5"):
            algo_map = {"3":"BFS","4":"DFS","5":"Dijkstra"}
            target = algo_map[choice]
            filtered = [q for q in QUESTIONS if q["algo"] == target]
            if not filtered:
                print(f"  {RE}Bu algo için soru bulunamadı.{R}"); time.sleep(1); continue
            random.shuffle(filtered)
            # Quiz motorunu filtered sorularla çalıştır
            score = 0
            wrong_algos = {target: {"total":0,"wrong":0}}
            start_time  = time.time()
            for idx, q_data in enumerate(filtered, 1):
                show_question(idx, len(filtered), q_data, score)
                chosen  = get_answer(len(q_data["opts"]))
                correct = (chosen == q_data["ans"])
                wrong_algos[target]["total"] += 1
                if correct: score += 1
                else:        wrong_algos[target]["wrong"] += 1
                show_result(correct, q_data, chosen)
            final_screen(score, len(filtered), wrong_algos, time.time()-start_time)
        elif choice == "6":
            print(f"\n  {GY}Görüşürüz! ⚡{R}\n")
            break
        else:
            print(f"  {RE}1-6 arasında bir sayı girin.{R}")
            time.sleep(1)
 
 
if __name__ == "__main__":
    main_menu()
 