#include "stack.h"

#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* чтение файла в стек через push */
static int read_file(const char *filename, Stack *s)
{
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr, "Ошибка: не удалось открыть файл '%s'\n", filename);
        return -1;
    }

    int tmp;
    int count = 0;
    while (fscanf(fp, "%d", &tmp) == 1) {
        if (stack_push(s, tmp) != 0) {
            stack_free(s);
            fclose(fp);
            return -1;
        }
        count++;  /* считаем прочитанные */
    }

    fclose(fp);

    if (count == 0) {
        fprintf(stderr, "Ошибка: файл '%s' пуст или не содержит чисел\n", filename);
        return -1;
    }
    return count;  /* вернули размер */
}

/* печать стека от дна к вершине */
static void stack_print(const Stack *s)
{
    if (stack_is_empty(s)) {
        printf("\n");
        return;
    }
    for (int i = 0; i <= s->top; i++) {
        printf("%d", s->data[i]);
        if (i < s->top) {
            printf(" ");
        }
    }
    printf("\n");  /* вывод от дна к вершине */
}

/* разбор строки как ровно одного целого числа; -1 если формат неверный */
static int parse_key(const char *str, int *out)
{
    char *end;
    errno = 0;
    long val = strtol(str, &end, 10);
    while (*end == ' ' || *end == '\t' || *end == '\r' || *end == '\n')
        end++;
    if (end == str || *end != '\0' || errno != 0 || val < INT_MIN || val > INT_MAX)
        return -1;
    *out = (int)val;
    return 0;
}

/* демонстрация поиска Бойера-Мура по подпоследовательности */
static void search_demo(const Stack *s, const int *keys, int keys_len)
{
    int views;
    int pos = boyer_moore_search(s, keys, keys_len, &views);

    /* Формируем строку вида "2 3 4" для вывода */
    char pat_str[256] = "";
    for (int i = 0; i < keys_len; i++) {
        char tmp[32];
        snprintf(tmp, sizeof(tmp), "%d", keys[i]);
        if (i > 0) strcat(pat_str, " ");
        strcat(pat_str, tmp);
    }

    if (pos != -1) {
        printf("Подпоследовательность [%s]: НАЙДЕНА, начало на позиции %d (просмотров: %d)\n",
               pat_str, pos, views);
    } else {
        printf("Подпоследовательность [%s]: не найдена (просмотров: %d)\n", pat_str, views);
    }
}  /* конец демо поиска */

/* запись результата в RBT и визуализация */
static void rbt_demo(Stack *s)
{
    RBTree tree;
    rbtree_init(&tree);

    printf("\nЗаписываем результат в красно-чёрное дерево...\n");

    for (int i = 0; i <= s->top; i++) {
        rbtree_insert(&tree, s->data[i]);  /* вставляем каждый элемент */
    }

    printf("Визуализация дерева (R — красный, B — чёрный):\n");
    rbtree_print_visual(&tree);

    rbtree_free(&tree);  /* чистим дерево */
}  /* конец демонстрации RBT */

int main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr, "Использование: %s <файл> [ключ поиска ...]\n", argv[0]);
        return EXIT_FAILURE;
    }
    const char *filename = argv[1];

    /*
     * Общий поток программы (согласно заданию лабораторной):
     * 1. Прочитать числа из файла → поместить в стек (push, LIFO).
     * 2. Вывести исходное содержимое.
     * 3. Выполнить цифровую (radix) сортировку стека.
     * 4. Вывести отсортированный стек (дно → вершина = по возрастанию).
     * 5. Продемонстрировать поиск методом Бойера-Мура по ключам.
     * 6. Записать отсортированный результат в красно-чёрное дерево
     *    и показать, что inorder-обход даёт тот же порядок.
     * 7. Освободить память.
     */

    printf("\nЧтение файла '%s'...\n", filename);

    Stack s;
    stack_init(&s);  /* инициализируем стек */

    int n = read_file(filename, &s);
    if (n < 0) {
        stack_free(&s);
        return EXIT_FAILURE;
    }

    /* Склонение слова "число" */
    const char *form = (n % 100 >= 11 && n % 100 <= 19) ? "чисел"
                     : (n % 10 == 1)                    ? "число"
                     : (n % 10 >= 2 && n % 10 <= 4)    ? "числа"
                                                       : "чисел";
    printf("Прочитано %d %s.\n", n, form);

    printf("\nИсходный стек (от дна к вершине):\n");
    stack_print(&s);  /* вывод до сортировки */

    printf("\nВыполняем цифровую сортировку стека...\n");
    radix_sort(&s);  /* сортируем */

    printf("Отсортированный стек (от дна к вершине):\n");
    stack_print(&s);

    printf("\n── Поиск методом Бойера-Мура ──────────────────────────\n");
    if (argc > 2) {
        /* Все аргументы после имени файла — одна подпоследовательность для поиска */
        int keys_len = argc - 2;
        int *keys = (int *)malloc((size_t)keys_len * sizeof(int));
        if (!keys) {
            fprintf(stderr, "Ошибка: не удалось выделить память для ключей\n");
            stack_free(&s);
            return EXIT_FAILURE;
        }
        int ok = 1;
        for (int i = 0; i < keys_len; i++) {
            if (parse_key(argv[i + 2], &keys[i]) != 0) {
                fprintf(stderr, "Ошибка: '%s' — не целое число\n", argv[i + 2]);
                ok = 0;
                break;
            }
        }
        if (ok) search_demo(&s, keys, keys_len);
        free(keys);
    } else {
        /* Интерактивный режим: вводим числа через пробел на одной строке */
        printf("Введите подпоследовательность для поиска (числа через пробел): ");
        char line[512];
        if (fgets(line, sizeof(line), stdin)) {
            /* Считаем числа токен за токеном */
            int keys[128];
            int keys_len = 0;
            char *p = line;
            char *end;
            while (keys_len < 128) {
                errno = 0;
                long val = strtol(p, &end, 10);
                if (end == p) break;  /* нет числа — конец ввода */
                if (errno != 0 || val < INT_MIN || val > INT_MAX) {
                    fprintf(stderr, "Ошибка: число вне диапазона int\n");
                    keys_len = 0;
                    break;
                }
                keys[keys_len++] = (int)val;
                p = end;
            }
            if (keys_len == 0) {
                fprintf(stderr, "Ошибка: не введено ни одного числа\n");
            } else {
                search_demo(&s, keys, keys_len);
            }
        } else {
            fprintf(stderr, "Ошибка: ввод не прочитан\n");
        }
    }
    printf("─────────────────────────────────────────────────\n");

    rbt_demo(&s);  /* записываем результат в дерево */

    stack_free(&s);  /* финальное освобождение */
    return EXIT_SUCCESS;
}