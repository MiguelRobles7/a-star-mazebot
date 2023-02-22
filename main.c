#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>

#define FREE 0
#define ALPHA 1
#define BETA 2

#define setY 2
#define setE 6

#define ROW_SIZE 7
#define COL_SIZE 5

#define BOARD_SIZE (ROW_SIZE * COL_SIZE)
typedef char board[BOARD_SIZE];
typedef struct {
	board ind;
	int size;
	char type;
} set; //set of alpha or beta, contains all indices its type in the board
//paired with a board of types another board of indices to its set
//set.ind[ind[x]]=x, ind[set.ind[y]]=y

typedef char printBuf[4 * ROW_SIZE + 2][6 * COL_SIZE + 7];//each cell is [4][6]


#ifdef __GNUC__
int println(const char *format, ...) __attribute__((format(printf, 1, 2)));
#endif

int println(const char *format, ...) {
	va_list args;
	va_start(args, format);
	int result = vprintf(format, args);
	printf("\n");
	va_end(args);
	return result;
}
//gets a valid point of P then convert to 0...BOARD_SIZE-1
int getPoint() {
	int res = 0, x, y;
	char c;
	while (res >= 0) {
		scanf(" %c", &c);
		if (c == '(') {
			res = scanf("%d ,", &x) + scanf("%d ", &y);
			if (getchar() != ')') res = 0;
		} else {
			ungetc(c, stdin);
			res = scanf("%d ,", &x) + scanf("%d", &y);
		}

		if (res == 2) { //if scanned 2 numbers
			if (1 <= x && x <= ROW_SIZE &&
				1 <= y && y <= COL_SIZE) {
				return (x - 1) * COL_SIZE + (y - 1);
			}
		}
		scanf("%*[^\n]%*c");
		println(
			"Invalid, please follow the format below\n"
			"  (row,col)\n"
			"  (row col)\n"
			"  row,col\n"
			"  row col\n"
		);
	}
	return -1;
}








//if pt is in set S
int ptInS(int pt) {
	#if (COL_SIZE&1)
	return pt%2 == 0;//since 0, 2, 4, ..., BOARD_SIZE-1
	#else
	return pt%2 == pt/COL_SIZE%2;//since %EVEN%2 == %2
	#endif
}
/**
 * @brief design of cell
 * 1 2 3
 * 4   6
 * 7 8 9
 * if adding a pointer, just add 16
 * @param buf 
 * @param pt 
 * @param dir 
 */
void pBAddLines(printBuf buf, int pt, int dir) {
	int x = pt/COL_SIZE * 4 + 2;
	int y = pt%COL_SIZE * 6 + 3;
	//copy paste brute force solution
	//down is horizontal flip of up, just flip x1+n with x1-n and \ with /
	//left is vertical flip of right
	switch (dir & (16-1))
	{
	case 1:
		buf[x][y+1] = '-';buf[x][y+2] = '-';
		buf[x+1][y] = '|';
		if (dir > 16) buf[x-1][y-2] = '\\';
		break;
	case 2:
		buf[x+1][y+2] = '\\';
		buf[x+1][y-2] = '/';
		if (dir > 16) buf[x-1][y] = '|';
		break;
	case 3:
		buf[x][y-1] = '-';buf[x][y-2] = '-';
		buf[x+1][y] = '|';
		if (dir > 16) buf[x-1][y+2] = '/';
		break;
	case 4:
		buf[x-1][y+2] = '/';
		buf[x+1][y+2] = '\\';
		if (dir > 16) {buf[x][y-1] = '-';buf[x][y-2] = '-';}
		break;
	case 6:
		buf[x-1][y-2] = '\\';
		buf[x+1][y-2] = '/';
		if (dir > 16) {buf[x][y+1] = '-';buf[x][y+2] = '-';}
		break;
	case 7:
		buf[x][y+1] = '-';buf[x][y+2] = '-';
		buf[x-1][y] = '|';
		if (dir > 16) buf[x+1][y-2] = '/';
		break;
	case 8:
		buf[x-1][y+2] = '/';
		buf[x-1][y-2] = '\\';
		if (dir > 16) buf[x+1][y] = '|';
		break;
	case 9:
		buf[x][y-1] = '-';buf[x][y-2] = '-';
		buf[x-1][y] = '|';
		if (dir > 16) buf[x+1][y+2] = '\\';
		break;
	}
}
//initialize buffer to its starting form
void pBInit(printBuf buf) {
	int i, j;
	for (i=0; i<ROW_SIZE * 4; i+=4) {
		for (j=0; j<COL_SIZE * 6; j+=6) {
			strncpy(&buf[i+0][j], "+-----", 6);
			strncpy(&buf[i+1][j], "|     ", 6);
			strncpy(&buf[i+2][j], "|     ", 6);
			strncpy(&buf[i+3][j], "|     ", 6);
		}
	}
	for (j=0; j<COL_SIZE * 6; j+=6)
		strncpy(&buf[i][j], "+-----", 6);
	for (i=0, j=1; j<=ROW_SIZE; j++) {
		strncpy(&buf[i++][COL_SIZE*6], "+     \n", 7);
		strncpy(&buf[i++][COL_SIZE*6], "|     \n", 7);
		snprintf(&buf[i][COL_SIZE*6], 7, "| (%d)   ", j);
		buf[i++][COL_SIZE*6+6] = '\n';
		strncpy(&buf[i++][COL_SIZE*6], "|     \n", 7);
	}
	strncpy(&buf[i++][COL_SIZE*6], "+     \n", 7);
	//add underlines
	for (int i=0; i<BOARD_SIZE; i++)
		if (ptInS(i))
			strncpy(&buf[i/COL_SIZE * 4 + 4][i % COL_SIZE * 6 + 1], "~~~~~", 5);

	for (i=0, j=1; j<=COL_SIZE; j++, i+=6)
		snprintf(&buf[ROW_SIZE*4+1][i], 7, "  (%d)  ", j);
	
	buf[ROW_SIZE*4+1][i++] = '\n'; buf[ROW_SIZE*4+1][i++] = '\0';
}
//fills up the buffer according to board
void pBSetBoard(printBuf buf, board board) {
	int x, y, pt;
	for (pt=0; pt<BOARD_SIZE; pt++) {
		x = pt/COL_SIZE * 4 + 2;
		y = pt%COL_SIZE * 6 + 3;

		strncpy(&buf[x-1][y-2], "     ", 5);
		strncpy(&buf[x][y-2], "     ", 5);
		strncpy(&buf[x+1][y-2], "     ", 5);
		if (board[pt] == ALPHA) {
			pBAddLines(buf, pt, 2);
			buf[x][y] = 'A';
		} else if (board[pt] == BETA) {
			pBAddLines(buf, pt, 8);
			buf[x][y] = 'B';
		} else {
			buf[x][y] = 'F';
		}
	}
}
//deletes a point on buffer
void pBDelPt(printBuf buf, int pt) {
	int x = pt/COL_SIZE * 4 + 2;
	int y = pt%COL_SIZE * 6 + 3;
	if (buf[x][y] == 'F') {println("ERROR at pBDelPt, unable to delete a FREE point"); exit(-1);}
	strncpy(&buf[x-1][y-2], " *** ", 5);
	strncpy(&buf[x][y-2], "* F *", 5);
	strncpy(&buf[x+1][y-2], " *** ", 5);
}
//moves a point on buffer
void pBMovePt(printBuf buf, int from, int to) {
	int x1 = from/COL_SIZE * 4 + 2,
		y1 = from%COL_SIZE * 6 + 3,
		x2 = to/COL_SIZE * 4 + 2,
		y2 = to%COL_SIZE * 6 + 3;
	if (buf[x2][y2] != 'F') {println("ERROR at pBufMovePt, moving to a point that is not FREE"); exit(-1);}
	if (buf[x1][y1] == 'F') {println("ERROR at pBufMovePt, unable to move a point that is FREE"); exit(-1);}

	//only one move can happen per turn
	buf[x2][y2] = buf[x1][y1];
	strncpy(&buf[x1-1][y1-2], "     ", 5);
	strncpy(&buf[x1][y1-2], "  F  ", 5);
	strncpy(&buf[x1+1][y1-2], "     ", 5);

	x2 = (x2 < x1) ?-1 :(x2 > x1); //sign function of x2-x1
	y2 = (y2 < y1) ?-1 :(y2 > y1); //sign function of y2-y1
	pBAddLines(buf, to, 16 + (5 + 3 * x2) + y2);
}
//highlights a point on buffer
void pBHighlightPt(printBuf buf, int pt) {
	int x = pt/COL_SIZE * 4 + 2;
	int y = pt%COL_SIZE * 6 + 3;
	for (int i=-1; i<=1; i++) {
		buf[x+i][y-3] = '{';
		buf[x+i][y+3] = '}';
	}
}
// reset highlights a point on buffer
void pBUnhighlightPt(printBuf buf, int pt) {
	int x = pt/COL_SIZE * 4 + 2;
	int y = pt%COL_SIZE * 6 + 3;
	for (int i=-1; i<=1; i++) {
		buf[x+i][y-3] = '|';
		buf[x+i][y+3] = '|';
	}
}











/**
 * @brief addition of element to a set
 * 
 * @param types board containing types
 * @param typeInd board containing indices to the set
 * @param set set containing indices to the board
 * @param pt point to insert in types
 */
void addPoint(board types, board typeInd, set* set, int pt) {
	if (types[pt] != FREE) {println("ERROR at addPoint, type is not FREE"); exit(-1);}
	types[pt] = set->type;
	typeInd[pt] = set->size;
	set->ind[set->size++] = pt;
}
/**
 * @brief subtraction of element in set
 * 
 * @param types board containing types
 * @param typeInd board containing indices to the set
 * @param set set containing indices to the board
 * @param pt point to delete in types
 */
void deletePoint(board types, board typeInd, set* set, int pt) {
	if (types[pt] != set->type) return; //no subtraction can occur

	int el = set->ind[--set->size]; //delete last element of set
	//el is index of affected element in typeInd
	set->ind[(int)typeInd[pt]] = el; //move el to the index of pt (since pt will be deleted)
	typeInd[el] = typeInd[pt]; //now update typeInd to match its index at set

	types[pt] = FREE;
}
//deletes then adds point
void movePoint(board types, board typeInd, set* set, int from, int to) {
	deletePoint(types, typeInd, set, from);
	addPoint(types, typeInd, set, to);
}
//if all points in set is in Y
int allY(set* set) {
	int i = set->size, pt;
	while (i-- > 0) {
		pt = set->ind[i];
		if (!ptInS(pt) || pt/COL_SIZE + 1 > setY)
			return 0;
	}
	return 1;
}
// if all points in set is in E
int allE(set* set) {
	int i = set->size, pt;
	while (i-- > 0) {
		pt = set->ind[i];
		if (!ptInS(pt) || pt/COL_SIZE + 1 < setE)
			return 0;
	}
	return 1;
}
//if gameover
int gameOver(board board, set *alpha, set *beta) {
	return alpha->size == 0 || beta->size == 0 || allY(alpha) || allE(beta);
}











int main() {
	board board = {}, //set of types
		ind; //set of indices to alpha and beta
	set alpha, beta; //set of indices to set of types

	int aTurn = 1, //aturn or bturn
		ok = 0; //if move is valid
	int prev, next; //moves
	int a, b, c, d; //x y coordinates of moves
	printBuf buf; //string representation of board, so effects can be applied easier

	const char* moveErr = ""; //if there is an illegal move
	int prevType = !aTurn; //who made prev move
	
	pBInit(buf);

	alpha.type = ALPHA; alpha.size = 0;
	beta.type = BETA; beta.size = 0;
	for (int i=0; i<COL_SIZE*setY; i++)
		if (ptInS(i)) addPoint(board, ind, &beta, i);
	for (int i=(setE-1)*COL_SIZE; i<BOARD_SIZE; i++)
		if (ptInS(i)) addPoint(board, ind, &alpha, i);

	pBSetBoard(buf, board);
	println("%s", buf[0]);
	println("|A| = %d, |B| = %d", alpha.size, beta.size);
	println("prev: (NA,NA)"); //prev is not in free, alpha, or beta
	prev = 1; //prev is free, but this will still work
	a=c=0; //so first iteration will never work

	while (1) {
		printf("%c turn: ", (aTurn) ?'A' :'B');
		next = getPoint();

		c = next/COL_SIZE + 1; d = next%COL_SIZE + 1;

		//nextPlayerMove
		if (aTurn && board[prev] == ALPHA && a == c + 1 && (b == d || b + 1 == d || b == d + 1)) {
			ok = !ok;
		} else if (!aTurn && board[prev] == BETA && a + 1 == c && (b == d || b + 1 == d || b == d + 1)) {
			ok = !ok;
		} else if (!ok) {
			if (prevType != aTurn)
				prevType = aTurn; //no invalid move for first turn
			else if (aTurn) {
				if (board[prev] == ALPHA)
					moveErr = "A can only normally move 1 cell upwards";
				else
					moveErr = "Player A can only move A"; 
			} else {
				if (board[prev] == BETA)
					moveErr = "B can only normally move 1 cell downwards";
				else
					moveErr = "Player B can only move B";
			}
			
		}
		if (ok) {
			//prevType = aTurn;//to determine if aTurn has changed
			if (board[next] == FREE) {
				pBSetBoard(buf, board);
				movePoint(board, ind, (aTurn) ?&alpha :&beta, prev, next);
				pBMovePt(buf, prev, next);
				ok = !ok;
				aTurn = !aTurn;
			} else if (aTurn && board[next] == BETA) {
				if (ptInS(next)) {
					pBSetBoard(buf, board);
					deletePoint(board, ind, &beta, next);
					pBDelPt(buf, next);

					movePoint(board, ind, &alpha, prev, next);
					pBMovePt(buf, prev, next);
					aTurn = !aTurn;
				} else {
					moveErr = "Cannot eat a unit in set S";
				}
				ok = !ok;
			} else if (!aTurn && board[next] == ALPHA) {
				if (ptInS(next)) {
					pBSetBoard(buf, board);
					deletePoint(board, ind, &alpha, next);
					pBDelPt(buf, next);

					movePoint(board, ind, &beta, prev, next);
					pBMovePt(buf, prev, next);
					aTurn = !aTurn;
				} else {
					moveErr = "Cannot eat a unit in set S";
				}
				ok = !ok;
			}
		}
		
		pBUnhighlightPt(buf, prev);
		pBHighlightPt(buf, next);

		if (gameOver(board, &alpha, &beta))
			break;

		println("%s", buf[0]);
		println("|A| = %d, |B| = %d", alpha.size, beta.size);

		if (*moveErr != '\0') {
			printf("Illegal move: ");
			println("%s", moveErr);
			moveErr = "";
		}

		prev = next;
		a=c; b=d;
		println("prev: (%d, %d)", a, b);
	}

	println("%s", buf[0]);
	if (beta.size == 0 || (alpha.size != 0 && allY(&alpha)))
		println("Congratulations, Alpha wins!");
	else if (alpha.size == 0 || (beta.size != 0 && allE(&beta)))
		println("Congratulations, Beta wins!");
		
	return 0;
}