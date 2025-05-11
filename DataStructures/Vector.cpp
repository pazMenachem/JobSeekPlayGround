#include <iostream>
#include <stdexcept>


using namespace std;

class Vector{
    public:
        Vector();
        void pushBack(int element);
        int pop();
        int find(int element);
        int operator[](int index);
        int* begin();
        int* end();
        void reset();
        ~Vector(){
            delete[] _arr;
        }

    private:
        int* copyElements(int newArrsize){
            int* newArr = new int[newArrsize];
            
            for (int i = 0; i < _currentSize; i++)
                newArr[i] = _arr[i];
            return newArr;
        }
        void modifySize(bool incDec){ // True - Increase / False - Decrease
            int* tmp = incDec? copyElements(_maxSize * 2) : copyElements(_maxSize * 0.5);
            delete[] _arr;
            _arr = tmp;
        }

        int* _arr;
        int _currentSize;
        int _maxSize;
};

Vector::Vector():_arr(new int[1]), _currentSize(0), _maxSize(1){}

int* Vector::begin(){
    return _arr;
}
int* Vector::end(){
    return _arr + _currentSize;
}

void Vector::pushBack(int element){
    if (_currentSize * 2 >= _maxSize)
        modifySize(true);
    _arr[_currentSize++] = element;
}

void Vector::reset(){
    _currentSize = 0;
}

int Vector::pop(){
    if (_currentSize){
            if ((static_cast<float>(_currentSize) / _maxSize) <= 0.25)
                modifySize(false);
            return _arr[--_currentSize];
        }
    throw out_of_range("No elements in vector.");
}

int Vector::find(int element){
    for(int i = 0; i < _currentSize; i++)
        if (element == _arr[i])
            return i;
    return -1;
}

int Vector::operator[](int index){
    if (index >= _currentSize)
        throw out_of_range("Index out of bound");
    return _arr[index];
}

int main(){
    Vector vec;
    vec.pushBack(5);
    vec.pushBack(5);
    vec.pushBack(3);
    vec.pushBack(2);
    vec.pushBack(4);
    cout << vec.find(5) << endl;
    cout << vec.pop() << endl;

    for (auto& element: vec)
        cout << element << " -> ";
    cout << endl;

    cout << "Great Success!";
    return 0;
}