import random

class GameField:
    """
    GameField object is used for keeping game field list.
    Game field list is two-dimensional array, each element is a filled or empty cell.
    If element is None - cell is empty.
    """
    def __init__(self, field=None):
        """
        Empty field is created while initialization state.
        It is possible to initialize object with not empty field - __init__ takes  field argument.
        """
        if field == None:
            self._field = [[None for x in range(4)] for y in range(4)] 
        else:
            self._field = field

    @property
    def field(self):
        """field is realized as property to make access and tests easier"""
        return self._field

    @field.setter
    def field(self, field):
        self._field = field

    @field.deleter
    def field(self):
        self._field = [[None for x in range(4)] for y in range(4)] 

    def push_value(self, val):
        """
        Method to push value to game field. It search random empty cell (with None value) and writes value to this cell.
        If there is no empty cell - value is not written
        """
        x, y = random.randint(0,3), random.randint(0,3)
        visited_cells = set()
        while self._field[y][x] != None and len(visited_cells) < 16:
            visited_cells.add((x,y))
            x, y = random.randint(0,3), random.randint(0,3)

        if len(visited_cells) < 16: 
            self._field[y][x] = val

class Game:
    """
    Main game class, it implements game logic. It makes slides on game field and pushes it to GameField object.
    Additionally, it pushes new values (2 or 4) to game field: chance to get 2 is 90%, 4 - 10%.
    """
    def __init__(self, game_field_cls=GameField, game_field_state=None):
        """
        Takes game field class as obligatory parameter
        """
        self.field = game_field_cls(field=game_field_state)
        self.score = 0
        self.values_to_push = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        self.win_value = 2048

    def set_score(self, score):
        """
        Sets internal game score to value
        """
        self.score = score

    def _update_score(self, add_score):
        """
        Updates internal game score
        """
        self.score += add_score

    def push_value(self):
        """
        Pushes value to game field.
        Random index from values list.
        """
        val = self.values_to_push[random.randint(0,9)]
        self.field.push_value(val)

    def slide_left(self):
        """
        Slides game field from raght to left and summarizes the same neihgbour values.
        Updates score. This method returns True if slide was done (if new field state != old field state), overwise returns False
        """
        add_score = 0
        temp_field = []

        for y in self.field.field:
            #remove None values from field
            temp_x = list(filter(lambda x: x != None, y))
            if len(temp_x) <= 1: #If there is empty list or list with one element - no need to sum, append it to result
                temp_field.append(self._fill_filed_none(temp_x))
                continue

            idx = 0
            res_x = []
            #Sum the same neighbour elements
            while idx <= len(temp_x)-1:
                if idx == len(temp_x)-1:
                    res_x.append(temp_x[idx])
                    break
                if temp_x[idx] == temp_x[idx+1]:
                    res_x.append(temp_x[idx]*2)
                    add_score += temp_x[idx]*2
                    idx = idx + 2
                else:
                    res_x.append(temp_x[idx])
                    idx = idx + 1
            temp_field.append(self._fill_filed_none(res_x))
        #check if old field state is not the same as new state
        result = self._check_avaliable_turn(temp_field)
        #if state changed
        if result:
            self.field.field = temp_field
            self._update_score(add_score)
        return result

    def slide_right(self):
        """
        Slide right = rotate + slide left + rotate back
        """
        self._rotate_180()
        result = self.slide_left()
        self._rotate_180()
        return result

    def slide_up(self):
        """
        Slide up = rotate + slide left + rotate back
        """
        self._rotate_90()
        result = self.slide_left()
        self._rotate_270()
        return result

    def slide_down(self):
        """
        Slide down = rotate + slide left + rotate back
        """
        self._rotate_270()
        result = self.slide_left()
        self._rotate_90()
        return result

    def _rotate_90(self):
        """
        rotate counterclockwise on 90 degree - for slide_up
        """
        self.field.field = [[self.field.field[x][y] for x in range(4)] for y in range(4)][::-1]

    def _rotate_180(self):
        """
        rotate counterclockwise on 180 degree - for slide_right
        """
        self.field.field = [y[::-1] for y in self.field.field]

    def _rotate_270(self):
        """
        rotate counterclockwise on 270 degree - for slide_down
        """
        self.field.field = [[self.field.field[x][y] for x in range(4)][::-1] for y in range(4)]

    def _check_avaliable_turn(self, temp_field):
        """
        compare old and new field states
        """
        return self.field.field != temp_field

    def _check_win(self):
        """
        Check if there is 2048 in game field
        """
        for cell in [y[x] for x in range(4) for y in self.field.field]:
            if cell == self.win_value:
                return True
            else:
                continue
        return False

    def _check_game_over(self):
        """
        Check if there are possible turns
        """
        #convert field to one dimension list
        cells = [self.field.field[y][x] for y in range(4) for x in range(4)]
        if None in cells: #if there is empty cells - there is possible turn
            return False

        for idx, cell in enumerate(cells[:-1]):
            if idx < 12:
                if idx in (3,7,11): #last elements in string have only on neighbour below
                    if cell == cells[idx+4]:
                        return False
                else: #all other elements have two neighbours on right and below
                    if (cell == cells[idx+1]) or (cell == cells[idx+4]):
                        return False
            else:
                if cell == cells[idx+1]:
                    return False
        return True

    def game_state(self):
        """
        Method returns full state of game
        """
        return {'win': self._check_win(), 'game_over': self._check_game_over(), 'score': self.score, 'field': self.field.field}

    @staticmethod
    def _fill_filed_none(temp_x):
        """
        fills each string with None values to len = 4
        """
        while len(temp_x) < 4:
            temp_x.append(None)
        return temp_x
