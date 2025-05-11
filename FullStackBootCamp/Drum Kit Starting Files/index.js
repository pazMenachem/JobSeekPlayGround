function main(){
    init();
};

function init(){
    document.querySelectorAll(".drum").forEach((element) => {
        if (!element)
            throw new Error("Button not found!")
        element.addEventListener("click", handleClick);
    });

    document.addEventListener("keydown", handleKeyPress)
};

/**
 * 
 * @param {MouseEvent} event 
 */
function handleClick(event){
    const button = event.currentTarget; 
    makeSound(button.textContent);
}

/**
 * 
 * @param {KeyboardEvent} event 
 */
function handleKeyPress(event){
    makeSound(event.key);
}

function makeSound(key){
    switch(key){
        case 'w':
            new Audio("./sounds/crash.mp3").play()
            break;
        case 'a':
            new Audio("./sounds/kick-bass.mp3").play()
            break;
        case 's':
            new Audio("./sounds/snare.mp3").play()
            break;
        case 'd':
            new Audio("./sounds/tom-1.mp3").play()
            break;
        case 'j':
            new Audio("./sounds/tom-2.mp3").play()
            break;
        case 'k':
            new Audio("./sounds/tom-3.mp3").play()
            break;
        case 'l':
            new Audio("./sounds/tom-4.mp3").play()
            break;
    }
}

document.addEventListener("DOMContentLoaded", main)