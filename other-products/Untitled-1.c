#include <stdio.h>
#define MAX 5

int stack[MAX];
int top = -1;

/* PUSH OPERATION */
void push() {
    int value;
    if (top == MAX - 1) {
        printf("Stack Overflow\n");
    } else {
        printf("Enter value to push: ");
        scanf("%d", &value);
        stack[++top] = value;
        printf("%d pushed into stack\n", value);
    }
}

/* POP OPERATION */
void pop() {
    if (top == -1) {
        printf("Stack Underflow\n");
    } else {
        printf("%d popped from stack\n", stack[top--]);
    }
}

/* PEEK OPERATION */
void peek() {
    if (top == -1) {
        printf("Stack is empty\n");
    } else {
        printf("Top element is: %d\n", stack[top]);
    }
}

/* DISPLAY OPERATION */
void display() {
    if (top == -1) {
        printf("Stack is empty\n");
    } else {
        printf("Stack elements are:\n");
        for (int i = top; i >= 0; i--) {
            printf("%d\n", stack[i]);
        }
    }
}

/* CHECK EMPTY */
void isEmpty() {
    if (top == -1)
        printf("Stack is Empty\n");
    else
        printf("Stack is NOT Empty\n");
}

/* CHECK FULL */
void isFull() {
    if (top == MAX - 1)
        printf("Stack is Full\n");
    else
        printf("Stack is NOT Full\n");
}


































.....................................................................................................................................................................................................................