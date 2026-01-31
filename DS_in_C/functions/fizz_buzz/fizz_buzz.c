#include <stdio.h>

void buildArray(int* arr, int arr_len, int lower, int jump);

int main() {

	// Example 1
	printf("\n# fizz_buzz example 1\n");
	int arr1[7];
	int arr_len1 = 7;

	int lower1 = -5;
	int jump1 = 4;

	buildArray(arr1, arr_len1, lower1, jump1);


}


void buildArray(int* arr, int arr_len, int lower, int jump) {
	
	for (int i = 0; i < arr_len; i++) {
		int result = lower + (i * jump);
		arr[i] = result;
	}
	
	// Print the array
	printf("Array length: %d\n", arr_len);

	printf("Array: [");
	for (int i = 0; i < arr_len-1; i++) {
		printf("%d, ", arr[i]);
	}
	printf("%d]\n\n", arr[arr_len-1]);


}
