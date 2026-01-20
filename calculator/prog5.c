// Christopher Vote	/	votec@oregonstate.edu
// CS 274		/	Randy Scovil
// prog5		/	11/26/25

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

// define macros for arithmetic operations
#define add(x, y) (x + y)
#define subtract(x, y) (x - y)
#define multiply(x, y) (x * y)
#define divide(x, y) (x / y)

// define static buffer
#define MAX_LENGTH 33

// define file path
#define LOGFILE "./prog5_log.txt"

//declare and define global var fileStream
FILE* fileStream = NULL;


//define struct
//	linked list node struct called Level
struct Level
{
	int type; // 0 means long, 1 means double, 2 means string
	long longvalue;
	double doublevalue;
	char stringvalue[33];
	struct Level* next;
} typedef Level;

// Push function

Level* push(Level* head, int in_type, long in_long, double in_double, char* in_string)
{
	Level* newLevel = (Level*)malloc(sizeof(Level));	// Create space, this will be the new head

	// Set the data and link the new level to the current head
	newLevel->type = in_type;
	newLevel->longvalue = in_long;
	newLevel->doublevalue = in_double;
	strncpy(newLevel->stringvalue, in_string, 32);
	newLevel->stringvalue[32] = '\0';

	newLevel->next = head;	// This new head points to the old head; the old head is now node 2

	return newLevel;	// Return the new head, this is the only way to get the new head address
}


// Pop function

Level* pop(Level** head)
{
	if (head == NULL || *head == NULL)
		return NULL;

	Level* currentNode = *head;
	*head = currentNode->next;
	currentNode->next = NULL;

	return currentNode;
}

// Linked list head

Level* head = NULL;


//declare functions

	// primary operations
void displayStack();
void drop();
void utilityDrop();
void addOp();
void subOp();
void timesOp();
void divOp();
void wordSquare();
void roll();
void logText(const char* aString);

	// helper functions
void stringifyStruct(Level* currLevel, char *stringStruct);
int validInput(char* buffer, int bufferLength);
int floatTest(char* buffer, int bufferLength);
int intTest(char* buffer, int bufferLength);
int stringTest(char* buffer, int bufferLength);
int operationVerify();
int countLevels();
int sufficientLevels();
void truncateStack();




int main(int argc, char*argv[])
{
	// declare file variables
	int fileDescriptor;
	char *filepath = LOGFILE;

	// create output file if it doesn't exist, otherwise truncate it.
	fileDescriptor = open(filepath, 
			O_RDWR | O_CREAT | O_TRUNC,
			S_IRUSR | S_IWUSR);

	// close the file
	close(fileDescriptor);

	while (1)
	{
	// display stack
	displayStack();

        // create log buffer
        char logBuffer[40];

	int levelCount = -7;		// variable for storing stack count

//	initialize output file output return variable (integer)
	int fileDescriptor = -7;

//	initialize dynamic array variables
	char* buffer = NULL;				// initial input
	size_t bufferSize = 0;				// size of initial input string
	ssize_t bufferLength = -7;

//	prompt user
	printf("# ");

//	get raw string and validate
	bufferLength = getline(&buffer, &bufferSize, stdin);

//	validate input stringlength
	if (bufferLength > 33) {
		logText("Bad Input\n");					
		free(buffer);
		continue;						// reloop
	}

//	validate input string characters
	int validate = validInput(buffer, bufferLength-1);		// bufferlength - 1 for '\n' character
	if (validate == -1) {
		logText("Bad input\n");				
		free(buffer);
		continue;						// reloop
	}

	// log user input including prompt
	sprintf(logBuffer, "%s%s", "# ", buffer);			// buffer includes '/n'
	fileDescriptor = open(LOGFILE, O_WRONLY | O_APPEND);
	write(fileDescriptor, logBuffer, bufferLength+2);
	close(fileDescriptor);

	//	remove '\n' and adjust length
	if (bufferLength > 0 && buffer[bufferLength-1] == '\n') {
		buffer[bufferLength-1] = '\0';
		bufferLength --;					// decrement length
	}
	


//	parse input
//		first check for Command operations and send to appropriate functions:
//				if the input is a 1-character parse potential commands
//					d : drop(), + : addOp(), - : subtOp(), * : timesOp(), / : divOp(), w : wordsquare(), r : roll()
//					q : Quit - handle locally in parser

	char firstChar = buffer[0];			// set first character in the string to variable firstChar
	char *endptr = NULL;				// for use in strtol
	long intValue = -7;				// for saving result from strtol
	int intChar = buffer[0];			// ascii integer value of the first character for parsing
	char tempStr[2] = {firstChar, '\0'};		// string value of first character for assignment usages


	if (bufferLength == 1) {
		if (firstChar == 'q') {
			free(buffer);
			exit(0);
		}
		else if (firstChar == 'd') { 
			drop();
			free(buffer);
			continue;
		} 
		else if (firstChar == '+') {
			addOp();
			free(buffer);
			continue;
		}
		else if (firstChar == '-') {
			subOp();
			free(buffer);
			continue;
		}
		else if (firstChar == '*') {
			timesOp();
			free(buffer);
			continue;
		}
		else if (firstChar == '/') {
			divOp();
			free(buffer);
			continue;
		}
		else if (firstChar == 'w') {
			wordSquare();
			free(buffer);
			continue;
		}
		else if (firstChar == 'r') {
			roll();
			free(buffer);
			continue;
		}
		//	Parse single-character integer
		else if (intChar >= 48 && intChar <= 57)
		{
			intValue = strtol(tempStr, &endptr, 10);
		

			// handle fifth level on stack if it exists
			levelCount = countLevels();
			if (levelCount == 5)	{
				truncateStack();
			}
		
			// push intValue to the stack
			head = push(head, 0, intValue, 0.0, "");
			free(buffer);
			continue;
		}

		//	Parse single-character string
		else if ((intChar == 32) || (intChar >= 97 && intChar <= 122))
		{

			// handle fifth level on stack if it exists
			levelCount = countLevels();
			if (levelCount == 5)	{
				truncateStack();
			}
			
			// push value to stack
			head = push(head, 2, 0, 0.0, tempStr);
			free(buffer);
			continue;
		}
		else {
			logText("Bad Input");				
			free(buffer);
			continue;
		}
	}
		// a flag to indicate if all datatype tests have failed after conditional checks
		int testFlag = -1;	

	// parsing logic for strings longer than 1 character
		// parse floats, then ints, then strings, to handle overlap.
		// 	Float check: check first character for period, plus, minus, digit; space okay in front only
			
		if (((intChar == 32) || (intChar == 43) || (intChar == 45) || (intChar == 46) || 
				(intChar >= 48 && intChar <= 57)))	{
			int isFloat = floatTest(buffer, bufferLength);
			if (isFloat) {							// run float test
				double floatString = strtod(buffer, &endptr);

				// handle fifth level on stack if it exists
				levelCount = countLevels();
				if (levelCount == 5)	{
					truncateStack();
				}

				
				// push value to stack
				head = push(head, 1, 0, floatString, "");
				testFlag = 0;					// set testFlag to 0 indicate a test passed
				free(buffer);
				continue;
			}
		}
	
		// 	Int check: check for digits, plus, minus; space okay in front only
		// 		potential int has same allowed initials as float minus period
		if ((intChar == 32) || (intChar == 43) || (intChar == 45) || 
				(intChar >= 48 && intChar <= 57))	{
			int isInt = intTest(buffer, bufferLength);			// Run integer test
			if (isInt) {
				long intString = strtol(buffer, &endptr, 10);

				// handle fifth level on stack if it exists
				levelCount = countLevels();
				if (levelCount == 5)	{
					truncateStack();
				}

				
				// push value to stack
				head = push(head, 0, intString, 0.0, "");
				testFlag = 0; 					// set testFlag to 0 to indicate a test has passed
				free(buffer);
				continue;
			}
		}
	
		// 	String check: check for lowercase letters, ints, space
		if (stringTest(buffer, bufferLength)) {

			// handle fifth level on stack if it exists
			levelCount = countLevels();
			if (levelCount == 5)	{
				truncateStack();
			}


			// push value to stack
			head = push(head, 2, 0, 0.0, buffer);
			testFlag = 0;						// set testFlag to 0 to indicate a test has passed
			free(buffer);
			continue;
		}	


		// run testFlag when no datatype match tests have passed
		if (testFlag == -1) {
			logText("Bad Input\n");
			free(buffer);
			continue;
		}
}	
}


/* @function displayStack - 
 * Displays all levels of the stack as currently constructed.
 * If stack is empty, displays words "Empty Stack". 
 * Called by main() at start of each round.
 * Also handles overflow by restricting levels to 5.
*/

void displayStack()
{
	// create log buffer
	char logBuffer[40];

	// initialize string array variables to store stringified structs
	char stringStruct1[MAX_LENGTH] = {0};
	char stringStruct2[MAX_LENGTH] = {0};
	char stringStruct3[MAX_LENGTH] = {0};
	char stringStruct4[MAX_LENGTH] = {0};
	char stringStruct5[MAX_LENGTH] = {0};

	// retreive level count
	int levelCount = countLevels();

	// check for empty stack case
	if (head == NULL)
	{
		logText("Empty Stack\n");
	}

	// check levels and stringify struct levels

	if (levelCount == 1)	{
		// retrieve level
		Level *levelOne = pop(&head);

		// sringify level
		stringifyStruct(levelOne, stringStruct1);

		// return level to stack
		levelOne->next = head;
		head = levelOne;

		// create output string
		sprintf(logBuffer, "%d: %s\n", 1, stringStruct1);
		logText(logBuffer);
		return;
	}

	if (levelCount == 2)	{

		// retrieve levels
		Level *levelOne = pop(&head);
		Level *levelTwo = pop(&head);

		// sringify level
		stringifyStruct(levelOne, stringStruct1);
		stringifyStruct(levelTwo, stringStruct2);

		// return levels to stack
		levelTwo->next = head;
		levelOne->next = levelTwo;
		head = levelOne;

		// print output
		sprintf(logBuffer, "%d: %s\n", 2, stringStruct2);
		logText(logBuffer);

		sprintf(logBuffer, "%d: %s\n", 1, stringStruct1);
		logText(logBuffer);
		return;
	}

	if (levelCount == 3)	{

		// retrieve levels
		Level *levelOne = pop(&head);
		Level *levelTwo = pop(&head);
		Level *levelThree = pop(&head);

		// sringify level
		stringifyStruct(levelOne, stringStruct1);
		stringifyStruct(levelTwo, stringStruct2);
		stringifyStruct(levelThree, stringStruct3);

		// return levels to stack
		levelThree->next = head;
		levelTwo->next = levelThree;
		levelOne->next = levelTwo;
		head = levelOne;

		// print output
		sprintf(logBuffer, "%d: %s\n", 3, stringStruct3);
		logText(logBuffer);
		
		sprintf(logBuffer, "%d: %s\n", 2, stringStruct2);
		logText(logBuffer);

		sprintf(logBuffer, "%d: %s\n", 1, stringStruct1);
		logText(logBuffer);

		return;
	}
	if (levelCount == 4)	{

		// retrieve levels
		Level *levelOne = pop(&head);
		Level *levelTwo = pop(&head);
		Level *levelThree = pop(&head);
		Level *levelFour = pop(&head);

		// sringify level
		stringifyStruct(levelOne, stringStruct1);
		stringifyStruct(levelTwo, stringStruct2);
		stringifyStruct(levelThree, stringStruct3);
		stringifyStruct(levelFour, stringStruct4);

		// return levels to stack
		levelFour->next = head;
		levelThree->next = levelFour;
		levelTwo->next = levelThree;
		levelOne->next = levelTwo;
		head = levelOne;

		// print output
		sprintf(logBuffer, "%d: %s\n", 4, stringStruct4);
		logText(logBuffer);

		sprintf(logBuffer, "%d: %s\n", 3, stringStruct3);
		logText(logBuffer);

		sprintf(logBuffer, "%d: %s\n", 2, stringStruct2);
		logText(logBuffer);

		sprintf(logBuffer, "%d: %s\n", 1, stringStruct1);
		logText(logBuffer);

		return;
	}

	if (levelCount == 5)	{

		// retrieve levels
		Level *levelOne = pop(&head);
		Level *levelTwo = pop(&head);
		Level *levelThree = pop(&head);
		Level *levelFour = pop(&head);
		Level *levelFive = pop(&head);

		// sringify level
		stringifyStruct(levelOne, stringStruct1);
		stringifyStruct(levelTwo, stringStruct2);
		stringifyStruct(levelThree, stringStruct3);
		stringifyStruct(levelFour, stringStruct4);
		stringifyStruct(levelFive, stringStruct5);

		// return levels to stack
		levelFive->next = head;
		levelFour->next = levelFive;
		levelThree->next = levelFour;
		levelTwo->next = levelThree;
		levelOne->next = levelTwo;
		head = levelOne;

		// print output
		sprintf(logBuffer, "%d: %s\n", 5, stringStruct5);
		logText(logBuffer);

		sprintf(logBuffer, "%d: %s\n", 4, stringStruct4);
		logText(logBuffer);
		
		sprintf(logBuffer, "%d: %s\n", 3, stringStruct3);
		logText(logBuffer);


		sprintf(logBuffer, "%d: %s\n", 2, stringStruct2);
		logText(logBuffer);


		sprintf(logBuffer, "%d: %s\n", 1, stringStruct1);
		logText(logBuffer);

		return;
	}

}



/* @function: drop - Removes the level at the top of the stack.*/

void drop()

{
	if (head == NULL) {
		logText("Insufficient Arguments\n");
		return;
	}
	else {
		Level* current = pop(&head);
		free(current);
		return;
	}
}

/* @function: utilityDrop - Removes the level at the top of the stack
 * and doesn't print or log anything.
*/

void utilityDrop()	{
	if (head == NULL) {
		return;
	}
	else {
		Level* current = pop(&head);
		free(current);
		return;
	}
}


/* @function: addOp - Performs Add operations on the top last two values entered
 * and stores the result.
 * If at least one operand is a string, the result is a concatenated string.
 * If both operands are integers the result is an integer.
 * Otherwise, the result is a float, as there is present at least one float 
 * and at most one integer in the operands.
*/

void addOp() 

{	
	// pop items at level one and level two in the stack
	// 	if in either case head is NULL print "Insufficient Arguments"

	if (!(head)) {					// first argument
		logText("Insufficient Arguments\n");
		return;
	}
	Level* levelOne = pop(&head);		// last input

	if (!(head)) {						// if levelTwo is NULL
		logText("Insufficient Arguments\n");
		levelOne->next = head;				// add levelOne back to the stack;
		head = levelOne;
		return;
	}
	
	Level* levelTwo = pop(&head);		// second-to-last input

	// set flag if a string is present
	int hasString = 0;					
	if ((levelOne->type == 2) || (levelTwo->type == 2)) {
		hasString = 1;
	}

	// set flag if no string is present and a float is present
	int hasFloat;
	if (!(hasString)) {
		hasFloat = 0;
		if ((levelOne->type == 1) || (levelTwo->type == 1)) {
			hasFloat = 1;
		}
	}	

	// if there is at least one string: concatenate with level 2 on the left and level 1 on the write
	if (hasString) {
		char outString[MAX_LENGTH] = {0};		
		if ((levelOne->type == 2) && (levelTwo->type == 2)) {
			sprintf(outString, "%s%s", levelTwo->stringvalue, levelOne->stringvalue);
			head = push(head, 2, 0, 0.0, outString);
			free(levelOne);
			free(levelTwo);
			return;
		}
		if (levelOne->type == 2) {
			if (levelTwo->type == 1) {				// if levelOne str and levelTwo float
				sprintf(outString, "%.10g%s", levelTwo->doublevalue, levelOne->stringvalue);
				head = push(head, 2, 0, 0.0, outString);
				free(levelOne);
				free(levelTwo);
				return;
			}
			else {							// levelOne str and levelTwo int
				sprintf(outString, "%d%s", levelTwo->longvalue, levelOne->stringvalue);
				head = push(head, 2, 0, 0.0, outString);
				free(levelOne);
				free(levelTwo);
				return;
			}
		}
		else {								// levelOne not string and levelTwo is string
			if (levelOne->type == 1) {
			sprintf(outString, "%s%.10g", levelTwo->stringvalue, levelOne->doublevalue) ;
			head = push(head, 2, 0, 0.0, outString);
			free(levelOne);
			free(levelTwo);
			return;			
			}
			else {							// levelOne is int and levelTwo is string
				sprintf(outString, "%s%d", levelTwo->stringvalue, levelOne->longvalue);
				head = push(head, 2, 0, 0.0, outString);
				free(levelOne);
				free(levelTwo);
				return;
			}
			}
		}
	else if (hasFloat) {							// if there are no strings (and there is a float)
		double sumFloat;
		if ((levelOne->type == 1) && (levelTwo->type == 1)) {
			sumFloat = add(levelOne->doublevalue, levelTwo->doublevalue);
			head = push(head, 1, 0, sumFloat, "");
			free(levelOne);
			free(levelTwo);
			return;	
		}
		else if ((levelOne->type == 1))	{				// if levelOne is float then levelTwo is integer
			sumFloat = add(levelOne->doublevalue, levelTwo->longvalue);
			head = push(head, 1, 0, sumFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}
		else {								// levelOne is int and levelTwo is float
			sumFloat = add(levelOne->longvalue, levelTwo->doublevalue);
			head = push(head, 1, 0, sumFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}		
	}
	else {									// both levels hold integers
		long sumInt;
		sumInt = add(levelOne->longvalue, levelTwo->longvalue);
		head = push(head, 0, sumInt, 0.0, "");
		free(levelOne);
		free(levelTwo);
		return;
	}
	
}


/* @function: subOp - Subtracts the number in level one (last input) from 
 * the number in level 2. 
 * Or, prints "Insufficient Arguments" for less than two arguments
 * or "Bad Arguments" if one argument is a string.
*/

void subOp() 
{
	// function to verify initial stack requirements
	int stackVerified = operationVerify();
	if (!(stackVerified))	{
		return;
	}
	Level *levelOne = pop(&head);
	Level *levelTwo = pop(&head);

	// check for float
	if ((levelOne->type == 1) || (levelTwo->type ==1)) {
		double subFloat;								// initialize variable for float sub result
		if ((levelOne->type == 1) && (levelTwo->type == 1)) {				// if both values are floats
			subFloat = subtract(levelTwo->doublevalue, levelOne->doublevalue);
			head = push(head, 1, 0, subFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}
		else if ((levelOne->type ==1))	{			// case: levelOne is float and levelTwo is Int
			subFloat = subtract(levelTwo->longvalue, levelOne->doublevalue);
			head = push(head, 1, 0, subFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}
		else	{				// case: levelOne is int and levelTwo is float
			subFloat = subtract(levelTwo->doublevalue, levelOne->longvalue);
			head = push(head, 1, 0, subFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}

	}
	else	{					// case: levelOne and levelTwo both ints
		long subInt = subtract(levelTwo->longvalue, levelOne->longvalue);
		head = push(head, 0, subInt, 0.0, "");
		free(levelOne);
		free(levelTwo);
		return;
	}
	
}


/* @function: timesOP - multiplies the numbers at levels 1 and 2.
 * If either level is a string, prints "Bad Arguments". 
 * If there are less than two arguments, prints "Insuficient Arguments".
 * If at least one number is a float, the product is a float;
 * otherwise it's an integer.
*/

void timesOp()

{
	// function to verify initial stack requirements
	int stackVerified = operationVerify();
	if (!(stackVerified))	{
		return;
	}
	Level *levelOne = pop(&head);
	Level *levelTwo = pop(&head);

	// check for float
	if ((levelOne->type == 1) || (levelTwo->type ==1)) {
		double timesFloat;								// initialize variable for float multiply result
		if ((levelOne->type == 1) && (levelTwo->type == 1)) {				// if both values are floats
			timesFloat = multiply(levelTwo->doublevalue, levelOne->doublevalue);
			head = push(head, 1, 0, timesFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}
		else if ((levelOne->type ==1))	{			// case: levelOne is float and levelTwo is Int
			timesFloat = multiply(levelTwo->longvalue, levelOne->doublevalue);
			head = push(head, 1, 0, timesFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}
		else	{				// case: levelOne is int and levelTwo is float
			timesFloat = multiply(levelTwo->doublevalue, levelOne->longvalue);
			head = push(head, 1, 0, timesFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}

	}
	else	{					// case: levelOne and levelTwo both ints
		long timesInt = multiply(levelTwo->longvalue, levelOne->longvalue);
		head = push(head, 0, timesInt, 0.0, "");
		free(levelOne);
		free(levelTwo);
		return;
	}
	
}


/* @function: divOP - divides the number at level 2 by the number at level 1.
 * If either level is a string, prints "Bad Arguments". 
 * If there are less than two arguments, prints "Insuficient Arguments".
 * If at least one number is a float, the product is a float;
 * otherwise it's an integer.
*/

void divOp()
{
	// function to verify initial stack requirements
	int stackVerified = operationVerify();
	if (!(stackVerified))	{
		return;
	}
	Level *levelOne = pop(&head);
	Level *levelTwo = pop(&head);

	// check for float
	if ((levelOne->type == 1) || (levelTwo->type ==1)) {
		double divFloat;								// initialize variable for float divide result
		if ((levelOne->type == 1) && (levelTwo->type == 1)) {				// if both values are floats
			divFloat = divide(levelTwo->doublevalue, levelOne->doublevalue);
			head = push(head, 1, 0, divFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}
		else if ((levelOne->type ==1))	{			// case: levelOne is float and levelTwo is Int
			divFloat = divide(levelTwo->longvalue, levelOne->doublevalue);
			head = push(head, 1, 0, divFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}
		else	{				// case: levelOne is int and levelTwo is float
			divFloat = divide(levelTwo->doublevalue, levelOne->longvalue);
			head = push(head, 1, 0, divFloat, "");
			free(levelOne);
			free(levelTwo);
			return;
		}

	}
	else	{					// case: levelOne and levelTwo both ints
		long divInt = divide(levelTwo->longvalue, levelOne->longvalue);
		head = push(head, 0, divInt, 0.0, "");
		free(levelOne);
		free(levelTwo);
		return;
	}
	
}


/* @function: wordSquare - creates a normal word square from the top two elements on the stack.
 * The order of operation takes the first entry and applies to it the second.
 * Thus, levelTwo is word1 and levelOne is wordTwo in the wordsquare. 
*/

void wordSquare()
{
	// buffer for printing and logging output
	char logBuffer[40];

	// check for adequate number of levels on the stack 
	if (!sufficientLevels())	{
		logText("Insufficient Arguments\n");
		return;
	}

	// pop top two levels
	Level* levelOne = pop(&head);
	Level* levelTwo = pop(&head);

	// initialize variables to store stringified structs
	char word1[40];
	char word2[40];

	// stringify the levels
	stringifyStruct(levelTwo, word1);
	stringifyStruct(levelOne, word2);
	
	// return levels to stack
	levelTwo->next = head;
	levelOne->next = levelTwo;
	head = levelOne;

	// size words
	size_t wordSize1 = strlen(word1);
	size_t wordSize2 = strlen(word2);

	// find length of shortest word and call it m, then add 1.
	size_t m;
	m = (wordSize1 < wordSize2 ? wordSize1 : wordSize2);
	m++;

        // initialize 2d array with m rows and wordSize1 columns
        char** normalWordSquare;

        // Allocate space for m rows
        normalWordSquare = malloc(m * sizeof(char*));

        // Allocate space for contents of each row, wordSize1 deep
        for (size_t i = 0; i < m; i++)
                normalWordSquare[i] = calloc(wordSize1, sizeof(char));

        // iteratively fill the word grid with word1 on each row
        for (size_t i = 0; i < m; i++)
        {
                for (size_t j = 0; j < wordSize1; j++)
                {
                        normalWordSquare[i][j] = word1[j];
                }
        }

        // edit the grid iteratively with the desired pattern from wordB
        //      edit rows 1 to m at relevant indices

        size_t n = 0;                      //      variable to track edit progress
        for (size_t i = 0; i < m; i++)
        {
                for (size_t j = 0; j < n; j++)
                        normalWordSquare[i][j] = word2[j];
                n++;
        }

        // log and print word square

        for (size_t i = 0; i < m; i++)
        {
                for (size_t j = 0; j < wordSize1; j++)
                {
			logBuffer[j] = normalWordSquare[i][j];
                }
		logBuffer[wordSize1] = '\n';
		logBuffer[wordSize1+1] = '\0';
		logText(logBuffer);
        }

        // free memory
        for (size_t i = 0; i < m; i++)
                free(normalWordSquare[i]);
        free(normalWordSquare);
}


/* @function: roll - Rotates the levels in the stack, such that all levels
 * move up one level, with the current top level rotating down to level 1.
 * If there are no levels on the stack, prints "Insufficient Arguments".
*/

void roll()
{
	// retrieve a count of the current stack size
	size_t levelCount;
	levelCount = countLevels();
	
	// verify at least one argument is present
	if (levelCount < 1)	{
		logText("Insufficient Arguments\n");
	}

	// build tierd level schems based on count and manually rotate levels
		// if five levels
	if (levelCount == 5)	{
		Level *levelOne = pop(&head);
		Level *levelTwo = pop(&head);
		Level *levelThree = pop(&head);
		Level *levelFour = pop(&head);
		Level *levelFive = pop(&head);
	
	// move each level up once and levelFive to the head
		levelFour->next = head;
		levelThree->next = levelFour;
		levelTwo->next = levelThree;
		levelOne->next = levelTwo;
		levelFive->next = levelOne;
		head = levelFive;
		return;
	}

		// if four levels
	if (levelCount == 4)	{
		Level *levelOne = pop(&head);
		Level *levelTwo = pop(&head);
		Level *levelThree = pop(&head);
		Level *levelFour = pop(&head);
	
	// move each level up once and levelFive to the head
		levelThree->next = head;
		levelTwo->next = levelThree;
		levelOne->next = levelTwo;
		levelFour->next = levelOne;
		head = levelFour;
		return;
	}
		// if three levels
	if (levelCount == 3)	{
		Level *levelOne = pop(&head);
		Level *levelTwo = pop(&head);
		Level *levelThree = pop(&head);
	
	// move each level up once and levelFive to the head
		levelTwo->next = head;
		levelOne->next = levelTwo;
		levelThree->next = levelOne;
		head = levelThree;
		return;
	}
		// if three levels
	if (levelCount == 2)	{
		Level *levelOne = pop(&head);
		Level *levelTwo = pop(&head);
	
	// move each level up once and levelFive to the head
		levelOne->next = head;
		levelTwo->next = levelOne;
		head = levelTwo;
		return;
	}
	// otherwise, levelCount < 2
	return;
}


/* @function: print - takes a string and both prints it to the screen
 * and logs it to a file.
*/

void logText(const char* text) 
{
	// print text to screen
	printf("%s", text);

	// open file and log text
	FILE *fileStream = fopen(LOGFILE, "a");
	fprintf(fileStream, "%s", text);

	// close file
	fclose(fileStream);
}


/* @function stringifyStruct - copies the value in a level into a string array.*/

void stringifyStruct(Level* currLevel, char *stringStruct)
{
	// stringify int
	if (currLevel->type == 0)	{
	sprintf(stringStruct, "%d", currLevel->longvalue);
	return;
	}

	// stringify float
	if (currLevel->type == 1)	{
	sprintf(stringStruct, "%.10g", currLevel->doublevalue);
	return;
	}

	// stringify string
	if (currLevel->type == 2)	{
	sprintf(stringStruct, "%s", currLevel->stringvalue);
	return;
	}
}


/*@ function: validInput - validates if all characters are within the range allowable for the program.
 * Acceptable characters are "abcdefghijklmnopqrstuvwxyz0123466789+*-/ "
  * @ char* aWord: a pointer to a sting
 * @ numChars: size of the input string by number of characters
 * @ returns: 0 if word is valid, otherwise -1.
**/

int validInput(char* buffer, int bufferLength)
{
        //              check ascii range 97 to 122 inclusive
        int intchar;

        for (int i = 0; i < bufferLength; i++) {
                intchar = buffer[i];
		if (intchar != 32 && intchar != 42 && intchar != 43 && !(intchar >= 45 && intchar <= 57) 
				&& !(intchar >= 97 && intchar <= 122)) {
				return -1;		// -1 for invalid input
				}
				}
        return 0;
}


/* @ function: floatTest - Checks a string for inclusion of one and only one period.
  * @ char* buffer: a pointer to a sting
 * @ bufferSize: size of the input string by number of characters
 * @ returns: 1 for True, otherwise 0.
*/

int floatTest(char* buffer, int bufferLength)
{
	char localChar;
	int counter = 0;
	for (int i = 0; i < bufferLength; i++) {
		localChar = buffer[i];
		if (localChar == '.') {
			counter ++;
		}
	}
	if (counter == 1) {
		return 1;				// return 1 for True float
	}
	return 0;					// return 0 for False float
}


/* @ function: intTest - Checks a string for inclusion of only integers beyond
  * the initial character.
  * @ char* buffer: a pointer to a sting
 * @ bufferSize: size of the input string by number of characters
 * @ returns: 1 for True, otherwise 0.
*/

int intTest(char* buffer, int bufferLength)
{
	int localIntChar;
	// check for all integers beyond initial character
	for (int i = 1; i < bufferLength; i++) {
		localIntChar = buffer[i];
		if ((localIntChar < 48 || localIntChar > 57)) {
			return 0;				// return 0 for False integer
		}
	}
	return 1;					// return 1 for True integer
}


/* @ function: stringTest - Checks if a string meets the requirements
 * to be treated as a string data type.
 * A string is valid if it contains only lowercase letters, integers, or 
 * whitespace.
 * @ char* buffer: a pointer to a sting
 * @ bufferSize: size of the input string by number of characters
 * @ returns: 0 if word is valid, otherwise -1.
*/

int stringTest(char* buffer, int bufferLength)
{
        int intChar;

        for (int i = 0; i < bufferLength; i++) {
                intChar = buffer[i];
                if ((intChar != 32) && !((intChar >= 48 && intChar <= 57) || (intChar >= 97 && intChar <= 122)))
					{
                        return 0;			// return 0 for False string
			}
        }
        return 1;					// return 1 for True string
}


/* @ function: preOperationVerify - preliminary validation steps common for
 * subtract, multiply, and divide operations.
 * Checks involve confirming that there are two elements on the stack and that
 * neither of the elements on the stack is a string.
 * returns: 0 if the validation is False, otherwise 1.
*/

int operationVerify() 
{
	// pop level 1
	// 	if a sring, bad argument; if Null, insufficient arguments
	if (!(head)) {						// if stack is empty
		logText("Insufficient Arguments\n");
		return 0;
	}
	Level *levelOne = pop(&head);
	if (levelOne->type == 2) {			// if levelOne is a string
		logText("Bad Arguments\n");
		levelOne->next = head;			// return levelOne to the stack
		head = levelOne;
		return 0;
	}
	// pop level 2
	//	check for string or NULL
       if (!(head)) {                                  // if levelTwo is NULL
                logText("Insufficient Arguments\n");
                levelOne->next = head;                  // return levelOne to stack
                head = levelOne;
                return 0;
        }
        Level *levelTwo = pop(&head);                   // pop second level
        if (levelTwo->type == 2) {                      // if levelTwo is string
               logText("Bad Arguments\n");

               // return both levels to the stack
               levelTwo->next = head;
               levelOne->next = levelTwo;
               head = levelOne;
               return 0;
	}
	// on verification success return levels to stack
	levelTwo->next = head;
	levelOne->next = levelTwo;
	head = levelOne;
	return 1;
}


/* @function countLevels - counts the number of items currently on the stack.
 * returns - an integer count of the number of levels on the stack.
*/

int countLevels()
{
	int count = 0;
	if (head == NULL)	{
		return count;
	}
	Level *levelOne = pop(&head);
	count++;
	if (head == NULL)	{
		levelOne->next = head;
		head = levelOne;
		return count;
	}
	Level *levelTwo = pop(&head);
	count++;
	if (head == NULL)	{
		levelTwo->next = head;
		levelOne->next = levelTwo;
		head = levelOne;
		return count;
	}
	Level *levelThree = pop(&head);
	count++;
	if (head == NULL)	{
		levelThree->next = head;
		levelTwo->next = levelThree;
		levelOne->next = levelTwo;
		head = levelOne;
		return count;
	}
	Level *levelFour = pop(&head);
	count++;
	if (head == NULL)	{
		levelFour->next = head;
		levelThree->next = levelFour;
		levelTwo->next = levelThree;
		levelOne->next = levelTwo;
		head = levelOne;
		return count;
	}
	Level *levelFive = pop(&head);
	count++;
	
	// reload stack
	levelFive->next = head;
	levelFour->next = levelFive;
	levelThree->next = levelFour;
	levelTwo->next = levelThree;
	levelOne->next = levelTwo;
	head = levelOne;
	return count;	
}


/* @function: sufficientLevels - checks that there are at least two levels
 * on the stack.
*/

int sufficientLevels()	{
	int levelCount = countLevels();
	if (levelCount < 2)	{
		return 0;		// False
	}
	return 1;			// True
}


/* @function truncateStack - removes the fifth item on the stack. */

void truncateStack()	{

	// access the fifth level by popping lower levels
	Level *levelOne = pop(&head);
	Level *levelTwo = pop(&head);
	Level *levelThree = pop(&head);
	Level *levelFour = pop(&head);

	// remove fifth level
	utilityDrop();

	//reload stack
	levelFour->next = head;
	levelThree->next = levelFour;
	levelTwo->next = levelThree;
	levelOne->next = levelTwo;
	head = levelOne;
	return;
}
