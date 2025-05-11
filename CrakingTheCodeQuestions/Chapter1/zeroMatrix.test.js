const FLAGGED = -1;

/**
 * 
 * @param {number[][]} matrix 
 * @returns {void}
*/
function zeroMatrix(matrix){
    const [rows, cols] = [matrix.length, matrix[0].length]
    
    function checkElement(row, col){
        switch(matrix[row][col]){
            case FLAGGED: return;
            case 0: {dfs(row, col); break;}
            default: {matrix[row][col] = FLAGGED; break;}
        }
    };
    
    function dfs(row, col){
        if (matrix[row][col] === FLAGGED) return;
        if (matrix[row][col] === 0) matrix[row][col] = FLAGGED;
        
        // RIGHT
        for (var i = col; i < cols; i++) checkElement(row, i);
        // LEFT
        for (var i = col; i >= 0; i--) checkElement(row, i);
        // DOWN
        for (var i = row; i < rows; i++) checkElement(i, col);
        // UP
        for (var i = row; i >= 0; i--) checkElement(i, col);
    }

    for (var row = 0; row < rows; row++)
        for (var col = 0; col < cols; col++)
            if (matrix[row][col] === 0)
                dfs(row, col);

    for (var row = 0; row < rows; row++)
        for (var col = 0; col < cols; col++)
            if (matrix[row][col] === FLAGGED)
                matrix[row][col] = 0;
};

describe("zeroMatrix", () => {
    test("1x1 no zero", () => {
      const matrix = [[1]];
      zeroMatrix(matrix);
      expect(matrix).toEqual([[1]]);
    });
  
    test("1x1 with zero", () => {
      const matrix = [[0]];
      zeroMatrix(matrix);
      expect(matrix).toEqual([[0]]);
    });
  
    test("2x2 with one zero", () => {
      const matrix = [
        [1, 0],
        [3, 4]
      ];
      zeroMatrix(matrix);
      expect(matrix).toEqual([
        [0, 0],
        [3, 0]
      ]);
    });
  
    test("3x3 with center zero", () => {
      const matrix = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 8, 9]
      ];
      zeroMatrix(matrix);
      expect(matrix).toEqual([
        [1, 0, 3],
        [0, 0, 0],
        [7, 0, 9]
      ]);
    });
  
    test("3x4 with multiple zeros", () => {
      const matrix = [
        [1, 2, 3, 0],
        [4, 5, 6, 7],
        [0, 9, 8, 1]
      ];
      zeroMatrix(matrix);
      expect(matrix).toEqual([
        [0, 0, 0, 0],
        [0, 5, 6, 0],
        [0, 0, 0, 0]
      ]);
    });
  
    test("4x4 with multiple zeros", () => {
      const matrix = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 0, 11],
        [12, 13, 14, 15]
      ];
      zeroMatrix(matrix);
      expect(matrix).toEqual([
        [0, 0, 0, 0],
        [0, 5, 0, 7],
        [0, 0, 0, 0],
        [0, 13, 0, 15]
      ]);
    });
    test("4x4 all zeros", () => {
      const matrix = [
        [0, 1, 2, 3],
        [4, 0, 6, 7],
        [8, 9, 0, 11],
        [12, 13, 14, 0]
      ];
      zeroMatrix(matrix);
      expect(matrix).toEqual([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
      ]);
    });
  });