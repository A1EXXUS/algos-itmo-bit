#include "radix_sort.h"
#include <stdio.h>
#include <stdlib.h>

static int read_file(const char *filename, int **out_arr)
{
    FILE *fp = fopen(filename, "r");  //(2)
    if (!fp) {  //(2)
        fprintf(stderr, "Ошибка: не удалось открыть файл '%s'\n", filename); //(1)
        return -1;  //(1)
    }

    int n = 0, tmp;  //(1)
    while (fscanf(fp, "%d", &tmp) == 1) n++;  //3*(n+1) + 2*n = 5n + 3

    if (n == 0) { //(1)
        fprintf(stderr, "Ошибка: файл '%s' пуст или не содержит чисел\n", filename); //(1)
        fclose(fp); //(1)
        return -1;  //(1)
    }

    rewind(fp); //(1)

    int *arr = (int *)malloc(n * sizeof(int)); //(5)
    if (!arr) {  //(2)
        fprintf(stderr, "Ошибка: не удалось выделить память\n"); //(1)
        fclose(fp); //(1)
        return -1;  //(1)
    }

    for (int i = 0; i < n; i++) {  //(1) + 1*(n+1) + 2*n = 3n + 2
        if (fscanf(fp, "%d", &arr[i]) != 1) {  //(4)
            fprintf(stderr, "Ошибка: неожиданный конец файла\n");  //(1)
            free(arr);  //(1)
            fclose(fp);  //(1)
            return -1;  //(1)
        }
    }
//(3n + 2) + 8*n = 11n + 2


    fclose(fp);  //(1)
    *out_arr = arr;  //(1)
    return n;  //(1)
}
//для функции read_file: (5) + (5n + 3) + (8) + (11n + 2) + (3) = 16n + 21
//Сложность: O(n)


static void print_array(const int *arr, int n)
{
    for (int i = 0; i < n; i++) {  //(1) + 1*(n+1) + 2*n = 3n + 2
        printf("%d", arr[i]);  //(2)
        if (i < n - 1)  //(2)
            printf(" ");  //(1)
    }
    printf("\n");  //(1)
}
//для функции print_array: (3n+2) + (5)*n + (1) = 8n + 3
//Сложность: O(n)

int main(int argc, char *argv[])
{
    if (argc < 2) {  //(1)
        fprintf(stderr, "Использование: %s <файл>\n", argv[0]);  //(2)
        return EXIT_FAILURE;  //(1)
    }
    const char *filename = argv[1];  //(2)

    printf("\nЧтение файла '%s'...\n", filename);  //(1)
    int *arr = NULL;  //(1)
    int  n   = read_file(filename, &arr);  //(3)
    if (n < 0) return EXIT_FAILURE;  //(2)
    printf("Прочитано %d чисел.\n", n);  //(1)

    printf("\nИсходный массив:\n");  //(1)
    print_array(arr, n);  //(1)

    printf("\nВыполняем Radix Sort...\n");  //(1)
    radix_sort(arr, n);  //(1)

    printf("Отсортированный массив:\n");  //(1)
    print_array(arr, n);  //(1)

    int max_val = 0;  //(1)
    for (int i = 0; i < n; i++) {  //(1) + 1*(n+1) + 2*n = 3n + 2
        int v = arr[i] < 0 ? -arr[i] : arr[i];  //(7)
        if (v > max_val) max_val = v;  //(2)
    }
    int d = 0;  //(1)
    int tmp = (max_val == 0) ? 1 : max_val;  //(3)
    while (tmp > 0) { //(1)
        d++;  //(2)
        tmp /= 10; //(2)
    }
//1*(d+1) + 4*d = 5d + 1

    int ops = 23*d*n + 191*d + 7*n + 19;
    printf("\n── Оценка сложности ─────────────────────────────\n"); //(1)
    printf("  n (элементов)           %d\n", n);  //(1)
    printf("  max элемент             %d\n", max_val);  //(1)
    printf("  d (разрядов)            %d\n", d);  //(1)
    printf("  k (основание, BASE)     10\n");  //(1)
    printf("  Операций:              %d\n", ops);  //(1)
    printf("  Доп. ячеек (узлов):    %d\n", n);  //(1)
    printf("─────────────────────────────────────────────────\n");  //(1)

    free(arr);  //(1)
    return EXIT_SUCCESS;  //(1)
}
// T_main (общий случай, neg_n > 0 и pos_n > 0):
//   прямые ops main:     12n + 5d + 35
//   read_file(n):        16n + 21
//   print_array(n) × 2: 16n + 6
//   radix_sort(n):       23d*n + 382d + 25n + 9*neg_n + 8*pos_n + 74
//   ──────────────────────────────────────────────────────────────────
//   Итого: 23d*n + 387d + (69n + 9*neg_n + 8*pos_n) + 136
//          при neg_n~pos_n~n/2: ≈ 23d*n + 387d + 77.5n + 136
// Сложность: O(d*n), при фиксированном d — O(n)
