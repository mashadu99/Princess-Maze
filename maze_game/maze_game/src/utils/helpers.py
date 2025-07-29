def find_char(grid, char):
    """
    מחזיר את המיקום הראשון של התו בגריד
    """
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == char:
                return (y, x)
    return None

def find_all_chars(grid, char):
    """
    מחזיר רשימה של כל המיקומים של תו מסוים (למשל דרקונים)
    """
    positions = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == char:
                positions.append((y, x))
    return positions
