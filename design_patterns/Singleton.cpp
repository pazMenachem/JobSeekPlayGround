/**
 * Singleton Design Pattern
 * 
 * Purpose: Ensures a class has only one instance and provides a global point
 *          of access to that instance.
 * 
 * Components:
 * - Singleton: Class that manages its own unique instance
 * 
 * Key Features:
 * - Private constructor
 * - Static instance access
 * - Lazy initialization
 * - Prevents copying/assignment
 * 
 * Usage Example:
 *   Singleton* instance = Singleton::getInstance();
 *   instance->func();
 */

#include <iostream>

class Singleton{
    public:
        // Get the singleton instance
        static Singleton* getInstance(){
            if (!_instance) _instance = new Singleton();
            return _instance;
        }
        // Prevent copying
        Singleton(const Singleton& other) = delete;
        Singleton& operator=(const Singleton& other) = delete;
        
        // Example method
        void func(){
            std::cout << "Hear me rawr!" << std::endl;
        }
        // Cleanup method
        static void deleteInstance(){
            delete(_instance);
            _instance = nullptr;
        }
    private:
        // Private constructor and instance pointer
        static Singleton* _instance;
        Singleton() = default;
};

// Initialize static member
Singleton* Singleton::_instance = nullptr;

class A{
    A() = default;
    public:
        void func(){
            std::cout << "Hear me rawr!" << std::endl;
        }
};

int main(){
    // Get singleton instance twice - should be same address
    Singleton* instance;
    instance = Singleton::getInstance();
    std::cout << "Address of first call: " << &(*instance) << std::endl;
    
    instance = Singleton::getInstance();
    std::cout << "Address of second call: " << &(*instance) << std::endl;

    // Cleanup
    Singleton::deleteInstance();
    return 0;
};