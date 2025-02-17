/**
 * Template Method Design Pattern
 * 
 * Purpose: Defines the skeleton of an algorithm in a method, deferring some steps
 *          to subclasses. Lets subclasses redefine certain steps of an algorithm
 *          without changing the algorithm's structure.
 * 
 * Components:
 * - IBaseGameLoader: Abstract class with template method
 * - WorldOfWarcraft, Diablo: Concrete implementations
 * 
 * Key Features:
 * - Fixed algorithm structure (load)
 * - Customizable steps (hooks)
 * - Default implementations where appropriate
 * 
 * Usage Example:
 *   WorldOfWarcraft wow;
 *   wow.load(2);  // Loads WoW with difficulty 2
 */

#include <iostream>

using namespace std;

// Abstract base class defining the template method
class IBaseGameLoader {
    public:
        ~IBaseGameLoader() = default;

        // Template method defining the algorithm structure
        void load(int difficultLevel) {
            setDifficult(difficultLevel);
            setLoadingScreen();
            initiateNpc();
        }

    protected:
        // Hook methods to be implemented by subclasses
        virtual void initiateNpc() = 0;
        virtual void setLoadingScreen() = 0;
        
        // Hook method with default implementation
        virtual void setDifficult(int difficultLevel) {
            cout << "Settings Difficulty" << endl;
            _diffcultLevel = difficultLevel;
        }

    private:
        int _diffcultLevel;
};

// Concrete implementation for World of Warcraft
class WorldOfWarcraft: public IBaseGameLoader {
    protected:
        void setLoadingScreen() override {
            cout << "Setting WoW loading screen" << endl;
        }
        void initiateNpc() override {
            cout << "Setting WoW Npc's" << endl;
        }
};

// Concrete implementation for Diablo
class Diablo: public IBaseGameLoader {
    protected:
        void setLoadingScreen() override {
            cout << "Setting Diablo loading screen" << endl;
        }
        void initiateNpc() override {
            cout << "Setting Diablo Npc's" << endl;
        }
};

int main() {
    WorldOfWarcraft wow;
    Diablo diablo;
    
    wow.load(2);
    diablo.load(3);
    
    return 0;
}