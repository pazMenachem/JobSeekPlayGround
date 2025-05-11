#include <iostream>
#include <format>

using namespace std;

typedef struct Node{
    int data;
    Node* left = nullptr;
    Node* right = nullptr;
}Node;

class BST{
    public:
        BST() = default;
        void insert(int val);
        bool remove(int val);
        Node* search(int val);
        void printTree();

        ~BST(){
            destHelper(_root);
            _root = nullptr;
        }

    private:
        Node* _root = nullptr;
        int _size = 0;

        void destHelper(Node* root){
            if (!root)
                return;
            destHelper(root->left);
            destHelper(root->right);
            delete(root);
        }
        Node* insertHelper(int val, Node* root){
            if (!root)
                return new Node{val};

            if (root->data >= val)
                root->left = insertHelper(val, root->left);
            if (root->data < val)
                root->right = insertHelper(val, root->right);

            return root;
        }
        Node* findSuccessor(Node* root){
            if (root->left && root->right){ // Two children case
                Node* tmp = root->left;        
                while (tmp->right) tmp = tmp->right;
                return tmp;
            };
            if (root->left) return root->left; // Only left Child
            if (root->right) return root->right; // Only Right Child
            return nullptr; // No children
        }
        Node* removeHelper(int val, Node* root, bool& found){
            if (!root)
                return nullptr;

            if (val == root->data){
                Node* tmp = findSuccessor(root);
                delete(root);
                found = true;
                return tmp;
            }

            if (root->data >= val)
                root->left = removeHelper(val, root->left, found);
            if (root->data < val)
                root->right = removeHelper(val, root->right, found);
            return root;
        }
        Node* searchHelper(int val, Node* root){
            if (!root)
                return nullptr;

            if (val == root->data)
                return root;

            if (root->data >= val)
                return searchHelper(val, root->left);
            return searchHelper(val, root->right);
        }
        void printHelper(Node* root){
            if (!root)
                return;
            printHelper(root->left);
            cout << root->data << " -> ";
            printHelper(root->right);
        }
};

void BST::printTree(){
    cout << format("BST ({} elements)\n", _size);
    printHelper(_root);
    cout << endl;
}

void BST::insert(int val){
    _root = insertHelper(val, _root);
    _size++;
}

bool BST::remove(int val){
    bool found = false;
    removeHelper(val, _root, found);
    if (found)
        _size--;
    return found;
}

Node* BST::search(int val){
    return searchHelper(val, _root);
}

int main(){
    BST bst;
    bst.insert(1);
    bst.insert(2);
    bst.insert(3);
    bst.insert(4);
    bst.insert(5);
    bst.insert(6);
    bst.insert(7);
    bst.printTree();
    bst.remove(6);
    cout << (bst.search(6) ? "val is found" : "val is not found") << endl;
    bst.printTree();
    cout << "Great Success!" << endl;
    return 0;
}