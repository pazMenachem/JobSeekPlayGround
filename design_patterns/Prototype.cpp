/**
 * Prototype Design Pattern
 * 
 * Purpose: Creates new objects by cloning existing ones.
 * 
 * Components:
 * - IPrototype: Base class with clone() method
 * - Human, Robot: Concrete classes that can be cloned
 * 
 * Key Features:
 * - Each class implements clone() method
 * - Uses ID system to track instances
 * - Supports deep copying of objects
 * 
 * Usage Example:
 *   Human original;
 *   Human* clone = static_cast<Human*>(original.clone());
 */

#include <format>
#include <iostream>
#include <vector>

#define ITERS 10

using namespace std;

// Base prototype class that defines cloning interface
class IPrototype{
    public:
        IPrototype(): _id(_nextId++){};
        virtual ~IPrototype() = default;
        virtual IPrototype* clone() = 0;
        virtual void communicate() = 0;
    protected:
    int _id;
    private:
    static int _nextId;
};

int IPrototype::_nextId = -2;

// Concrete prototype that can be cloned
class Human: public IPrototype{
    public:
        Human() = default;
        Human(const Human& other){
            cout << format("Creating another human using Copy c'tur!") << endl;
        };
        ~Human() = default;
        IPrototype* clone() override{
            return new Human(*this);
        }
        void communicate(){cout << format("Hello! I'm human number {}", _id) << endl;};
    private:
};

// Another concrete prototype
class Robot: public IPrototype{
    public:
        Robot() = default;
        Robot(const Robot& other){
            cout << format("Creating another Robot using Copy c'tur!") << endl;
        };
        ~Robot() = default;
        IPrototype* clone() override{
            return new Robot(*this);
        };
        void communicate(){cout << format("Hello! I'm Robot number {}", _id) << endl;};
    private:
};

int main(){
    // Example usage of the Prototype pattern
    Human mainHuman;
    Robot mainRobot;
    vector<IPrototype*> vec;

    // Create multiple clones
    for (int i = 0; i < ITERS * 2; i += 2){
        vec.push_back(static_cast<Human*>(mainHuman.clone()));
        vec.push_back(static_cast<Robot*>(mainRobot.clone()));
    }

    // Test the clones
    for(auto* it: vec) it->communicate();
    
    // Cleanup
    for(auto* it: vec) delete(it);

    return 0;
}
