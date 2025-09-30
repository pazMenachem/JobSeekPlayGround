#include <iostream>
#include <string>
#include <cassert>

using namespace std;

int conversion(int source, int destination) {
    // better version
    // sets different bits.
    int diff = source ^ destination;
    int count = 0;
    while (diff) {
        count++;
        diff &= (diff - 1); // Remove rightmost set bit
    }
    return count;
}

// int count = 0;
// while (source || destination){
//     if ((source & 1) ^ (destination & 1)) count++;
//     source >>= 1;
//     destination >>= 1;
// }
// return count;


void runTests() {
    cout << "Running tests..." << endl;
    
    // Test case 1: 29 (11101) to 15 (01111) -> 2 flips
    int result1 = conversion(29, 15);
    assert(result1 == 2);
    cout << "✓ Test 1 passed: 29 -> 15 = " << result1 << " flips" << endl;
    
    // Test case 2: 0 to 0 -> 0 flips
    int result2 = conversion(0, 0);
    assert(result2 == 0);
    cout << "✓ Test 2 passed: 0 -> 0 = " << result2 << " flips" << endl;
    
    // Test case 3: 0 to 1 -> 1 flip
    int result3 = conversion(0, 1);
    assert(result3 == 1);
    cout << "✓ Test 3 passed: 0 -> 1 = " << result3 << " flips" << endl;
    
    // Test case 4: 1 to 0 -> 1 flip
    int result4 = conversion(1, 0);
    assert(result4 == 1);
    cout << "✓ Test 4 passed: 1 -> 0 = " << result4 << " flips" << endl;
    
    // Test case 5: 7 (111) to 3 (011) -> 1 flip
    int result5 = conversion(7, 3);
    assert(result5 == 1);
    cout << "✓ Test 5 passed: 7 -> 3 = " << result5 << " flips" << endl;
    
    // Test case 6: 15 (1111) to 0 -> 4 flips
    int result6 = conversion(15, 0);
    assert(result6 == 4);
    cout << "✓ Test 6 passed: 15 -> 0 = " << result6 << " flips" << endl;
    
    // Test case 7: 255 (11111111) to 0 -> 8 flips
    int result7 = conversion(255, 0);
    assert(result7 == 8);
    cout << "✓ Test 7 passed: 255 -> 0 = " << result7 << " flips" << endl;
    
    // Test case 8: 5 (101) to 10 (1010) -> 4 flips
    int result8 = conversion(5, 10);
    assert(result8 == 4);
    cout << "✓ Test 8 passed: 5 -> 10 = " << result8 << " flips" << endl;
    
    // Test case 9: 12 (1100) to 3 (0011) -> 4 flips
    int result9 = conversion(12, 3);
    assert(result9 == 4);
    cout << "✓ Test 9 passed: 12 -> 3 = " << result9 << " flips" << endl;
    
    // Test case 10: 1775 to 1783 -> 2 flip
    int result10 = conversion(1775, 1783);
    assert(result10 == 2);
    cout << "✓ Test 10 passed: 1775 -> 1783 = " << result10 << " flips" << endl;
    
    cout << "All tests passed! 🎉" << endl;
}

int main(){
    // runTests();
    cout << (1 << 2);
    cout << "\nGreat success!" << endl;
    return 0;
}