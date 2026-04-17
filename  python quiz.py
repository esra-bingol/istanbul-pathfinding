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
        "q": "Which data structure does BFS use?",
        "opts": ["Stack", "Queue", "Priority Queue", "Linked List"],
        "ans": 1,
        "exp": "BFS uses a Queue that works with FIFO (first in, first out) logic. "
               "This way it explores nodes at each level in order.",
        "algo": "BFS",
    },
    {
        "q": "Which algorithm guarantees the shortest path in an unweighted graph?",
        "opts": ["DFS", "Only Dijkstra", "BFS and Dijkstra", "Neither"],
        "ans": 2,
        "exp": "In an unweighted graph, BFS always finds the path with the fewest edges. "
               "Dijkstra also works correctly because all weights are considered equal (1).",
        "algo": "BFS",
    },
    {
        "q": "What is the time complexity of DFS?",
        "opts": ["O(V²)", "O(E log V)", "O(V + E)", "O(V × E)"],
        "ans": 2,
        "exp": "DFS visits each node (V) and each edge (E) at most once. "
               "Therefore the time complexity is O(V + E).",
        "algo": "DFS",
    },
    {
        "q": "Why doesn't Dijkstra's algorithm work with negative weight edges?",
        "opts": [
            "Because it is too slow",
            "It enters an infinite loop with negative cycles",
            "Only integer weights are supported",
            "Priority queue cannot sort negative values",
        ],
        "ans": 1,
        "exp": "Dijkstra finalizes the distance to a node when it reaches it. "
               "Negative edges break this assumption; a shorter path to an already-finalized "
               "node can be found via a negative edge, causing an infinite loop.",
        "algo": "Dijkstra",
    },
    {
        "q": "How does the A* algorithm differ from Dijkstra?",
        "opts": [
            "A* ignores weights",
            "A* uses a heuristic function",
            "A* always visits fewer nodes",
            "A* only works on grid graphs",
        ],
        "ans": 1,
        "exp": "A* adds a goal estimate (heuristic) to Dijkstra: f(n) = g(n) + h(n). "
               "g(n) is the actual cost, h(n) is the estimated remaining cost. "
               "With a good heuristic it explores far fewer nodes.",
        "algo": "Dijkstra",
    },
    {
        "q": "Why is BFS memory complexity O(V)?",
        "opts": [
            "It stores the entire graph in memory",
            "In the worst case it adds all nodes to the queue",
            "It uses separate memory for each edge",
            "Recursive calls create stack overflow",
        ],
        "ans": 1,
        "exp": "BFS can add all nodes to the queue in the worst case (if the goal is on "
               "the last level). In wide graphs this consumes a lot of memory. "
               "DFS only stores the active branch and uses less memory.",
        "algo": "BFS",
    },
    {
        "q": "Which of the following is a FALSE statement about DFS?",
        "opts": [
            "Uses a Stack data structure",
            "Finds the optimal path in an unweighted graph",
            "Can be written recursively",
            "Has O(V+E) time complexity",
        ],
        "ans": 1,
        "exp": "DFS is not optimal! It returns the first path it finds to the goal, "
               "but this may not be the shortest. It can find a very long path in mazes "
               "while BFS or Dijkstra finds a shorter one.",
        "algo": "DFS",
    },
    {
        "q": "Which algorithm is most suitable for city navigation (Google Maps)?",
        "opts": ["BFS", "DFS", "Dijkstra / A*", "All give the same performance"],
        "ans": 2,
        "exp": "City maps are weighted graphs (different road lengths). "
               "BFS ignores weights, DFS is not optimal. "
               "Google Maps uses a combination of A* and Dijkstra.",
        "algo": "Dijkstra",
    },
    {
        "q": "How many steps does BFS need to reach all cells in a 5×5 grid from the start? "
             "(No obstacles, 4-directional movement)",
        "opts": ["4 steps", "8 steps", "16 steps", "24 steps"],
        "ans": 1,
        "exp": "In a 5×5 grid, the farthest corner (4,4) has Manhattan distance 4+4=8. "
               "Since BFS expands layer by layer, it reaches all cells in 8 steps. "
               "All 25 cells are explored.",
        "algo": "BFS",
    },
    {
        "q": "Which data structure makes Dijkstra most efficient?",
        "opts": ["Array", "Linked List", "Min-Heap (Priority Queue)", "Hash Table"],
        "ans": 2,
        "exp": "In Dijkstra, at each step the node with the lowest cost must be found. "
               "Min-Heap does this in O(log V). "
               "With an Array it becomes O(V²) — very slow for large graphs.",
        "algo": "Dijkstra",
    },
    {
        "q": "In which situation is DFS more advantageous than BFS?",
        "opts": [
            "When looking for the shortest path",
            "When the graph is very wide (high branching factor)",
            "When checking if a path exists",
            "When there are negative weights",
        ],
        "ans": 1,
        "exp": "In very wide (high branching factor) graphs, BFS's queue explodes. "
               "DFS is advantageous because it only keeps the active branch in memory. "
               "For example, DFS is more applicable in a chess game tree.",
        "algo": "DFS",
    },
    {
        "q": "What is the Manhattan heuristic and why is it used in A*?",
        "opts": [
            "It is the Euclidean distance calculation",
            "h(n) = |x1-x2| + |y1-y2| — optimal estimate for grid movement",
            "It is the average of the weights",
            "It is a special version of Dijkstra",
        ],
        "ans": 1,
        "exp": "Manhattan distance is the number of horizontal + vertical moves. "
               "Since it never exceeds the actual distance in 4-directional grid movement, "
               "it is an 'admissible' heuristic. This keeps A* optimal.",
        "algo": "Dijkstra",
    },
    {
        "q": "When Pikachu hits an obstacle, which algorithm should run again?",
        "opts": [
            "DFS — because it is the fastest",
            "The selected algorithm, recalculated from the new position to the goal",
            "Always BFS",
            "No need to run any algorithm",
        ],
        "ans": 1,
        "exp": "When an obstacle is placed, the current path becomes invalid. "
               "Pikachu's current position is taken as the new starting point "
               "and the selected algorithm recalculates the path to the goal.",
        "algo": "BFS",
    },
    {
        "q": "What happens when all edges in BFS are assigned equal cost?",
        "opts": [
            "BFS gives wrong results",
            "BFS gives equivalent optimal results to Dijkstra",
            "BFS runs slower",
            "BFS enters an infinite loop",
        ],
        "ans": 1,
        "exp": "When all edges have equal weight, fewest edges = shortest distance for BFS. "
               "In this case Dijkstra's priority queue advantage disappears "
               "and both find the same optimal path.",
        "algo": "BFS",
    },
    {
        "q": "Which algorithm is an 'uninformed' (blind) search algorithm?",
        "opts": [
            "Only A*",
            "Only Dijkstra",
            "BFS and DFS",
            "None",
        ],
        "ans": 2,
        "exp": "BFS and DFS are 'uninformed' (blind) searches — they don't know how far "
               "they are from the goal. A* and Greedy Search are 'informed' searches "
               "that use heuristics.",
        "algo": "BFS",
    },
    {
        "q": "What is the risk in the recursive implementation of DFS?",
        "opts": [
            "Excessive memory usage",
            "Giving wrong results",
            "Stack Overflow (too deep recursion)",
            "Guaranteed infinite loop",
        ],
        "ans": 2,
        "exp": "Python's recursion limit is ~1000. In very deep graphs (1000+ nodes) "
               "a RecursionError occurs. That's why iterative DFS "
               "(using an explicit stack) is preferred for large graphs.",
        "algo": "DFS",
    },
    {
        "q": "How does Dijkstra's algorithm determine which nodes to visit?",
        "opts": [
            "In random order",
            "In alphabetical order",
            "By lowest total cost from the start",
            "By closest to the goal (heuristic)",
        ],
        "ans": 2,
        "exp": "In Dijkstra, at each step the node with the lowest g(n) value "
               "(total cost from start) is selected from the priority queue. "
               "Unlike A*, it does not consider the estimated distance to the goal (h).",
        "algo": "Dijkstra",
    },
    {
        "q": "In this application, what color does BFS use to show visited cells?",
        "opts": ["Green", "Purple", "Blue", "Yellow"],
        "ans": 2,
        "exp": "In the app: BFS=Blue (#3b82f6), DFS=Purple (#a855f7), Dijkstra=Green (#22c55e). "
               "The found path is shown in golden yellow (#fbbf24) for all algorithms.",
        "algo": "BFS",
    },
    {
        "q": "What is the BFS traversal order from A to D in the following graph?\n"
             "     A-B, A-C, B-D, C-D",
        "opts": ["A, B, D", "A, C, D", "A, B, C, D", "A, D"],
        "ans": 2,
        "exp": "BFS first adds A's neighbors (B and C) to the queue. "
               "Then processes B (finds D but C is ahead in the queue). "
               "Processes C, then processes D. Order: A → B → C → D.",
        "algo": "BFS",
    },
    {
        "q": "If we set the heuristic h(n)=0, which algorithm does A* become?",
        "opts": ["BFS", "DFS", "Dijkstra", "Greedy Search"],
        "ans": 2,
        "exp": "In A*, f(n) = g(n) + h(n). When h(n)=0, f(n)=g(n) remains. "
               "This is exactly what Dijkstra does: it expands only based on actual cost. "
               "So Dijkstra is a special case of A* with h=0.",
        "algo": "Dijkstra",
    },
]
 
 
# ── Quiz motoru ────────────────────────────────────────────────────────────────
 
def banner():
    clear()
    print()
    print(f"  {YE}{B}╔══════════════════════════════════════════════════════╗{R}")
    print(f"  {YE}{B}║     ISTANBUL PATHFINDING — ALGORITHM QUIZ  ⚡         ║{R}")
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
    print(f"  {GY}Question {idx}/{total}   {YE}Score: {score}{R}   {GY}{algo_badge(q_data['algo'])}{R}")
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
            raw = input(f"  {YE}Your answer ({'/'.join(valid)}): {R}").strip().upper()
            if raw in valid:
                return ord(raw) - 65
            print(f"  {RE}Invalid! Enter one of the letters: {'/'.join(valid)}.{R}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {GY}Quiz cancelled.{R}\n")
            sys.exit(0)
 
 
def show_result(correct, q_data, chosen_idx):
    chosen  = q_data["opts"][chosen_idx]
    correct_opt = q_data["opts"][q_data["ans"]]
 
    print()
    if correct:
        print(f"  {GR}{B}✓  Correct!{R}")
    else:
        print(f"  {RE}{B}✗  Wrong!{R}  Correct answer: {GR}{B}{chr(65+q_data['ans'])} — {correct_opt}{R}")

    print()
    print(f"  {GY}Explanation:{R}")
    exp_lines = textwrap.wrap(q_data["exp"], width=56)
    for line in exp_lines:
        print(f"  {GY}{line}{R}")
    print()
    input(f"  {GY}Press Enter to continue...{R}")
 
 
def final_screen(score, total, wrong_algos, time_taken):
    clear()
    banner()
 
    pct = score / total * 100
    if pct == 100:
        grade, color, emoji = "PERFECT",       GR, "⚡"
    elif pct >= 80:
        grade, color, emoji = "EXCELLENT",     GR, "🌟"
    elif pct >= 60:
        grade, color, emoji = "GOOD",          YE, "👍"
    elif pct >= 40:
        grade, color, emoji = "AVERAGE",       YE, "📚"
    else:
        grade, color, emoji = "NEEDS WORK",    RE, "💪"
 
    print(f"  {color}{B}{'─'*54}{R}")
    print(f"  {color}{B}  {emoji}  {grade}  {emoji}{R}")
    print(f"  {color}{B}{'─'*54}{R}")
    print()
    print(f"  {WH}Score:    {color}{B}{score}/{total}{R}  {GY}({pct:.0f}%){R}")

    m = int(time_taken // 60)
    s = int(time_taken % 60)
    print(f"  {WH}Time:     {GY}{m}:{s:02d}{R}")
    print()

    divider("─", 54)
    print(f"  {CY}{B}Performance by Algorithm:{R}")
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
        print(f"  {YE}Weak Topics:{R}")
        for algo, data in wrong_algos.items():
            if data["wrong"] > 0:
                print(f"    {GY}• Review {algo} again{R}")
    print()
    divider()
    print()
 
 
def run_quiz(num_questions=10, shuffle=True):
    banner()
    print(f"  {WH}{num_questions} of {len(QUESTIONS)} questions will be asked.{R}")
    print(f"  {GY}An explanation will be shown after each question.{R}")
    print()
    input(f"  {YE}Press Enter to start...{R}")
 
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
        print(f"  {CY}{B}1{R}  Short Quiz  (10 questions)")
        print(f"  {CY}{B}2{R}  Full Quiz   (20 questions - all)")
        print(f"  {CY}{B}3{R}  BFS questions only")
        print(f"  {CY}{B}4{R}  DFS questions only")
        print(f"  {CY}{B}5{R}  Dijkstra questions only")
        print(f"  {CY}{B}6{R}  Exit")
        divider()
        print()
 
        try:
            choice = input(f"  {YE}Your choice (1-6): {R}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {GY}Goodbye!{R}\n")
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
                print(f"  {RE}No questions found for this algorithm.{R}"); time.sleep(1); continue
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
            print(f"\n  {GY}Goodbye! ⚡{R}\n")
            break
        else:
            print(f"  {RE}Enter a number between 1-6.{R}")
            time.sleep(1)
 
 
if __name__ == "__main__":
    main_menu()
 