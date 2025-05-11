/**
 *
 * @param {string} str 
 * @returns {boolean}
 * @Note I know split creates an array, Decided to use it only since str is immutable in Js, otherwise run time is O(N^2)
 * Current run time - O(NLogN)
 * With using data structure - We can use set and run time will be O(N), space complexity - O(N)
 */

function isUnique(str) {
    str = str.split('').sort().join('');
    for (var i = 1; i < str.length; i++)
      if (str[i] == str[i - 1])
        return false;
    return true;
  }
  
  describe('isUnique', () => {
    test('returns true for empty string', () => {
      expect(isUnique('')).toBe(true);
    });
  
    test('returns true for single character', () => {
      expect(isUnique('a')).toBe(true);
    });
  
    test('returns true for all unique characters', () => {
      expect(isUnique('abcdefg')).toBe(true);
    });
  
    test('returns false for string with repeated characters', () => {
      expect(isUnique('hello')).toBe(false);
    });
  
    test('is case sensitive', () => {
      expect(isUnique('aA')).toBe(true);
    });
  
    test('returns false for string with all same characters', () => {
      expect(isUnique('aaaaaa')).toBe(false);
    });
  
    test('returns true for numbers and letters uniquely mixed', () => {
      expect(isUnique('a1b2c3')).toBe(true);
    });
  
    test('returns false for long string with duplicates far apart', () => {
      expect(isUnique('abcdefghija')).toBe(false);
    });
  
    test('returns true for all printable ASCII characters', () => {
      const uniqueASCII = Array.from({ length: 128 }, (_, i) => String.fromCharCode(i)).join('');
      expect(isUnique(uniqueASCII)).toBe(true);
    });
  
    test('returns false when non-printable duplicates exist', () => {
      expect(isUnique('\x00a\x00')).toBe(false);
    });
  });