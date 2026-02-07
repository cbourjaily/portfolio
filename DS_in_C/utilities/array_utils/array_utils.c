#include <stdio.h>
#include "array_utils.h"

void buildArray(int* arr, size_t arr_len, int lower, int jump) {

        for (int i = 0; i < arr_len; i++) {
                int result = lower + (i * jump);
                arr[i] = result;
        }
}

void printArray(int* arr, size_t arr_len) {

        printf("ARR Size: %ld ", arr_len);

        printf("[");
        for (int i = 0; i < arr_len-1; i++) {
                printf("%d, ", arr[i]);
        }
        printf("%d]\n", arr[arr_len-1]);
}

void reverse(int* arr, size_t arr_len) {
        for (int i = 0; i < arr_len / 2; i++) {
                int left = arr[i];
                int right = arr[arr_len-1-i];
                arr[i] = right;
                arr[arr_len-1-i] = left;
        }
}

