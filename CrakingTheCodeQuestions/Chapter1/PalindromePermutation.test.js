/**
 * 
 * @param {string} str 
 * @returns {Boolean}
 */
function palindromePermutation(str){
    const map = new Map();
    var once = true;
    
    for (const char of str.toLocaleLowerCase().replaceAll(' ', '')){
        if (!map.has(char))
            map.set(char, 0);
        map.set(char, map.get(char) + 1);   
    }
    
    for (const [_, value] of map.entries()){
        if (value % 2 == 1){
            if (!once) return false;
            once = false;
        }
    }
    return true;
}

describe('PalindromePermutation', () => {
    test('Empty', () => {
     expect(palindromePermutation('')).toBe(true);
    });
    test('Base', () => {
     expect(palindromePermutation('a')).toBe(true);
    });
    test('Correct Case', () => {
     expect(palindromePermutation('aab')).toBe(true);
    });
    test('Wrong Case', () => {
     expect(palindromePermutation('aaby')).toBe(false);
    });
    test('Correct Case II', () => {
     expect(palindromePermutation('aabb')).toBe(true);
    });
    test('Wrong Case II', () => {
     expect(palindromePermutation('aabbxy')).toBe(false);
    });
    test('Correct Case III', () => {
     expect(palindromePermutation('Tact Coa')).toBe(true);
    });
    test('Wrong Case III', () => {
     expect(palindromePermutation('Tact boa')).toBe(false);
    });
});