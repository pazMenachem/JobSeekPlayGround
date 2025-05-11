/**
 * 
 * @param {Object} map 
 * @param {char} element 
 */
function helper(map, element){
    if (element in map)
        map[element]++;
    else
        map[element] = 1;
}

/**
 * 
 * @param {string} str1 
 * @param {string} str2
 * @returns {boolean}
 * Run time complexity - O(N)
 * Space complexity - O(N)
 */
function checkPermutation(str1, str2){
    if (str1.length != str2.length)
        return false;
    
    const [mapStr1, mapStr2] = [{}, {}];
    for (var i = 0; i < str1.length; i++){
        helper(mapStr1, str1[i]);
        helper(mapStr2, str2[i]);
    }

    for (const key in mapStr1) {
        if (!(key in mapStr2)) return false;
        if (mapStr1[key] !== mapStr2[key]) return false;
    }

    return true;
};

/**
 * Offical solution O(NLogN)
 * @param {string} stringOne 
 * @param {string} stringTwo 
 * @returns {boolean}
 */
var checkPermute = function(stringOne, stringTwo) {
    // if different lengths, return false
    if (stringOne.length !== stringTwo.length) {
      return false;
    // else sort and compare 
    // (doesnt matter how it's sorted, as long as it's sorted the same way)
    } else {
      var sortedStringOne = stringOne.split('').sort().join('');
      var sortedStringTwo = stringTwo.split('').sort().join('');
      return sortedStringOne === sortedStringTwo;
    }
  };

describe('checkPermutation Performance', () => {
    test('Benchmark with different sizes', () => {
        const testSizes = [100, 1000, 10000, 100000, 1000000];
        
        testSizes.forEach(size => {
            const str1 = "a".repeat(size);
            const str2 = "a".repeat(size);
            
            var startTime = performance.now();
            checkPermutation(str1, str2);
            var endTime = performance.now();
            
            console.log(`My Solution - Size ${size}: ${endTime - startTime} milliseconds`);
            
            startTime = performance.now();
            checkPermute(str1, str2);
            endTime = performance.now();
            
            console.log(`Offical Solution - Size ${size}: ${endTime - startTime} milliseconds`);
        });
    });
});

describe('checkPermutation', () => {
    test('Empty strings', () => {
        expect(checkPermutation('', '')).toBe(true);
    });
    
    test('One letter', () => {
        expect(checkPermutation('a', 'a')).toBe(true);
    });
    
    test('One letter', () => {
        expect(checkPermutation('a', 'b')).toBe(false);
    });
    
    test('Same letters, different order', () => {
        expect(checkPermutation('ab', 'ba')).toBe(true);
    });

    test('Same letters, different order and distance', () => {
        expect(checkPermutation('abcd', 'dbca')).toBe(true);
    });

    test('Not premutation', () => {
        expect(checkPermutation('aaa', 'bbb')).toBe(false);
    });

    test('Close to permutation', () => {
        expect(checkPermutation('aba', 'aca')).toBe(false);
    });

    test('Different Lengths', () => {
        expect(checkPermutation('b', 'aab')).toBe(false);
    });
});