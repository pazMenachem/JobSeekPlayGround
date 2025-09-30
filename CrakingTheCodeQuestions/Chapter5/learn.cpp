#include <iostream>
#include <string>

using namespace std;

int repeatedArithmeticShift(int x, int count) {
    for (int i = 0; i < count; i++) {
    x = x >> 1; // II Arithmetic shift by 1
    }
    return x;
 }
 
//  int repeatedLogicalShift(int x, int count) {
//     for (int i = 0; i < count; i++) {
//     x >>>= 1; // Logical shift by 1
//     }
//     return x;
// }

int main(){
    // cout << repeatedArithmeticShift(-93242, 40) << endl;
    cout << ((110 & 1) == 0 && (110 & 2) == 2) << endl;
    cout << "Great success!\n" << endl;
    return 0;
}