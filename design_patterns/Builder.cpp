/**
 * Builder Design Pattern
 * 
 * Purpose: Separates the construction of complex objects from their representation,
 *          allowing the same construction process to create different representations.
 * 
 * Components:
 * - Person: Product class that's being built
 * - Builder: Builder class with fluent interface for construction
 * 
 * Key Features:
 * - Step-by-step construction
 * - Method chaining (fluent interface)
 * - Clear separation of construction and representation
 * 
 * Usage Example:
 *   Person p = Builder()
 *              .addFirstName("John")
 *              .addLastName("Doe")
 *              .addAge(30)
 *              .build();
 */

#include <stdio.h>
#include <iostream>
#include <string>

// Product class that will be built
class Person {
    public:
        // Constructor with all required parameters
        Person(const std::string& firstName, 
              const std::string& lastName, 
              int age): 
            _firstName(firstName), 
            _lastName(lastName), 
            _age(age) {}

    private:
        std::string _firstName;
        std::string _lastName;
        int _age;
};

// Builder class with fluent interface
class Builder {
    public:
        Builder() = default;

        // Add first name to the person
        Builder& addFirstName(std::string firstName) {
            _firstName = std::move(firstName);
            return *this;
        }

        // Add last name to the person
        Builder& addLastName(std::string lastName) {
            _lastName = std::move(lastName);
            return *this;
        }

        // Add age to the person
        Builder& addAge(int age) {
            _age = age;
            return *this;
        }

        // Create the final Person object
        Person build() {
            Person p{_firstName, _lastName, _age};
            std::cout << "Address of Person in creation: " << &p << std::endl;
            return p;
        }

    private:
        std::string _firstName;
        std::string _lastName;
        int _age;
};

int main() {
    // Example usage of Builder pattern
    Person p = Builder()
        .addFirstName("Nick")
        .addLastName("Ger")
        .addAge(33)
        .build();
    
    std::cout << "Address of Person in main: " << &p << std::endl;
    return 0;
}