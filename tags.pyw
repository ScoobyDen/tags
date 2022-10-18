from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint
from winsound import Beep
from time import sleep

def music():
    Beep(100, 100)
    Beep(200, 200)
    Beep(300, 250)

def refreshText():
    textSteps["text"] = f"Зроблено ходів: {steps[diffCombobox.current()]}"
    textRecord["text"] = f"Рекорд ходів: {record[diffCombobox.current()]}"

def saveRecords():
    global record
    # відкриваємо та записуємо 
    try:
        f = open("steps.dat", "w", encoding="utf-8")
        for i in range(len(steps)):
            # Перевіряємо: щоб побити рекорд, кількість кроків для кожного рівня має бути більшою за нуль, але менше попереднього рекорду
            if (steps[i] > 0 and steps[i] < record[i]):
                record[i] = steps[i]
            f.write(str(record[i]) + "\n")
        f.close()
    # У разі помилки створення та запису
    except:
        messagebox.showerror("Помилка",
                             "Виникла помилка з файлом при збереженні рекорду")

def getRecordSteps():
    try:
        m = []
        f = open("steps.dat", "r", encoding="utf-8")
        for line in f.readlines():
            m.append(int(line))
        f.close()
    except:
        #якщо помилка створюємо список вручну
        m = []
    # перевіряємо: довжина списку повинна бути ровно 6! 
    if (len(m) != 6):
        for i in range(6):
            m.append(1000 + 1000 * i)

    return m

def seeEnd(event):
    global dataImage
    Beep(1082, 25)
    for i in range(n):
        for j in range(m):
            dataImage[i][j] = copyData[i][j]                                                    #відновлюємо з copyData значення в dataImage
    updatePictures()

def seeStart(event):
    global copyData, dataImage
    Beep(1632, 25)
    for i in range(n):
        for j in range(m):
            copyData[i][j] = dataImage[i][j]                                                    #передаємо значення напряму, копіюя їх
            dataImage[i][j] = i * n + j                                                         #формуємо зібране поле, встановлюя значення 0-15 включно
    updatePictures()

def isCheckImage():
    global imageBackground
    if (image.get()):
        imageBackground = imageBackground01
        Beep(1000, 25)
    else:
        imageBackground = imageBackground02
        Beep(1300, 25)
    updatePictures()

def go(x,y):
    global steps, playGame
    if (x + 1 < n and dataImage[x + 1][y] == blackImg):
        exchangeImage(x, y, x + 1, y)
    elif (x - 1 >= 0 and dataImage[x - 1][y] == blackImg):
        exchangeImage(x, y, x - 1, y)
    elif (y + 1 < m and dataImage[x][y + 1] == blackImg):
        exchangeImage(x, y, x, y + 1)
    elif (y - 1 >= 0 and dataImage[x][y - 1] == blackImg):
        exchangeImage(x, y, x, y - 1)
    else:
        Beep(500, 100)
        return 0
    
    Beep(1400, 5)
    #якщо гра йде та мєтод виконується (не спрацювало return 0), то ми додаємо +1 крок
    if (playGame):
        steps[diffCombobox.current()] += 1
        refreshText()
        #зазделегіть припускаємо що користувач виграв. задача алгоритму доказати що це не так
        win = True
        #в циклах обходимо весь список dataimage
        for i in range(n):
            for j in range(m):
                #порівнюємо праву нижню клітину з blackImg
                if ( i == n - 1 and j == m - 1):
                    #якщо хоча б один з виразів - False, то win стане False
                    win = win and dataImage[i][j] == blackImg
                #в іншому випадку порівнюєм з числовим рядом 0...14 включно
                else:
                    win = win and dataImage[i][j] == i * n + j
        if (win):
            dataImage[n - 1][m - 1] = blackImg -1                           #встановлюємо замість вільного поля спрайт для цльності зображення
            updatePictures()

            messagebox.showinfo("Вітаю!", "Ви виграли!")
            music()

            saveRecords()
            playGame = False
            refreshText()   
    
    
def updatePictures():
    #за допомгою цикла проходимо всі labelImage[][] і встановлюємо в них необхідні зображення
    for i in range(n):
        for j in range(m):
            labelImage[i][j]["image"] = imageBackground[dataImage[i][j]]
    root.update() 

def resetPictures():
    global dataImage, steps, playGame
    steps[diffCombobox.current()] = 0
    playGame = False
    #налаштовуємо стан віджетів
    startButton["state"] = NORMAL
    resetButton["state"] = DISABLED
    diffCombobox["state"] = "readonly"
    radio01["state"] = NORMAL
    radio02["state"] = NORMAL
    #заповнюємо dataImage[][] первинними значеннями 
    for i in range(n):
        for j in range(m):
            dataImage[i][j] = i * n + j
    dataImage[n - 1][m - 1] = blackImg
    Beep(800, 50)
    Beep(810, 35)

    updatePictures()
    refreshText()


def exchangeImage(x1, y1, x2, y2):
    global dataImage, labelImage
    #змінюємо математичну модель
    dataImage[x1][y1], dataImage[x2][y2] = dataImage[x2][y2], dataImage[x1][y1]
    #отримуємо зображення по номеру з dataImage і встановлюємо його в labelImage
    labelImage[x1][y1]["image"] = imageBackground[dataImage[x1][y1]]
    labelImage[x2][y2]["image"] = imageBackground[dataImage[x2][y2]]
    root.update()
    sleep(0.01)

def shufflePictures(x, y):
    if (diffCombobox.current() < 5):
        count = (2 + diffCombobox.current()) ** 4                           #кількість пермішування в залежності від рівня складності
        noDirection = 0                                             #заборона напряку
        for i in range(count):
            direction = noDirection                                 #задаємо свідомо истинну комбінацію для while
            while (direction == noDirection):                       #отримуємо число, точно не дублююче попереднє
                direction = randint(0, 3)
            if (direction == 0 and x + 1 < n):                      #вниз
                exchangeImage(x, y, x + 1, y)                       #обмінюємо поточну та спрайт нижче
                x += 1                                              #збільшуємо х, т.я. пусте місце перемістилося в позицію х +1
                noDirection = 1                                     #забороняємо напрямок, тобто не повинно повернутися назад наступного разу
            elif (direction == 1 and x - 1 >= 0):                   #вверх
                exchangeImage(x, y, x - 1, y)                      
                x -= 1                                              
                noDirection = 0
            elif (direction == 2 and y + 1 < m):                    #вправо
                exchangeImage(x, y, x, y + 1)                      
                y += 1                                              
                noDirection = 3
            elif (direction == 3 and y - 1 >= 0):                   #вліво
                exchangeImage(x, y, x, y - 1)                      
                y -= 1                                              
                noDirection = 2
    else:
        exchangeImage(n - 1, m - 3, n - 1, m - 2)
    
    Beep(1750, 50)

    resetButton["state"] = NORMAL


def startNewRound():
    global steps, playGame
    #гра почалася
    playGame = True

    #обнуляємо кількість шагів дял поточного рівня
    steps[diffCombobox.current()] = 0
    #зкидаємо стан кнопок
    diffCombobox["state"] = DISABLED
    startButton["state"] = DISABLED
    radio01["state"] = DISABLED
    radio02["state"] = DISABLED

    Beep(750, 50)                                               #звуковий сігнал

    #знаходимо координати пустого поля перебором кожного поля двувимірного списку dataImage[][]
    x = 0
    y = 0
    for i in range (n):
        for j in range(m):
            #при співпаданні числа в dataImage[][] з номером пустого поля передаємо в x/y лічильники циклів
            #тому що їх значення і будуть шукаємими координатами
            if (dataImage[i][j] == blackImg):
                x = i
                y = j

    shufflePictures(x, y)
    refreshText()

#================ ПОЧАТОК ПРОГРАМИ

root = Tk()
root.resizable(False, False)
root.title("Tags")

#ярлик зроблений на сайті https://www.favicon.by/
root.iconbitmap("icon\icon.ico")

#кольори
back = "#373737"
fore = "#AFAFAF"

#геометрія вікна
WIDTH = 422
HEIGHT = 730
POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

#встановлюємо фоновий колір
root["bg"] = back

#=============== НАДПИСИ І КНОПКИ

#Кнопка подивитися зібране
seeButton = Button(root, text="Подивитися, як повинно бути", width=56)
seeButton.place(x=10, y=620)
seeButton.bind("<Button-1>", seeStart)
seeButton.bind("<ButtonRelease>", seeEnd)

#Кнопка старт
startButton = Button(text="Старт", width=56)
startButton.place(x=10, y=650)
startButton["command"] = startNewRound

#Кнопка сбросу
resetButton = Button(root, text="Сброс", width=56)
resetButton.place(x=10, y=680)
resetButton["command"] = resetPictures

#інфопанель
textSteps = Label(root, bg=back, fg=fore)
textSteps.place(x=10, y=550)
textRecord = Label(root, bg=back, fg=fore)
textRecord.place(x=10, y=570)
#мітка складності
Label(root, bg=back, fg=fore, text="Складність").place(x=267, y=550)

#назви ступенів складності перемішування
itemDiff =["Тільки почав", "Трішки почитав", "Знаю print()", "Зрозумів сортування", "Вивчив лабіринт", "Задонатив!"]
#Випадаючий список
diffCombobox = ttk.Combobox(root, width=20, values=itemDiff, state="readonly")
diffCombobox.place(x=270, y=570)
diffCombobox.bind("<<ComboboxSelected>>", lambda e: refreshText())

#по замовчунню пункт: "тільки почав"
diffCombobox.current(0)

#Радіоперемикачи
image = BooleanVar()                                                        #створюємо змінну
image.set(True)                                                             #встановлюємо значення
#створюємо радіо-кнопку та прив'язуємо до неї змінну image
radio01 = Radiobutton(root, text="Фара", variable=image, value=True, activebackground=back, bg=back, fg=fore)
radio02 = Radiobutton(root, text="Соня", variable=image, value=False, activebackground=back, bg=back, fg=fore)
radio01["command"] = isCheckImage
radio02["command"] = isCheckImage 
radio01.place(x=150, y=548)
radio02.place(x=150, y=568)

#============= ЗОБРАЖЕННЯ

#розмір поля
n = 4
m = 4

#розмір повного зображення
pictureWidth = 400
pictureHeight = 532
#ширина та висота одного зображення
widthPic = pictureWidth / n
heightPic = pictureHeight / m

fileName = ["img01.png", "img02.png", "img03.png", "img04.png", "img05.png", "img06.png", "img07.png", "img08.png",
            "img09.png", "img10.png", "img11.png", "img12.png", "img13.png", "img14.png", "img15.png", "img16.png", "black.png"]

imageBackground = []                                                        #активне зображення
imageBackground01 = []                                                      #космос
imageBackground02 = []                                                      #соня

#додаємо в списки елементи та завантажуємо в них об'єкти PhotoImage
for name in fileName:
    imageBackground01.append(PhotoImage(file="image01/" + name))
    imageBackground02.append(PhotoImage(file="image02/" + name))
#номер зображення пустого поля
blackImg = 16

#встановлюємо набір спрайтів "Космос"
imageBackground = imageBackground01

#мітки Label
labelImage = []

#математична модель ігрового поля
dataImage = []

#для створення копії моделі ігрового поля при просмотрі по кнопці "Подивитися, як повинно бути"
copyData = []

for i in range(n):
    #починаємо заповнювати списк
    labelImage.append([])
    dataImage.append([])
    copyData.append([])
    for j in range(m):
        #формула i * n + j згенерує ряд чисел 0, 1, 2 і т.д. Це і є номера зібраної версії зображення
        dataImage[i].append(i * n + j)
        copyData[i].append(i * n + j)
        #створюємо та налаштовуємо Label, в який будемо виводити PhotoImage з imageBackground
        labelImage[i].append(Label(root, bg=back))
        labelImage[i][j]["bd"] = 1
        labelImage[i][j].place(x=10 + j * widthPic, y=10 + i * heightPic)
        #що трапиться при натисканні на Label
        labelImage[i][j].bind("<Button-1>", lambda e, x=i, y=j: go(x, y))
        #встановлюємо зображення
        labelImage[i][j]["image"] = imageBackground[dataImage[i][j]]

# ============= ХОДИ ===========
steps = [0, 0, 0, 0, 0]

#почалась гра?
playGame = False

#найменша кількість шагів для збору головоломки
record = getRecordSteps()

refreshText()

resetPictures()
root.mainloop()