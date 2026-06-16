#include "stack.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BASE 10
#define STACK_INIT_CAP 8

/* ===================== РЕАЛИЗАЦИЯ СТЕКА ===================== */

void stack_init(Stack *s)
{
    s->data = NULL;
    s->top = -1;
    s->capacity = 0;
    /* обнуляем структуру стека */
}

int stack_is_empty(const Stack *s)
{
    return s->top == -1;  /* проверка пустоты по top */
}

int stack_size(const Stack *s)
{
    return s->top + 1;  /* количество элементов */
}

int stack_push(Stack *s, int value)
{
    if (s->top + 1 >= s->capacity) {
        int new_cap = (s->capacity == 0) ? STACK_INIT_CAP : s->capacity * 2;
        int *tmp = (int *)realloc(s->data, new_cap * sizeof(int));
        if (!tmp) {
            fprintf(stderr, "Ошибка: не удалось выделить память для стека\n");
            return -1;
        }
        s->data = tmp;
        s->capacity = new_cap;  /* увеличиваем ёмкость */
    }
    s->top++;
    s->data[s->top] = value;
    return 0;  /* элемент добавлен на вершину */
}

int stack_pop(Stack *s, int *out)
{
    if (stack_is_empty(s)) {
        fprintf(stderr, "Ошибка: стек пуст\n");
        return -1;
    }
    *out = s->data[s->top];  /* берём значение с вершины */
    s->top--;
    return 0;  /* сняли элемент */
}

int stack_peek(const Stack *s, int *out)
{
    if (stack_is_empty(s)) {
        fprintf(stderr, "Ошибка: стек пуст\n");
        return -1;
    }
    *out = s->data[s->top];  /* смотрим вершину без удаления */
    return 0;
}

void stack_free(Stack *s)
{
    free(s->data);
    s->data = NULL;
    s->top = -1;
    s->capacity = 0;  /* освобождаем буфер */
}

/* ===================== ВСПОМОГАТЕЛЬНЫЕ ДЛЯ СОРТИРОВКИ ===================== */

static int find_max(const Stack *s)
{
    if (stack_is_empty(s)) return 0;
    int max_val = s->data[0];
    for (int i = 1; i <= s->top; i++) {
        if (s->data[i] > max_val) {
            max_val = s->data[i];  /* обновляем максимум */
        }
    }
    return max_val;  /* максимум определяет число разрядов */
}

/* Один проход цифровой сортировки по разряду exp (через стеки-корзины) */
static void counting_sort_by_stack(Stack *s, int exp)
{
    if (stack_size(s) <= 1) return;

    Stack buckets[BASE];
    for (int j = 0; j < BASE; j++) {
        stack_init(&buckets[j]);  /* инициализируем 10 корзин */
    }

    /* реверс, чтобы обрабатывать от дна (как будто в порядке поступления) */
    Stack rev;
    stack_init(&rev);
    int val;
    while (!stack_is_empty(s)) {
        stack_pop(s, &val);
        stack_push(&rev, val);  /* перекладываем в обратном порядке */
    }

    /* распределение по корзинам */
    while (!stack_is_empty(&rev)) {
        stack_pop(&rev, &val);
        int digit = (val / exp) % BASE;
        stack_push(&buckets[digit], val);  /* кидаем в нужную корзину */
    }
    stack_free(&rev);  /* rev больше не нужен */

    /* сбор из корзин 0..9 с восстановлением порядка через temp */
    for (int j = 0; j < BASE; j++) {
        Stack temp;
        stack_init(&temp);

        while (!stack_is_empty(&buckets[j])) {
            stack_pop(&buckets[j], &val);
            stack_push(&temp, val);  /* реверс содержимого корзины */
        }

        while (!stack_is_empty(&temp)) {
            stack_pop(&temp, &val);
            stack_push(s, val);  /* второй реверс восстанавливает порядок */
        }
        stack_free(&temp);  /* temp для этой корзины готов */
    }

    for (int j = 0; j < BASE; j++) {
        stack_free(&buckets[j]);  /* освобождаем корзины */
    }
}

/* сортировка неотрицательных (определяет число проходов по max) */
static void radix_sort_nonneg(Stack *s)
{
    if (stack_size(s) <= 1) return;

    int max_val = find_max(s);
    for (int exp = 1; max_val / exp > 0; exp *= BASE) {
        counting_sort_by_stack(s, exp);  /* проход по разряду */
    }
}

/* ===================== ОСНОВНАЯ ЦИФРОВАЯ СОРТИРОВКА ===================== */

/* Основная цифровая сортировка стека (с обработкой отрицательных) */
void radix_sort(Stack *s)
{
    int n = stack_size(s);
    if (n <= 1) return;

    Stack neg, pos;
    stack_init(&neg);
    stack_init(&pos);  /* готовим два вспомогательных стека */

    int val;
    while (!stack_is_empty(s)) {
        stack_pop(s, &val);
        if (val < 0) {
            stack_push(&neg, -val);  /* сохраняем модуль */
        } else {
            stack_push(&pos, val);
        }
    }

    radix_sort_nonneg(&neg);
    radix_sort_nonneg(&pos);  /* сортируем отдельно */

    /* собираем отрицательные (большие модули первыми → самые отрицательные внизу) */
    while (!stack_is_empty(&neg)) {
        stack_pop(&neg, &val);
        stack_push(s, -val);  /* первое push — самое отрицательное в дно */
    }

    /* реверс положительных, чтобы маленькие шли первыми после отрицательных */
    Stack pos_rev;
    stack_init(&pos_rev);
    while (!stack_is_empty(&pos)) {
        stack_pop(&pos, &val);
        stack_push(&pos_rev, val);  /* реверс pos */
    }
    while (!stack_is_empty(&pos_rev)) {
        stack_pop(&pos_rev, &val);
        stack_push(s, val);  /* теперь по возрастанию */
    }
    stack_free(&pos_rev);

    stack_free(&neg);
    stack_free(&pos);  /* чистим вспомогательные */
}

/* ===================== ПОИСК БОЙЕРА-МУРА ===================== */

/* Строит текст ";число;число;..." от дна к вершине (для поиска целыми токенами) */
static char *build_text_from_stack(const Stack *s)
{
    if (stack_is_empty(s)) {
        char *empty = (char *)malloc(3);
        if (empty) strcpy(empty, ";;");
        return empty;
    }

    /* Оценим размер буфера */
    size_t buf_size = (size_t)stack_size(s) * 16 + 4;
    char *text = (char *)malloc(buf_size);
    if (!text) return NULL;

    text[0] = '\0';
    strcat(text, ";");  /* ведущий разделитель */

    for (int i = 0; i <= s->top; i++) {
        char numstr[32];
        snprintf(numstr, sizeof(numstr), "%d", s->data[i]);
        strcat(text, numstr);
        strcat(text, ";");  /* каждый элемент + разделитель */
    }
    return text;  /* текст вида ;val;val;... */
}

/* Преобразует позицию совпадения в тексте в индекс числа в стеке (0 = дно) */
static int find_element_index(const Stack *s, int match_start)
{
    if (match_start < 0 || stack_is_empty(s)) return -1;

    int offset = 0;   /* позиция открывающего ';' текущего токена */

    for (int i = 0; i <= s->top; i++) {
        if (match_start == offset) {
            return i;  /* нашли, какой по счёту элемент */
        }

        char numstr[32];
        int dlen = snprintf(numstr, sizeof(numstr), "%d", s->data[i]);

        /* Продвигаемся: цифры + замыкающий ';' (он же открывающий для следующего) */
        offset += dlen + 1;  /* двигаем указатель на следующий токен */
    }
    return -1;
}

/* Таблица плохого символа (bad character) для алфавита 256 */
static void compute_bad_char(const char *pat, int m, int bad[256])
{
    for (int i = 0; i < 256; i++) {
        bad[i] = -1;
    }
    for (int i = 0; i < m; i++) {
        bad[(unsigned char)pat[i]] = i;
    }
}

/* Классический Бойер-Мур с эвристикой плохого символа.
 * Возвращает индекс первого вхождения или -1.
 * *views увеличивается на каждое сравнение символов. */
static int boyer_moore(const char *txt, int n, const char *pat, int m, int *views)
{
    *views = 0;
    if (m == 0) return 0;
    if (n < m) return -1;

    int bad[256];
    compute_bad_char(pat, m, bad);  /* предобработка таблицы плохого символа */

    int shift = 0;
    while (shift <= n - m) {
        int j = m - 1;

        /* Сравниваем с конца паттерна */
        while (j >= 0 && txt[shift + j] == pat[j]) {
            (*views)++;
            j--;
        }

        if (j < 0) {
            /* Полное совпадение */
            return shift;
        } else {
            (*views)++;
        }

        /* Сдвиг по плохому символу */
        int bad_char = (unsigned char)txt[shift + j];
        int bad_idx = bad[bad_char];
        int move = (j - bad_idx > 1) ? (j - bad_idx) : 1;
        shift += move;  /* пропускаем по эвристике */
    }
    return -1;
}

/* Поиск Бойера-Мура: ищет подпоследовательность keys[0..keys_len-1] в стеке.
 * Возвращает позицию первого элемента совпадения или -1. */
int boyer_moore_search(const Stack *s, const int *keys, int keys_len, int *views)
{
    *views = 0;
    if (keys_len <= 0) return -1;

    /* Строим паттерн ";k0;k1;...;kN-1;" — разделители гарантируют поиск целых токенов */
    size_t pat_size = (size_t)keys_len * 16 + 4;
    char *pat = (char *)malloc(pat_size);
    if (!pat) return -1;

    pat[0] = '\0';
    strcat(pat, ";");
    for (int i = 0; i < keys_len; i++) {
        char numstr[32];
        snprintf(numstr, sizeof(numstr), "%d", keys[i]);
        strcat(pat, numstr);
        strcat(pat, ";");
    }

    char *text = build_text_from_stack(s);
    if (!text) {
        free(pat);
        return -1;
    }

    int n = (int)strlen(text);
    int m = (int)strlen(pat);

    int char_pos = boyer_moore(text, n, pat, m, views);  /* запускаем BM */
    int elem_idx = (char_pos >= 0) ? find_element_index(s, char_pos) : -1;

    free(text);
    free(pat);
    return elem_idx;  /* позиция начала подпоследовательности в стеке */
}

/* ===================== КРАСНО-ЧЁРНОЕ ДЕРЕВО ===================== */

static RBNode *create_node(int value)
{
    RBNode *node = (RBNode *)malloc(sizeof(RBNode));
    if (!node) {
        fprintf(stderr, "Ошибка: malloc для узла RBT\n");
        exit(EXIT_FAILURE);
    }
    node->value = value;
    node->color = RED;
    node->left = NULL;
    node->right = NULL;
    node->parent = NULL;
    return node;  /* новый красный узел */
}

static void left_rotate(RBTree *t, RBNode *x)
{
    RBNode *y = x->right;
    x->right = y->left;
    if (y->left != NULL) {
        y->left->parent = x;
    }
    y->parent = x->parent;
    if (x->parent == NULL) {
        t->root = y;
    } else if (x == x->parent->left) {
        x->parent->left = y;
    } else {
        x->parent->right = y;
    }
    y->left = x;
    x->parent = y;  /* левый поворот выполнен */
}  /* левый поворот */

static void right_rotate(RBTree *t, RBNode *y)
{
    RBNode *x = y->left;
    y->left = x->right;
    if (x->right != NULL) {
        x->right->parent = y;
    }
    x->parent = y->parent;
    if (y->parent == NULL) {
        t->root = x;
    } else if (y == y->parent->right) {
        y->parent->right = x;
    } else {
        y->parent->left = x;
    }
    x->right = y;
    y->parent = x;  /* структура связей обновлена */
}  /* правый поворот */

static void insert_fixup(RBTree *t, RBNode *z)
{
    while (z->parent != NULL && z->parent->color == RED) {
        RBNode *gp = z->parent->parent;
        if (z->parent == gp->left) {
            RBNode *y = gp->right; /* uncle */
            if (y != NULL && y->color == RED) {
                /* случай 1: дядя красный — перекрашиваем */
                z->parent->color = BLACK;
                y->color = BLACK;
                gp->color = RED;
                z = gp;
            } else {
                if (z == z->parent->right) {
                    /* случай 2: левый поворот */
                    z = z->parent;
                    left_rotate(t, z);
                }
                /* случай 3: правый поворот + перекраска */
                z->parent->color = BLACK;
                gp->color = RED;
                right_rotate(t, gp);
            }
        } else {
            RBNode *y = gp->left;
            if (y != NULL && y->color == RED) {
                z->parent->color = BLACK;
                y->color = BLACK;
                gp->color = RED;
                z = gp;
            } else {
                if (z == z->parent->left) {
                    z = z->parent;
                    right_rotate(t, z);
                }
                z->parent->color = BLACK;
                gp->color = RED;
                left_rotate(t, gp);
            }
        }
    }
    t->root->color = BLACK;  /* корень всегда чёрный после фикса */
}

void rbtree_init(RBTree *t)
{
    t->root = NULL;  /* пустое дерево */
}

void rbtree_insert(RBTree *t, int value)  /* вставка с балансировкой */
{
    RBNode *z = create_node(value);
    RBNode *y = NULL;
    RBNode *x = t->root;

    while (x != NULL) {
        y = x;
        if (z->value < x->value) {
            x = x->left;
        } else {
            x = x->right;
        }
    }  /* нашли место для вставки */

    z->parent = y;
    if (y == NULL) {
        t->root = z;
    } else if (z->value < y->value) {
        y->left = z;
    } else {
        y->right = z;
    }

    insert_fixup(t, z);  /* восстанавливаем свойства RBT */
}

static void inorder_helper(const RBNode *node)
{
    if (node == NULL) return;
    inorder_helper(node->left);
    printf("%d ", node->value);
    inorder_helper(node->right);
}

void rbtree_inorder_print(const RBTree *t)
{
    inorder_helper(t->root);
    printf("\n");
}

/* Рекурсивно печатает поддерево с отступами.
 * Обход: правое поддерево → текущий узел → левое поддерево.
 * Такой порядок даёт «повёрнутое» дерево: правые ветви рисуются
 * вверху экрана, левые — внизу, корень — посередине.
 *
 * node    — текущий узел (никогда не NULL при входе)
 * prefix  — строка-отступ, накопленная от корня до родителя
 * is_left — 1, если node является левым ребёнком своего родителя
 *           (влияет на выбор символа ветви и продолжения отступа)
 */
static void print_visual_helper(const RBNode *node, const char *prefix, int is_left)
{
    char new_prefix[512];

    /* --- правое поддерево (печатается выше текущего узла) --- */
    if (node->right != NULL) {
        /* Если текущий узел — левый ребёнок, правее него будет
         * вертикальная черта │, иначе просто пробелы. */
        snprintf(new_prefix, sizeof(new_prefix), "%s%s", prefix,
                 is_left ? "│   " : "    ");
        print_visual_helper(node->right, new_prefix, 0);
    }

    /* --- сам узел --- */
    /* ┌── обозначает правого ребёнка (ветвь идёт вниз-влево на экране),
     * └── обозначает левого ребёнка  (ветвь идёт вверх-влево).
     * Формат метки: [R:42] или [B:42] — цвет и значение. */
    printf("%s%s[%c:%d]\n",
           prefix,
           is_left ? "└── " : "┌── ",
           node->color == RED ? 'R' : 'B',
           node->value);

    /* --- левое поддерево (печатается ниже текущего узла) --- */
    if (node->left != NULL) {
        /* Если текущий узел — правый ребёнок, левее него вертикальная
         * черта │ (чтобы показать, что ветвь ещё продолжается вниз).
         * Если левый — пробелы, ветвь уже закрыта символом └──. */
        snprintf(new_prefix, sizeof(new_prefix), "%s%s", prefix,
                 is_left ? "    " : "│   ");
        print_visual_helper(node->left, new_prefix, 1);
    }
}

/* Печатает всё дерево целиком.
 * Корень выводится без отступа и без символа ветви.
 * Правое поддерево — выше корня на экране (отступ 4 пробела).
 * Левое поддерево  — ниже  корня на экране (отступ 4 пробела).
 *
 * Пример вывода для дерева {20, 10, 30}:
 *     ┌── [R:30]
 *     [B:20]
 *     └── [R:10]
 */
void rbtree_print_visual(const RBTree *t)
{
    if (t->root == NULL) { printf("(пусто)\n"); return; }

    /* правое поддерево корня — is_left=0, значит будет ┌── */
    if (t->root->right != NULL)
        print_visual_helper(t->root->right, "    ", 0);

    /* сам корень — без префикса и без символа ветви */
    printf("[%c:%d]\n",
           t->root->color == RED ? 'R' : 'B',
           t->root->value);

    /* левое поддерево корня — is_left=1, значит будет └── */
    if (t->root->left != NULL)
        print_visual_helper(t->root->left, "    ", 1);
}

static void free_helper(RBNode *node)
{
    if (node == NULL) return;
    free_helper(node->left);
    free_helper(node->right);
    free(node);
}

void rbtree_free(RBTree *t)
{
    free_helper(t->root);
    t->root = NULL;
}