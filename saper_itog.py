from tkinter import *
from random import choice
import os
from datetime import datetime


roaming = os.getenv('APPDATA')
path = os.path.dirname(roaming) + '\Local\Saper'
try:
    os.mkdir(path)
except OSError:
    pass


class Field(object):
    def __init__(self, master, row, column):
        self.but1 = Button(master, text='   ')
        self.mine = False
        self.value = 0
        self.viewed = False
        self.znamya = 0
        self.about = []
        self.colour = 'black'
        self.bg = None
        self.row = row
        self.column = column

    def viewAround(self):
        return self.about

    def setAround(self):
        if self.row == 0:
            self.about.append([self.row + 1, self.column])
            if self.column == 0:
                self.about.append([self.row, self.column + 1])
                self.about.append([self.row + 1, self.column + 1])
            elif self.column == len(but[self.row]) - 1:
                self.about.append([self.row, self.column - 1])
                self.about.append([self.row + 1, self.column - 1])
            else:
                self.about.append([self.row, self.column - 1])
                self.about.append([self.row, self.column + 1])
                self.about.append([self.row + 1, self.column + 1])
                self.about.append([self.row + 1, self.column - 1])
        elif self.row == len(but) - 1:
            self.about.append([self.row - 1, self.column])
            if self.column == 0:
                self.about.append([self.row, self.column + 1])
                self.about.append([self.row - 1, self.column + 1])
            elif self.column == len(but[self.row]) - 1:
                self.about.append([self.row, self.column - 1])
                self.about.append([self.row - 1, self.column - 1])
            else:
                self.about.append([self.row, self.column - 1])
                self.about.append([self.row, self.column + 1])
                self.about.append([self.row - 1, self.column + 1])
                self.about.append([self.row - 1, self.column - 1])
        else:
            self.about.append([self.row - 1, self.column])
            self.about.append([self.row + 1, self.column])
            if self.column == 0:
                self.about.append([self.row, self.column + 1])
                self.about.append([self.row + 1, self.column + 1])
                self.about.append([self.row - 1, self.column + 1])
            elif self.column == len(but[self.row]) - 1:
                self.about.append([self.row, self.column - 1])
                self.about.append([self.row + 1, self.column - 1])
                self.about.append([self.row - 1, self.column - 1])
            else:
                self.about.append([self.row, self.column - 1])
                self.about.append([self.row, self.column + 1])
                self.about.append([self.row + 1, self.column + 1])
                self.about.append([self.row + 1, self.column - 1])
                self.about.append([self.row - 1, self.column + 1])
                self.about.append([self.row - 1, self.column - 1])

    def view(self, event):
        unscores = 0
        if mines == []:
            inst(0, self.about, self.row, self.column)
        if self.value == 0:
            self.colour = 'yellow'
            self.value = None
            self.bg = 'lightgrey'
        elif self.value == 1:
            self.colour = 'green'
        elif self.value == 2:
            self.colour = 'blue'
        elif self.value == 3:
            self.colour = 'red'
        elif self.value == 4:
            self.colour = 'purple'

        if self.mine and not self.viewed and not self.znamya:
            self.but1.configure(text='B', bg='red')
            self.viewed = True
            for q in mines:
                but[q[0]][q[1]].view('<Button-1>')
            lose()
            unscores += 1
            path_inf = path + '\\games_info.txt'
            with open(path_inf, 'a', encoding='utf-8') as f:
                f.write("Проиграно партий:" + str(unscores) + "\n")

        elif not self.viewed and not self.znamya:
            self.but1.configure(text=self.value, fg=self.colour, bg=self.bg)
            self.viewed = True
            if self.value == None:
                for k in self.about:
                    but[k[0]][k[1]].view('<Button-1>')

    def setFlag(self, event):
        scores = 0
        if self.znamya == 0 and not self.viewed:
            self.znamya = 1
            self.but1.configure(text='F', bg='yellow')
            znamyas.append([self.row, self.column])
        elif self.znamya == 1:
            self.znamya = 2
            self.but1.configure(text='?', bg='blue')
            znamyas.pop(znamyas.index([self.row, self.column]))
        elif self.znamya == 2:
            self.znamya = 0
            self.but1.configure(text='   ', bg='white')
        if sorted(mines) == sorted(znamyas) and mines != []:
            winer()
            scores += 1
            path_inf = path + '\\games_info.txt'
            with open(path_inf, 'a', encoding='utf-8') as f:
                f.write("Выиграно партий:" + str(scores) + "\n")


def lose():
    loseW = Tk()
    loseW.title('Вы проиграли')
    loseW.geometry('300x100')
    loseLabe = Label(loseW, text='В следующий раз повезет больше!' + "\n")
    loseLabe.pack()
    game_time = datetime.now() - start
    time_labe = Label(loseW, text='Время игры: ' + str(game_time) + "\n")
    time_labe.pack()
    mines = []
    loseW.mainloop()


def inst(q, around, row, column):
    if q == bombs:
        for i in but:
            for j in i:
                for k in j.about:
                    if but[k[0]][k[1]].mine:
                        but[but.index(i)][i.index(j)].value += 1
        return
    a = choice(but)
    b = choice(a)
    if [but.index(a), a.index(b)] not in mines and [but.index(a), a.index(b)] not in around and [
        but.index(a), a.index(b)] != [row,
                                      column]:
        b.mine = True
        mines.append([but.index(a), a.index(b)])
        inst(q + 1, around, row, column)
    else:
        inst(q, around, row, column)


def winer():
    winw = Tk()
    winw.geometry('300x100')
    winw.title('Вы победили!')
    winLabe = Label(winw, text='Поздравляем!' + "\n")
    winLabe.pack()
    game_time = datetime.now() - start
    time_labe = Label(winw, text='Время игры:' + str(game_time))
    time_labe.pack()
    winw.mainloop()


def cheat(event):
    for t in mines:
        but[t[0]][t[1]].setFlag('<Button-1>')


def game(high, lenght):
    root = Tk()
    name = entername.get().strip()[:20].replace(', ', ',')
    if not name:
        name = 'Unknown_player'
    path_inf = path + '\\games_info.txt'
    with open(path_inf, 'a', encoding='utf-8') as f:
            f.write(name + ", ")

    root.title(name)
    global but
    global mines
    global znamyas
    znamyas = []
    mines = []
    but = [[Field(root, row, column) for column in range(high)] for row in
           range(lenght)]
    for i in but:
        for j in i:
            j.but1.grid(column=i.index(j), row=but.index(i), ipadx=7,
                        ipady=1)
            j.but1.bind('<Button-1>', j.view)
            j.but1.bind('<Button-3>', j.setFlag)
            j.setAround()
    but[0][0].but1.bind('<Control-Button-1>', cheat)
    root.resizable(False, False)
    root.mainloop()


def count_mines():
    global bombs
    if mineText.get('1.0', END) == '\n':
        bombs = 10
    else:
        bombs = int(mineText.get('1.0', END))
    if highText.get('1.0', END) == '\n':
        high = 9
    else:
        high = int(highText.get('1.0', END))
    if lenghtText.get('1.0', END) == '\n':
        lenght = 9
    else:
        lenght = int(lenghtText.get('1.0', END))
    game(high, lenght)


settings = Tk()
settings.title('Настройки')
settings.geometry('200x200')
mineText = Text(settings, width=5, height=1)
minelabel = Label(settings, height=1, text='Бомбы:')
highText = Text(settings, width=5, height=1)
highlabel = Label(settings, height=1, text='Ширина:')
lenghtText = Text(settings, width=5, height=1)
lenghtlabel = Label(settings, height=1, text='Высота:')
mineBut = Button(settings, text='Начать', command=count_mines)
mname = Label(settings, height=1, text='Имя игрока:')
entername = Entry(settings, width=20)
author = Label(settings, height=1, text='Автор: Наземцев Сергей, 2020')
mineBut.place(x=70, y=150)
mineText.place(x=75, y=5)
minelabel.place(x=5, y=5)
highText.place(x=75, y=30)
highlabel.place(x=5, y=30)
lenghtText.place(x=75, y=55)
lenghtlabel.place(x=5, y=55)
mname.place(x=55, y=90)
entername.place(x=35, y=120)
author.place(x=20, y=180)
start = datetime.now()
settings.mainloop()


