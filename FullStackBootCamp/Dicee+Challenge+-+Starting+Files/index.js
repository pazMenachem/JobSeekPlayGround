/**
 * Game state and cached DOM elements
 */
let gameElements = null;

/**
 * Initialize the game and cache DOM elements
 */
function initializeGame() {
    try {
        gameElements = {
            rollButton: document.querySelector(".btn-success"),
            declaration: document.querySelector("h1"),
            cube1: document.querySelector(".img1"),
            cube2: document.querySelector(".img2")
        };

        // Validate all elements exist
        Object.entries(gameElements).forEach(([key, element]) => {
            if (!element) throw new Error(`Could not find ${key} element`);
        });

        gameElements.rollButton.addEventListener("click", handleClick);
    } catch (error) {
        console.error("Failed to initialize game:", error);
    }
}

/**
 * Handle dice roll click event
 */
function handleClick() {
    try {
        const player1Score = getRandomNum();
        const player2Score = getRandomNum();
        
        updateDiceImages(player1Score, player2Score);
        updateWinnerDeclaration(player1Score, player2Score);
    } catch (error) {
        console.error("Error during game play:", error);
    }
}

/**
 * Generate random number between 1 and 6
 * @param {number} min - Minimum value (inclusive)
 * @param {number} max - Maximum value (inclusive)
 * @returns {number} Random number between min and max
 */
function getRandomNum(min = 1, max = 6) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Update winner declaration based on scores
 * @param {number} player1Score - First player's score
 * @param {number} player2Score - Second player's score
 */
function updateWinnerDeclaration(player1Score, player2Score) {
    if (player1Score > player2Score) {
        gameElements.declaration.textContent = "Player One Wins!";
    } else if (player2Score > player1Score) {
        gameElements.declaration.textContent = "Player Two Wins!";
    } else {
        gameElements.declaration.textContent = "Draw!";
    }
}

/**
 * Update dice images based on scores
 * @param {number} player1Score - First player's score
 * @param {number} player2Score - Second player's score
 */
function updateDiceImages(player1Score, player2Score) {
    gameElements.cube1.src = `./images/dice${player1Score}.png`;
    gameElements.cube2.src = `./images/dice${player2Score}.png`;
}

// Initialize game when DOM is loaded
document.addEventListener("DOMContentLoaded", initializeGame);


// *** My Code ** ///
// document.addEventListener("DOMContentLoaded", () => {
//     const rollButton = document.querySelector(".btn-success");
//     rollButton.addEventListener("click", handleClick);
// })

// function handleClick(){
//     const player1 = getRandomNum();
//     const player2 = getRandomNum();
//     changeCubes(player1, player2);
//     getWinner(player1, player2);
// };

// function getRandomNum(begin = 0, end = 6){
//   return Math.floor(Math.random() * end) + 1 + begin
// };

// function getWinner(player1, player2){
//     const Declaration = document.querySelector("h1");
//     if (player1 > player2){
//         Declaration.innerText = "Player one wins!";
//     }
//     if (player2 > player1){
//         Declaration.innerText = "Player Two wins!";
//     }
//     if (player1 == player2){
//         Declaration.innerText = "Draw!"
//     }
// }

// function changeCubes(player1, player2){
//   const cube1 = document.querySelector(".img1");
//   const cube2 = document.querySelector(".img2");
//   cube1.setAttribute("src", "./images/dice" + player1 + ".png");
//   cube2.setAttribute("src", "./images/dice" + player2 + ".png");
// };

