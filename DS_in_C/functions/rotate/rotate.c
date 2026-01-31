#include <stdio.h>

/* File name: rotate.c
 * Author: Christopher Vote
 * Description: This program includes a function which recieves an array of integers and an integer for steps.
 * 		The function returns a pointer to a new integer array containing the same elements as the original
 * 		array, but with each element shifted right or left by the number of steps provided (left if the steps
 * 		parameter is negative and right if it is positive).
*/

int* rotate(int* arr, size_t arr_len, int step);
void buildArray(int* arr, size_t arr_len, int lower, int jump);
void printArray(int* arr, size_t arr_len);

int main() {
	printf("# rotate example 1\n");

	int arr1[6];
	int arr_len1 = 6;
	int lower = -20;
	int jump = 7;

	printf("Array before rotate:\n");
	buildArray(arr1, arr_len1, lower, jump);
	printArray(arr1, arr_len1);

	int step1 = 1;
	int step2 = 2;
	int step3 = 0;
	int step4 = -1;
	int step5 = -2;
	int step6 = 28;
	int step7 = -100;
	int step8 = 268435456;
	int step9 = -2147483648;

	newArray1 = rotate(arr, arr_len, step1);
	printArray(newArray1, arr_len);
}

int* rotate(int* arr, size_t arr_len, int step) {
	int newArray[arr_len];
	modStep = step % arr_len;

	if (modStep == 0) {
		for (size_t i = 0; i < arr_len; i++) {
			newArray[i] = arr[i]
		}
	}
	else if (modStep > 0) {
		for (size_t i = 0; i < arr_len; i++) {
			if ((i + modStep) < arr_len) {
				newArray[i] = arr[i + modStep];
			}
			else if ((i + modStep) > arr_len) {
				newArray[i] = arr[((i + modStep) % arr_len)];
			}
		}
	}
	else {		// if (modStep < 0)
		if ((i + arr_len - modStep) <= arr_len) {
			newArr[i] = arr[(i + arr_len - modStep)];
		}
		else {
			newArr[i] = arr[(i + arr_len - modStep) % arr_len];
		}
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

