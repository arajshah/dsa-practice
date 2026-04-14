class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        for row in range(9):
            curr_row = set()
            for col in range(9):
                if board[row][col] in '123456789':
                    
                    if board[row][col] in curr_row:
                        return False

                    curr_row.add(board[row][col])

        for col in range(9):
            curr_col = set()
            for row in range(9):
                if board[row][col] in '123456789':
                    
                    if board[row][col] in curr_col:
                        return False

                    curr_col.add(board[row][col])

        DIRS = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
        for nr, nc in DIRS:
            box = set()
            for row in range(nr, nr + 3):
                for col in range(nc, nc + 3):
                    if board[row][col] in '123456789':

                        if board[row][col] in box:
                            return False
                        
                        box.add(board[row][col])
        
        return True