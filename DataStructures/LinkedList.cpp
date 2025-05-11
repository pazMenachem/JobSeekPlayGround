#include <iostream>

using namespace std;

typedef struct Node{
    int data;
    Node* next = nullptr;
}Node;

class LinkedList{
    public:
        void insert(int val);
        void remove(int val);
        void print();
        Node* search(int val);
        ~LinkedList();

    private:
        Node* _head = nullptr;
        int _size = 0;
};

LinkedList::~LinkedList(){
    Node* tmp = nullptr;
    while(_head){
        tmp = _head;
        _head = _head->next;
        delete(tmp);
    }
    _size = 0;
}

void LinkedList::insert(int val){
    _head = new Node{val, _head};
    _size++;
}

void LinkedList::remove(int val){
    if (!_head) return;
    Node* tmp = _head;
    Node* prev = nullptr;

    if (_head->data == val){
        _head = tmp->next;
        delete(tmp);
        _size--;
        return;
    }

    while(tmp){
        if (tmp->data == val){
            prev->next = tmp->next;
            delete(tmp);
            _size--;
            return;
        }
        prev = tmp;
        tmp = tmp->next;
    }
}

void LinkedList::print(){
    Node* tmp = _head;
    
    while(tmp){
        cout << tmp->data << " -> ";
        tmp = tmp->next;
    }
    cout << endl;
}
Node* LinkedList::search(int val){
    Node* tmp = _head;
    
    while(tmp){
        if (tmp->data == val) return tmp;
        tmp = tmp->next;
    }
    return nullptr;
}

int main(){
    LinkedList ll; 
    ll.insert(1);
    ll.insert(2);
    ll.insert(3);
    ll.insert(4);
    ll.insert(5);
    ll.print();
    ll.remove(3);
    ll.print();
    ll.search(2);
    cout << "Great Success!" << endl;
    return 0;
}
