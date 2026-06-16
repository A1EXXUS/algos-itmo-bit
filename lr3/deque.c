#include "deque.h"
#include <stdio.h>
#include <stdlib.h>

#define BASE 10  /* основание системы счисления для цифровой сортировки */

/* ──────────────────── Операции дека ──────────────────── */

/* Инициализация пустого дека */
void deque_init(Deque *d)
{
    d->front = NULL;
    d->back  = NULL;
    d->size  = 0;
}

/* Проверка дека на пустоту */
int deque_is_empty(const Deque *d)
{
    return d->size == 0;
}

/* Добавление элемента в голову дека */
int deque_push_front(Deque *d, int value)
{
    /* создаём новый узел */
    DNode *node = (DNode *)malloc(sizeof(DNode));
    if (!node) {
        fprintf(stderr, "Ошибка: malloc вернул NULL\n");
        return -1;
    }

    /* новый узел становится головой: prev пуст, next — прежняя голова */
    node->value = value;
    node->prev  = NULL;
    node->next  = d->front;

    if (d->front != NULL)
        d->front->prev = node;  /* связываем прежнюю голову с новым узлом */
    else
        d->back = node;         /* дек был пуст — узел также является хвостом */

    d->front = node;
    d->size++;
    return 0;
}

/* Добавление элемента в хвост дека */
int deque_push_back(Deque *d, int value)
{
    /* создаём новый узел */
    DNode *node = (DNode *)malloc(sizeof(DNode));
    if (!node) {
        fprintf(stderr, "Ошибка: malloc вернул NULL\n");
        return -1;
    }

    /* новый узел становится хвостом: next пуст, prev — прежний хвост */
    node->value = value;
    node->next  = NULL;
    node->prev  = d->back;

    if (d->back != NULL)
        d->back->next = node;  /* связываем прежний хвост с новым узлом */
    else
        d->front = node;       /* дек был пуст — узел также является головой */

    d->back = node;
    d->size++;
    return 0;
}

/* Извлечение элемента из головы дека */
int deque_pop_front(Deque *d, int *out)
{
    if (d->size == 0) {
        fprintf(stderr, "Ошибка: дек пуст\n");
        return -1;
    }

    /* запоминаем голову и её значение, сдвигаем голову на следующий узел */
    DNode *node = d->front;
    *out = node->value;
    d->front = node->next;

    if (d->front != NULL)
        d->front->prev = NULL;  /* новая голова не имеет предыдущего узла */
    else
        d->back = NULL;         /* извлекли последний элемент — дек пуст */

    free(node);
    d->size--;
    return 0;
}

/* Извлечение элемента из хвоста дека */
int deque_pop_back(Deque *d, int *out)
{
    if (d->size == 0) {
        fprintf(stderr, "Ошибка: дек пуст\n");
        return -1;
    }

    /* запоминаем хвост и его значение, сдвигаем хвост на предыдущий узел */
    DNode *node = d->back;
    *out = node->value;
    d->back = node->prev;

    if (d->back != NULL)
        d->back->next = NULL;  /* новый хвост не имеет следующего узла */
    else
        d->front = NULL;       /* извлекли последний элемент — дек пуст */

    free(node);
    d->size--;
    return 0;
}

/* Освобождение всех узлов дека */
void deque_free(Deque *d)
{
    /* проходим по списку, освобождая каждый узел */
    DNode *cur = d->front;
    while (cur != NULL) {
        DNode *tmp = cur;
        cur = cur->next;
        free(tmp);
    }
    d->front = NULL;
    d->back  = NULL;
    d->size  = 0;
}

/* ──────────────── Цифровая сортировка дека ──────────────── */

/* Поиск максимального значения в непустом деке —
 * определяет число разрядов (проходов сортировки) */
static int find_max(const Deque *d)
{
    int max = d->front->value;
    const DNode *cur = d->front->next;
    while (cur != NULL) {
        if (cur->value > max)
            max = cur->value;
        cur = cur->next;
    }
    return max;
}

/* Один проход сортировки по разряду exp (1, 10, 100, ...).
 * Вместо массивов используются 10 деков-корзин — по одному на цифру от 0 до 9 */
static void counting_sort_by_deque(Deque *d, int exp)
{
    Deque buckets[BASE];
    int value;

    /* инициализируем корзины */
    for (int j = 0; j < BASE; j++)
        deque_init(&buckets[j]);

    /* фаза распределения: извлекаем числа из дека
     * и раскладываем по корзинам согласно текущей цифре */
    while (!deque_is_empty(d)) {
        deque_pop_front(d, &value);
        int digit = (value / exp) % BASE;  /* цифра текущего разряда */
        deque_push_back(&buckets[digit], value);
    }

    /* фаза сбора: возвращаем числа в дек, обходя корзины от 0 до 9.
     * Порядок FIFO (push_back/pop_front) обеспечивает устойчивость */
    for (int j = 0; j < BASE; j++) {
        while (!deque_is_empty(&buckets[j])) {
            deque_pop_front(&buckets[j], &value);
            deque_push_back(d, value);
        }
    }
}

/* Цифровая сортировка дека из неотрицательных чисел */
static void radix_sort_nonneg(Deque *d)
{
    if (d->size <= 1) return;  /* нечего сортировать */

    /* проходы по разрядам от младшего к старшему,
     * пока в максимуме остаются цифры */
    int max_val = find_max(d);
    for (int exp = 1; max_val / exp > 0; exp *= BASE)
        counting_sort_by_deque(d, exp);
}

/* Цифровая сортировка дека с поддержкой отрицательных чисел */
void radix_sort(Deque *d)
{
    if (d->size <= 1) return;  /* нечего сортировать */

    /* вспомогательные деки: модули отрицательных и положительные числа */
    Deque neg, pos;
    deque_init(&neg);
    deque_init(&pos);

    /* разделяем исходный дек на два по знаку */
    int value;
    while (!deque_is_empty(d)) {
        deque_pop_front(d, &value);
        if (value < 0)
            deque_push_back(&neg, -value);  /* храним модуль */
        else
            deque_push_back(&pos, value);
    }

    /* сортируем обе части как неотрицательные */
    radix_sort_nonneg(&neg);
    radix_sort_nonneg(&pos);

    /* собираем результат: отрицательные идут первыми.
     * Дек neg отсортирован по модулю, поэтому берём с хвоста:
     * наибольший модуль даёт наименьшее отрицательное число */
    while (!deque_is_empty(&neg)) {
        deque_pop_back(&neg, &value);
        deque_push_back(d, -value);  /* возвращаем знак */
    }

    /* положительные добавляем в исходном (возрастающем) порядке */
    while (!deque_is_empty(&pos)) {
        deque_pop_front(&pos, &value);
        deque_push_back(d, value);
    }
}

/* ──────────────── Поиск подстроки методом Райта ──────────────── */

/* Поиск подстроки keys[0..m-1] в отсортированном деке.
 * Шаг 1: методом Райта находим узел со значением keys[0] —
 *   стартуем с середины и движемся по prev/next до нужного значения.
 * Шаг 2: откатываемся до первого вхождения keys[0] (при дубликатах
 *   Райт мог попасть в середину серии).
 * Шаг 3: для каждого вхождения keys[0] последовательно проверяем,
 *   совпадают ли следующие m-1 узлов с keys[1..m-1].
 * Возвращает первый узел найденной подстроки или NULL. */
const DNode *wright_search(const Deque *d, const int *keys, int m,
                           int *pos, int *views)
{
    *views = 0;
    *pos   = -1;
    if (d->size == 0 || m <= 0)
        return NULL;

    int key = keys[0];

    /* шаг 1а: выходим на средний элемент списка */
    const DNode *cur = d->front;
    int idx = 0;
    int mid = d->size / 2;
    while (idx < mid) {
        cur = cur->next;
        idx++;
    }

    /* шаг 1б: сравниваем первый ключ со средним элементом и
     * двигаемся влево или вправо, пока значения «загораживают» ключ */
    (*views)++;
    if (key < cur->value) {
        /* идём к голове по prev */
        cur = cur->prev;
        idx--;
        while (cur != NULL && cur->value > key) {
            (*views)++;
            cur = cur->prev;
            idx--;
        }
        if (cur == NULL) return NULL;
        (*views)++;
        if (cur->value != key) return NULL;
    } else if (key > cur->value) {
        /* идём к хвосту по next */
        cur = cur->next;
        idx++;
        while (cur != NULL && cur->value < key) {
            (*views)++;
            cur = cur->next;
            idx++;
        }
        if (cur == NULL) return NULL;
        (*views)++;
        if (cur->value != key) return NULL;
    }
    /* cur->value == key */

    /* шаг 2: откатываемся до первого вхождения keys[0] */
    while (cur->prev != NULL && cur->prev->value == key) {
        cur = cur->prev;
        idx--;
    }

    /* шаг 3: перебираем все вхождения keys[0], проверяя остаток подстроки */
    while (cur != NULL && cur->value == key) {
        const DNode *check = cur;
        int ok = 1;
        for (int i = 1; i < m; i++) {
            check = check->next;
            (*views)++;
            if (check == NULL || check->value != keys[i]) {
                ok = 0;
                break;
            }
        }
        if (ok) {
            *pos = idx;
            return cur;  /* подстрока найдена */
        }
        cur = cur->next;
        idx++;
    }

    return NULL;  /* подстрока в деке не найдена */
}
