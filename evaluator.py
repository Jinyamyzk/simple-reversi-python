import stone


class Evaluator:
    def eval(self, a_board, my_stone):
        pass

class PutPosEvaluator(Evaluator):
    """evaluate the number of possible positions to put stones."""

    def eval(self, a_board, my_stone):
        _my_putpos = self._count_putpos(a_board, my_stone)
        _opp_putpos = self._count_putpos(a_board, stone.reverse(my_stone))
        _eval = _my_putpos - _opp_putpos
        return _eval

    def _count_putpos(self, a_board, my_stone):
        _count = 0
        for x in range(1, 9):
            for y in range(1, 9):
                if a_board.possible_to_put_stone_at(my_stone, (x, y)):
                    _count += 1
        return _count


class PutPosCornerEvaluator(Evaluator):
    """evaluate the number of possible positions to put stones and the corners."""

    def __init__(self, my_pos_rate = 1, opp_pos_rate = 1, corner_rate = 1):
        self.my_pos_rate = my_pos_rate
        self.opp_pos_rate = opp_pos_rate
        self.corner_rate = corner_rate

    def eval(self, a_board, my_stone):
        _my_putpos = self._count_putpos(a_board, my_stone)
        _opp_putpos = self._count_putpos(a_board, stone.reverse(my_stone))
        _eval = self.my_pos_rate * _my_putpos - self.opp_pos_rate * _opp_putpos + self.corner_rate * self._eval_corners(a_board, my_stone)
        return _eval

    def _count_putpos(self, a_board, my_stone):
        _count = 0
        for x in range(1, 9):
            for y in range(1, 9):
                if a_board.possible_to_put_stone_at(my_stone, (x, y)):
                    _count += 1
        return _count

    def _eval_corners(self, a_board, my_stone):
        _opp_stone = stone.reverse(my_stone)
        _point = 0
        _corners = ((1, 1), (1, 8), (8, 1), (8, 8))
        _corner_point = 10
        for _c in _corners:
            _s = a_board.get_at(_c)
            if _s == my_stone:
                _point += _corner_point
            elif _s == _opp_stone:
                _point -= _corner_point
        return _point


class StoneNumEvaluator(Evaluator):
    """evaluator for the last period which evaluate the number of stones"""

    def eval(self, a_board, my_stone):
        _my_count = a_board.count_stones(my_stone)
        _opp_count = a_board.count_stones(stone.reverse(my_stone))
        _eval = _my_count - _opp_count
        return _eval


class JinyaEvaluator(Evaluator):
    """evaluator used in Jinya's reversi program."""

    def is_corner_mine(self, a_board, _points, my_stone):
        if a_board.get_at((1, 1)) == my_stone:
            _points[0][1] *= -1
            _points[1][0] *= -1
        elif a_board.get_at((1, 8)) == my_stone:
            _points[6][0] *= -1
            _points[7][1] *= -1
        elif a_board.get_at((8, 1)) == my_stone:
            _points[0][6] *= -1
            _points[1][7] *= -1
        elif a_board.get_at((8, 8)) == my_stone:
            _points[6][7] *= -1
            _points[7][6] *= -1
        return _points

    def eval(self, a_board, my_stone):
        _points = (
            ( 45, -11,  4, -1, -1,  4, -11,  45),
            (-11, -16, -1, -3, -3, -1, -16, -11),
            (  4,  -1,  2, -1, -1,  2,  -1,   4),
            ( -1,  -3, -1,  0,  0, -1,  -3,  -1),
            ( -1,  -3, -1,  0,  0, -1,  -3,  -1),
            (  4,  -1,  2, -1, -1,  2,  -1,   4),
            (-11, -16, -1, -3, -3, -1, -16, -11),
            ( 45, -11,  4, -1, -1,  4, -11,  45)
        )
        _points = self.is_corner_mine(a_board, _points, my_stone)
        _opp_stone = stone.reverse(my_stone)
        _my_point = 0
        _opp_point = 0
        for x in range(8):
            for y in range(8):
                s = a_board.get_at((x+1,y+1))
                if s == my_stone:
                    _my_point += _points[x][y]
                elif s == _opp_stone:
                    _opp_point += _points[x][y]
        _eval = _my_point - _opp_point
        return _eval
