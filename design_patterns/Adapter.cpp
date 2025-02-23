#include <iostream>
#include <string>

using namespace std;

class IBookReader{
    public:
        virtual void loadBook(string book) = 0;
        virtual void startReading() = 0;
        virtual ~IBookReader() = default;
};

class EnglishBook: public IBookReader{
    public:
        void loadBook(string book) override{
            _book = book;
            cout << "Loading english book" << endl;
        };
        void startReading() override{
            cout << "Reading english book" << endl;
        };
    private:
    string _book;
};

class FrenchBook: public IBookReader{
    public:
        void loadBook(string book) override{
            _book = book;
            cout << "Loading french book" << endl;
        };
        void startReading() override{
            cout << "Reading french book" << endl;
        };
    private:
    string _book;
};

class FrenchEnglishReaderAdapter: public IBookReader{
    public:
        void loadBook(string frenchBook) override{
            loadBook(_translateBook(frenchBook));
        };
        void startReading() override{
            cout << "Reading english translated book!" << endl;
        }
    private:
        string _translateBook(string book){
          cout << "translating the book" << endl;
          return book;  
        };
};

int main(){

    return 0;
}