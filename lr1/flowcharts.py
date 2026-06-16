import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ── Цвета ──────────────────────────────────────────────────
C_TERM   = "#2c3e50"   # терминатор (начало/конец)
C_PROC   = "#2980b9"   # процесс
C_DEC    = "#e67e22"   # решение
C_IO     = "#27ae60"   # ввод/вывод
C_WHITE  = "white"
C_ARROW  = "#555555"
FONT     = "DejaVu Sans"

# ═══════════════════════════════════════════════════════════
#  Вспомогательные функции рисования
# ═══════════════════════════════════════════════════════════

def add_box(ax, x, y, w, h, text, color, fontsize=9, text_color="white", style="round,pad=0.1"):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle=style, linewidth=1.2,
                         edgecolor="white", facecolor=color, zorder=3)
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, color=text_color,
            fontfamily=FONT, zorder=4,
            wrap=True, multialignment="center")

def add_diamond(ax, x, y, w, h, text, fontsize=8.5):
    # рисуем ромб через четыре точки
    xs = [x,       x + w/2, x,       x - w/2, x]
    ys = [y + h/2, y,       y - h/2, y,       y + h/2]
    ax.fill(xs, ys, color=C_DEC, zorder=3)
    ax.plot(xs, ys, color="white", lw=1.2, zorder=4)
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, color="white",
            fontfamily=FONT, zorder=5, multialignment="center")

def arrow(ax, x1, y1, x2, y2, label="", label_side="right"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=C_ARROW,
                                lw=1.4, mutation_scale=14), zorder=2)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        dx = 0.13 if label_side == "right" else -0.13
        ax.text(mx + dx, my, label, fontsize=7.5, color="#333",
                fontfamily=FONT, ha="left" if label_side == "right" else "right",
                va="center", zorder=5)

def hline(ax, x1, y, x2):
    ax.plot([x1, x2], [y, y], color=C_ARROW, lw=1.4, zorder=2)

def vline(ax, x, y1, y2):
    ax.plot([x, x], [y1, y2], color=C_ARROW, lw=1.4, zorder=2)


# ═══════════════════════════════════════════════════════════
#  1. main()
# ═══════════════════════════════════════════════════════════
def draw_main():
    fig, ax = plt.subplots(figsize=(6, 14))
    ax.set_xlim(0, 6); ax.set_ylim(0, 14)
    ax.axis("off")
    ax.set_facecolor("#f4f6f8"); fig.patch.set_facecolor("#f4f6f8")
    ax.set_title("main()", fontsize=13, fontweight="bold",
                 fontfamily=FONT, pad=10)

    W, H = 3.6, 0.55

    # узлы (x, y, текст, цвет)
    nodes = [
        (3, 13.2, "НАЧАЛО",                        C_TERM),
        (3, 12.3, "show_menu()\nВыбор структуры",   C_IO),
        (3, 11.3, "static_init(), dynamic_init(),\nvector_init()",  C_PROC),
        (3, 10.3, "read_file(INPUT_FILE, mode, ...)\nЧтение чисел из файла", C_IO),
        (3,  9.3, "n <= 0?",                        C_DEC),   # ромб
        (3,  8.3, "get_array_ptr()\nПолучить указатель на массив", C_PROC),
        (3,  7.3, "print_array()\nВывод исходного массива",        C_IO),
        (3,  6.3, "radix_sort(arr, sz)\nСортировка",               C_PROC),
        (3,  5.3, "print_array()\nВывод отсортированного массива", C_IO),
        (3,  4.3, "find_max() + вычисление d\nОценка сложности",   C_PROC),
        (3,  3.3, "Вывод O(d*(n+k)), O(n+k)",                      C_IO),
        (3,  2.3, "cleanup()\nОсвобождение памяти",                C_PROC),
        (3,  1.3, "КОНЕЦ",                                         C_TERM),
    ]

    diamond_idx = 4  # индекс ромба

    for i, (x, y, txt, col) in enumerate(nodes):
        if i == diamond_idx:
            add_diamond(ax, x, y, W + 0.4, 0.65, txt)
        else:
            add_box(ax, x, y, W, H, txt, col)

    # стрелки вниз между последовательными блоками
    seq = [0,1,2,3,4]   # до ромба
    for i in range(len(seq)-1):
        yi = nodes[seq[i]][1] - H/2
        yn = nodes[seq[i+1]][1] + H/2 if seq[i+1] != diamond_idx else nodes[seq[i+1]][1] + 0.325
        arrow(ax, 3, yi, 3, yn)

    # после ромба: нет → вниз
    arrow(ax, 3, nodes[4][1] - 0.325, 3, nodes[5][1] + H/2, "Нет")
    for i in range(5, len(nodes)-1):
        yi = nodes[i][1] - H/2
        yn = nodes[i+1][1] + H/2
        arrow(ax, 3, yi, 3, yn)

    # ромб: да → вправо → вниз к КОНЕЦ
    ax.text(4.1, 9.3, "Да", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3 + (W+0.4)/2, 9.3, 5.3)
    vline(ax, 5.3, 9.3, 1.3)
    arrow(ax, 5.3, 1.3, 3 + W/2, 1.3)

    plt.tight_layout()
    plt.savefig("flowchart_1_main.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: flowchart_1_main.png")


# ═══════════════════════════════════════════════════════════
#  2. read_file()
# ═══════════════════════════════════════════════════════════
def draw_read_file():
    fig, ax = plt.subplots(figsize=(7, 15))
    ax.set_xlim(0, 7); ax.set_ylim(0, 15)
    ax.axis("off")
    ax.set_facecolor("#f4f6f8"); fig.patch.set_facecolor("#f4f6f8")
    ax.set_title("read_file()", fontsize=13, fontweight="bold",
                 fontfamily=FONT, pad=10)

    W, H = 4.0, 0.55

    # Последовательные блоки
    blocks = [
        (3.5, 14.2, "НАЧАЛО",                                     C_TERM),
        (3.5, 13.2, "fopen(filename, \"r\")",                     C_IO),
        (3.5, 12.2, "fp == NULL?",                                 C_DEC),
        (3.5, 11.1, "n = 0",                                       C_PROC),
        (3.5, 10.1, "fscanf(fp) == 1?",                            C_DEC),  # цикл 1
        (3.5,  9.1, "n++",                                         C_PROC),
        (3.5,  8.1, "n == 0?",                                     C_DEC),
        (3.5,  7.1, "rewind(fp)  /  i = 0",                       C_PROC),
        (3.5,  6.1, "i < n?",                                      C_DEC),  # цикл 2
        (3.5,  5.1, "fscanf(fp, val)",                             C_IO),
        (3.5,  4.1, "mode == 1?",                                  C_DEC),
        (3.5,  3.1, "static/dynamic/vector push(val)",             C_PROC),
        (3.5,  2.1, "i++",                                         C_PROC),
        (3.5,  1.2, "fclose(fp) → return n",                       C_IO),
        (3.5,  0.4, "КОНЕЦ",                                       C_TERM),
    ]

    diamond_idx = {2, 4, 6, 8, 10}

    for i, (x, y, txt, col) in enumerate(blocks):
        if i in diamond_idx:
            add_diamond(ax, x, y, W + 0.6, 0.65, txt)
        else:
            add_box(ax, x, y, W, H, txt, col)

    def top(i):
        return blocks[i][1] + (0.325 if i in diamond_idx else H/2)
    def bot(i):
        return blocks[i][1] - (0.325 if i in diamond_idx else H/2)

    # прямые стрелки вниз
    straight = [(0,1),(1,2),(3,4),(5,4),(7,8),(9,10),(11,12),(12,13),(13,14)]
    for a_i, b_i in straight:
        arrow(ax, 3.5, bot(a_i), 3.5, top(b_i))

    # ромб 2 (fp==NULL): Нет → следующий, Да → return -1 справа
    arrow(ax, 3.5, bot(2), 3.5, top(3), "Нет")
    ax.text(5.55, 12.2, "Да", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3.5 + (W+0.6)/2, 12.2, 6.3)
    ax.text(6.3, 11.5, "return -1", fontsize=8, color=C_IO,
            fontfamily=FONT, ha="center", va="top",
            bbox=dict(boxstyle="round,pad=0.2", facecolor=C_IO, edgecolor="white", alpha=0.85))
    vline(ax, 6.3, 12.2, 11.2)

    # ромб 4 (fscanf цикл 1): Да → n++, Нет → дальше
    arrow(ax, 3.5, bot(4), 3.5, top(5), "Да")
    # Нет — выход из цикла 1
    ax.text(1.3, 10.1, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3.5 - (W+0.6)/2, 10.1, 0.9)
    vline(ax, 0.9, 10.1, 8.1)
    arrow(ax, 0.9, 8.1, 3.5 - (W+0.6)/2, 8.1)

    # n++ → обратно вверх к fscanf (петля)
    hline(ax, 3.5 + W/2, 9.1, 6.5)
    vline(ax, 6.5, 9.1, 10.1)
    arrow(ax, 6.5, 10.1, 3.5 + (W+0.6)/2, 10.1)

    # ромб 6 (n==0): Нет → rewind, Да → return -1
    arrow(ax, 3.5, bot(6), 3.5, top(7), "Нет")
    ax.text(5.55, 8.1, "Да", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3.5 + (W+0.6)/2, 8.1, 6.3)
    ax.text(6.3, 7.4, "return -1", fontsize=8, color=C_IO,
            fontfamily=FONT, ha="center", va="top",
            bbox=dict(boxstyle="round,pad=0.2", facecolor=C_IO, edgecolor="white", alpha=0.85))
    vline(ax, 6.3, 8.1, 7.0)

    # ромб 8 (i<n цикл 2): Да → fscanf, Нет → fclose
    arrow(ax, 3.5, bot(8), 3.5, top(9), "Да")
    ax.text(1.3, 6.1, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3.5 - (W+0.6)/2, 6.1, 0.7)
    vline(ax, 0.7, 6.1, 1.2)
    arrow(ax, 0.7, 1.2, 3.5 - W/2, 1.2)

    # ромб 10 (mode): Да → push, Нет тоже → push (упрощаем — mode выбирает вариант)
    arrow(ax, 3.5, bot(10), 3.5, top(11), "mode\nветка")

    # i++ → обратно к i<n
    hline(ax, 3.5 + W/2, 2.1, 6.2)
    vline(ax, 6.2, 2.1, 6.1)
    arrow(ax, 6.2, 6.1, 3.5 + (W+0.6)/2, 6.1)

    plt.tight_layout()
    plt.savefig("flowchart_2_read_file.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: flowchart_2_read_file.png")


# ═══════════════════════════════════════════════════════════
#  3. radix_sort() + find_max()
# ═══════════════════════════════════════════════════════════
def draw_radix_sort():
    fig, ax = plt.subplots(figsize=(6, 13))
    ax.set_xlim(0, 6); ax.set_ylim(0, 13)
    ax.axis("off")
    ax.set_facecolor("#f4f6f8"); fig.patch.set_facecolor("#f4f6f8")
    ax.set_title("radix_sort()  +  find_max()", fontsize=13,
                 fontweight="bold", fontfamily=FONT, pad=10)

    W, H = 3.8, 0.58

    blocks = [
        (3, 12.3, "НАЧАЛО",                                       C_TERM),
        (3, 11.4, "n <= 1?",                                       C_DEC),
        # find_max subgraph
        (3, 10.3, "max = arr[0]  /  i = 1",                       C_PROC),
        (3,  9.3, "i < n?",                                        C_DEC),
        (3,  8.3, "arr[i] > max?",                                 C_DEC),
        (3,  7.5, "max = arr[i]",                                  C_PROC),
        (3,  6.5, "i++",                                           C_PROC),
        # radix loop
        (3,  5.5, "exp = 1",                                       C_PROC),
        (3,  4.5, "max_val / exp > 0?",                            C_DEC),
        (3,  3.5, "counting_sort_by_digit(arr, n, exp)",           C_PROC),
        (3,  2.5, "exp *= 10",                                     C_PROC),
        (3,  1.5, "КОНЕЦ",                                         C_TERM),
    ]

    diamond_idx = {1, 3, 4, 8}

    for i, (x, y, txt, col) in enumerate(blocks):
        if i in diamond_idx:
            add_diamond(ax, x, y, W + 0.4, 0.65, txt)
        else:
            add_box(ax, x, y, W, H, txt, col)

    def top(i): return blocks[i][1] + (0.325 if i in diamond_idx else H/2)
    def bot(i): return blocks[i][1] - (0.325 if i in diamond_idx else H/2)

    # 0→1
    arrow(ax, 3, bot(0), 3, top(1))
    # 1 Нет → 2
    arrow(ax, 3, bot(1), 3, top(2), "Нет")
    # 1 Да → КОНЕЦ (справа)
    ax.text(4.55, 11.4, "Да", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3 + (W+0.4)/2, 11.4, 5.3)
    vline(ax, 5.3, 11.4, 1.5)
    arrow(ax, 5.3, 1.5, 3 + W/2, 1.5)

    # 2→3
    arrow(ax, 3, bot(2), 3, top(3))
    # 3 Да → 4
    arrow(ax, 3, bot(3), 3, top(4), "Да")
    # 3 Нет → 7 (exp=1)
    ax.text(1.2, 9.3, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3 - (W+0.4)/2, 9.3, 0.7)
    vline(ax, 0.7, 9.3, 5.5)
    arrow(ax, 0.7, 5.5, 3 - W/2, 5.5)

    # 4 Нет → i++ (пропускаем обновление max)
    arrow(ax, 3, bot(4), 3, top(6), "Нет")   # 4→6
    # 4 Да → 5
    ax.text(4.45, 8.3, "Да", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3 + (W+0.4)/2, 8.3, 4.8)
    vline(ax, 4.8, 8.3, 7.5)
    arrow(ax, 4.8, 7.5, 3 + W/2, 7.5)   # → max=arr[i]
    arrow(ax, 3, bot(5), 3, top(6))     # 5→6

    # 6→3 (петля i++)
    hline(ax, 3 + W/2, 6.5, 5.5)
    vline(ax, 5.5, 6.5, 9.3)
    arrow(ax, 5.5, 9.3, 3 + (W+0.4)/2, 9.3)

    # 7→8
    arrow(ax, 3, bot(7), 3, top(8))
    # 8 Да → 9
    arrow(ax, 3, bot(8), 3, top(9), "Да")
    # 8 Нет → КОНЕЦ
    ax.text(1.2, 4.5, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3 - (W+0.4)/2, 4.5, 0.5)
    vline(ax, 0.5, 4.5, 1.5)
    arrow(ax, 0.5, 1.5, 3 - W/2, 1.5)

    # 9→10
    arrow(ax, 3, bot(9), 3, top(10))
    # 10→8 (петля)
    hline(ax, 3 + W/2, 2.5, 5.4)
    vline(ax, 5.4, 2.5, 4.5)
    arrow(ax, 5.4, 4.5, 3 + (W+0.4)/2, 4.5)

    plt.tight_layout()
    plt.savefig("flowchart_3_radix_sort.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: flowchart_3_radix_sort.png")


# ═══════════════════════════════════════════════════════════
#  4. counting_sort_by_digit()
# ═══════════════════════════════════════════════════════════
def draw_counting_sort():
    fig, ax = plt.subplots(figsize=(6, 16))
    ax.set_xlim(0, 6); ax.set_ylim(0, 16)
    ax.axis("off")
    ax.set_facecolor("#f4f6f8"); fig.patch.set_facecolor("#f4f6f8")
    ax.set_title("counting_sort_by_digit()", fontsize=13,
                 fontweight="bold", fontfamily=FONT, pad=10)

    W, H = 4.0, 0.58

    blocks = [
        (3, 15.3, "НАЧАЛО",                                           C_TERM),
        (3, 14.4, "malloc(output, n)",                                 C_PROC),
        # шаг 1
        (3, 13.4, "Шаг 1: i=0, count[i]=0\n(k=10 итераций)",         C_PROC),
        # шаг 2
        (3, 12.3, "Шаг 2: i=0",                                       C_PROC),
        (3, 11.3, "i < n?",                                            C_DEC),
        (3, 10.4, "digit=(arr[i]/exp)%10\ncount[digit]++  /  i++",    C_PROC),
        # шаг 3
        (3,  9.4, "Шаг 3: i=1",                                       C_PROC),
        (3,  8.4, "i < 10?",                                           C_DEC),
        (3,  7.5, "count[i] += count[i-1]\ni++",                      C_PROC),
        # шаг 4
        (3,  6.5, "Шаг 4: i = n-1",                                   C_PROC),
        (3,  5.5, "i >= 0?",                                           C_DEC),
        (3,  4.5, "digit=(arr[i]/exp)%10\noutput[count[digit]-1]=arr[i]\ncount[digit]--  /  i--", C_PROC),
        # шаг 5
        (3,  3.4, "Шаг 5: i=0",                                       C_PROC),
        (3,  2.4, "i < n?",                                            C_DEC),
        (3,  1.5, "arr[i]=output[i]  /  i++",                         C_PROC),
        (3,  0.5, "free(output)",                                      C_PROC),
    ]

    # добавим КОНЕЦ отдельно ниже, но места нет — уберём его в подпись
    diamond_idx = {4, 7, 10, 13}

    for i, (x, y, txt, col) in enumerate(blocks):
        if i in diamond_idx:
            add_diamond(ax, x, y, W + 0.4, 0.68, txt)
        else:
            add_box(ax, x, y, W, H, txt, col)

    def top(i): return blocks[i][1] + (0.34 if i in diamond_idx else H/2)
    def bot(i): return blocks[i][1] - (0.34 if i in diamond_idx else H/2)

    straight = [(0,1),(1,2),(2,3),(3,4),(6,7),(9,10),(12,13),(14,15)]
    for a_i, b_i in straight:
        arrow(ax, 3, bot(a_i), 3, top(b_i))

    # цикл шаг 2: i<n Да→10, 10→петля, Нет→шаг3
    arrow(ax, 3, bot(4), 3, top(5), "Да")
    hline(ax, 3+W/2, 10.4, 5.5); vline(ax, 5.5, 10.4, 11.3)
    arrow(ax, 5.5, 11.3, 3+(W+0.4)/2, 11.3)
    ax.text(1.2, 11.3, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3-(W+0.4)/2, 11.3, 0.7); vline(ax, 0.7, 11.3, 9.4)
    arrow(ax, 0.7, 9.4, 3-W/2, 9.4)

    # цикл шаг 3: i<10 Да→7 Нет→шаг4
    arrow(ax, 3, bot(7), 3, top(8), "Да")
    hline(ax, 3+W/2, 7.5, 5.5); vline(ax, 5.5, 7.5, 8.4)
    arrow(ax, 5.5, 8.4, 3+(W+0.4)/2, 8.4)
    ax.text(1.2, 8.4, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3-(W+0.4)/2, 8.4, 0.7); vline(ax, 0.7, 8.4, 6.5)
    arrow(ax, 0.7, 6.5, 3-W/2, 6.5)

    # цикл шаг 4: i>=0 Да→11 Нет→шаг5
    arrow(ax, 3, bot(10), 3, top(11), "Да")
    hline(ax, 3+W/2, 4.5, 5.5); vline(ax, 5.5, 4.5, 5.5)
    arrow(ax, 5.5, 5.5, 3+(W+0.4)/2, 5.5)
    ax.text(1.2, 5.5, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3-(W+0.4)/2, 5.5, 0.7); vline(ax, 0.7, 5.5, 3.4)
    arrow(ax, 0.7, 3.4, 3-W/2, 3.4)

    # цикл шаг 5: i<n Да→14 Нет→15
    arrow(ax, 3, bot(13), 3, top(14), "Да")
    hline(ax, 3+W/2, 1.5, 5.5); vline(ax, 5.5, 1.5, 2.4)
    arrow(ax, 5.5, 2.4, 3+(W+0.4)/2, 2.4)
    ax.text(1.2, 2.4, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3-(W+0.4)/2, 2.4, 0.7); vline(ax, 0.7, 2.4, 0.5)
    arrow(ax, 0.7, 0.5, 3-W/2, 0.5)

    plt.tight_layout()
    plt.savefig("flowchart_4_counting_sort.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: flowchart_4_counting_sort.png")


# ═══════════════════════════════════════════════════════════
#  5. vector_push()
# ═══════════════════════════════════════════════════════════
def draw_vector_push():
    fig, ax = plt.subplots(figsize=(6, 11))
    ax.set_xlim(0, 6); ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_facecolor("#f4f6f8"); fig.patch.set_facecolor("#f4f6f8")
    ax.set_title("vector_push()", fontsize=13, fontweight="bold",
                 fontfamily=FONT, pad=10)

    W, H = 3.8, 0.58

    blocks = [
        (3, 10.3, "НАЧАЛО",                                            C_TERM),
        (3,  9.4, "size >= capacity?",                                 C_DEC),
        (3,  8.3, "capacity == 0?",                                    C_DEC),
        (3,  7.3, "new_cap = 4",                                       C_PROC),
        (3,  6.3, "new_cap = capacity * 2",                            C_PROC),
        (3,  5.3, "realloc(data, new_cap)",                            C_PROC),
        (3,  4.3, "tmp == NULL?",                                      C_DEC),
        (3,  3.3, "Ошибка: exit()",                                    C_TERM),
        (3,  2.4, "data = tmp\ncapacity = new_cap",                    C_PROC),
        (3,  1.4, "data[size] = val\nsize++",                          C_PROC),
        (3,  0.5, "КОНЕЦ",                                             C_TERM),
    ]

    diamond_idx = {1, 2, 6}

    for i, (x, y, txt, col) in enumerate(blocks):
        if i in diamond_idx:
            add_diamond(ax, x, y, W + 0.4, 0.68, txt)
        else:
            add_box(ax, x, y, W, H, txt, col)

    def top(i): return blocks[i][1] + (0.34 if i in diamond_idx else H/2)
    def bot(i): return blocks[i][1] - (0.34 if i in diamond_idx else H/2)

    # 0→1
    arrow(ax, 3, bot(0), 3, top(1))

    # 1 Да → 2 (нужно расширять)
    arrow(ax, 3, bot(1), 3, top(2), "Да")
    # 1 Нет → 9 (пропускаем расширение)
    ax.text(4.6, 9.4, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3+(W+0.4)/2, 9.4, 5.4)
    vline(ax, 5.4, 9.4, 1.4)
    arrow(ax, 5.4, 1.4, 3+W/2, 1.4)

    # 2 Да → 3 (capacity==0 → new_cap=4)
    arrow(ax, 3, bot(2), 3, top(3), "Да")
    # 2 Нет → 4 (capacity*2)
    ax.text(4.6, 8.3, "Нет", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3+(W+0.4)/2, 8.3, 5.4)
    vline(ax, 5.4, 8.3, 6.3)
    arrow(ax, 5.4, 6.3, 3+W/2, 6.3)

    # 3→5, 4→5
    arrow(ax, 3, bot(3), 3, top(5))
    arrow(ax, 3, bot(4), 3, top(5))

    # 5→6
    arrow(ax, 3, bot(5), 3, top(6))

    # 6 Да → 7 (ошибка)
    ax.text(4.6, 4.3, "Да", fontsize=7.5, color="#333", fontfamily=FONT, va="center")
    hline(ax, 3+(W+0.4)/2, 4.3, 5.4)
    vline(ax, 5.4, 4.3, 3.3)
    arrow(ax, 5.4, 3.3, 3+W/2, 3.3)

    # 6 Нет → 8
    arrow(ax, 3, bot(6), 3, top(8), "Нет")

    # 8→9→10
    arrow(ax, 3, bot(8), 3, top(9))
    arrow(ax, 3, bot(9), 3, top(10))

    plt.tight_layout()
    plt.savefig("flowchart_5_vector_push.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: flowchart_5_vector_push.png")


# ── Запуск всех схем ───────────────────────────────────────
import os
os.chdir("/Users/alexxo/Desktop/algos/lr1")

draw_main()
draw_read_file()
draw_radix_sort()
draw_counting_sort()
draw_vector_push()
print("\nВсе блок-схемы сохранены в /Users/alexxo/Desktop/algos/lr1/")
