from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint
from winsound import Beep

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
#seeButton.bind("<Button-1>, seeStart")
#seeButton.bind("<ButtonRelease>", seeEnd)

#Кнопка старт
startButton = Button(text="Старт", width=56)
startButton.place(x=10, y=650)
#startButton["command"] = startNewRound

#Кнопка сбросу
resetButton = Button(root, text="Сброс", width=56)
resetButton.place(x=10, y=680)
#resetButton["command"] = resetPictures

#інфопанель
textSteps = Label(root, bg=back, fg=fore)
textSteps.place(x=10, y=550)
textRecord = Label(root, bg=back, fg=fore)
textRecord.place(x=10, y=570)
#мітка складності
Label(root, bg=back, fg=fore, text="Складність").place(x=267, y=550)

#назви ступенів складності перемішування
itemDiff =["Тільки почав", "Трішки почитав", "Зная print()", "Зрозумів сортування", "Вивчив лабіринт", "Задонатив!"]
#Випадаючий список
diffCombobox = ttk.Combobox(root, width=20, values=itemDiff, state="readonly")
diffCombobox.place(x=270, y=570)
#diffCombobox.bind("<<ComboboxSelected>>", lamda e: refreshText())

#по замовчунню пункт: "тільки почав"
diffCombobox.current(0)

#Радіоперемикачи
image = BooleanVar()                                                        #створюємо змінну
image.set(True)                                                             #встановлюємо значення
#створюємо радіо-кнопку та прив'язуємо до неї змінну image
radio01 = Radiobutton(root, text="Космос", variable=image, value=True, activebackground=back, bg=back, fg=fore)
radio02 = Radiobutton(root, text="Соня", variable=image, value=False, activebackground=back, bg=back, fg=fore)
#radio01["command"] = isCheckImage
#radio02["command"] = isCheckImage 
radio01.place(x=150, y=548)
radio02.place(x=150, y=568)

root.mainloop()