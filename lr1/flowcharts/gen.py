"""
Генератор блок-схем: ГОСТ-подобный стиль, чёрно-белый, русские описания.
"""
import graphviz, os

OUT = os.path.dirname(os.path.abspath(__file__))

BASE_GRAPH = {
    "rankdir":  "TB",
    "splines":  "spline",
    "nodesep":  "0.55",
    "ranksep":  "0.70",
    "fontname": "Arial",
    "bgcolor":  "white",
    "margin":   "0.5",
}
BASE_NODE = {
    "fontname": "Arial",
    "fontsize": "18",
    "style":    "filled",
    "fillcolor":"white",
    "color":    "black",
    "penwidth": "1.3",
}
BASE_EDGE = {
    "fontname": "Arial",
    "fontsize": "15",
    "color":    "black",
    "penwidth": "1.2",
    "arrowsize":"0.75",
}

def mk(g):
    def term(n, lbl):
        g.node(n, label=lbl, shape="oval",
               width="2.2", height="0.55", **BASE_NODE)
    def proc(n, lbl, w="3.8"):
        g.node(n, label=lbl, shape="box",
               width=w, height="0.65", **BASE_NODE)
    def dec(n, lbl, w="3.2"):
        g.node(n, label=lbl, shape="diamond",
               width=w, height="0.85", **BASE_NODE)
    def io(n, lbl, w="3.8"):
        g.node(n, label=lbl, shape="parallelogram",
               width=w, height="0.65", **BASE_NODE)
    def ann(n, lbl):
        g.node(n, label=lbl, shape="box",
               style="dashed", color="gray40",
               fontcolor="gray30", fontsize="11",
               fontname="Arial", width="3.2", height="0.50")
    def e(a, b, lbl="", **kw):
        g.edge(a, b, label=lbl, **{**BASE_EDGE, **kw})
    def ae(src, dst):
        g.edge(src, dst,
               style="dashed", color="gray50",
               arrowhead="none", penwidth="0.8",
               constraint="false")
    return term, proc, dec, io, ann, e, ae


def join(g, n):
    g.node(n, label="", shape="point", width="0.12", height="0.12",
           style="filled", fillcolor="black", color="black")


def save(g, name):
    path = os.path.join(OUT, name)
    g.render(path, format="png", cleanup=True)
    print(f"  {name}.png")


# ═══════════════════════════════════════════════════════════════
#  1. main()
# ═══════════════════════════════════════════════════════════════
def draw_main():
    g = graphviz.Digraph("main", graph_attr={**BASE_GRAPH,
        "ranksep": "0.35", "nodesep": "0.30"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",     "начало")
    io  ("menu",  "вывести меню выбора\nструктуры данных")
    io  ("inp",   "считать выбор пользователя\n(1 — статический, 2 — динамический, 3 — вектор)")
    proc("ini",   "инициализировать все три структуры данных")
    io  ("rdmsg", "вывести «Чтение файла input.txt…»")
    proc("rd",    "прочитать числа из файла\nв выбранную структуру данных")
    dec ("chk",   "ошибка чтения\nили файл пустой?", w="3.2")
    io  ("fail",  "return EXIT_FAILURE")
    io  ("rdok",  "вывести «Прочитано N чисел.»")
    proc("ptr",   "получить указатель на массив\nи его размер")
    io  ("pr1",   "вывести «Исходный массив:»\nи все элементы arr[]")
    io  ("srtmsg","вывести «Выполняем Radix Sort…»")
    proc("srt",   "выполнить цифровую сортировку\nRadix Sort (LSD)")
    io  ("pr2",   "вывести «Отсортированный массив:»\nи все элементы arr[]")
    proc("cmx",   "найти максимальный элемент,\nвычислить число разрядов d")
    io  ("prx",   "вывести: n, max, d, k,\nоперации = T,  доп. ячеек = M")
    proc("cln",   "освободить выделенную память")
    io  ("ret_ok","вернуть EXIT_SUCCESS")
    term("e",     "конец")

    ann("a_rd",  'read_file("input.txt", mode, &sa, &da, &v)')
    ann("a_ptr", "get_array_ptr(mode, &sa, &da, &v, &arr, &sz)")
    ann("a_srt", "radix_sort(arr, sz)")
    ann("a_cmx", "find_max(arr,sz)  +  цикл: tmp /= 10")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("rd"); sg.node("a_rd")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ptr"); sg.node("a_ptr")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("srt"); sg.node("a_srt")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("cmx"); sg.node("a_cmx")

    e("s","menu"); e("menu","inp"); e("inp","ini"); e("ini","rdmsg")
    e("rdmsg","rd"); e("rd","chk")
    e("chk","fail",  lbl="да"); e("fail","e")
    e("chk","rdok",  lbl="нет")
    e("rdok","ptr"); e("ptr","pr1"); e("pr1","srtmsg")
    e("srtmsg","srt"); e("srt","pr2")
    e("pr2","cmx"); e("cmx","prx"); e("prx","cln"); e("cln","ret_ok"); e("ret_ok","e")

    ae("rd","a_rd"); ae("ptr","a_ptr"); ae("srt","a_srt"); ae("cmx","a_cmx")
    save(g, "1_main")


# ═══════════════════════════════════════════════════════════════
#  2. read_file()
# ═══════════════════════════════════════════════════════════════
def draw_read_file():
    g = graphviz.Digraph("read_file", graph_attr={**BASE_GRAPH,
        "ranksep": "0.70", "nodesep": "0.55"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",    "начало")
    proc("fop",  "открыть файл для чтения")
    dec ("fnl",  "файл открыт\nуспешно?")
    io  ("r1",   "вывести сообщение об ошибке открытия;\nвернуть −1")

    proc("cnt",  "ПЕРВЫЙ ПРОХОД:\nсчитать все числа, подсчитать n\n(цикл fscanf до EOF: n++)")
    dec ("ne",   "n равно нулю\n(файл пустой)?")
    io  ("r2",   "вывести сообщение «файл пуст»;\nзакрыть файл; вернуть −1")

    proc("rw",   "перемотать файл в начало (rewind)")
    proc("fill", "ВТОРОЙ ПРОХОД:\nдля i = 0..n−1: считать число val из файла,\nдобавить val в выбранную структуру данных")
    proc("fc",   "закрыть файл")
    io  ("rn",   "вернуть n")
    term("e",    "конец")

    ann("a_fop",  'fopen(filename, "r")')
    ann("a_cnt",  'while (fscanf(fp,"%d",&tmp)==1) n++')
    ann("a_fill", 'for(i=0;i<n;i++){\n  fscanf(fp,"%d",&val);\n  push(sa|da|v, val); }')

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("fop");  sg.node("a_fop")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("cnt");  sg.node("a_cnt")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("fill"); sg.node("a_fill")

    e("s","fop"); e("fop","fnl")
    e("fnl","cnt", lbl="да")
    e("fnl","r1",  lbl="нет"); e("r1","e")
    e("cnt","ne")
    e("ne","rw",   lbl="нет")
    e("ne","r2",   lbl="да"); e("r2","e")
    e("rw","fill"); e("fill","fc"); e("fc","rn"); e("rn","e")

    ae("fop","a_fop"); ae("cnt","a_cnt"); ae("fill","a_fill")
    save(g, "2_read_file")


# ═══════════════════════════════════════════════════════════════
#  3. radix_sort() + find_max()
# ═══════════════════════════════════════════════════════════════
def draw_radix_sort():
    g = graphviz.Digraph("radix_sort", graph_attr={**BASE_GRAPH,
        "ranksep": "0.75", "nodesep": "0.60"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",    "начало")
    dec ("trv",  "n ≤ 1\n(массив пустой или из 1 элемента)?")
    io  ("ret0", "вернуть\n(массив уже отсортирован)")
    term("e0",   "конец")

    proc("fmx",  "найти максимальный элемент max:\nпройти по всем arr[i],\nзапомнить наибольший")
    proc("exp1", "начальный разряд exp ← 1")
    proc("loop", "ЦИКЛ пока max / exp > 0:\n  сортировка подсчётом по цифре разряда exp\n  перейти к следующему разряду: exp ← exp × 10")
    term("e",    "конец")

    ann("a_fmx",  "for(i=1;i<n;i++) if(arr[i]>max) max=arr[i]")
    ann("a_loop", "while(max/exp>0){\n  counting_sort_by_digit(arr,n,exp);\n  exp*=BASE; }")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("fmx");  sg.node("a_fmx")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("loop"); sg.node("a_loop")

    e("s","trv")
    e("trv","ret0", lbl="да"); e("ret0","e0")
    e("trv","fmx",  lbl="нет")
    e("fmx","exp1"); e("exp1","loop"); e("loop","e")

    ae("fmx","a_fmx"); ae("loop","a_loop")
    save(g, "3_radix_sort")


# ═══════════════════════════════════════════════════════════════
#  4. counting_sort_by_digit() — все шаги 1-5, одна схема
# ═══════════════════════════════════════════════════════════════
def draw_counting_sort():
    g = graphviz.Digraph("cs", graph_attr={**BASE_GRAPH,
        "ranksep": "0.70", "nodesep": "0.55"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",      "начало")
    proc("mal",    "выделить вспомогательный массив output[n]")
    dec ("mnl",    "выделение памяти\nуспешно?")
    term("merr",   "вывести сообщение\nоб ошибке выделения памяти\nи завершить программу")

    proc("s1",  "ШАГ 1: обнулить массив count[0..9]")
    proc("s2",  "ШАГ 2: подсчитать цифры текущего разряда\nдля каждого элемента массива")
    proc("s3",  "ШАГ 3: накопить префиксные суммы\nв массиве count")
    proc("s4",  "ШАГ 4: разместить элементы в output[]\nв обратном порядке (стабильность)")
    proc("s5",  "ШАГ 5: скопировать output[]\nобратно в arr[]")
    proc("fr",  "освободить вспомогательный массив output")
    term("e",   "конец")

    ann("a_mal", "output = malloc(n * sizeof(int))")
    ann("a_s1",  "for(i=0;i<10;i++) count[i]=0")
    ann("a_s2",  "for(i=0;i<n;i++) count[(arr[i]/exp)%BASE]++")
    ann("a_s3",  "for(i=1;i<10;i++) count[i]+=count[i-1]")
    ann("a_s4",  "for(i=n-1;i>=0;i--){\n  d=(arr[i]/exp)%BASE;\n  output[--count[d]]=arr[i]; }")
    ann("a_s5",  "for(i=0;i<n;i++) arr[i]=output[i]")
    ann("a_fr",  "free(output)")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("mal"); sg.node("a_mal")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s1");  sg.node("a_s1")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s2");  sg.node("a_s2")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s3");  sg.node("a_s3")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s4");  sg.node("a_s4")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s5");  sg.node("a_s5")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("fr");  sg.node("a_fr")

    e("s","mal"); e("mal","mnl")
    e("mnl","s1",   lbl="да")
    e("mnl","merr", lbl="нет")
    e("s1","s2"); e("s2","s3"); e("s3","s4"); e("s4","s5"); e("s5","fr"); e("fr","e")

    ae("mal","a_mal"); ae("s1","a_s1"); ae("s2","a_s2"); ae("s3","a_s3")
    ae("s4","a_s4");   ae("s5","a_s5"); ae("fr","a_fr")
    save(g, "4_counting_sort")


# ═══════════════════════════════════════════════════════════════
#  5. vector_push()
# ═══════════════════════════════════════════════════════════════
def draw_vector_push():
    g = graphviz.Digraph("vector_push", graph_attr={**BASE_GRAPH,
        "ranksep": "0.70", "nodesep": "0.60"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",      "начало")
    dec ("chk",    "массив заполнен?\n(size ≥ capacity)")
    dec ("ini",    "вектор ещё не создан?\n(capacity == 0)")
    proc("nc4",    "установить начальную ёмкость 4")
    proc("nc2",    "удвоить ёмкость:\nnew_cap ← capacity × 2")
    proc("ral",    "перевыделить блок памяти:\nrealloc(data, new_cap × sizeof(int))")
    dec ("rnl",    "перевыделение\nуспешно?")
    term("rerr",   "вывести сообщение\nоб ошибке памяти\nи завершить программу")
    proc("upd",    "сохранить новый указатель и ёмкость")
    proc("wrt",    "записать val в позицию data[size]")
    proc("inc",    "увеличить size на 1")
    term("e",      "конец")

    ann("a_nc4",  "new_cap = VECTOR_INIT_CAP  (= 4)")
    ann("a_nc2",  "new_cap = v->capacity * 2")
    ann("a_ral",  "tmp = realloc(v->data, new_cap * sizeof(int))")
    ann("a_upd",  "v->data = tmp;  v->capacity = new_cap")
    ann("a_wrt",  "v->data[v->size] = val")
    ann("a_inc",  "v->size++")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("nc4"); sg.node("a_nc4")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("nc2"); sg.node("a_nc2")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ral"); sg.node("a_ral")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("upd"); sg.node("a_upd")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("wrt"); sg.node("a_wrt")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("inc"); sg.node("a_inc")

    e("s",   "chk")
    e("chk", "ini",    lbl="да")
    e("chk", "wrt",    lbl="нет")
    e("ini", "nc4",    lbl="да")
    e("ini", "nc2",    lbl="нет")
    e("nc4", "ral")
    e("nc2", "ral")
    e("ral", "rnl")
    e("rnl", "upd",  lbl="да")
    e("rnl", "rerr", lbl="нет")
    e("upd", "wrt")
    e("wrt", "inc"); e("inc","e")

    ae("nc4","a_nc4"); ae("nc2","a_nc2")
    ae("ral","a_ral"); ae("upd","a_upd")
    ae("wrt","a_wrt"); ae("inc","a_inc")
    save(g, "5_vector_push")


print("Генерация блок-схем...")
draw_main()
draw_read_file()
draw_radix_sort()
draw_counting_sort()
draw_vector_push()
print("Готово.")
