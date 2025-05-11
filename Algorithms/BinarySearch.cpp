#include <iostream>
#include <vector>

using namespace std;

#define NOT_FOUND -1

int binarySearch(const vector<int>& vec, int target, int left, int right){
    int mid = left + (right - left) / 2;
    
    if (!(right - left)) return NOT_FOUND;
    
    if (vec[mid] == target) return mid;
    if (vec[mid] > target) return binarySearch(vec, target, left, mid - 1);
    return binarySearch(vec, target, mid + 1, right);
}

int main(){
    vector<int> vec{1,2,3,4,5,6};
    int target = 8;
    cout << target << (binarySearch(vec, target, 0, vec.size() - 1) == NOT_FOUND? " Is NOT in the vector" : " Is IN the vector") << endl;
    return 0;
}