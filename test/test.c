// clang -O0 -g test/test.c -o test/test.bc
#include <stdio.h>

// 定义一个函数原型
typedef void (*operation_func)(int, int);

// 定义一个结构体 Operation，包含一个函数指针和指向下一个结构体的指针
typedef struct Operation {
    operation_func operation;  // 当前结构体的函数指针
    struct Operation *next;    // 指向下一个 Operation 结构体的指针
} Operation;

// 定义两个操作函数
void add(int a, int b) {
    printf("Addition result: %d\n", a + b);
}

void multiply(int a, int b) {
    printf("Multiplication result: %d\n", a * b);
}

void subtract(int a, int b) {
    printf("Subtraction result: %d\n", a - b);
}

int main() {
    // 创建三个结构体实例，并设置链式结构
    Operation op1, op2, op3;
    
    // 初始化 op1
    op1.operation = add;
    op1.next = &op2;

    // 初始化 op2
    op2.operation = multiply;
    op2.next = &op3;

    // 初始化 op3
    op3.operation = subtract;
    op3.next = NULL;  // 结束链表

    // 链式调用
    Operation *current = &op1;
    while (current != NULL) {
        current->operation(10, 5);  // 调用当前结构体中的操作函数
        current = current->next;    // 跳转到下一个结构体
    }

    return 0;
}
