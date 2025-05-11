#include <stdlib.h>
#include <stdio.h>

typedef struct Object{
    int data;
}Object;

// void contentModify(Object* ptr){
//     ptr->data = 10;
// }

// void ptrContentModify(){
//     Object* ptr = malloc(sizeof(Object));
// }

void func(Object* ptr){
    printf("Address of ptr in func-> %d\n", &ptr);
    printf("Address of ptr content in func-> %d\n", &(*ptr));
}

void ptrParamCopy(){
    Object* ptr = malloc(sizeof(Object));
    printf("Address of ptr before call -> %d\n", &ptr);
    printf("Address of ptr content before call -> %d\n", &(*ptr));
    func(ptr);
    free(ptr);
}

int main(){
    return 0;
}
