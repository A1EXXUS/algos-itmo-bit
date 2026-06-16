#include "deque.h"
#include <stdio.h>
#include <stdlib.h>

/* Чтение чисел из файла в дек.
 * Возвращает число прочитанных элементов или -1 при ошибке */
static int read_file(const char *filename, Deque *d)
{
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr, "Ошибка: не удалось открыть файл '%s'\n", filename);
        return -1;
    }

    /* читаем числа по одному и добавляем в хвост дека */
    int tmp;
    while (fscanf(fp, "%d", &tmp) == 1) {
        if (deque_push_back(d, tmp) != 0) {
            deque_free(d);
            fclose(fp);
            return -1;
        }
    }

    fclose(fp);
    if (deque_is_empty(d)) {
        fprintf(stderr, "Ошибка: файл '%s' пуст или не содержит чисел\n", filename);
        return -1;
    }
    return d->size;
}

/* Вывод содержимого дека от головы к хвосту */
static void deque_print(const Deque *d)
{
    const DNode *cur = d->front;
    while (cur != NULL) {
        printf("%d", cur->value);
        if (cur->next != NULL)
            printf(" ");
        cur = cur->next;
    }
    printf("\n");
}

/* Вывод подстроки ключей в формате [a, b, c] */
static void print_keys(const int *keys, int m)
{
    printf("[");
    for (int i = 0; i < m; i++) {
        printf("%d", keys[i]);
        if (i < m - 1) printf(", ");
    }
    printf("]");
}

/* Поиск подстроки методом Райта с выводом результата */
static void search_demo(const Deque *d, const int *keys, int m)
{
    int pos, views;
    const DNode *node = wright_search(d, keys, m, &pos, &views);
    print_keys(keys, m);
    if (node != NULL)
        printf(": НАЙДЕНА с позиции %d (просмотров: %d)\n", pos, views);
    else
        printf(": не найдена (просмотров: %d)\n", views);
}

int main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr, "Использование: %s <файл> [ключ поиска ...]\n", argv[0]);
        return EXIT_FAILURE;
    }
    const char *filename = argv[1];

    /* читаем входные данные в дек */
    printf("\nЧтение файла '%s'...\n", filename);
    Deque d;
    deque_init(&d);
    int n = read_file(filename, &d);
    if (n < 0) return EXIT_FAILURE;
    const char *form = (n % 100 >= 11 && n % 100 <= 19) ? "чисел"
                     : (n % 10 == 1)                    ? "число"
                     : (n % 10 >= 2 && n % 10 <= 4)    ? "числа"
                                                        : "чисел";
    printf("Прочитано %d %s.\n", n, form);

    printf("\nИсходный дек:\n");
    deque_print(&d);

    /* цифровая сортировка дека */
    printf("\nВыполняем цифровую сортировку дека...\n");
    radix_sort(&d);

    printf("Отсортированный дек:\n");
    deque_print(&d);

    /* поиск подстроки методом Райта: элементы из аргументов или с клавиатуры */
    printf("\n── Поиск подстроки методом Райта ────────────────────────\n");
    if (argc > 2) {
        int m = argc - 2;
        int *keys = malloc(m * sizeof(int));
        if (!keys) {
            fprintf(stderr, "Ошибка: malloc вернул NULL\n");
            deque_free(&d);
            return EXIT_FAILURE;
        }
        for (int i = 0; i < m; i++)
            keys[i] = atoi(argv[2 + i]);
        search_demo(&d, keys, m);
        free(keys);
    } else {
        printf("Введите подстроку для поиска (числа через пробел): ");
        char line[256];
        if (!fgets(line, sizeof(line), stdin)) {
            fprintf(stderr, "Ошибка: не удалось прочитать ввод\n");
        } else {
            int keys[64];
            int m = 0;
            char *p = line;
            int val, consumed;
            while (m < 64 && sscanf(p, "%d%n", &val, &consumed) == 1) {
                keys[m++] = val;
                p += consumed;
            }
            if (m == 0)
                fprintf(stderr, "Ошибка: введите хотя бы одно целое число\n");
            else
                search_demo(&d, keys, m);
        }
    }
    printf("──────────────────────────────────────────────────────────\n");

    /* освобождаем память дека */
    deque_free(&d);
    return EXIT_SUCCESS;
}
