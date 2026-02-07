#include <stdio.h>

/* File name: min_max.c
 * Author: Christopher Vote
 * Description: The program takes an array of integers, a parameter with the size of the array, 
 * 		and mutates an empty array of size 2, and modifies the empty array to contain
 * 		the minimum value from the integer array at index 0 and the maximum value from
 * 		the integer array at index 1. 
*/

void minMax(int* arr, int arr_len, int* mm);


int main() {
	// Example 1
	printf("# min_max example 1\n");

	printf("STAT_ARR Size: 5 ");

	int arr1[5] = {7, 8, 6, -5, 4};
	int arr_len1 = 5;
	int mm1[2];

	printf("[");
	for (int i = 0; i < arr_len1 - 1; i++) {
		printf("%d, ", arr1[i]);
	}
	printf("%d]\n", arr1[arr_len1-1]);

	minMax(arr1, arr_len1, mm1);

	printf("Min: %d, Max: %d\n\n", mm1[0], mm1[1]);


	// Example 2
	printf("# min_max example 2\n");

	printf("STAT_ARR Size: 1 ");

	int arr2[1] = {100};
	int arr_len2 = 1;
	int mm2[2];

	printf("[");
	for (int i = 0; i < arr_len2 - 1; i++) {
		printf("%d, ", arr2[i]);
	}
	printf("%d]\n", arr2[arr_len2-1]);

	minMax(arr2, arr_len2, mm2);

	printf("Min: %d, Max: %d\n\n", mm2[0], mm2[1]);

	
	// Example 3
	printf("# min_max example 3\n");

	printf("STAT_ARR Size: 3 ");

	int arr3[3] = {3, 3, 3};
	int arr_len3 = 3;
	int mm3[2];

	printf("[");
	for (int i = 0; i < arr_len3 - 1; i++) {
		printf("%d, ", arr3[i]);
	}
	printf("%d]\n", arr3[arr_len3-1]);

	minMax(arr3, arr_len3, mm3);

	printf("Min: %d, Max: %d\n\n", mm3[0], mm3[1]);

	return 0;
}



void minMax(int* arr, int arr_len, int* mm) {
	int min = arr[0];
	int max = arr[0];

	for (int i = 0; i < arr_len; i++) {
		if (arr[i] < min) {
			min = arr[i];
		}
		if (arr[i] > max) {
			max = arr[i];
		}
	}
	mm[0] = min;
	mm[1] = max;
}

	
