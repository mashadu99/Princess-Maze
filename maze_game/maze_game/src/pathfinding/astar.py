import heapq


def movement_cost(tile):
    """
    מחשב את עלות התנועה למשבצת מסוימת.
    """
    if tile == 'B':  # בוץ
        return 3
    elif tile == 'I':  # קרח
        return 2
    else:  # משבצת רגילה
        return 1


def manhattan_distance(pos1, pos2):
    """
    מחשב את מרחק מנהטן בין שתי נקודות.
    זוהי היוריסטיקה שלנו - הערכה אופטימית של המרחק.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def find_path(grid, start, end):
    """
    אלגוריתם A* למציאת הנתיב הקצר ביותר עם תמיכה בעלויות תנועה שונות.
    :param grid: רשימה של רשימות המייצגת את מפת המשחק.
    :param start: קואורדינטת התחלה (y, x).
    :param end: קואורדינטת יעד (y, x).
    :return: רשימת קואורדינטות של הנתיב, או רשימה ריקה אם לא נמצא נתיב.
    """
    print(f"A*: Finding path from {start} to {end}")  # Debug
    open_list = [(0, start, [])]  # ערימת מינימום: (f_cost, position, path)
    closed_set = set()
    g_costs = {start: 0}

    while open_list:
        current_f, current_pos, path = heapq.heappop(open_list)

        if current_pos == end:
            print(f"A*: Found path with total cost {g_costs[current_pos]}")  # Debug
            return path + [current_pos]

        if current_pos in closed_set:
            continue

        closed_set.add(current_pos)

        y, x = current_pos
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 4 כיוונים
        
        for dy, dx in directions:
            neighbor_pos = (y + dy, x + dx)
            ny, nx = neighbor_pos

            if not (0 <= ny < len(grid) and 0 <= nx < len(grid[0])):
                continue

            # הדרקון מתייחס לקירות כמכשולים
            if grid[ny][nx] == 'W':
                continue

            # חישוב עלות התנועה למשבצת השכנה
            tile_cost = movement_cost(grid[ny][nx])
            if tile_cost > 1:  # Debug: show when considering expensive tiles
                print(f"A*: Considering tile {grid[ny][nx]} at {neighbor_pos} with cost {tile_cost}")
            new_g_cost = g_costs[current_pos] + tile_cost
            
            if neighbor_pos not in g_costs or new_g_cost < g_costs[neighbor_pos]:
                g_costs[neighbor_pos] = new_g_cost
                h_cost = manhattan_distance(neighbor_pos, end)
                f_cost = new_g_cost + h_cost
                print(f"A*: Adding {neighbor_pos} with g_cost={new_g_cost}, h_cost={h_cost}, f_cost={f_cost}")  # Debug
                heapq.heappush(open_list, (f_cost, neighbor_pos, path + [current_pos]))
    
    print("A*: No path found")  # Debug
    return [] # לא נמצא נתיב