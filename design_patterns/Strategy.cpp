/**
 * Strategy Design Pattern
 * 
 * Purpose: Defines a family of algorithms and makes them interchangeable.
 *          Lets the algorithm vary independently from clients that use it.
 * 
 * Components:
 * - IOperation: Strategy interface for operations
 * - AddOperation, SubtractOperation: Concrete strategies
 * - Calculator: Context that uses the strategies
 * 
 * Key Features:
 * - Interchangeable algorithms
 * - Clean separation of operations
 * - Simple strategy switching
 * 
 * Usage Example:
 *   AddOperation add;
 *   Calculator calc;
 *   calc.calculate(add, 10, 5);  // Returns 15
 */

#include <iostream>

using namespace std;

// Strategy interface defining the algorithm contract
class IOperation {
    public:
        virtual ~IOperation() = default;
        // Pure virtual function that concrete strategies must implement
        virtual int calculate(int a, int b) = 0;
};

// Concrete strategy implementing addition operation
class AddOperation: public IOperation {
    public:
        // Implements the calculation strategy for addition
        int calculate(int a, int b) override { 
            return a + b; 
        }
};

// Concrete strategy implementing subtraction operation
class SubtractOperation: public IOperation {
    public:
        // Implements the calculation strategy for subtraction
        int calculate(int a, int b) override { 
            return a - b; 
        }
};

// Context class that uses different strategies
class Calculator {
    public:
        // Executes the given operation strategy
        // @param operation - The strategy to use
        // @param a, b - Numbers to operate on
        // @return Result of the operation
        int calculate(IOperation& operation, int a, int b) const {
            return operation.calculate(a, b);
        }
};

int main() {
    // Create strategy instances
    AddOperation add;
    SubtractOperation sub;
    Calculator calc;

    // Test different strategies
    cout << "Add operation: " << calc.calculate(add, 10, 5) << endl;
    cout << "Subtract operation: " << calc.calculate(sub, 10, 5) << endl;

    return 0;
}