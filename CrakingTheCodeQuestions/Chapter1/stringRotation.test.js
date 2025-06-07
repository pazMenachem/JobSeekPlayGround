/**
 * @param {string} str1
 * @param {string} str2
 * @returns {boolean}
 */
function stringRotation(str1, str2){
    return str1.length === str2.length && str1.concat(str1).includes(str2);
}

describe('stringRotation', () => {
    test('base case I', () => {
        expect(stringRotation('waterBottle', 'erBottlewat')).toBe(true);
    });
    test('base case II', () => {
        expect(stringRotation('abcd', 'cdab')).toBe(true);
    });
    test('More than one Prefix', () => {
        expect(stringRotation('ababcd', 'abcdab')).toBe(true);
    });
    test('case sensitive', () => {
        expect(stringRotation('ababcd', 'ABCDAB')).toBe(false);
    });
    test('base string longer than rotated', () => {
        expect(stringRotation('aa', 'a')).toBe(false);
    });
    test('base string shorter than rotated', () => {
        expect(stringRotation('aa', 'aaaaa')).toBe(false);
    });
    test('empty str1', () => {
        expect(stringRotation('', 'aaaaa')).toBe(false);
    });
    test('empty str2', () => {
        expect(stringRotation('aaaaa', '')).toBe(false);
    });
});