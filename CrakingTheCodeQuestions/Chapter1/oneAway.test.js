/**
 * Checks if two strings are one edit away (insert, remove, replace).
 * 
 * Time Complexity: O(n)
 * Space Complexity: O(1)
 * 
 * @param {string} s - First string
 * @param {string} t - Second string
 * @returns {boolean} - True if one edit away, else false
 */
function oneAway(s, t) {
    if (s === t || Math.abs(s.length - t.length) >= 2) return false;

    const [shorter, longer] = s.length <= t.length ? [s, t] : [t, s];
    let [short, long] = [0, 0];
    let fix = 0;

    while (short < shorter.length || long < longer.length) {
        if (shorter[short] === longer[long]) {
            short++;
            long++;
        } else {
            if (fix) return false;
            fix++;

            if (shorter.length === longer.length) {
                short++;
                long++;
            } else {
                long++;
            }
        }
    }
    return fix === 1;
}

describe('oneAway', () => {
    test('insert case', () => {
        expect(oneAway("ab", "acb")).toBe(true);
    });

    test('replace case', () => {
        expect(oneAway("pale", "bale")).toBe(true);
    });

    test('delete case', () => {
        expect(oneAway("pale", "ple")).toBe(true);
    });

    test('equal strings (should be false)', () => {
        expect(oneAway("test", "test")).toBe(false);
    });

    test('more than one edit', () => {
        expect(oneAway("abc", "adcba")).toBe(false);
    });

    test('empty and single char', () => {
        expect(oneAway("", "a")).toBe(true);
        expect(oneAway("a", "")).toBe(true);
    });

    test('length difference > 1', () => {
        expect(oneAway("a", "abc")).toBe(false);
    });
});