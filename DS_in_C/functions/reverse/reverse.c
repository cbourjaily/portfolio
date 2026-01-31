#include <stdio.h>


/* Program name: reverse.c
 * Author: Christopher Vote
 * Description: This program includes a function which reverses the order of the elements in 
 * 		an integer array.
*/

void buildArray(int* arr, size_t arr_len, int lower, int jump); 
void reverse(int* arr, size_t arr_len);
void printArray(int* arr, size_t arr_len);

int main() {
	// Example 1
	printf("# reverse example 1\n");

	int arr1[6];
	size_t arr_len1 = 6;
	int lower1 = -20;
	int jump1 = 7;
	
	printf("Start array:\n");
	buildArray(arr1, arr_len1, lower1, jump1);

	reverse(arr1, arr_len1);
	printf("Reversed array:\n");
	


	return 0;
}


void reverse(int* arr, size_t arr_len); {
	for (int i = 0; i < arr_len / 2; i++) {
		int left = arr[i];
		int right = arr[arr_len-1-i];
		arr[i] = right;
		arr[arr_len-1-i] = left;
	}
}



void buildArray(int* arr, size_t arr_len, int lower, int jump) {

        for (int i = 0; i < arr_len; i++) {
                int result = lower + (i * jump);
                arr[i] = result;
        }
	printArray(arr, arr_len);
}

void printArray(int* arr, size_t arr_len) {

        printf("ARR Size: %ld ", arr_len);

        printf("[");
        for (int i = 0; i < arr_len-1; i++) {
                printf("%d, ", arr[i]);
        }
        printf("%d]\n", arr[arr_len-1]);
}







