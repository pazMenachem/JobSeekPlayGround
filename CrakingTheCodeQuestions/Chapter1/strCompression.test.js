function strComp (string) {
    var compressed = '';
    var currChar = '';
    var currCount = '';
    var maxCount = 1;
    for (var i = 0; i < string.length; i++) {
      if (currChar !== string[i]) {
        console.log(currChar, string[i], i);
        compressed = compressed + currChar + currCount;
        maxCount = Math.max(maxCount, currCount);
        currChar = string[i];
        currCount = 1;
      } else {
        currCount++;
      }
    }
    compressed = compressed + currChar + currCount;
    maxCount = Math.max(maxCount, currCount);
  
    return maxCount === 1 ? string : compressed;
};

describe('strComp', () => {
    test('One Char', () => {
      expect(strComp('a')).toBe('a');
    });

    test('Same number of char', () => {
        expect(strComp('aaaaa')).toBe('a5');
    });

    test('One char of each', () => {
        expect(strComp('abc')).toBe('abc');
    });
    
    test('Multiple charcters', () => {
        expect(strComp('aaabbbcccd')).toBe('a3b3c3d1');
    });
}); 