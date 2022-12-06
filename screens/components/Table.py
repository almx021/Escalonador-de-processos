from tkinter import *

import numpy as np

from typing import List, Tuple
from numpy.typing import ArrayLike, NDArray


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

blue = "#035AA4"
red = "#EE3124"
white = "#CDCCCC"
yellow = "#BA8843"

class Table(Frame):
    def __init__(self, master, headers: List[str] | None, row_height: int = 20, header_height: int = 20):
        super().__init__(master, relief="sunken", borderwidth=1)

        self.headers = headers
        self.header_height = header_height

        self.row_height = row_height
        self.table = np.array([
            np.array([], dtype=np.chararray),
            np.array([], dtype=np.uint32),
            np.array([], dtype=np.int32)
        ])

    def render(self):
        self.scrollbar = Scrollbar(self, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = Canvas(self, background="#FFFFFF")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Configure scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.bind("<Configure>", func=lambda _: self._update_canvas())
        self.canvas.bind("<Configure>", func=lambda _: self._render_static_objects())

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self._render_static_objects()
        self._update_canvas()
    
    def _render_static_objects(self):
        self.canvas.delete("static")
        self.canvas.update_idletasks()

        width = self.canvas.winfo_width()

        y = self.header_height / 2

        column_width = width / len(self.headers)

        base = np.linspace(0.5, len(self.headers) - 0.5, num=len(self.headers))
        label_x = column_width * base

        self.canvas.create_rectangle(0, 0, width, self.header_height, fill=yellow)
        for index in range(len(self.headers)):
            x = label_x[index]

            self.canvas.create_text(x, y, anchor="center", text=self.headers[index], tags=("static"), fill="#FFFFFF", font=("Arial", 12, "bold"), justify="center")
    
    def insert_row(self, row: List):
        for index, item in enumerate(row):
            self.table[index].append(item)
        
        self._update_canvas()
    
    def set(self, table):
        self.table = table

        self._update_canvas()
    
    def _update_canvas(self):
        # self.canvas.update_idletasks()
        # canvas_width = self.canvas.winfo_width()

        # # Data relative to their x component
        # rectangles_data_x: List[Tuple[float, float]] = []

        # # Data relative to their y component
        # rectangles_data_y: List[Tuple[float, float]] = []

        # cell_width = canvas_width / self.column_amount

        # # For each column in the table, set their xa and xb
        # for i in range(len(self.table)):
        #     rectangles_data_x.append((cell_width * i, cell_width * (i + 1)))

        # for i in range(len(self.table[0])):
        #     rectangles_data_y.append((self.row_height * i, self.row_height * (i + 1)))
        
        # self.canvas.delete("all")


        # # Display header
        # ya, yb = rectangles_data_y[0]
        # for i in range(len(self.table)):
        #     xa, xb = rectangles_data_x[i]
        #     self.canvas.create_text(
        #         (xa + xb) / 2,
        #         (ya + yb) / 2,
        #         anchor="center",
        #         text=str(self.table[i][0]),
        #         font=("Arial", 12, "bold")
        #     )
        
        # # Display the rest
        # for j in range(1, len(self.table[0])):
        #     ya, yb = rectangles_data_y[j]
        #     for i in range(len(self.table)):
        #         xa, xb = rectangles_data_x[i]
        #         self.canvas.create_text(
        #             (xa + xb) / 2,
        #             (ya + yb) / 2,
        #             anchor="center",
        #             text=self.table[i][j],
        #             font=("Arial", 12)
        #         )

        # self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()

        column_amount = len(self.headers)
        column_width = width / column_amount

        _, process_amount = self.table.shape

        base = np.linspace(0.5, len(self.headers) - 0.5, num=column_amount)
        label_x = column_width * base

        base = np.linspace(0.5, process_amount - 0.5, num=process_amount)
        label_y = self.row_height * base + self.header_height

        rectangle_y0 = np.linspace(self.header_height, self.header_height + process_amount * self.row_height, num=process_amount + 1)
        rectangle_y1 = rectangle_y0 + self.row_height

        colors = ["#035AA4", "#EE3124"]

        self.canvas.delete("dynamic")
        for i in range(process_amount):
            y = label_y[i]
            self.canvas.create_rectangle(0, rectangle_y0[i], width, rectangle_y1[i], fill=colors[i % 2], tags=("dynamic"))
            for j in range(0, column_amount):
                x = label_x[j]
                self.canvas.create_text(x, y, anchor="center", text=self.table[j][i], fill="#FFFFFF", tags=("dynamic"))

        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()
        
