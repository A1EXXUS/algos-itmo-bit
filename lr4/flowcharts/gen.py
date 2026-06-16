"""
Генератор блок-схем для lr4: ГОСТ-подобный стиль, чёрно-белый, русские описания.
Адаптировано под стек на массиве + radix через стеки-корзины + поиск Бойера-Мура.
"""
import graphviz, os

OUT = os.path.dirname(os.path.abspath(__file__))

BASE_GRAPH = {
    "rankdir":  "TB",
    "splines":  "spline",
    "nodesep":  "0.80",
    "ranksep":  "1.00",
    "fontname": "Arial",
    "bgcolor":  "white",
    "margin":   "0.15",
}
BASE_NODE = {
    "fontname": "Arial",
    "fontsize": "26",
    "style":    "filled",
    "fillcolor":"white",
    "color":    "black",
    "penwidth": "1.5",
}
BASE_EDGE = {
    "fontname": "Arial",
    "fontsize": "22",
    "color":    "black",
    "penwidth": "1.4",
    "arrowsize":"0.9",
}

def mk(g):
    def term(n, lbl):
        g.node(n, label=lbl, shape="oval",
               width="2.6", height="0.65", **BASE_NODE)
    def proc(n, lbl, w="5.0"):
        g.node(n, label=lbl, shape="box",
               width=w, height="0.80", **BASE_NODE)
    def dec(n, lbl, w="4.0"):
        g.node(n, label=lbl, shape="diamond",
               width=w, height="1.00", **BASE_NODE)
    def io(n, lbl, w="5.0"):
        g.node(n, label=lbl, shape="parallelogram",
               width=w, height="0.80", **BASE_NODE)
    def ann(n, lbl):
        g.node(n, label=lbl, shape="box",
               style="dashed", color="gray40",
               fontcolor="gray30", fontsize="22",
               fontname="Arial", width="3.8", height="0.55")
    def e(a, b, lbl="", **kw):
        g.edge(a, b, label=lbl, **{**BASE_EDGE, **kw})
    def ae(src, dst):
        g.edge(src, dst,
               style="dashed", color="gray50",
               arrowhead="none", penwidth="0.9",
               constraint="false")
    return term, proc, dec, io, ann, e, ae


def save(g, name):
    path = os.path.join(OUT, name)
    g.render(path, format="pdf", cleanup=True)
    print(f"  {name}.pdf")
    # Также генерируем png для удобства (как в lr3)
    g.render(path, format="png", cleanup=True)
    print(f"  {name}.png")


# ═══════════════════════════════════════════════════════════════
#  1. main()
# ═══════════════════════════════════════════════════════════════
def draw_main():
    g = graphviz.Digraph("main", graph_attr={**BASE_GRAPH,
        "ranksep": "0.55", "nodesep": "0.45"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",      "начало")
    proc("arg",    "определить имя входного файла")
    io  ("rdmsg",  "вывести сообщение о начале чтения")
    proc("rd",     "прочитать числа из файла в стек\n(через stack_push)")
    dec ("chk",    "ошибка чтения\nили файл пустой?", w="4.0")
    io  ("fail",   "вывести сообщение об ошибке")
    term("efail",  "конец")
    io  ("rdok",   "вывести количество прочитанных чисел")
    io  ("pr1",    "вывести исходный стек\n(от дна к вершине)")
    io  ("srtmsg", "вывести сообщение о начале сортировки")
    proc("srt",    "выполнить цифровую сортировку стека\n(Radix Sort LSD через стеки-корзины)")
    io  ("pr2",    "вывести отсортированный стек\n(от дна к вершине)")
    proc("srch",   "выполнить поиск методом Бойера-Мура\nпо ключам из аргументов\nили введённым с клавиатуры")
    io  ("prsr",   "вывести результат поиска:\nпозицию числа в стеке\nили сообщение об отсутствии")
    proc("rbt",    "записать результат в красно-чёрное дерево\n(вставить все элементы)")
    io  ("prbt",   "вывести inorder обход дерева\n(должен совпадать с отсортированным)")
    proc("cln",    "освободить выделенную память")
    term("e",      "конец")

    ann("a_rd",   "read_file(filename, &s)")
    ann("a_srt",  "radix_sort(&s)")
    ann("a_srch", "boyer_moore_search(&s, key, &views)")
    ann("a_rbt",  "rbtree_insert(&tree, val) для каждого")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("rd");   sg.node("a_rd")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("srt");  sg.node("a_srt")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("srch"); sg.node("a_srch")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("rbt");  sg.node("a_rbt")

    e("s","arg"); e("arg","rdmsg"); e("rdmsg","rd"); e("rd","chk")
    e("chk","fail",   lbl="да");  e("fail","efail")
    e("chk","rdok",   lbl="нет")
    e("rdok","pr1"); e("pr1","srtmsg"); e("srtmsg","srt")
    e("srt","pr2"); e("pr2","srch"); e("srch","prsr"); e("prsr","rbt")
    e("rbt","prbt"); e("prbt","cln"); e("cln","e")

    ae("rd","a_rd"); ae("srt","a_srt"); ae("srch","a_srch"); ae("rbt","a_rbt")
    save(g, "1_main")


# ═══════════════════════════════════════════════════════════════
#  2. read_file()
# ═══════════════════════════════════════════════════════════════
def draw_read_file():
    g = graphviz.Digraph("read_file", graph_attr={**BASE_GRAPH})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",    "начало")
    proc("fop",  "открыть файл для чтения")
    dec ("fnl",  "файл открыт\nуспешно?")
    io  ("ferr", "вывести сообщение\nоб ошибке открытия файла")
    io  ("r1",   "return -1")
    term("e1",   "конец")

    proc("fill", "читать числа из файла одно за другим,\nдобавлять каждое в стек (stack_push)")
    dec ("ne",   "стек пустой\n(файл не содержал чисел)?")
    io  ("eerr", "вывести сообщение:\nфайл пустой или не содержит чисел")
    io  ("r2",   "return -1")
    term("e2",   "конец")

    proc("fc",   "закрыть файл")
    io  ("rn",   "return stack_size (количество прочитанных чисел)")
    term("e",    "конец")

    ann("a_fop",  'fopen(filename, "r")')
    ann("a_fill", 'while(fscanf(fp,"%d",&tmp)==1)\n  stack_push(s, tmp)')
    ann("a_ne",   "stack_is_empty(s)")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("fop");  sg.node("a_fop")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("fill"); sg.node("a_fill")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ne");   sg.node("a_ne")

    e("s","fop"); e("fop","fnl")
    e("fnl","fill", lbl="да")
    e("fnl","ferr", lbl="нет"); e("ferr","r1"); e("r1","e1")
    e("fill","ne")
    e("ne","fc",   lbl="нет")
    e("ne","eerr", lbl="да"); e("eerr","r2"); e("r2","e2")
    e("fc","rn"); e("rn","e")

    ae("fop","a_fop"); ae("fill","a_fill"); ae("ne","a_ne")
    save(g, "2_read_file")


# ═══════════════════════════════════════════════════════════════
#  3. radix_sort()
# ═══════════════════════════════════════════════════════════════
def draw_radix_sort():
    g = graphviz.Digraph("radix_sort", graph_attr={**BASE_GRAPH})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",    "начало")
    dec ("trv",  "стек содержит\nменее двух элементов?")
    io  ("ret0", "return  (стек уже отсортирован)")
    term("e0",   "конец")

    proc("init", "инициализировать два вспомогательных стека:\nneg (модули отрицательных) и pos (положительные)")
    proc("spl",  "ЦИКЛ — разделить исходный стек по знаку:\n  отрицательные → neg (по модулю)\n  неотрицательные → pos")
    proc("sneg", "отсортировать стек neg как неотрицательный\n(найти максимум, обойти по разрядам)")
    proc("spos", "отсортировать стек pos как неотрицательный\n(найти максимум, обойти по разрядам)")
    proc("mrg",  "собрать результат в исходный стек:\n  из neg брать pop (большие модули первыми)\n  из pos — реверс, чтобы маленькие первыми")
    io  ("ret",  "return")
    term("e",    "конец")

    ann("a_init", "Stack neg, pos;\nstack_init(&neg); stack_init(&pos)")
    ann("a_spl",  "while(!stack_is_empty(s)) {\n  pop(s,&v);\n  v<0 ? push(&neg,-v)\n       : push(&pos,v); }")
    ann("a_sneg", "radix_sort_nonneg(&neg)")
    ann("a_spos", "radix_sort_nonneg(&pos)")
    ann("a_mrg",  "while(!empty(neg)) pop(&neg,&v); push(s,-v);\n/* реверс pos через pos_rev */\nwhile(!empty(pos_rev)) pop(&pos_rev,&v); push(s,v)")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("init"); sg.node("a_init")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("spl");  sg.node("a_spl")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("sneg"); sg.node("a_sneg")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("spos"); sg.node("a_spos")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("mrg");  sg.node("a_mrg")

    e("s","trv")
    e("trv","ret0", lbl="да"); e("ret0","e0")
    e("trv","init", lbl="нет")
    e("init","spl"); e("spl","sneg"); e("sneg","spos"); e("spos","mrg")
    e("mrg","ret"); e("ret","e")

    ae("init","a_init"); ae("spl","a_spl")
    ae("sneg","a_sneg"); ae("spos","a_spos"); ae("mrg","a_mrg")
    save(g, "3_radix_sort")


# ═══════════════════════════════════════════════════════════════
#  4. counting_sort_by_stack()
# ═══════════════════════════════════════════════════════════════
def draw_counting_sort_stack():
    g = graphviz.Digraph("css", graph_attr={**BASE_GRAPH})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",  "начало")
    proc("s1", "ШАГ 1:\nинициализировать десять пустых\nстеков-корзин (0–9)")
    proc("s2", "ШАГ 2:\nреверс исходного стека (чтобы\nобрабатывать от дна),\nвычислить цифру разряда,\nположить элемент в соответствующую корзину")
    proc("s3", "ШАГ 3:\nдля каждой корзины 0–9:\n  реверс через temp,\n  вернуть элементы в исходный стек\n(двойной реверс сохраняет порядок)")
    io  ("ret", "return")
    term("e",  "конец")

    ann("a_s1", "Stack buckets[10];\nfor(j=0;j<10;j++) stack_init(&buckets[j])")
    ann("a_s2", "/* rev для порядка от дна */\nwhile(!empty(s)) pop(s,&v); push(&rev,v);\nwhile(!empty(rev)) {\n  pop(&rev,&v);\n  digit=(v/exp)%BASE;\n  push(&buckets[digit],v); }")
    ann("a_s3", "for(j=0;j<BASE;j++) {\n  while(!empty(buckets[j])) pop(&buckets[j],&v); push(&temp,v);\n  while(!empty(temp)) pop(&temp,&v); push(s,v);\n}")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s1"); sg.node("a_s1")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s2"); sg.node("a_s2")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s3"); sg.node("a_s3")

    e("s","s1"); e("s1","s2"); e("s2","s3"); e("s3","ret"); e("ret","e")

    ae("s1","a_s1"); ae("s2","a_s2"); ae("s3","a_s3")
    save(g, "4_counting_sort_stack")


# ═══════════════════════════════════════════════════════════════
#  5a/5b. push и pop стека (на массиве)
# ═══════════════════════════════════════════════════════════════
def draw_stack_ops():
    GA = {**BASE_GRAPH, "ranksep": "0.90", "nodesep": "0.70"}

    # ── push ───────────────────────────────────────────────
    gpush = graphviz.Digraph("push", graph_attr=GA)
    term, proc, dec, io, ann, e, ae = mk(gpush)

    term("ps",   "начало")
    proc("pchk", "top + 1 >= capacity?")
    dec ("pfull","нужно расширить?")
    proc("presz", "new_cap = capacity==0 ? 8 : capacity*2\nrealloc(data, new_cap)")
    dec ("pok",  "realloc успешен?")
    io  ("perr", "вывести ошибку malloc")
    io  ("pret0","return -1")
    term("pe0",  "конец")
    proc("pput", "top++\ndata[top] = value")
    io  ("pret", "return 0")
    term("pe",   "конец")

    ann("pa_chk",  "if (top + 1 >= capacity)")
    ann("pa_resz", "new_cap = ...; realloc")
    ann("pa_put",  "top++; data[top] = value")

    with gpush.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pchk"); sg.node("pa_chk")
    with gpush.subgraph() as sg:
        sg.attr(rank="same"); sg.node("presz"); sg.node("pa_resz")
    with gpush.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pput"); sg.node("pa_put")

    e("ps","pchk"); e("pchk","pfull")
    e("pfull","presz", lbl="да")
    e("pfull","pput",  lbl="нет")
    e("presz","pok")
    e("pok","perr", lbl="нет"); e("perr","pret0"); e("pret0","pe0")
    e("pok","pput", lbl="да")
    e("pput","pret"); e("pret","pe")

    ae("pchk","pa_chk"); ae("presz","pa_resz"); ae("pput","pa_put")
    save(gpush, "5a_push")

    # ── pop ────────────────────────────────────────────────
    gpop = graphviz.Digraph("pop", graph_attr=GA)
    term, proc, dec, io, ann, e, ae = mk(gpop)

    term("pos",  "начало")
    dec ("poem", "стек пустой?")
    io  ("poer", "вывести сообщение об ошибке")
    io  ("por0", "return -1")
    term("poe0", "конец")
    proc("poget", "out = data[top]\ntop--")
    io  ("por",  "return 0")
    term("poe",  "конец")

    ann("poa_em",  "if (top == -1)")
    ann("poa_get", "*out = data[top]; top--;")

    with gpop.subgraph() as sg:
        sg.attr(rank="same"); sg.node("poem");  sg.node("poa_em")
    with gpop.subgraph() as sg:
        sg.attr(rank="same"); sg.node("poget"); sg.node("poa_get")

    e("pos","poem")
    e("poem","poer", lbl="да");  e("poer","por0"); e("por0","poe0")
    e("poem","poget", lbl="нет")
    e("poget","por"); e("por","poe")

    ae("poem","poa_em"); ae("poget","poa_get")
    save(gpop, "5b_pop")


# ═══════════════════════════════════════════════════════════════
#  6. boyer_moore_search()
# ═══════════════════════════════════════════════════════════════
def draw_boyer_moore_search():
    g = graphviz.Digraph("bm", graph_attr={**BASE_GRAPH,
        "ranksep": "0.40", "nodesep": "0.60"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",    "начало")
    proc("bld",  "построить текст:\n\";val1;val2;...;\" от дна к вершине")
    proc("pat",  "pat = \";\" + str(key) + \";\"")
    proc("bm",   "выполнить Бойер-Мур(text, pat)\nполучить char_pos и views")
    dec ("fnd",  "совпадение найдено?")
    io  ("map",  "map char_pos → индекс элемента\n(0 = дно)")
    io  ("retf", "return elem_idx")
    term("ef",   "конец")
    io  ("retn", "return -1")
    term("en",   "конец")

    ann("a_bld",  "build_text_from_stack(s)")
    ann("a_pat",  "snprintf(\";%d;\", key)")
    ann("a_bm",   "boyer_moore(text, n, pat, m, &views)")
    ann("a_map",  "find_element_index(s, char_pos)")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("bld");  sg.node("a_bld")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pat");  sg.node("a_pat")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("bm");   sg.node("a_bm")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("map");  sg.node("a_map")

    e("s","bld"); e("bld","pat"); e("pat","bm")
    e("bm","fnd")
    e("fnd","map", lbl="да")
    e("fnd","retn", lbl="нет"); e("retn","en")
    e("map","retf"); e("retf","ef")

    ae("bld","a_bld"); ae("pat","a_pat"); ae("bm","a_bm"); ae("map","a_map")
    save(g, "6_boyer_moore_search")


print("Генерация блок-схем lr4...")
draw_main()
draw_read_file()
draw_radix_sort()
draw_counting_sort_stack()
draw_stack_ops()
draw_boyer_moore_search()
print("Готово.")