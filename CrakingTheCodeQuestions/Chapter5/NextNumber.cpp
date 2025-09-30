#include <iostream>
#include <string>
#include <cassert>

using namespace std;

void nextNumber(int num, int& small, int& large) {
    small = large = -1;
    
    // Use bit manipulation to find patterns more efficiently
    int temp = num;
    int pos = 0;
    
    while (temp) {
        if ((temp & 3) == 2 && small == -1) small = num ^ (3 << pos);
        if ((temp & 3) == 1 && large == -1) large = num ^ (3 << pos);
        temp >>= 1;
        pos++;
    }
}

// int tmp, i, small_iter, large_iter;
// small_iter = large_iter = large = small = -1;
// tmp = num;
// i = 0;
// while (tmp){
//     if ((tmp & 1) == 0 && (tmp & 2) == 2) if (small_iter == -1) small_iter = i;
//     if ((tmp & 1) == 1 && (tmp & 2) == 0) if (large_iter == -1) large_iter = i;
//     tmp >>= 1;
//     i++;
// }
// if (small_iter != -1) {
//     small = num;
//     small = small | 1 << small_iter;
//     small = small & (~0 ^ (1 << small_iter + 1));
// }

// if (large_iter != -1){
//     large = num;
//     large = large & (~0 ^ (1 << large_iter));
//     large = large | 1 << large_iter + 1;
// }

void runTests() {
    cout << "Running tests..." << endl;
    
    int small, large;
    
    // Test case 1: 1775 (11011101111) -> next smaller and larger with same number of 1s
    nextNumber(1775, small, large);
    assert(small == 1759);  // 11011101110
    assert(large == 1783);  // 11011110111
    cout << "✓ Test 1 passed: 1775 -> small=" << small << ", large=" << large << endl;
    
    // Test case 2: 0 -> edge case
    nextNumber(0, small, large);
    assert(small == -1);  // No smaller number with 0 bits
    assert(large == -1);   // 1 has one bit
    cout << "✓ Test 2 passed: 0 -> small=" << small << ", large=" << large << endl;
    
    // Test case 3: 1 -> edge case
    nextNumber(1, small, large);
    assert(small == -1);  // No smaller number with 1 bit
    assert(large == 2);   // 10 has one bit
    cout << "✓ Test 3 passed: 1 -> small=" << small << ", large=" << large << endl;
    
    // Test case 4: 15 (1111) -> all 1s case
    nextNumber(15, small, large);
    assert(small == -1);   // 1110
    assert(large == 23);   // 10111
    cout << "✓ Test 4 passed: 15 -> small=" << small << ", large=" << large << endl;
    
    // Test case 5: 255 (11111111) -> all 1s case
    nextNumber(255, small, large);
    assert(small == -1);
    assert(large == 383);  // 101111111
    cout << "✓ Test 5 passed: 255 -> small=" << small << ", large=" << large << endl;
    
    // Test case 6: 3 (11) -> simple case
    nextNumber(3, small, large);
    assert(small == -1);   // No smaller with 2 bits
    assert(large == 5);    // 101
    cout << "✓ Test 6 passed: 3 -> small=" << small << ", large=" << large << endl;
    
    // Test case 7: 7 (111) -> simple case
    nextNumber(7, small, large);
    assert(small == -1);   // No smaller with 3 bits
    assert(large == 11);   // 1011
    cout << "✓ Test 7 passed: 7 -> small=" << small << ", large=" << large << endl;
    
    cout << "All tests passed! 🎉" << endl;
}

int main(){
    runTests();
    cout << "Great success!" << endl;
    return 0;
}