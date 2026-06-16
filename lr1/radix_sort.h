#ifndef RADIX_SORT_H
#define RADIX_SORT_H

#include <stdlib.h>

/* ───── Статический массив ───── */
#define STATIC_MAX 1000

typedef struct {
    int data[STATIC_MAX]; /* фиксированный буфер */
    int size;             /* фактическое число элементов */
} StaticArray;

/* ───── Динамический массив ───── */
typedef struct {
    int *data; /* указатель на heap-память */
    int size;  /* фактическое число элементов */
} DynamicArray;

/* ───── Вектор (авторасширяемый) ───── */
typedef struct {
    int *data;    /* указатель на heap-память */
    int size;     /* фактическое число элементов */
    int capacity; /* выделенная ёмкость */
} Vector;

/* --- Инициализация --- */
void static_init(StaticArray *sa);
void dynamic_init(DynamicArray *da);
void vector_init(Vector *v);

/* --- Добавление элемента --- */
int  static_push(StaticArray *sa, int val);
void dynamic_push(DynamicArray *da, int val, int n);
void vector_push(Vector *v, int val);

/* --- Освобождение памяти --- */
void dynamic_free(DynamicArray *da);
void vector_free(Vector *v);

/*
 * Цифровая сортировка (Radix Sort, LSD — от младшего разряда к старшему).
 *
 * Принимает массив arr из n целых неотрицательных чисел,
 * сортирует его «на месте» (результат остаётся в arr).
 *
 * Сложность:
 *   Время    — O(d × (n + k))  где d — количество цифр в max-элементе,
 *                                    k — основание (10 для десятичной),
 *                                    n — число элементов.
 *   Память   — O(n + k)        вспомогательный массив + счётчики.
 *
 * При фиксированных d и k сложность линейная: O(n).
 */
void radix_sort(int *arr, int n);

/* Вспомогательная функция: найти максимальный элемент в arr[0..n-1] */
int find_max(const int *arr, int n);

/*
 * Считать числа из файла filename.
 * Способ хранения выбирается параметром mode:
 *   1 — статический массив
 *   2 — динамический массив
 *   3 — вектор
 *
 * Заполняет переданные структуры (только одну, соответствующую mode).
 * Возвращает количество прочитанных чисел или -1 при ошибке.
 */
int read_file(const char *filename, int mode,
              StaticArray *sa, DynamicArray *da, Vector *v);

/* Вывести массив arr из n элементов на экран. */
void print_array(const int *arr, int n);

#endif /* RADIX_SORT_H */
