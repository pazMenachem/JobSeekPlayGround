#include <stdio.h>
#include <stdlib.h>

typedef struct Node{
    int data;
    struct Node* next;
}Node;

void print_list(Node* head){
    Node* tmp = head;

    while (tmp){
        printf("%d -> ", tmp->data);
        tmp = tmp->next;
    }
    printf("\n");
}

Node* add_node(Node* head, int val){
    Node* newNode = (Node*) malloc(sizeof(Node));
    if (!newNode)
        return head;

    newNode->data = val;
    newNode->next = head;
    return newNode;
}

Node* reverse_list(Node* head){
    if (!head){
        return NULL;
    }
    Node* next = head->next;
    Node* curr = head;
    Node* prev = NULL;


    while (next){
        curr->next = prev;
        prev = curr;
        curr = next;
        next = next->next;
    }
    curr->next = prev;
    return curr;
}

void free_list(Node* head){
    while (!head){
        Node* tmp = head->next;
        free(head);
        head = tmp;
    }
}

int main(){
    Node* list = NULL;
    list = add_node(list, 1);
    list = add_node(list, 2);
    list = add_node(list, 3);
    list = add_node(list, 4);
    
    print_list(list);
    list = reverse_list(list);
    print_list(list);

    free_list(list);
    list = NULL;
    return 0;
}