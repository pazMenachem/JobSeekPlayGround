#include <iostream>
#include <string>
#include <cassert>

using namespace std;

string binaryToString(double num){
    if (!num) return "0.0";

    string res;
    while (num && res.length() < 32){
        num *= 2;
        if (num >= 1){
            res.push_back('1');
            num -= 1;
        }
        else
            res.push_back('0');
    }
    return num ?  "ERROR" : "0." + res;
};

void runTests() {
    cout << "Running tests..." << endl;
    
    // Test case 1: 0.5 -> "0.1" (terminates in 1 step)
    string result1 = binaryToString(0.5);
    assert(result1 == "0.1");
    cout << "✓ Test 1 passed: 0.5 -> " << result1 << endl;
    
    // Test case 2: 0.25 -> "0.01"
    string result2 = binaryToString(0.25);
    assert(result2 == "0.01");
    cout << "✓ Test 2 passed: 0.25 -> " << result2 << endl;
    
    // Test case 3: 0.75 -> "0.11"
    string result3 = binaryToString(0.75);
    assert(result3 == "0.11");
    cout << "✓ Test 3 passed: 0.75 -> " << result3 << endl;
    
    // Test case 4: 0.1 -> should hit the cap and return "ERROR"
    string result4 = binaryToString(0.1);
    assert(result4 == "ERROR");
    cout << "✓ Test 4 passed: 0.1 -> " << result4 << " (hit the cap)" << endl;
    
    // Test case 5: 0.35 -> should also hit the cap and return "ERROR"
    string result5 = binaryToString(0.35);
    assert(result5 == "ERROR");
    cout << "✓ Test 5 passed: 0.35 -> " << result5 << " (hit the cap)" << endl;
    
    // Additional edge cases
    // Test case 6: 0.0 -> "0."
    string result6 = binaryToString(0.0);
    assert(result6 == "0.0");
    cout << "✓ Test 6 passed: 0.0 -> " << result6 << endl;
    
    // Test case 7: 0.125 -> "0.001" (1/8)
    string result7 = binaryToString(0.125);
    assert(result7 == "0.001");
    cout << "✓ Test 7 passed: 0.125 -> " << result7 << endl;
    
    cout << "All tests passed! 🎉" << endl;
}

int main(){
    runTests();
    cout << "Great success!" << endl;
    return 0;
}