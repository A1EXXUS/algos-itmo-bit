#include "radix_sort.h"
#include <stdio.h>
#include <stdlib.h>

#define BASE 10

typedef struct Node {
    int         value;
    struct Node *next;
} Node;

typedef struct {
    Node *tail;
    int   size;
} Queue;

static void queue_init(Queue *q)
{
    q->tail = NULL; //(3)
    q->size = 0;  //(3)
}
//Сложность: O(1)

static int queue_is_empty(const Queue *q)
{
    return q->size == 0; //(4)
}
//Сложность: O(1)

static int enqueue(Queue *q, int value)
{
    Node *node = (Node *)malloc(sizeof(Node)); //(4)
    if (!node) {  //(2)
        fprintf(stderr, "Ошибка: malloc вернул NULL\n");  //(1)
        return -1;  //(1)
    }

    node->value = value;  //(3)

    if (q->size == 0) {  //(3)
        node->next = node;  //(3)
    } else {
        node->next = q->tail->next;  //(6)
        q->tail->next = node;  //(4)
    }
    q->tail = node;  //(3)
    q->size++;  //(4)
    return 0;  //(1)
}
//Сложность: O(1)

static int dequeue(Queue *q, int *out)
{
    if (q->size == 0) {  //(3)
        fprintf(stderr, "Ошибка: очередь пуста\n");  //(1)
        return -1;  //(1)
    }

    Node *head = q->tail->next;  //(4)
    *out = head->value;  //(4)

    if (head == q->tail) {  //(3)
        q->tail = NULL;  //(3)
    } else {
        q->tail->next = head->next;  //(6)
    }
    free(head);  //(1)
    q->size--;  //(4)
    return 0;  //(1)
}
//Сложность: O(1)

static void queue_free(Queue *q)
{
    if (q->size == 0) return;  //(4)

    Node *head = q->tail->next;  //(4)
    Node *cur  = head;  //(1)

    do {
        Node *tmp = cur;  //(1)
        cur = cur->next;  //(3)
        free(tmp);  //(1)
    } while (cur != head);  //(1)
    // n + 5*n = 6n

    q->tail = NULL;  //(3)
    q->size = 0;  //(3)
}
//15 + 6n
// Сложность: O(n)

int find_max(const int *arr, int n)
{
    int max = arr[0];  //(2)
    for (int i = 1; i < n; i++) {  //(1) + (n+1) + 2*n = 3*n + 2
        if (arr[i] > max) //(2)
            max = arr[i];  //(2)
    }
    return max;  //(1)
}
//2 + (3n + 2) + 4*n + 1 = 7n + 5
// Сложность: O(n)

static void counting_sort_by_queue(int *arr, int n, int exp)
{
    Queue buckets[BASE];

    for (int j = 0; j < BASE; j++)  // 1 + (k + 1) + 2*k = 3*k + 2
        queue_init(&buckets[j]); //(2 + 6)
//(3k + 2) + 8*k = 11k + 2

    for (int i = 0; i < n; i++) {  //(1) + (n+1) + 2*n = 3*n + 2
        int digit = (arr[i] / exp) % BASE;  //(4)
        if (enqueue(&buckets[digit], arr[i]) != 0) {  //(5)
            fprintf(stderr, "Ошибка: enqueue вернул -1\n");  //(1)
            exit(EXIT_FAILURE);  //(1)
        }
    }
// (3n + 2) + 4n + 5n = 12n + 2

    int idx = 0;  //(1)
    for (int j = 0; j < BASE; j++) {  //(1) + (k + 1) + 2*k = 3*k + 2
        while (!queue_is_empty(&buckets[j])) {  //(4)
            dequeue(&buckets[j], &arr[idx]);  //(5)
            idx++;  //(2)
        }
    }
//(3k + 2) + 4(n+k) + (5 + 2)*n

    for (int j = 0; j < BASE; j++)  // 1 + (k + 1) + 2*k = 3*k + 2
        queue_free(&buckets[j]); // 6n + 11k + 2
}
// (11k + 2) + (12n + 2) + 1 + (3k + 2) + 4(n+k) + 7n = 18k + 23 n + 7
// Сложность: O(n) (при BASE = const = 10)

static void radix_sort_nonneg(int *arr, int n)
{
    if (n <= 1) return;  //(2)
    int max_val = find_max(arr, n);  // 7n + 13 + 1
    for (int exp = 1; max_val / exp > 0; exp *= BASE) // 1 + (d+1)*2 + d*2 = 4d + 3
        counting_sort_by_queue(arr, n, exp); //(1)
}
// 2 + 7n + 14 + 4d + 3 + d*(23n + 187) = 23d*n + 191d + 7n + 19
// Сложность: O(d*n) (при BASE = const = 10)

void radix_sort(int *arr, int n)
{
    if (n <= 1) return;  //(2)

    int neg_n = 0;  //(1)
    for (int i = 0; i < n; i++)  // 1 + (n+1) + n*2 = 3n + 2
        if (arr[i] < 0) neg_n++;  //(4)
    //3n + 2 + 4n = 7n + 2
    int pos_n = n - neg_n;  //(2)

    if (neg_n == 0) {  //(1)
        radix_sort_nonneg(arr, n);  //(1)
        return;  //(1)
    }
    if (pos_n == 0) {  //(1)
        for (int i = 0; i < n; i++)  // 1 + (n+1) + n*2 = 3n + 2
            arr[i] = -arr[i];  //(3)
        // 3n + 2 + 3n = 6n + 2
        radix_sort_nonneg(arr, n);  //(1)
        for (int i = 0, j = n - 1; i < j; i++, j--) {  // i=0 (1), j=n-1 (2), i<j (⌊n/2⌋+1), i++,j-- (4*⌊n/2⌋): 5⌊n/2⌋ + 4
            int tmp = arr[i];  //(2)
            arr[i] = arr[j];   //(2)
            arr[j] = tmp;      //(2)
        }
        // тело: 6*⌊n/2⌋, итого: 11⌊n/2⌋ + 4
        for (int i = 0; i < n; i++)  // 1 + (n+1) + n*2 = 3n + 2
            arr[i] = -arr[i];  //(3)
        return;  //(1)
    }

    int *neg = (int *)malloc(neg_n * sizeof(int)); //(5)
    int *pos = (int *)malloc(pos_n * sizeof(int)); //(5)
    if (!neg || !pos) {  //(3)
        fprintf(stderr, "Ошибка: malloc в radix_sort\n"); //(1)
        free(neg); free(pos); exit(EXIT_FAILURE); //(3)
    }

    int ni = 0, pi = 0;  //(2)
    for (int i = 0; i < n; i++) {  //1 + (n+1) + 2*n = (3n+2)
        if (arr[i] < 0) neg[ni++] = -arr[i];  //(8)
        else            pos[pi++] =  arr[i];  //(5)
    }
    //2 + (3n + 2) + (8)*n = 11n + 4 (если все числа положительные)
    //2 + (3n + 2) + (5)*n = 8n + 4 (если все числа отрицательные)

    radix_sort_nonneg(neg, neg_n); //(1)
    radix_sort_nonneg(pos, pos_n); //(1)

    int idx = 0;  //(1)
    for (int i = neg_n - 1; i >= 0; i--)  // i=neg_n-1 (2), i>=0 (neg_n+1), i-- (2*neg_n): 3*neg_n + 3
        arr[idx++] = -neg[i];  //(6)
    // 3*neg_n + 3 + 6*neg_n = 9*neg_n + 3
    for (int i = 0; i < pos_n; i++)  // 1 + (pos_n+1) + 2*pos_n = 3*pos_n + 2
        arr[idx++] = pos[i];  //(5)
    // 3*pos_n + 2 + 5*pos_n = 8*pos_n + 2

    free(neg);  //(1)
    free(pos);  //(1)
}
// Общий случай (neg_n > 0, pos_n > 0):
// 2+1+(7n+2)+2+1+1+5+5+3+(11n+4)+2+1+(9*neg_n+3)+(8*pos_n+2)+2
// = 18n + 9*neg_n + 8*pos_n + 36  (worst: 27n + 36)
//   T_nonneg(neg_n) + T_nonneg(pos_n) = 23d*n + 382d + 7n + 38
//   Итого: 23d*n + 382d + (25n + 9*neg_n + 8*pos_n) + 74
//          при neg_n~pos_n~n/2: ≈ 23d*n + 382d + 33.5n + 74
// Сложность: O(d*n), при фиксированном d — O(n)
