
/**
 * 
 * @param {number[][]} matrix
 * @returns {void}
 * 
 */
function rotateMatrix(matrix) {
    const n = matrix.length
    if (n === 1) return matrix;

    const rowLimit = n % 2 == 0? n / 2 : n / 2 + 1
    var top, bot, left, right;

    for (var row = 0; row < rowLimit; row++)
        for (var col = row; col < n - 1 - row; col++){
            top   = matrix[row][col];
            right = matrix[col][n - 1 - row];
            bot   = matrix[n - 1 - row][n - 1 - col];
            left  = matrix[n - 1 - col][row];
            [matrix[row][col], matrix[col][n - 1 - row], matrix[n - 1 - row][n - 1 - col], matrix[n - 1 - col][row]] = [left, top, right, bot]
        }
}

describe("rotateMatrix", () => {
    test('1x1', () => {
        const matrix = [
            [1]
        ];
        
          rotateMatrix(matrix);
        
          expect(matrix).toEqual([
            [1]
          ]);        
    });

    test('Odd matrix 3x3', () => {
        const matrix = [
          [1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]
        ];
      
        rotateMatrix(matrix);
      
        expect(matrix).toEqual([
          [7, 4, 1],
          [8, 5, 2],
          [9, 6, 3]
        ]);
      });

    test('even matrix 2x2', () => {
        const matrix = [
          [1, 2],
          [3, 4]
        ];
      
        rotateMatrix(matrix);
      
        expect(matrix).toEqual([
          [3, 1],
          [4, 2]
        ]);
      });

    test('Larger even matrix 4x4', () => {
        const matrix = [
          [1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12],
          [13, 14, 15, 16]
        ];
      
        rotateMatrix(matrix);
      
        expect(matrix).toEqual([
            [13, 9, 5, 1],
            [14, 10, 6, 2],
            [15, 11, 7, 3],
            [16, 12, 8, 4]
        ]);
      });
});