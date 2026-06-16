#ifndef DEQUE_H
#define DEQUE_H

/* Узел двусвязного списка */
typedef struct DNode {
    int           value;  /* хранимое число */
    struct DNode *prev;   /* предыдущий узел (NULL у головы) */
    struct DNode *next;   /* следующий узел (NULL у хвоста) */
} DNode;

/* Дек на базе двусвязного списка:
 * вставка и удаление с обоих концов за O(1) */
typedef struct {
    DNode *front;  /* голова дека */
    DNode *back;   /* хвост дека */
    int    size;   /* число элементов */
} Deque;

/* Операции дека */
void deque_init(Deque *d);
int  deque_is_empty(const Deque *d);
int  deque_push_front(Deque *d, int value);
int  deque_push_back(Deque *d, int value);
int  deque_pop_front(Deque *d, int *out);
int  deque_pop_back(Deque *d, int *out);
void deque_free(Deque *d);

/* Цифровая сортировка (LSD Radix Sort) дека по возрастанию,
 * поддерживает отрицательные числа */
void radix_sort(Deque *d);

/* Поиск подстроки методом Райта в отсортированном по возрастанию деке.
 * keys — массив из m элементов (искомая последовательность соседних значений).
 * Возвращает первый узел подстроки (или NULL), в *pos — его позицию от 0 (или -1),
 * в *views — число просмотренных узлов */
const DNode *wright_search(const Deque *d, const int *keys, int m, int *pos, int *views);

#endif
