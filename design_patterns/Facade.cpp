#include <iostream>

class DbManager {
public:
    void doStuff() { std::cout << "DbManager: Handling database operations.\n"; }
};

class NpcManager {
public:
    void doStuff() { std::cout << "NpcManager: Managing NPCs.\n"; }
};

class Settings {
public:
    void doStuff() { std::cout << "Settings: Managing game settings.\n"; }
};

class ScreenLoader {
public:
    void doStuff() { std::cout << "ScreenLoader: Loading screens.\n"; }
};

class CharacterManager {
public:
    void doStuff() { std::cout << "CharacterManager: Managing character stats.\n"; }
};

// Facade Class
class Game {
public:
    Game() : _settings(), _screenLoader(), _npcManager(), _charManager(), _dbManager() {
        std::cout << "Game: Initializing subsystems.\n";
    }

    void saveGame() {
        std::cout << "Game: Saving Game...\n";
        _settings.doStuff();
        _npcManager.doStuff();
        _dbManager.doStuff();
    }

    void run() {
        std::cout << "Game: Running Game...\n";
        _dbManager.doStuff();
        _npcManager.doStuff();
        _charManager.doStuff();
    }

    void getHighScore() {
        std::cout << "Game: Getting High Score...\n";
        _screenLoader.doStuff();
        _charManager.doStuff();
        _settings.doStuff();
    }

private:
    Settings _settings;
    ScreenLoader _screenLoader;
    NpcManager _npcManager;
    CharacterManager _charManager;
    DbManager _dbManager;
};

int main() {
    Game game;
    game.run();
    game.saveGame();
    game.getHighScore();
    return 0;
}