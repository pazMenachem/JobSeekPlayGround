#include <vector>
#include <iostream>

using namespace std;

vector<int> combineVectors(vector<int> vecA, vector<int> vecB){
    vector<int> newVec(vecA.size() + vecB.size());
    int a = 0, b = 0;
    for (int i = 0; i < newVec.size(); i++){
        if (a >= vecA.size()) {newVec[i] = vecB[b++]; continue;}
        if (b >= vecB.size()) {newVec[i] = vecA[a++]; continue;}
        if (vecA[a] <= vecB[b]) newVec[i] = vecA[a++];
        else newVec[i] = vecB[b++];
    }
    return newVec;
}

vector<int> mergeSort(vector<int>& vec){
    int mid = vec.size() / 2;
    
    if (!mid) return vec;

    vector<int> left(vec.begin(), vec.begin() + mid);
    vector<int> right(vec.begin() + mid, vec.end());

    return combineVectors(mergeSort(left), mergeSort(right));
}

int main(){
    vector<int> vec{3, 1, 5, 4, 2};
    // cout << *(vec.begin() + 2) << endl;
    vector<int> res(mergeSort(vec));
    for (auto& it: res) cout << it << endl; 
    return 0;
}