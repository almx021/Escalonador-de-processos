from tkinter import *

from typing import List, Tuple

# class TableRow(Frame):
#     def __init__(self, master, column_amount: int, values: List[str]) -> None:
#         super().__init__(self, master)
#         self.column_amount = column_amount
#         self.values = values
#         self.entries: List[Entry] = list()

#         for _ in range(self.column_amount):
#             self.grid_columnconfigure(index=0, weight=1)
        
#         assert len(self.values) >= self.column_amount, Exception(args=f"Expected {self.column_amount} elements, got {len(self.values)}")

#         for i in range(self.column_amount):
#             e = Entry(self, state='readonly')
#             e.insert(0, self.values[i])
#             self.entries.append(e)
        
#         for i, entry in enumerate(self.entries):
#             entry.grid(row=0, column=i)

class Table(Frame):
    def __init__(self, master, headers: List[str] | None, row_height: int):
        super().__init__(master, relief="sunken", borderwidth=1)

        self.column_amount = len(headers)

        self.row_height = row_height
        self.table: List[List] = list()

        for item in headers:
            self.table.append([item])

    def render(self):
        self.scrollbar = Scrollbar(self, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = Canvas(self, background="#FFFFFF")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Configure scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.bind("<Configure>", func=lambda _: self._update_canvas())

        self._update_canvas()
    
    def insert_row(self, row: List):
        for index, item in enumerate(row):
            self.table[index].append(item)
        
        self._update_canvas()
    
    def set(self, table: List[List]):

        for index, column in enumerate(self.table):
            table[index].insert(0, column[0])

        self.table = table
        print(self.table)

        self._update_canvas()
    
    def _update_canvas(self):
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()

        # Data relative to their x component
        rectangles_data_x: List[Tuple[float, float]] = []

        # Data relative to their y component
        rectangles_data_y: List[Tuple[float, float]] = []

        cell_width = canvas_width / self.column_amount

        # For each column in the table, set their xa and xb
        for i in range(len(self.table)):
            rectangles_data_x.append((cell_width * i, cell_width * (i + 1)))

        for i in range(len(self.table[0])):
            rectangles_data_y.append((self.row_height * i, self.row_height * (i + 1)))
        
        self.canvas.delete("all")


        # Display header
        ya, yb = rectangles_data_y[0]
        for i in range(len(self.table)):
            xa, xb = rectangles_data_x[i]
            self.canvas.create_text(
                (xa + xb) / 2,
                (ya + yb) / 2,
                anchor="center",
                text=str(self.table[i][0]),
                font=("Arial", 12, "bold")
            )
        
        # Display the rest
        for j in range(1, len(self.table[0])):
            ya, yb = rectangles_data_y[j]
            for i in range(len(self.table)):
                xa, xb = rectangles_data_x[i]
                self.canvas.create_text(
                    (xa + xb) / 2,
                    (ya + yb) / 2,
                    anchor="center",
                    text=self.table[i][j],
                    font=("Arial", 12)
                )

        self.canvas.config(scrollregion=self.canvas.bbox("all"))
