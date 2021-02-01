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
from random import random
from PIL import Image
import numpy as np
import cv2 as cv
import os


class Cell:
    def __init__(self, pos_y=0, pos_x=0, alive=False):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__alive = alive

    def get_alive(self):
        return self.__alive

    def set_alive(self, is_alive):
        self.__alive = is_alive

    def eye(self):
        pos = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                pos.append([self.__pos_y + i, self.__pos_x + j])

        pos.pop(4)

        # Ordem da lista
        # 1 - 2 - 3
        # 4 -   - 5
        # 6 - 7 - 8
        return pos

    def __str__(self):
        return f'██({self.__pos_y}, {self.__pos_x})' if self.__alive else f'░░({self.__pos_y}, {self.__pos_x})'


class Grid:
    def __init__(self, column=1, line=1, weight=.8):
        self.__column = column if isinstance(column, int) and column > 0 else 1
        self.__line = line if isinstance(line, int) and line > 0 else 1
        self.__weight = weight if 0.0 < weight < 1.0 else .8

        # Gera uma matriz aleatoria com zeros e uns
        self.__mx = [[1 if random() > self.__weight else 0 for j in range(self.__column)] for i in range(self.__line)]

    def get_grid(self):
        return self.__mx

    def get_column(self):
        return self.__column

    def get_line(self):
        return self.__line

    def update_grid(self, matrix):
        tr_fs = True

        # Verifica se a matriz é feita de zeros e uns
        for i in matrix:
            for j in i:
                tr_fs = j == 0 or j == 1

                if not tr_fs:
                    print('Update fail: elements different of 0 or 1')
                    return

        # Verifica o tamano da matriz
        if len(matrix[:]) == self.__column and len(matrix[0]) == self.__line and tr_fs:
            self.__mx = matrix
        else:
            one = 'bigger' if len(matrix[:]) > self.__column else 'equal' if len(
                matrix[:]) == self.__column else 'lower'
            two = 'bigger' if len(matrix[0]) > self.__line else 'equal' if len(matrix[0]) == self.__line else 'lower'
            print(f'Update fail: length is {one}, height is {two}')

    def __str__(self):
        line = ''

        for i in self.__mx:
            value = ['██' if j == 1 else '░░' for j in i]

            line += ''.join(value)
            line += '\n'

        return line


class World:
    def __init__(self, grid):
        self.__population = []
        self.__mn_gd = grid

        for i, line in zip(self.__mn_gd.get_grid(), range(self.__mn_gd.get_line())):
            temp1 = []

            for j, column in zip(i, range(self.__mn_gd.get_column())):
                alive = True if j == 1 else False
                temp1.append(Cell(line, column, alive))

            self.__population.append(temp1)

    def tick(self):
        self.__selection()

        matrix = []

        for i in self.__population:
            temp = []

            for j in i:
                temp.append(1 if j.get_alive() else 0)

            matrix.append(temp)

        self.__mn_gd.update_grid(matrix)

    def get_img(self):
        img = []

        for i in self.__population:
            temp = []

            for j in i:
                temp.append(0 if j.get_alive() else 255)

            img.append(temp)

        return img

    def __selection(self):
        temp_pop = [[Cell() for j in range(self.__mn_gd.get_column())] for i in range(self.__mn_gd.get_line())]

        for i in range(self.__mn_gd.get_line()):
            for j in range(self.__mn_gd.get_column()):
                value = self.__population[i][j].eye()

                value[2][1] = value[2][1] if value[2][1] < self.__mn_gd.get_line() else 0
                value[4][1] = value[4][1] if value[4][1] < self.__mn_gd.get_line() else 0
                value[7][1] = value[7][1] if value[7][1] < self.__mn_gd.get_line() else 0
                value[7][0] = value[7][0] if value[7][0] < self.__mn_gd.get_column() else 0
                value[6][0] = value[6][0] if value[6][0] < self.__mn_gd.get_column() else 0
                value[5][0] = value[5][0] if value[5][0] < self.__mn_gd.get_column() else 0

                neighbor = 0

                for k in value:
                    neighbor += 1 if self.__population[k[0]][k[1]].get_alive() else 0

                if self.__population[i][j].get_alive():
                    if neighbor < 2:
                        temp_pop[i][j] = Cell(i, j, False)

                    elif neighbor > 3:
                        temp_pop[i][j] = Cell(i, j, False)

                    elif neighbor == 3 or neighbor == 2:
                        temp_pop[i][j] = self.__population[i][j]

                    else:
                        temp_pop[i][j] = self.__population[i][j]

                else:
                    if neighbor == 3:
                        temp_pop[i][j] = Cell(i, j, True)

                    else:
                        temp_pop[i][j] = self.__population[i][j]

        self.__population = temp_pop

    def __str__(self):
        line = ''

        for i in self.__population:
            value = ['██' if j else '░░' for j in [w.get_alive() for w in i]]

            line += ''.join(value)
            line += '\n'

        return line


class Img:
    def __init__(self, world, frame=1, size=(150, 150)):
        self.__frame = frame
        self.__world = world
        self.__size = size

    def png(self):
        if os.path.exists(os.getcwd() + '/temp'):
            os.chdir(os.getcwd() + '/temp')
        else:
            os.mkdir(os.getcwd() + '/temp')

        for time in range(self.__frame):
            image = Image.fromarray(np.array(self.__world.get_img(), np.uint8))
            image = image.resize(self.__size, Image.BOX)
            image.save(f'img-{time}.png')

            print(time)
            self.__world.tick()

    def gif(self):
        self.__frame = self.__frame if self.__frame < 150 else 150
        im = []

        for time in range(self.__frame):
            image = Image.fromarray(np.array(self.__world.get_img(), np.uint8))
            image = image.convert('RGB')
            im.append(image.resize(self.__size, Image.BOX))

            self.__world.tick()

        im[0].save('new.gif', save_all=True, append_images=im[1:], optimize=False, duration=self.__frame, loop=0)

    def cv2(self):
        while True:
            image = Image.fromarray(np.array(self.__world.get_img(), np.uint8))
            image = image.convert('RGB')
            image = image.resize(self.__size, Image.BOX)

            cv.imshow('img', cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR))

            self.__world.tick()

            if cv.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    grid = 80

    new = World(Grid(grid, grid, .8))

    gif = Img(new, 500, (grid*3 if grid > 100 else grid*8, grid*3 if grid > 100 else grid*8))
    gif.cv2()

