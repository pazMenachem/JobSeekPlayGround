#include <iostream>
#include <string>
#include <cassert>

using namespace std;

int pairWiseSwap(int num) {
    /*

        0xAAAAAAAA = 1010 1010 1010 1010 1010 1010 1010 1010
        0x55555555 = 0101 0101 0101 0101 0101 0101 0101 0101

        Original: 6 = 0000 0000 0000 0000 0000 0000 0000 0110
                Position: 3 2 1 0
                Bits:    0 0 1 1 0

        Step 1: Extract even bits
        num & 0xAAAAAAAA = 0000 0000 0000 0000 0000 0000 0000 0010
                        (bit 1 is set)

        Step 2: Extract odd bits  
        num & 0x55555555 = 0000 0000 0000 0000 0000 0000 0000 0100
                        (bit 2 is set)

        Step 3: Shift even bits right
        (0010) >> 1 = 0001

        Step 4: Shift odd bits left
        (0100) << 1 = 1000

        Step 5: OR them together
        0001 | 1000 = 1001 = 9
    */
    return ((num & 0xAAAAAAAA) >> 1) | ((num & 0x55555555) << 1);
};
// int mask, i, odd, even;
// i = 0;
// while (i < sizeof(num) * 8){
//     even = num & (1 << i);
//     odd = num & (1 << i + 1);
//     mask = ~0;
//     mask ^= 1 << i;
//     mask ^= 1 << i + 1; 
//     num &= mask;
//     num |= (even << 1);
//     num |= (odd >> 1);
//     i += 2;
// }
// return num;

void runTests() {
    cout << "Running tests..." << endl;
    
    // Test case 1: 5 (0101) -> 10 (1010) after swap
    int result1 = pairWiseSwap(5);
    assert(result1 == 10);
    cout << "✓ Test 1 passed: 5 -> " << result1 << endl;
    
    // Test case 2: 10 (1010) -> 5 (101) after swap
    int result2 = pairWiseSwap(10);
    assert(result2 == 5);
    cout << "✓ Test 2 passed: 10 -> " << result2 << endl;
    
    // Test case 3: 0 -> 0 (no change)
    int result3 = pairWiseSwap(0);
    assert(result3 == 0);
    cout << "✓ Test 3 passed: 0 -> " << result3 << endl;
    
    // Test case 4: 1 (01) -> 2 (10) after swap
    int result4 = pairWiseSwap(1);
    assert(result4 == 2);
    cout << "✓ Test 4 passed: 1 -> " << result4 << endl;
    
    // Test case 5: 2 (10) -> 1 (01) after swap
    int result5 = pairWiseSwap(2);
    assert(result5 == 1);
    cout << "✓ Test 5 passed: 2 -> " << result5 << endl;
    
    // Test case 6: 3 (11) -> 3 (11) after swap (no change)
    int result6 = pairWiseSwap(3);
    assert(result6 == 3);
    cout << "✓ Test 6 passed: 3 -> " << result6 << endl;
    
    // Test case 7: 6 (0110) -> 9 (1001) after swap
    int result7 = pairWiseSwap(6);
    assert(result7 == 9);
    cout << "✓ Test 7 passed: 6 -> " << result7 << endl;
    
    // Test case 8: 9 (1001) -> 6 (110) after swap
    int result8 = pairWiseSwap(9);
    assert(result8 == 6);
    cout << "✓ Test 8 passed: 9 -> " << result8 << endl;
    
    // Test case 9: 12 (1100) -> 12 (1100) after swap (no change)
    int result9 = pairWiseSwap(12);
    assert(result9 == 12);
    cout << "✓ Test 9 passed: 12 -> " << result9 << endl;
    
    // Test case 10: 15 (1111) -> 15 (1111) after swap (no change)
    int result10 = pairWiseSwap(15);
    assert(result10 == 15);
    cout << "✓ Test 10 passed: 15 -> " << result10 << endl;
    
    cout << "All tests passed! 🎉" << endl;
}

int main(){
    runTests();
    cout << "\nGreat success!" << endl;
    return 0;
}