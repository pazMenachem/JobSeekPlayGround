/**
 *  @param {string} str 
 *  @returns {string}
 */
function URLify(str){
    return str.trimEnd().replaceAll(' ', '%20');
}

describe('URLify', () => {
    test('Normal input', () => {
        expect(URLify('Mr John Smith    ')).toBe('Mr%20John%20Smith');
    });
    test('Empty input', () => {
        expect(URLify('')).toBe('');
    });
    test('Non spaces input', () => {
        expect(URLify('a')).toBe('a');
    });
    test('One space input', () => {
        expect(URLify('a a  ')).toBe('a%20a');
    });
});
