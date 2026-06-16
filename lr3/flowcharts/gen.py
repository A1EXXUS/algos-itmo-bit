"""
Генератор блок-схем для lr3: ГОСТ-подобный стиль, чёрно-белый, русские описания.
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
    proc("rd",     "прочитать числа из файла в дек")
    dec ("chk",    "ошибка чтения\nили файл пустой?", w="4.0")
    io  ("fail",   "вывести сообщение об ошибке")
    term("efail",  "конец")
    io  ("rdok",   "вывести количество прочитанных чисел")
    io  ("pr1",    "вывести исходный дек")
    io  ("srtmsg", "вывести сообщение о начале сортировки")
    proc("srt",    "выполнить цифровую сортировку дека\n(Radix Sort LSD через деки-корзины)")
    io  ("pr2",    "вывести отсортированный дек")
    proc("srch",   "выполнить поиск методом Райта\nпо ключам из аргументов\nили введённым с клавиатуры")
    io  ("prsr",   "вывести результат поиска:\nпозицию найденного элемента\nили сообщение об отсутствии")
    proc("cln",    "освободить выделенную память")
    term("e",      "конец")

    ann("a_rd",   "read_file(filename, &d)")
    ann("a_srt",  "radix_sort(&d)")
    ann("a_srch", "wright_search(&d, key, &pos, &views)")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("rd");   sg.node("a_rd")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("srt");  sg.node("a_srt")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("srch"); sg.node("a_srch")

    e("s","arg"); e("arg","rdmsg"); e("rdmsg","rd"); e("rd","chk")
    e("chk","fail",   lbl="да");  e("fail","efail")
    e("chk","rdok",   lbl="нет")
    e("rdok","pr1"); e("pr1","srtmsg"); e("srtmsg","srt")
    e("srt","pr2"); e("pr2","srch"); e("srch","prsr"); e("prsr","cln"); e("cln","e")

    ae("rd","a_rd"); ae("srt","a_srt"); ae("srch","a_srch")
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

    proc("fill", "читать числа из файла одно за другим,\nдобавлять каждое в хвост дека")
    dec ("ne",   "дек пустой\n(файл не содержал чисел)?")
    io  ("eerr", "вывести сообщение:\nфайл пустой или не содержит чисел")
    io  ("r2",   "return -1")
    term("e2",   "конец")

    proc("fc",   "закрыть файл")
    io  ("rn",   "return d->size  (количество прочитанных чисел)")
    term("e",    "конец")

    ann("a_fop",  'fopen(filename, "r")')
    ann("a_fill", 'while(fscanf(fp,"%d",&tmp)==1)\n  deque_push_back(d,tmp)')
    ann("a_ne",   "deque_is_empty(d)")

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
    dec ("trv",  "дек содержит\nменее двух элементов?")
    io  ("ret0", "return  (дек уже отсортирован)")
    term("e0",   "конец")

    proc("init", "инициализировать два вспомогательных дека:\nneg (модули отрицательных) и pos (положительные)")
    proc("spl",  "ЦИКЛ — разделить исходный дек по знаку:\n  отрицательные → neg (по модулю)\n  неотрицательные → pos")
    proc("sneg", "отсортировать дек neg как неотрицательный\n(найти максимум, обойти по разрядам)")
    proc("spos", "отсортировать дек pos как неотрицательный\n(найти максимум, обойти по разрядам)")
    proc("mrg",  "собрать результат в исходный дек:\n  из neg брать с хвоста, возвращать знак «минус»\n  из pos брать с головы")
    io  ("ret",  "return")
    term("e",    "конец")

    ann("a_init", "Deque neg, pos;\ndeque_init(&neg); deque_init(&pos)")
    ann("a_spl",  "while(!deque_is_empty(d)) {\n  pop_front(d,&v);\n  v<0 ? push_back(&neg,-v)\n       : push_back(&pos,v); }")
    ann("a_sneg", "radix_sort_nonneg(&neg)")
    ann("a_spos", "radix_sort_nonneg(&pos)")
    ann("a_mrg",  "while(!empty(neg)) pop_back(&neg,&v);\n  push_back(d,-v);\nwhile(!empty(pos)) pop_front(&pos,&v);\n  push_back(d,v)")

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
#  4. counting_sort_by_deque()
# ═══════════════════════════════════════════════════════════════
def draw_counting_sort_deque():
    g = graphviz.Digraph("csd", graph_attr={**BASE_GRAPH})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",  "начало")
    proc("s1", "ШАГ 1:\nинициализировать десять пустых\nдеков-корзин (0–9)")
    proc("s2", "ШАГ 2:\nизвлечь все элементы из исходного дека,\nвычислить цифру текущего разряда,\nположить элемент в соответствующую корзину")
    proc("s3", "ШАГ 3:\nпоследовательно извлечь все элементы\nиз корзин 0–9 и вернуть в исходный дек\n(порядок FIFO сохраняет устойчивость)")
    io  ("ret", "return")
    term("e",  "конец")

    ann("a_s1", "Deque buckets[10];\nfor(j=0;j<10;j++) deque_init(&buckets[j])")
    ann("a_s2", "while(!deque_is_empty(d)) {\n  pop_front(d,&v);\n  digit=(v/exp)%BASE;\n  push_back(&buckets[digit],v); }")
    ann("a_s3", "for(j=0;j<BASE;j++)\n  while(!deque_is_empty(&buckets[j])) {\n    pop_front(&buckets[j],&v);\n    push_back(d,v); }")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s1"); sg.node("a_s1")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s2"); sg.node("a_s2")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("s3"); sg.node("a_s3")

    e("s","s1"); e("s1","s2"); e("s2","s3"); e("s3","ret"); e("ret","e")

    ae("s1","a_s1"); ae("s2","a_s2"); ae("s3","a_s3")
    save(g, "4_counting_sort_deque")


# ═══════════════════════════════════════════════════════════════
#  5a/5b. push_front() и push_back()
# ═══════════════════════════════════════════════════════════════
def draw_push():
    GA = {**BASE_GRAPH, "ranksep": "0.90", "nodesep": "0.70"}

    # ── push_front ───────────────────────────────────────────────
    gpf = graphviz.Digraph("push_front", graph_attr=GA)
    term, proc, dec, io, ann, e, ae = mk(gpf)

    term("pf_s",   "начало")
    proc("pf_m",   "выделить память для нового узла")
    dec ("pf_nl",  "память выделена\nуспешно?")
    io  ("pf_er",  "вывести сообщение об ошибке")
    io  ("pf_r0",  "return -1")
    term("pf_e0",  "конец")
    proc("pf_lnk", "заполнить поля нового узла:\nvalue, prev=NULL, next=текущая голова")
    dec ("pf_em",  "дек был\nпустым?")
    proc("pf_np",  "обновить ссылку prev\nу прежней головы на новый узел")
    proc("pf_bt",  "установить новый узел\nкак хвост дека")
    proc("pf_upd", "обновить голову дека;\nувеличить счётчик элементов")
    io  ("pf_r",   "return 0")
    term("pf_e",   "конец")

    ann("pf_am",   "node = malloc(sizeof(DNode))")
    ann("pf_alk",  "node->value = value;\nnode->prev  = NULL;\nnode->next  = d->front")
    ann("pf_aem",  "deque_is_empty(d)")
    ann("pf_anp",  "d->front->prev = node")
    ann("pf_abt",  "d->back = node")
    ann("pf_aup",  "d->front = node;\nd->size++")

    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pf_m");   sg.node("pf_am")
    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pf_lnk"); sg.node("pf_alk")
    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pf_em");  sg.node("pf_aem")
    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pf_np");  sg.node("pf_anp")
    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pf_bt");  sg.node("pf_abt")
    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pf_upd"); sg.node("pf_aup")

    e("pf_s","pf_m"); e("pf_m","pf_nl")
    e("pf_nl","pf_er",  lbl="нет"); e("pf_er","pf_r0"); e("pf_r0","pf_e0")
    e("pf_nl","pf_lnk", lbl="да")
    e("pf_lnk","pf_em")
    e("pf_em","pf_np",  lbl="нет"); e("pf_np","pf_upd")
    e("pf_em","pf_bt",  lbl="да");  e("pf_bt","pf_upd")
    e("pf_upd","pf_r"); e("pf_r","pf_e")

    ae("pf_m","pf_am"); ae("pf_lnk","pf_alk"); ae("pf_em","pf_aem")
    ae("pf_np","pf_anp"); ae("pf_bt","pf_abt"); ae("pf_upd","pf_aup")
    save(gpf, "5a_push_front")

    # ── push_back ────────────────────────────────────────────────
    gpb = graphviz.Digraph("push_back", graph_attr=GA)
    term, proc, dec, io, ann, e, ae = mk(gpb)

    term("pb_s",   "начало")
    proc("pb_m",   "выделить память для нового узла")
    dec ("pb_nl",  "память выделена\nуспешно?")
    io  ("pb_er",  "вывести сообщение об ошибке")
    io  ("pb_r0",  "return -1")
    term("pb_e0",  "конец")
    proc("pb_lnk", "заполнить поля нового узла:\nvalue, next=NULL, prev=текущий хвост")
    dec ("pb_em",  "дек был\nпустым?")
    proc("pb_nb",  "обновить ссылку next\nу прежнего хвоста на новый узел")
    proc("pb_fr",  "установить новый узел\nкак голову дека")
    proc("pb_upd", "обновить хвост дека;\nувеличить счётчик элементов")
    io  ("pb_r",   "return 0")
    term("pb_e",   "конец")

    ann("pb_am",   "node = malloc(sizeof(DNode))")
    ann("pb_alk",  "node->value = value;\nnode->next  = NULL;\nnode->prev  = d->back")
    ann("pb_aem",  "deque_is_empty(d)")
    ann("pb_anb",  "d->back->next = node")
    ann("pb_afr",  "d->front = node")
    ann("pb_aup",  "d->back = node;\nd->size++")

    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pb_m");   sg.node("pb_am")
    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pb_lnk"); sg.node("pb_alk")
    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pb_em");  sg.node("pb_aem")
    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pb_nb");  sg.node("pb_anb")
    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pb_fr");  sg.node("pb_afr")
    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("pb_upd"); sg.node("pb_aup")

    e("pb_s","pb_m"); e("pb_m","pb_nl")
    e("pb_nl","pb_er",  lbl="нет"); e("pb_er","pb_r0"); e("pb_r0","pb_e0")
    e("pb_nl","pb_lnk", lbl="да")
    e("pb_lnk","pb_em")
    e("pb_em","pb_nb",  lbl="нет"); e("pb_nb","pb_upd")
    e("pb_em","pb_fr",  lbl="да");  e("pb_fr","pb_upd")
    e("pb_upd","pb_r"); e("pb_r","pb_e")

    ae("pb_m","pb_am"); ae("pb_lnk","pb_alk"); ae("pb_em","pb_aem")
    ae("pb_nb","pb_anb"); ae("pb_fr","pb_afr"); ae("pb_upd","pb_aup")
    save(gpb, "5b_push_back")


# ═══════════════════════════════════════════════════════════════
#  5c/5d. pop_front() и pop_back()
# ═══════════════════════════════════════════════════════════════
def draw_pop():
    GA = {**BASE_GRAPH, "ranksep": "0.90", "nodesep": "0.70"}

    # ── pop_front ────────────────────────────────────────────────
    gpf = graphviz.Digraph("pop_front", graph_attr=GA)
    term, proc, dec, io, ann, e, ae = mk(gpf)

    term("ppf_s",  "начало")
    dec ("ppf_em", "дек пустой?")
    io  ("ppf_er", "вывести сообщение об ошибке")
    io  ("ppf_r0", "return -1")
    term("ppf_e0", "конец")
    proc("ppf_h",  "запомнить текущую голову;\nсчитать значение;\nсдвинуть голову на следующий узел")
    dec ("ppf_1",  "новая голова\nсуществует?")
    proc("ppf_np", "обнулить ссылку prev\nновой головы")
    proc("ppf_bt", "дек стал пустым —\nобнулить указатель на хвост")
    proc("ppf_f",  "освободить память удалённого узла;\nуменьшить счётчик элементов")
    io  ("ppf_r",  "return 0")
    term("ppf_e",  "конец")

    ann("ppf_ah",  "old = d->front;\n*out = old->value;\nd->front = old->next")
    ann("ppf_a1",  "d->front != NULL")
    ann("ppf_anp", "d->front->prev = NULL")
    ann("ppf_abt", "d->back = NULL")
    ann("ppf_af",  "free(old);\nd->size--")

    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppf_h");  sg.node("ppf_ah")
    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppf_1");  sg.node("ppf_a1")
    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppf_np"); sg.node("ppf_anp")
    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppf_bt"); sg.node("ppf_abt")
    with gpf.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppf_f");  sg.node("ppf_af")

    e("ppf_s","ppf_em")
    e("ppf_em","ppf_er", lbl="да");  e("ppf_er","ppf_r0"); e("ppf_r0","ppf_e0")
    e("ppf_em","ppf_h",  lbl="нет")
    e("ppf_h","ppf_1")
    e("ppf_1","ppf_np",  lbl="да");  e("ppf_np","ppf_f")
    e("ppf_1","ppf_bt",  lbl="нет"); e("ppf_bt","ppf_f")
    e("ppf_f","ppf_r"); e("ppf_r","ppf_e")

    ae("ppf_h","ppf_ah"); ae("ppf_1","ppf_a1")
    ae("ppf_np","ppf_anp"); ae("ppf_bt","ppf_abt"); ae("ppf_f","ppf_af")
    save(gpf, "5c_pop_front")

    # ── pop_back ─────────────────────────────────────────────────
    gpb = graphviz.Digraph("pop_back", graph_attr=GA)
    term, proc, dec, io, ann, e, ae = mk(gpb)

    term("ppb_s",  "начало")
    dec ("ppb_em", "дек пустой?")
    io  ("ppb_er", "вывести сообщение об ошибке")
    io  ("ppb_r0", "return -1")
    term("ppb_e0", "конец")
    proc("ppb_h",  "запомнить текущий хвост;\nсчитать значение;\nсдвинуть хвост на предыдущий узел")
    dec ("ppb_1",  "новый хвост\nсуществует?")
    proc("ppb_nb", "обнулить ссылку next\nнового хвоста")
    proc("ppb_fr", "дек стал пустым —\nобнулить указатель на голову")
    proc("ppb_f",  "освободить память удалённого узла;\nуменьшить счётчик элементов")
    io  ("ppb_r",  "return 0")
    term("ppb_e",  "конец")

    ann("ppb_ah",  "old = d->back;\n*out = old->value;\nd->back = old->prev")
    ann("ppb_a1",  "d->back != NULL")
    ann("ppb_anb", "d->back->next = NULL")
    ann("ppb_afr", "d->front = NULL")
    ann("ppb_af",  "free(old);\nd->size--")

    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppb_h");  sg.node("ppb_ah")
    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppb_1");  sg.node("ppb_a1")
    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppb_nb"); sg.node("ppb_anb")
    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppb_fr"); sg.node("ppb_afr")
    with gpb.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ppb_f");  sg.node("ppb_af")

    e("ppb_s","ppb_em")
    e("ppb_em","ppb_er", lbl="да");  e("ppb_er","ppb_r0"); e("ppb_r0","ppb_e0")
    e("ppb_em","ppb_h",  lbl="нет")
    e("ppb_h","ppb_1")
    e("ppb_1","ppb_nb",  lbl="да");  e("ppb_nb","ppb_f")
    e("ppb_1","ppb_fr",  lbl="нет"); e("ppb_fr","ppb_f")
    e("ppb_f","ppb_r"); e("ppb_r","ppb_e")

    ae("ppb_h","ppb_ah"); ae("ppb_1","ppb_a1")
    ae("ppb_nb","ppb_anb"); ae("ppb_fr","ppb_afr"); ae("ppb_f","ppb_af")
    save(gpb, "5d_pop_back")


# ═══════════════════════════════════════════════════════════════
#  6. wright_search()
# ═══════════════════════════════════════════════════════════════
def draw_wright_search():
    g = graphviz.Digraph("wright", graph_attr={**BASE_GRAPH,
        "ranksep": "0.32", "nodesep": "0.60"})
    term, proc, dec, io, ann, e, ae = mk(g)

    term("s",    "начало")
    proc("ini",  "инициализировать счётчик просмотров,\nустановить позицию «не найден»")
    dec ("emp",  "дек пустой?")
    io  ("rn",   "return NULL  (искать не в чём)")
    term("en",   "конец")

    proc("mid",  "ШАГ 1:\nвыйти на средний элемент —\nпройти size/2 шагов от головы по next")
    proc("cmp",  "ШАГ 2:\nсравнить ключ со средним элементом\n(увеличить счётчик просмотров)")
    dec ("eq",   "ключ равен\nзначению?")
    io  ("rfnd", "записать позицию;\nreturn узел  (найден)")
    term("efnd", "конец")

    dec ("lt",   "ключ меньше\nсреднего?")
    proc("left", "ШАГ 3а:\nдвигаться влево по prev,\nсчитать просмотры,\nпока value > ключа")
    proc("rght", "ШАГ 3б:\nдвигаться вправо по next,\nсчитать просмотры,\nпока value < ключа")
    proc("chk",  "ШАГ 4:\nесли узел существует —\nсравнить value с ключом\n(увеличить счётчик просмотров)")
    dec ("fnd",  "узел существует\nи value == ключу?")
    io  ("rfnd2","записать позицию;\nreturn узел  (найден)")
    term("efnd2","конец")
    io  ("rnl",  "return NULL  (ключ отсутствует)")
    term("enl",  "конец")

    ann("a_ini",  "*views=0; *pos=-1")
    ann("a_emp",  "d->size == 0")
    ann("a_mid",  "cur=d->front; idx=0;\nmid=d->size/2;\nwhile(idx<mid){\n  cur=cur->next; idx++;}")
    ann("a_cmp",  "(*views)++")
    ann("a_lt",   "key < cur->value")
    ann("a_left", "cur=cur->prev; idx--;\nwhile(cur && cur->value>key){\n  (*views)++;\n  cur=cur->prev; idx--;}")
    ann("a_rght", "cur=cur->next; idx++;\nwhile(cur && cur->value<key){\n  (*views)++;\n  cur=cur->next; idx++;}")

    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("ini");  sg.node("a_ini")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("emp");  sg.node("a_emp")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("mid");  sg.node("a_mid")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("cmp");  sg.node("a_cmp")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("lt");   sg.node("a_lt")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("left"); sg.node("a_left")
    with g.subgraph() as sg:
        sg.attr(rank="same"); sg.node("rght"); sg.node("a_rght")

    e("s","ini"); e("ini","emp")
    e("emp","rn",  lbl="да");  e("rn","en")
    e("emp","mid", lbl="нет")
    e("mid","cmp"); e("cmp","eq")
    e("eq","rfnd", lbl="да");  e("rfnd","efnd")
    e("eq","lt",   lbl="нет")
    e("lt","left", lbl="да")
    e("lt","rght", lbl="нет")
    e("left","chk"); e("rght","chk")
    e("chk","fnd"); e("fnd","rfnd2", lbl="да"); e("rfnd2","efnd2")
    e("fnd","rnl", lbl="нет");  e("rnl","enl")

    ae("ini","a_ini"); ae("emp","a_emp"); ae("mid","a_mid")
    ae("cmp","a_cmp"); ae("lt","a_lt")
    ae("left","a_left"); ae("rght","a_rght")
    save(g, "6_wright_search")


print("Генерация блок-схем lr3...")
draw_main()
draw_read_file()
draw_radix_sort()
draw_counting_sort_deque()
draw_push()
draw_pop()
draw_wright_search()
print("Готово.")
