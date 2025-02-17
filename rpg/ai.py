from simpleai.search import SearchProblem, breadth_first
from config import MAP_SIZE


class EnemyAI(SearchProblem):
    def __init__(self, enemy, player):
        self.enemy = enemy
        self.player = player
        self.goal = (player.x, player.y)
        super().__init__(initial_state=(enemy.x, enemy.y))

    def actions(self, state):
        x, y = state
        # Limit search radius to prevent freezing on large maps
        search_radius = 10
        possible_moves = [(nx, ny) for nx, ny in (
            (x + 1, y), (x - 1, y), 
            (x, y + 1), (x, y - 1)
        ) if 0 <= nx < MAP_SIZE and 0 <= ny < MAP_SIZE]
        # Only return moves within search radius
        return [(nx, ny) for nx, ny in possible_moves 
                if abs(nx - x) + abs(ny - y) <= search_radius]

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state == self.goal

def get_enemy_move(enemy, player):
    # Add distance check to prevent pathfinding when too far
    distance = abs(enemy.x - player.x) + abs(enemy.y - player.y)
    if distance > 10:  # Reduced from 20 to 10 to match search radius
        dx = 1 if player.x > enemy.x else -1 if player.x < enemy.x else 0
        dy = 1 if player.y > enemy.y else -1 if player.y < enemy.y else 0
        new_x = max(0, min(MAP_SIZE - 1, enemy.x + dx))
        new_y = max(0, min(MAP_SIZE - 1, enemy.y + dy))
        return (new_x, new_y)
        
    ai = EnemyAI(enemy, player)
    solution = breadth_first(ai, graph_search=True)  # Added graph_search=True to prevent revisiting states
    path = solution.path()
    return path[1][1] if len(path) > 1 else (enemy.x, enemy.y)