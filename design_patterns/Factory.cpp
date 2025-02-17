/**
 * Factory Design Pattern
 * 
 * Purpose: Creates objects without exposing creation logic to the client.
 * 
 * Components:
 * - Pokemon: Abstract base class defining interface
 * - Pikachu, Mewo, Charizard: Concrete Pokemon classes
 * - FactoryPokemon: Factory class that creates Pokemon instances
 * 
 * Key Features:
 * - Centralized object creation
 * - Error handling for invalid types
 * - Uses map to store creation functions
 * 
 * Usage Example:
 *   FactoryPokemon factory;
 *   Pokemon* pika = factory.createPokemon(1);  // Creates Pikachu
 */

#include <iostream>
#include <unordered_map>
#include <functional>
#include <vector>

using namespace std;

// Abstract base class defining Pokemon interface
class IPokemon {
    public:
        IPokemon() = default;
        virtual ~IPokemon() = default;
        virtual void mainAttack() = 0;
        virtual void secondaryAttack() = 0;
};

// Concrete Pokemon: Pikachu
class Pikachu: public IPokemon {
    public:
        void mainAttack() override {
            cout << "Pika main attack!" << endl;
        }
        void secondaryAttack() override {
            cout << "Pika secondary attack!" << endl;
        }   
};

// Concrete Pokemon: Mewo
class Mewo: public IPokemon {
    public:
        void mainAttack() override {
            cout << "Mewo main attack!" << endl;
        }   
        void secondaryAttack() override {
            cout << "Mewo secondary attack!" << endl;
        }
};

// Concrete Pokemon: Charizard
class Charizard: public IPokemon {
    public:
        void mainAttack() override {
            cout << "Charizard main attack!" << endl;
        }   
        void secondaryAttack() override {
            cout << "Charizard secondary attack!" << endl;
        }
};

// Factory class for creating Pokemon
class FactoryPokemon {
    public:
        // Initialize factory with Pokemon creators
        FactoryPokemon() {
            _pokemon_table[1] = []() { return new Pikachu(); };
            _pokemon_table[2] = []() { return new Mewo(); };
            _pokemon_table[3] = []() { return new Charizard(); };
        }

        // Create Pokemon by type number
        IPokemon* createPokemon(int num) {
            try {
                return _pokemon_table.at(num)();
            }
            catch(const exception& e) {
                cout << "Error: No Pokemon at that number!" << endl;
                return nullptr;
            }
        }
    private:
        // Map of Pokemon creators
        unordered_map<int, function<IPokemon*()>> _pokemon_table;
};

int main() {
    // Example usage of Factory pattern
    FactoryPokemon fact;
    vector<IPokemon*> pokeVec;

    // Create different types of Pokemon
    pokeVec.push_back(fact.createPokemon(1));  // Pikachu
    pokeVec.push_back(fact.createPokemon(2));  // Mewo
    pokeVec.push_back(fact.createPokemon(3));  // Charizard
    pokeVec.push_back(fact.createPokemon(4));  // Invalid - returns nullptr

    // Test Pokemon attacks
    for (auto it: pokeVec) {
        if (it) {  // Check for nullptr
            it->mainAttack();
            it->secondaryAttack();
        }
        delete(it);
    }

    return 0;
}