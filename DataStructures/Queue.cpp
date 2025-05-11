#include <vector>
#include <iostream>
#include <memory>
#include <stdexcept>

using namespace std;

typedef struct Node{
    int data;
    shared_ptr<Node> next;
    shared_ptr<Node> prev;
}Node;

class Queue{
    public:
        void insert(int element);
        int removeFirst();
    private:
        shared_ptr<Node> _first = nullptr;
        shared_ptr<Node> _last = nullptr;
};

void Queue::insert(int element){
    shared_ptr<Node> newNode = make_shared<Node>(element, nullptr, _last);
    if (_first)
        _last->next = newNode;
    else
        _first = newNode;
    _last = newNode;
}

int Queue::removeFirst(){
    if (!_first)
        throw out_of_range("Queue is empty.");
    
    int res = _first->data;
    _first = _first->next;
    
    if (_first) _first->prev = nullptr;
    else _last = nullptr;
    
    return res;
}

int main(){
    Queue que;
    que.insert(1);
    que.insert(2);
    que.insert(3);

    try{
        cout << que.removeFirst() << endl;
        cout << que.removeFirst() << endl;
        cout << que.removeFirst() << endl;
        cout << que.removeFirst() << endl;
    }
    catch(out_of_range&){
        cout << "Great Success!" << endl;
    }
    que.insert(1);
    que.insert(2);
    que.insert(3);

    try{
        cout << que.removeFirst() << endl;
        cout << que.removeFirst() << endl;
        cout << que.removeFirst() << endl;
        cout << que.removeFirst() << endl;
    }
    catch(out_of_range&){
        cout << "Great Success!" << endl;
    }
    return 0;
}
