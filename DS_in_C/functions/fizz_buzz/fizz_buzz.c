#include <stdio.h>
#define FIZZ "fizz"
#define BUZZ "buzz"
#define FIZZBUZZ "fizzbuzz"

/* Program name: fizz_buzz.c
 * Author: Christopher Vote
 * Description: This program processes an array of integers and prints a modified form. 
 * 		Values divisible by both 3 and 5 are replaced with "fizz_buzz". Values divisible
 * 		by 3 are replaced with "fizz", and values divisible by 5 are replaced with "buzz".
*/

void buildArray(int* arr, int arr_len, int lower, int jump);
void fizzBuzz(int* arr, int arr_len);

int main() {

	// Example 1
	printf("# fizz_buzz example 1\n");
	int arr1[7];
	int arr_len1 = 7;

	int lower1 = -5;
	int jump1 = 4;

	buildArray(arr1, arr_len1, lower1, jump1);


}

void fizzBuzz(int* arr, int arr_len) {

	printf("[");
	for (int i = 0; i < arr_len-1; i++) {
		if ((arr[i] % 5 == 0) && (arr[i] % 3 == 0)) {
			printf("%s, ", FIZZBUZZ);
		}
		else if (arr[i] % 3 == 0) {
			printf("%s, ", FIZZ);
		}
		else if (arr[i] % 5 == 0) {
			printf("%s, ", BUZZ);
		}
		else {
			printf("%d, ", arr[i]);
		}
	}
	int endVal = arr[arr_len-1];
	if ((endVal % 5 == 0) && (endVal % 3 == 0)) {
		printf("%s]\n", FIZZBUZZ);
	}
	else if (endVal % 3 == 0) {
		printf("%s]\n", FIZZ);
	}
	else if (endVal % 5 == 0) {
		printf("%s]\n", BUZZ);
	}
	else {
		printf("%d]\n", endVal);
	}
}


void buildArray(int* arr, int arr_len, int lower, int jump) {
	
	for (int i = 0; i < arr_len; i++) {
		int result = lower + (i * jump);
		arr[i] = result;
	}
	
	// Print the array
	printf("ARR Size: %d ", arr_len);

	printf("[");
	for (int i = 0; i < arr_len-1; i++) {
		printf("%d, ", arr[i]);
	}
	printf("%d]\n", arr[arr_len-1]);
}
