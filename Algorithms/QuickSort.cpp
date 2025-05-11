#include <iostream>
#include <random>
#include <vector>

using namespace std;

// Random number generator
std::random_device rd;   // Get random seed
std::mt19937 gen(rd());  // Mersenne Twister engine

void quickSort(vector<int>& vec, int left, int right){
    if (left >= right) return;
    std::uniform_int_distribution<int> dist(left, right);
    int pivotIndex = dist(gen);
    
    std::swap(vec[pivotIndex], vec[right]);
    int leftBound = left;
    int rightBound = right;
    int currentPivot = right;
    
    while (left <= right){
        if (vec[right] >= vec[currentPivot]){
            right--;  
            continue;
        }
        if (vec[left] < vec[currentPivot]){
            left++;  
            continue;
        }
        std::swap(vec[left], vec[right]);
    }

    std::swap(vec[left], vec[currentPivot]);
    quickSort(vec, leftBound, left - 1);
    quickSort(vec, left + 1, rightBound);
}

int main(){
    vector<int> vec{4, 2, 6, 3, 5, 9, 1};
    quickSort(vec, 0, vec.size() - 1);
    for (int i = 0; i < vec.size(); i++)
        cout << vec[i] << endl;
    cout << "Great success!" << endl;
    return 0;
}