from typing import Dict


class Number:
    PLUS = '+'
    MINUS = '-'

    def __init__(self, number: int):
        self.data: Dict[int, int] = {}
        self.sign: str = Number.PLUS
        if number < 0:
            self.sign = Number.MINUS
            number = -number

        rank = 1

        while number > 0:
            self.data[rank] = number % 10
            number //= 10
            rank += 1

        self.max_rank = rank - 1

    def __str__(self) -> str:
        result = ''
        if self.sign == Number.MINUS:
            result += Number.MINUS

        for rank in range(self.max_rank, 0, -1):
            result += str(self.data[rank])

        return result

    def __repr__(self) -> str:
        return f"Number({str(self)})"

    def __int__(self):
        # запрещено использовать
        number = 0
        for rank, value in self.data.items():
            number += value * 10**(rank-1)
        if self.sign == Number.MINUS:
            return -number
        return number

    def __add__(self, other: 'Number') -> 'Number':
        """ Складывание двух чисел """

        # решение через число
        # return Number(int(self) + int(other))

        # если числа разного знака, выполняем вычитание
        if self.sign != other.sign:
            if self.sign == Number.PLUS:
                return self - -other
            else:
                return other - -self

        new_data: Dict[int, int] = {}
        adder = 0
        rank = 1
        while True:
            s = adder
            adder = 0

            if rank in self.data:
                s += self.data[rank]

            if rank in other.data:
                s += other.data[rank]

            new_data[rank] = s % 10
            if s > 10:
                adder = s // 10
            rank += 1

            if rank > max(self.max_rank, other.max_rank) + 1:
                break

        num = Number(0)
        num.data = new_data
        num.max_rank = rank - 1
        num.sign = self.sign

        if num.data[num.max_rank] == 0:
            del num.data[num.max_rank]
            num.max_rank -= 1
        return num

    def __sub__(self, other: 'Number') -> 'Number':
        """ Вычитание из числа другого числа """
        # решение через число
        # return Number(int(self) - int(other))

        # если числа + и -, то складываем оба (будет + и +)
        # если числа - и +, то складываем оба (будет - и -)
        if self.sign != other.sign:
            return self + -other

        # если числа - и - выполняем вычитание наоборот (- и +)
        if self.sign == Number.MINUS:
            return -other - -self

        # остается вычитание двух положительных чисел

        # если первое число меньше
        if other > self:
            return -(other - self)

        # первое число больше
        new_data: Dict[int, int] = {}
        adder = 0
        max_rank = 0
        for rank in range(1, self.max_rank + 1):
            s = adder
            adder = 0
            s += self.data[rank]

            if rank in other.data:
                s -= other.data[rank]

            if s < 0:
                s += 10
                adder = -1

            new_data[rank] = s
            max_rank = rank
            rank += 1

        num = Number(0)
        num.data = new_data
        num.max_rank = max_rank
        return num

    def __neg__(self) -> 'Number':
        n = Number(0)
        n.data = self.data.copy()
        n.max_rank = self.max_rank
        if self.sign == Number.PLUS:
            n.sign = Number.MINUS
        else:
            n.sign = Number.PLUS
        return n

    def __eq__(self, other: 'Number') -> bool:
        if self.max_rank != other.max_rank or self.sign != other.sign:
            return False

        for rank in range(self.max_rank, 0, -1):
            if self.data[rank] != other.data[rank]:
                return False
        return True

    def __ne__(self, other: 'Number') -> bool:
        return not self == other

    def __cmp__(self, other: 'Number'):
        if self == other:
            return 0

        # если не равен знак, то больше число у которого плюс
        if self.sign != other.sign:
            if self.sign == Number.PLUS:
                return 1
            else:
                return -1

        # сравниваем кол-во цифр (больше то, у которого цифр больше)
        # в случае отрицания наоборот
        if self.max_rank > other.max_rank:
            if self.sign == Number.PLUS:
                return 1
            else:
                return -1
        elif self.max_rank < other.max_rank:
            if self.sign == Number.PLUS:
                return -1
            else:
                return 1

        # знак и кол-во разрядов равно, сравниваем цифры начиная с макс разряда
        for rank in range(self.max_rank, 0, -1):
            if self.data[rank] > other.data[rank]:
                if self.sign == Number.PLUS:
                    return 1
                else:
                    return -1
            elif self.data[rank] < other.data[rank]:
                if self.sign == Number.PLUS:
                    return -1
                else:
                    return 1

    def __lt__(self, other):
        return self.__cmp__(other) == -1

    def __gt__(self, other):
        return self.__cmp__(other) == 1

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other


print(Number(100) + Number(200), 300)
print(Number(-100) + Number(200), 100)
print(Number(100) + Number(-200), -100)
print(Number(-100) + Number(-200), -300)

print(Number(100) - Number(200), -100)
print(Number(-100) - Number(200), -300)
print(Number(100) - Number(-200), 300)
print(Number(-100) - Number(-200), 100)

print(Number(0) + Number(0), 0)