/**
 * Decorator Design Pattern
 * 
 * Purpose: Dynamically adds responsibilities to objects without altering their code.
 * 
 * Components:
 * - INotifier: Base interface
 * - BaseNotifier: Basic notification
 * - EmailNotifier, WhatsAppNotifier: Decorators
 */

#include <iostream>
using namespace std;

// Base interface
class INotifier {
    public:
        virtual ~INotifier() = default;
        virtual void sendNotify() const = 0;
};

// Basic notification implementation
class BaseNotifier: public INotifier {
    public:
        void sendNotify() const override {
            cout << "Base notification" << endl;
        }
};

// Base decorator
class NotifierDecorator: public INotifier {
    public:
        NotifierDecorator(INotifier* notifier): _notifier(notifier) {}
        
        void sendNotify() const override {
            if (_notifier) {
                _notifier->sendNotify();
            }
        }
        
    protected:
        INotifier* _notifier;
};

// Email decorator
class EmailNotifier: public NotifierDecorator {
    public:
        EmailNotifier(INotifier* notifier): NotifierDecorator(notifier) {}
        
        void sendNotify() const override {
            NotifierDecorator::sendNotify();
            cout << "Email notification sent" << endl;
        }
};

// WhatsApp decorator
class WhatsAppNotifier: public NotifierDecorator {
    public:
        WhatsAppNotifier(INotifier* notifier): NotifierDecorator(notifier) {}
        
        void sendNotify() const override {
            NotifierDecorator::sendNotify();
            cout << "WhatsApp notification sent" << endl;
        }
};

int main() {
    BaseNotifier base;
    EmailNotifier email(&base);
    WhatsAppNotifier whatsapp(&email);
    
    whatsapp.sendNotify();
    
    return 0;
}
