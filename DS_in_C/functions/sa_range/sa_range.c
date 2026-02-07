#include <stdio.h>
#include <stdlib.h>

/* Program name: sa_range.c
 * Author: Christopher Vote
 * Description: This program takes two integers, start and end, and returns a static array 
 * which contains all the consecutive integers between start and end (inclusive).
*/

int* saRange(int start, int end, size_t size, int* outArray);
void printArray(int* arr, size_t arr_len, int start, int end);
size_t sizeArray(int start, int end); 

int main() {
	printf("#sa_range example 1\n");

	int start1 = 1;
	int end1 = 3;
	size_t size1;
	size1 = sizeArray(start1, end1);
	int outArray1[size1 + 1];
	
	saRange(start1, end1, size1, outArray1);
	printArray(outArray1, size1, start1, end1);

	int start2 = -1;
	int end2 = 2;
	size_t size2; 
	size2 = sizeArray(start2, end2);
	int outArray2[size2];

	saRange(start2, end2, size2, outArray2);
	printArray(outArray2, size2, start1, end1);

	int start3 = 0;
	int end3 = 0;
	size_t size3;
      	size3 = sizeArray(start3, end3);
	int outArray3[size3];
	
	saRange(start3, end3, size3, outArray3);
	printArray(outArray3, size3, start3, end3);

	int start4 = 0;
	int end4 = -3;
	size_t size4;
	size4 = sizeArray(start4, end4);
	int outArray4[size4];
	
	saRange(start4, end4, size4, outArray4);
	printArray(outArray4, size4, start4, end4);

	int start5 = -95;
	int end5 = -89;
	size_t size5;
	size5 = sizeArray(start5, end5);
	int outArray5[size5];
	
	saRange(start5, end5, size5, outArray5);
	printArray(outArray5, size5, start5, end5);

	int start6 = -89;
	int end6 = -95;
	size_t size6;
	size6 = sizeArray(start6, end6);
	int outArray6[size6];
	
	saRange(start6, end6, size6, outArray6);
	printArray(outArray6, size6, start6, end6);

	return 0;
}


int* saRange(int start, int end, size_t size, int* outArray) {
	if (start <= end) {
		for (int i = 0; i < size; i++) {
			outArray[i] = start;
			start++;
		}
	}
	else {
		for (int i = 0; i < size; i++) {
			outArray[i] = start;
			start--;
		}
	}
}


void printArray(int* arr, size_t arr_len, int start, int end) {

	printf("Start:     %d, End:     %d, ARR Size: %ld ", start, end, arr_len);

        printf("[");
        for (int i = 0; i < arr_len-1; i++) {
                printf("%d, ", arr[i]);
        }
        printf("%d]\n", arr[arr_len-1]);
}

size_t sizeArray(int start, int end) {
	size_t arraySize;
	if ((start == 0 || end == 0) || (start > 0 && end > 0) || (start < 0 && end < 0)) {
		arraySize = abs(start) > abs(end) ? abs(start) - abs(end) : abs(end) - abs(start);
		arraySize++;
	}
	else {
		arraySize = start > end ? start - end : end - start;
		arraySize++;
	}

	return arraySize;
}







	
