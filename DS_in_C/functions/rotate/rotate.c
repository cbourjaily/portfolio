#include <stdio.h>

/* File name: rotate.c
 * Author: Christopher Vote
 * Description: This program includes a function which recieves an array of integers and an integer for steps.
 * 		The function returns a pointer to a new integer array containing the same elements as the original
 * 		array, but with each element shifted right or left by the number of steps provided (left if the steps
 * 		parameter is negative and right if it is positive).
*/

int* rotate(int* arr, size_t arr_len, int step, int* newArray);
void buildArray(int* arr, size_t arr_len, int lower, int jump);
void printArray(int* arr, size_t arr_len);
void printRotate(int* arr, size_t arr_len, int step);

int main() {
	printf("# rotate example 1\n");
	
	int step1 = 1;
	int step2 = 2;
	int step3 = 0;
	int step4 = -1;
	int step5 = -2;
	int step6 = 28;
	int step7 = -100;
	int step8 = 268435456;
	int step9 = -2147483648;

	int arr1[7];
	int arr_len1 = 6;
	int lower1 = -20;
	int jump1 = 7;
	int newArray1[arr_len1];

	buildArray(arr1, arr_len1, lower1, jump1);
	printArray(arr1, arr_len1);

	rotate(arr1, arr_len1, step1, newArray1);
	printRotate(newArray1, arr_len1, step1);

	rotate(arr1, arr_len1, step2, newArray1);
	printRotate(newArray1, arr_len1, step2);

	rotate(arr1, arr_len1, step3, newArray1);
	printRotate(newArray1, arr_len1, step3);

	rotate(arr1, arr_len1, step4, newArray1);
	printRotate(newArray1, arr_len1, step4);

	rotate(arr1, arr_len1, step5, newArray1);
	printRotate(newArray1, arr_len1, step5);

	rotate(arr1, arr_len1, step6, newArray1);
	printRotate(newArray1, arr_len1, step6);

	rotate(arr1, arr_len1, step7, newArray1);
	printRotate(newArray1, arr_len1, step7);

	rotate(arr1, arr_len1, step8, newArray1);
	printRotate(newArray1, arr_len1, step8);

	rotate(arr1, arr_len1, step9, newArray1);
	printRotate(newArray1, arr_len1, step9);

	printArray(arr1, arr_len1);
}

int* rotate(int* arr, size_t arr_len, int step, int* newArray) {
	int modStep = step % (int)arr_len;

	for (size_t i = 0; i < arr_len; i++) {
		size_t new_index = (i + modStep + arr_len) % arr_len;
		newArray[new_index] = arr[i];
	}

	return newArray;
}

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

void printRotate(int* arr, size_t arr_len, int step) {

        printf("ARR Size: %ld ", arr_len);

        printf("[");
        for (int i = 0; i < arr_len-1; i++) {
                printf("%d, ", arr[i]);
        }
        printf("%d] %d\n", arr[arr_len-1], step);
}
