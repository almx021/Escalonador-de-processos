from tkinter import *

from random import randint

from screens.components.Table import Table

def main():
    window = Tk()
    window.geometry("800x600")

    window.grid_rowconfigure(index=0, weight=1)
    window.grid_rowconfigure(index=1, weight=12)

    window.grid_columnconfigure(index=0, weight=1)
    window.grid_columnconfigure(index=1, weight=1)
    window.grid_columnconfigure(index=2, weight=1)
    window.grid_columnconfigure(index=3, weight=1)

    table = Table(window, ["Index 1", "Index 2", "Index 3"], 20)
    table.grid(row=1, column=0, columnspan=4, sticky="nsew")
    table.render()

    e1 = Entry(window)
    e1.grid(row=0, column=0, sticky="ew", padx=2)

    e2 = Entry(window)
    e2.grid(row=0, column=1, sticky="ew", padx=2)

    e3 = Entry(window)
    e3.grid(row=0, column=2, sticky="ew", padx=2)

    e4 = Button(window, text="Insert", command=lambda: table.insert_row([e1.get(), e2.get(), e3.get(), "?"]))
    e4.grid(row=0, column=3, sticky="ew", padx=2)

    table.set([["A", "D", "G", "J"], ["B", "E", "H", "K"], ["C", "F", "I", "L"]])

    window.mainloop()

if __name__ == "__main__":
    main()