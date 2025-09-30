#include <iostream>
#include <string>
#include <cassert>

using namespace std;

int flipBitToWin(int num) {
    int maxLength = 1;
    int currentLength = 0;
    int previousLength = 0;
    
    while (num) {
        if (num & 1) currentLength++;
        else {
            previousLength = (num & 2) == 0 ? 0 : currentLength;
            currentLength = 0;
        }
        
        maxLength = max(maxLength, currentLength + previousLength + 1);
        num >>= 1;
    }
    
    return maxLength;
}

void runTests() {
    cout << "Running tests..." << endl;
    
    int result1 = flipBitToWin(1775);
    assert(result1 == 8);
    cout << "✓ Test 1 passed: 1775 -> " << result1 << endl;
    
    int result2 = flipBitToWin(0);
    assert(result2 == 1);
    cout << "✓ Test 2 passed: 0 -> " << result2 << endl;
    
    int result3 = flipBitToWin(1);
    assert(result3 == 2);
    cout << "✓ Test 3 passed: 1 -> " << result3 << endl;
    
    int result4 = flipBitToWin(15);
    assert(result4 == 5);
    cout << "✓ Test 4 passed: 15 -> " << result4 << endl;
    
    int result5 = flipBitToWin(255);
    assert(result5 == 9);
    cout << "✓ Test 5 passed: 255 -> " << result5 << endl;
    
    int result6 = flipBitToWin(3);
    assert(result6 == 3);
    cout << "✓ Test 6 passed: 3 -> " << result6 << endl;
    
    int result7 = flipBitToWin(7);
    assert(result7 == 4);
    cout << "✓ Test 7 passed: 7 -> " << result7 << endl;
    
    cout << "All tests passed! 🎉" << endl;
}

int main(){
    runTests();
    cout << "Great success!" << endl;
    return 0;
}