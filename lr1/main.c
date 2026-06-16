#include <stdio.h>
#include <stdlib.h>

#include "radix_sort.h"

/* Вывести меню и вернуть выбор пользователя (1, 2 или 3). */
static int show_menu(void)
{
    int choice = 0; /* +1 присваивание */

    printf("\n╔══════════════════════════════════════╗\n");
    printf("║   Цифровая сортировка (Radix Sort)   ║\n");
    printf("╠══════════════════════════════════════╣\n");
    printf("║  Выберите структуру данных:          ║\n");
    printf("║  1. Статический массив               ║\n");
    printf("║  2. Динамический массив              ║\n");
    printf("║  3. Вектор (авторасширяемый)         ║\n");
    printf("╚══════════════════════════════════════╝\n");
    printf("Ваш выбор: ");

    /* Цикл до тех пор, пока не введут корректное значение */
    while (scanf("%d", &choice) != 1 || choice < 1 || choice > 3) { /* +1 вызов, +3 сравнения */
        int c;
        while ((c = getchar()) != '\n' && c != EOF); /* очистка stdin */
        printf("Неверный ввод. Введите 1, 2 или 3: ");
    }

    return choice; /* +1 выход */
}
/* Итого (корректный ввод с первой попытки): 6 операций
   (1 присв. + 1 вызов + 3 сравн. + 1 выход) */

/* Получить указатель на данные и размер из выбранной структуры. */
static void get_array_ptr(int mode,
                           StaticArray *sa, DynamicArray *da, Vector *v,
                           int **arr_out, int *n_out)
{
    if (mode == 1) {           /* +1 сравнение */
        *arr_out = sa->data;   /* +2 ссылки (->data), +1 разым. (*arr_out), +1 присваивание */
        *n_out   = sa->size;   /* +2 ссылки (->size), +1 разым. (*n_out),   +1 присваивание */
    } else if (mode == 2) {    /* +1 сравнение */
        *arr_out = da->data;   /* +2 ссылки (->data), +1 разым. (*arr_out), +1 присваивание */
        *n_out   = da->size;   /* +2 ссылки (->size), +1 разым. (*n_out),   +1 присваивание */
    } else {
        *arr_out = v->data;    /* +2 ссылки (->data), +1 разым. (*arr_out), +1 присваивание */
        *n_out   = v->size;    /* +2 ссылки (->size), +1 разым. (*n_out),   +1 присваивание */
    }
}
/* Итого: 10 операций (mode==1: 1 сравн. + 4 + 4 + 1 выход)
          11 операций (mode==2: 1+1 сравн. + 4 + 4 + 1 выход)
          11 операций (mode==3: 1+1 сравн. + 4 + 4 + 1 выход) */

/* Освободить ресурсы выбранной структуры. */
static void cleanup(int mode, DynamicArray *da, Vector *v)
{
    if (mode == 2) dynamic_free(da); /* +1 сравнение[, +1 вызов если истина] */
    if (mode == 3) vector_free(v);   /* +1 сравнение[, +1 вызов если истина] */
}
/* Итого: 3 операции (mode==1: 2 сравн. + 1 выход)
          4 операции (mode==2 или 3: 2 сравн. + 1 вызов + 1 выход) */

int main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr, "Использование: %s <файл>\n", argv[0]);
        return EXIT_FAILURE;
    }
    const char *filename = argv[1]; /* +1 присваивание */

    int mode = show_menu(); /* +1 вызов, +1 присваивание */

    StaticArray  sa;
    DynamicArray da;
    Vector       v;
    static_init(&sa);  /* +1 вызов */
    dynamic_init(&da); /* +1 вызов */
    vector_init(&v);   /* +1 вызов */

    printf("\nЧтение файла '%s'...\n", filename);
    int n = read_file(filename, mode, &sa, &da, &v); /* +1 вызов, +1 присваивание */
    if (n <= 0) {                                       /* +1 сравнение */
        cleanup(mode, &da, &v);
        return EXIT_FAILURE;
    }
    printf("Прочитано %d чисел.\n", n);

    int *arr = NULL; /* +1 присваивание */
    int  sz  = 0;    /* +1 присваивание */
    get_array_ptr(mode, &sa, &da, &v, &arr, &sz); /* +1 вызов */

    printf("\nИсходный массив:\n");
    print_array(arr, sz); /* O(n) */

    printf("\nВыполняем Radix Sort...\n");
    radix_sort(arr, sz); /* O(d*(n+k)) */

    printf("Отсортированный массив:\n");
    print_array(arr, sz); /* O(n) */

    /* Вычисляем d — количество разрядов максимального числа */
    int max_val = find_max(arr, sz);               /* +1 вызов, +1 присваивание */
    int d   = 0;                                   /* +1 присваивание */
    int tmp = (max_val == 0) ? 1 : max_val;        /* +1 сравнение, +1 присваивание */
    while (tmp > 0) { d++; tmp /= 10; }            /* d итераций */

    int ops = 6*sz + 6 + d*(26*sz + 125);
    printf("\n── Оценка сложности ─────────────────────────────\n");
    printf("  n (элементов)           %d\n", sz);
    printf("  max элемент             %d\n", max_val);
    printf("  d (разрядов)            %d\n", d);
    printf("  k (основание, BASE)     10\n");
    printf("  Операций:              %d\n", ops);
    printf("  Доп. ячеек:            %d\n", sz + 10);
    printf("─────────────────────────────────────────────────\n");

    cleanup(mode, &da, &v); /* +1 вызов */
    return EXIT_SUCCESS;    /* +1 возврат */
}
