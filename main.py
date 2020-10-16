"""
///////////////////////////////////////////////////// Game of Life /////////////////////////////////////////////////////
                         ______     __  __        _____     __  __     __  __     ______
                        /\  __ \   /\ \_\ \      /\  __-.  /\ \/\ \   /\ \/ /    /\  ___\
                        \ \  __<   \ \____ \     \ \ \/\ \ \ \ \_\ \  \ \  _"-.  \ \  __\
                         \ \_____\  \/\_____\     \ \____-  \ \_____\  \ \_\ \_\  \ \_____\
                          \/_____/   \/_____/      \/____/   \/_____/   \/_/\/_/   \/_____/



Feito por: Savio Goncalves Mendonca (DUKE)
Data de criacao: 2020-10-16
Vercao python: 3.8

------------------------------------------------------------------------------------------------------------------------
Informacoes adicionais:

    >> Apenas por divercao

------------------------------------------------------------------------------------------------------------------------
"""


class Cell:
    def __init__(self, pos_y, pos_x, alive):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.alive = alive

    def eye(self):
        pos = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                pos.append([self.pos_y + i, self.pos_x + j])

        pos.pop(4)

        # Ordem da lista
        # 1 - 2 - 3
        # 4 -   - 5
        # 6 - 7 - 8
        return pos

    def __str__(self):
        return f'██({self.pos_y}, {self.pos_x})' if self.alive else f'░░({self.pos_y}, {self.pos_x})'


if __name__ == '__main__':
    new = Cell(5, 3, True)
    print(new.eye())
