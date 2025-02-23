/**
 * State Design Pattern
 * 
 * Purpose: Allows an object to alter its behavior when its internal state changes.
 *          The object will appear to change its class.
 * 
 * Components:
 * - IState: Interface defining state behavior
 * - Phone: Context class that maintains current state
 * - Concrete States: OffState, LockedState, ReadyState
 * 
 * State Transitions:
 * - Off -> Locked (via clickHome/clickOnOff)
 * - Locked -> Ready (via clickHome)
 * - Locked -> Off (via clickOnOff)
 * - Ready -> Locked (via clickOnOff)
 */

#include <iostream>
#include <string>

using namespace std;

// Forward declarations
class Phone;
class IState;

/**
 * Abstract State interface
 * Defines operations all concrete states must implement
 */
class IState {
    public:
        IState(Phone* phone):_phone(phone) {};
        virtual ~IState() = default;
        
        // Pure virtual methods to be implemented by concrete states
        virtual string clickHome() = 0;    // Handles home button click
        virtual string clickOnOff() = 0;   // Handles power button click
    protected:
        Phone* _phone;  // Reference to context
};

/**
 * Context class
 * Maintains current state and delegates state-specific behavior
 */
class Phone {
    public:
        Phone():_state(nullptr) {};
        void init();  // Initialize with default state

        // State management
        void setState(IState* newState) {
            delete _state;
            _state = newState;
        };

        // Phone actions
        string lock() {
            return "Locking phone and turning of screen.";  
        };
        string home() {
            return "Going to home-screen.";  
        };
        string unlock() {
            return "Unlocking the phone to home.";  
        };
        string turnOn() {
            return "Turning screen on, device still locked.";  
        };
        IState* getState() { return _state; };
    private:
        IState* _state;  // Current state
};

/**
 * Concrete State: Ready State
 * Phone is unlocked and ready for use
 */
class ReadyState: public IState {
    public:
        ReadyState(Phone* phone):IState(phone) {};
        string clickHome() override {
            return _phone->home();
        };
        string clickOnOff() override;  // Transitions to LockedState
};

/**
 * Concrete State: Locked State
 * Phone is on but locked
 */
class LockedState: public IState {
    public:
        LockedState(Phone* phone):IState(phone) {};
        string clickHome() override;    // Transitions to ReadyState
        string clickOnOff() override;   // Transitions to OffState
};

/**
 * Concrete State: Off State
 * Phone screen is off
 */
class OffState: public IState {
    public:
        OffState(Phone* phone):IState(phone) {};
        string clickHome() override;    // Transitions to LockedState
        string clickOnOff() override;   // Transitions to LockedState
};

// Implementation of state transitions
void Phone::init() {
    _state = new OffState(this);
}

string ReadyState::clickOnOff() {
    _phone->setState(new LockedState(_phone));
    return _phone->lock();
}

string LockedState::clickHome() {
    _phone->setState(new ReadyState(_phone));
    return _phone->unlock();
}

string LockedState::clickOnOff() {
    _phone->setState(new OffState(_phone));
    return _phone->turnOn();
}

string OffState::clickHome() {
    _phone->setState(new LockedState(_phone));
    return _phone->turnOn();
}

string OffState::clickOnOff() {
    _phone->setState(new LockedState(_phone));
    return _phone->turnOn();
}

int main() {
    // Create and initialize phone
    Phone phone;
    phone.init();
    
    // Test state transitions
    cout << phone.getState()->clickHome() << endl;    // Off -> Locked
    cout << phone.getState()->clickHome() << endl;    // Locked -> Ready
    cout << phone.getState()->clickOnOff() << endl;   // Ready -> Locked
    cout << phone.getState()->clickOnOff() << endl;   // Locked -> Off
    
    return 0;
}
