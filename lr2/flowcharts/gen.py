"""
Генератор блок-схем для lr2: ГОСТ-подобный стиль, чёрно-белый, русские описания.
Блоки содержат только русский текст. Код — только в пунктирных аннотациях.
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
    "fontsize": "15",
    "style":    "filled",
    "fillcolor":"white",
    "color":    "black",
    "penwidth": "1.3",
}
BASE_EDGE = {
    "fontname": "Arial",
    "fontsize": "13",
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

    term("s",      "начало")
    proc("arg",    "определить имя входного файла")
    io  ("rdmsg",  "вывести сообщение о начале чтения файла")
    proc("rd",     "прочитать числа из файла в массив")
    dec ("chk",    "ошибка чтения\nили файл пустой?", w="3.2")
    io  ("fail",   "вывести сообщение об ошибке")
    term("efail",  "конец")
    io  ("rdok",   "вывести количество прочитанных чисел")
    io  ("pr1",    "вывести исходный массив")
    io  ("srtmsg", "вывести сообщение о начале сортировки")
    proc("srt",    "выполнить цифровую сортировку\nRadix Sort LSD через кольцевые очереди")
    io  ("pr2",    "вывести отсортированный массив")
    proc("cmx",    "найти максимальный элемент,\nвычислить число разрядов")
    io  ("prx",    "вывести оценку сложности:\nколичество элементов, максимум,\nчисло разрядов, число операций")
    proc("cln",    "освободить выделенную память")
    term("e",      "конец")

    ann("a_rd",  'read_file(filename, &arr)\nвозвращает n; malloc внутри')
    ann("a_srt", "radix_sort(arr, n)")
    ann("a_cmx", "find_max(arr, n) + цикл: tmp /= 10")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("rd");  sg.node("a_rd")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("srt"); sg.node("a_srt")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("cmx"); sg.node("a_cmx")

    e("s","arg"); e("arg","rdmsg"); e("rdmsg","rd"); e("rd","chk")
    e("chk","fail",   lbl="да"); e("fail","efail")
    e("chk","rdok",   lbl="нет")
    e("rdok","pr1"); e("pr1","srtmsg"); e("srtmsg","srt")
    e("srt","pr2"); e("pr2","cmx"); e("cmx","prx"); e("prx","cln"); e("cln","e")

    ae("rd","a_rd"); ae("srt","a_srt"); ae("cmx","a_cmx")
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
    io  ("ferr", "вывести сообщение\nоб ошибке открытия файла")
    io  ("r1",   "return -1")
    term("e1",   "конец")

    proc("cnt",  "ПЕРВЫЙ ПРОХОД:\nпрочитать все числа из файла,\nподсчитать их количество")
    dec ("ne",   "файл не содержит\nни одного числа?")
    io  ("eerr", "вывести сообщение:\nфайл пустой или не содержит чисел")
    io  ("r2",   "закрыть файл, return -1")
    term("e2",   "конец")

    proc("rw",   "перемотать файл в начало")
    proc("mal",  "выделить динамический массив\nдля хранения чисел")
    dec ("mnl",  "память выделена\nуспешно?")
    io  ("merr", "вывести сообщение об ошибке памяти")
    io  ("r3",   "закрыть файл, return -1")
    term("e3",   "конец")

    proc("fill", "ВТОРОЙ ПРОХОД:\nпоследовательно считать все числа\nв выделенный массив")
    proc("fc",   "закрыть файл,\nпередать указатель на массив вызывающей стороне")
    io  ("rn",   "return n  (количество прочитанных чисел)")
    term("e",    "конец")

    ann("a_fop",  'fopen(filename, "r")')
    ann("a_cnt",  'while (fscanf(fp,"%d",&tmp)==1) n++')
    ann("a_mal",  "arr = malloc(n * sizeof(int))")
    ann("a_fill", 'for(i=0;i<n;i++) fscanf(fp,"%d",&arr[i])')

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("fop");  sg.node("a_fop")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("cnt");  sg.node("a_cnt")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("mal");  sg.node("a_mal")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("fill"); sg.node("a_fill")

    e("s","fop"); e("fop","fnl")
    e("fnl","cnt",  lbl="да")
    e("fnl","ferr", lbl="нет"); e("ferr","r1"); e("r1","e1")
    e("cnt","ne")
    e("ne","rw",   lbl="нет")
    e("ne","eerr", lbl="да"); e("eerr","r2"); e("r2","e2")
    e("rw","mal"); e("mal","mnl")
    e("mnl","fill", lbl="да")
    e("mnl","merr", lbl="нет"); e("merr","r3"); e("r3","e3")
    e("fill","fc"); e("fc","rn"); e("rn","e")

    ae("fop","a_fop"); ae("cnt","a_cnt"); ae("mal","a_mal"); ae("fill","a_fill")
    save(g, "2_read_file")


# ═══════════════════════════════════════════════════════════════
#  3. radix_sort() + find_max()
# ═══════════════════════════════════════════════════════════════
def draw_radix_sort():
    g = graphviz.Digraph("radix_sort", graph_attr={**BASE_GRAPH,
        "ranksep": "0.75", "nodesep": "0.60"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",    "начало")
    dec ("trv",  "массив содержит\nменее двух элементов?")
    io  ("ret0", "return  (массив уже отсортирован)")
    term("e0",   "конец")

    proc("fmx",  "найти максимальный элемент массива,\nзапомнить его значение")
    proc("exp1", "установить начальный разряд (единицы)")
    proc("loop", "ЦИКЛ — пока не обработаны все разряды\nмаксимального числа:\n  отсортировать массив по текущему разряду\n  перейти к следующему разряду")
    io  ("ret",  "return")
    term("e",    "конец")

    ann("a_fmx",  "for(i=1;i<n;i++)\n  if(arr[i]>max) max=arr[i]")
    ann("a_exp1", "exp = 1")
    ann("a_loop", "while(max_val/exp>0){\n  counting_sort_by_queue(arr,n,exp);\n  exp*=BASE; }")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("fmx");  sg.node("a_fmx")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("exp1"); sg.node("a_exp1")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("loop"); sg.node("a_loop")

    e("s","trv")
    e("trv","ret0", lbl="да"); e("ret0","e0")
    e("trv","fmx",  lbl="нет")
    e("fmx","exp1"); e("exp1","loop"); e("loop","ret"); e("ret","e")

    ae("fmx","a_fmx"); ae("exp1","a_exp1"); ae("loop","a_loop")
    save(g, "3_radix_sort")


# ═══════════════════════════════════════════════════════════════
#  4. counting_sort_by_queue()
# ═══════════════════════════════════════════════════════════════
def draw_counting_sort_queue():
    g = graphviz.Digraph("csq", graph_attr={**BASE_GRAPH,
        "ranksep": "0.70", "nodesep": "0.55"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",  "начало")
    proc("s1", "ШАГ 1:\nинициализировать десять пустых\nкольцевых очередей (корзины 0–9)")
    proc("s2", "ШАГ 2:\nдля каждого элемента массива\nвычислить цифру текущего разряда\nи добавить элемент в соответствующую корзину")
    proc("s3", "ШАГ 3:\nпоследовательно извлечь все элементы\nиз корзин 0–9 обратно в массив\n(порядок FIFO сохраняет устойчивость)")
    proc("s4", "ШАГ 4:\nосвободить все десять очередей")
    io  ("ret", "return")
    term("e",  "конец")

    ann("a_s1", "for(j=0;j<10;j++) queue_init(&buckets[j])")
    ann("a_s2", "for(i=0;i<n;i++){\n  digit=(arr[i]/exp)%BASE;\n  enqueue(&buckets[digit],arr[i]); }")
    ann("a_s3", "idx=0;\nfor(j=0;j<BASE;j++)\n  while(!queue_is_empty(&buckets[j]))\n    dequeue(&buckets[j],&arr[idx++]);")
    ann("a_s4", "for(j=0;j<10;j++) queue_free(&buckets[j])")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s1"); sg.node("a_s1")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s2"); sg.node("a_s2")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s3"); sg.node("a_s3")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s4"); sg.node("a_s4")

    e("s","s1"); e("s1","s2"); e("s2","s3"); e("s3","s4"); e("s4","ret"); e("ret","e")

    ae("s1","a_s1"); ae("s2","a_s2"); ae("s3","a_s3"); ae("s4","a_s4")
    save(g, "4_counting_sort_queue")


# ═══════════════════════════════════════════════════════════════
#  5. enqueue() + dequeue()
# ═══════════════════════════════════════════════════════════════
def draw_enqueue_dequeue():
    ANN = dict(shape="box", style="dashed", color="gray40",
               fontcolor="gray30", fontsize="12", fontname="Courier New",
               width="3.4", height="0.50", margin="0.15")
    AE  = dict(style="dashed", color="gray50",
               arrowhead="none", penwidth="0.9", constraint="false")
    N = {**BASE_NODE}
    E = BASE_EDGE

    def nd(sg, nid, lbl, shape="box", w="3.8", h="0.65"):
        sg.node(nid, label=lbl, shape=shape, width=w, height=h, **N)

    def same(sg, *ids):
        with sg.subgraph() as r:
            r.attr(rank="same")
            for i in ids:
                r.node(i)

    # ── enqueue ──────────────────────────────────────────────────
    ge = graphviz.Digraph("enq_deq", graph_attr={**BASE_GRAPH,
             "ranksep": "0.70", "nodesep": "0.70"})

    with ge.subgraph(name="cluster_enq") as sg:
        sg.attr(label="Добавление в очередь — enqueue()",
                style="rounded", color="black",
                penwidth="1.4", fontname="Arial", fontsize="15",
                margin="20")

        nd(sg, "eq_s",  "начало",                                          "oval",    "2.2","0.55")
        nd(sg, "eq_m",  "выделить память\nдля нового узла",                "box",     "3.8","0.65")
        nd(sg, "eq_nl", "память выделена\nуспешно?",                       "diamond", "3.2","0.85")
        nd(sg, "eq_er", "вывести сообщение об ошибке",                     "parallelogram","3.8","0.65")
        nd(sg, "eq_r0", "return -1",                                      "parallelogram","2.6","0.55")
        nd(sg, "eq_e0", "конец",                                          "oval",    "2.2","0.55")
        nd(sg, "eq_v",  "записать значение в поле узла",                   "box",     "3.8","0.65")
        nd(sg, "eq_em", "очередь пустая?",                                 "diamond", "3.2","0.85")
        nd(sg, "eq_1",  "замкнуть узел на себя —\nон становится и головой, и хвостом","box","3.8","0.65")
        nd(sg, "eq_n",  "вставить новый узел\nмежду хвостом и головой кольца",       "box","3.8","0.65")
        nd(sg, "eq_t",  "обновить хвост очереди,\nувеличить счётчик элементов",      "box","3.8","0.65")
        nd(sg, "eq_r",  "return 0",                                       "parallelogram","2.6","0.55")
        nd(sg, "eq_e",  "конец",                                          "oval",    "2.2","0.55")

        sg.node("a_eq_m", "node = malloc(sizeof(Node))",              **ANN)
        sg.node("a_eq_v", "node->value = value",                      **ANN)
        sg.node("a_eq_1", "node->next = node",                        **ANN)
        sg.node("a_eq_n", "node->next = tail->next;\ntail->next = node", **ANN)
        sg.node("a_eq_t", "q->tail = node;\nq->size++",               **ANN)

        same(sg, "eq_m",  "a_eq_m")
        same(sg, "eq_v",  "a_eq_v")
        same(sg, "eq_1",  "a_eq_1")
        same(sg, "eq_n",  "a_eq_n")
        same(sg, "eq_t",  "a_eq_t")

    ge.edge("eq_s","eq_m",   **E)
    ge.edge("eq_m","eq_nl",  **E)
    ge.edge("eq_nl","eq_er", label="нет", **E)
    ge.edge("eq_er","eq_r0", **E)
    ge.edge("eq_r0","eq_e0", **E)
    ge.edge("eq_nl","eq_v",  label="да",  **E)
    ge.edge("eq_v","eq_em",  **E)
    ge.edge("eq_em","eq_1",  label="да",  **E)
    ge.edge("eq_em","eq_n",  label="нет", **E)
    ge.edge("eq_1","eq_t",   **E)
    ge.edge("eq_n","eq_t",   **E)
    ge.edge("eq_t","eq_r",   **E)
    ge.edge("eq_r","eq_e",   **E)

    for src, dst in [("eq_m","a_eq_m"),("eq_v","a_eq_v"),
                     ("eq_1","a_eq_1"),("eq_n","a_eq_n"),("eq_t","a_eq_t")]:
        ge.edge(src, dst, **AE)

    save(ge, "5a_enqueue")

    # ── dequeue ──────────────────────────────────────────────────
    gd = graphviz.Digraph("deq", graph_attr={**BASE_GRAPH,
             "ranksep": "0.70", "nodesep": "0.70"})

    with gd.subgraph(name="cluster_deq") as sg:
        sg.attr(label="Извлечение из очереди — dequeue()",
                style="rounded", color="black",
                penwidth="1.4", fontname="Arial", fontsize="15",
                margin="20")

        nd(sg, "dq_s",  "начало",                                              "oval",    "2.2","0.55")
        nd(sg, "dq_em", "очередь пустая?",                                     "diamond", "3.2","0.85")
        nd(sg, "dq_er", "вывести сообщение об ошибке",                         "parallelogram","3.8","0.65")
        nd(sg, "dq_r0", "return -1",                                          "parallelogram","2.6","0.55")
        nd(sg, "dq_e0", "конец",                                              "oval",    "2.2","0.55")
        nd(sg, "dq_h",  "получить голову очереди,\nсчитать её значение в выходной параметр","box","3.8","0.65")
        nd(sg, "dq_1",  "в очереди\nостался один элемент?",                    "diamond", "3.2","0.85")
        nd(sg, "dq_t",  "обнулить хвост —\nочередь стала пустой",              "box",     "3.8","0.65")
        nd(sg, "dq_n",  "перешить кольцо —\nисключить голову из цепочки",      "box",     "3.8","0.65")
        nd(sg, "dq_f",  "освободить память узла,\nуменьшить счётчик элементов","box",     "3.8","0.65")
        nd(sg, "dq_r",  "return 0",                                           "parallelogram","2.6","0.55")
        nd(sg, "dq_e",  "конец",                                              "oval",    "2.2","0.55")

        sg.node("a_dq_h", "head = tail->next;\n*out = head->value",       **ANN)
        sg.node("a_dq_t", "q->tail = NULL",                               **ANN)
        sg.node("a_dq_n", "tail->next = head->next",                      **ANN)
        sg.node("a_dq_f", "free(head);\nq->size--",                       **ANN)

        same(sg, "dq_h", "a_dq_h")
        same(sg, "dq_t", "a_dq_t")
        same(sg, "dq_n", "a_dq_n")
        same(sg, "dq_f", "a_dq_f")

    gd.edge("dq_s","dq_em",  **E)
    gd.edge("dq_em","dq_er", label="да",  **E)
    gd.edge("dq_er","dq_r0", **E)
    gd.edge("dq_r0","dq_e0", **E)
    gd.edge("dq_em","dq_h",  label="нет", **E)
    gd.edge("dq_h","dq_1",   **E)
    gd.edge("dq_1","dq_t",   label="да",  **E)
    gd.edge("dq_1","dq_n",   label="нет", **E)
    gd.edge("dq_t","dq_f",   **E)
    gd.edge("dq_n","dq_f",   **E)
    gd.edge("dq_f","dq_r",   **E)
    gd.edge("dq_r","dq_e",   **E)

    for src, dst in [("dq_h","a_dq_h"),("dq_t","a_dq_t"),
                     ("dq_n","a_dq_n"),("dq_f","a_dq_f")]:
        gd.edge(src, dst, **AE)

    save(gd, "5b_dequeue")


print("Генерация блок-схем lr2...")
draw_main()
draw_read_file()
draw_radix_sort()
draw_counting_sort_queue()
draw_enqueue_dequeue()
print("Готово.")
