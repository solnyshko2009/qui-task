import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("!Tequila Sunrise!")
        self.window.geometry("300x400")
        
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        # Загружаем изображение для фона
        self.bg_image = tk.PhotoImage(file="Tequila_Sunrise_full.png")
        
        # Создаем Label с фоновым изображением
        self.bg_label = tk.Label(self.window, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Загружаем изображение для кнопок
        self.load_image()
        
        self.create_widgets()
    
    def load_image(self):
            self.button_image = tk.PhotoImage(file="Tequila_Sunrise.png")
    
    def create_widgets(self):
        display_frame = tk.Frame(self.window, height=50)
        display_frame.pack(pady=10, padx=10, fill=tk.X)
        
        display = tk.Entry(
            display_frame, 
            textvariable=self.result_var, 
            font=('Arial', 18), 
            justify='right', 
            state='readonly',
        )
        display.pack(fill=tk.BOTH, ipady=5)
        
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        buttons = [
            ['C', '√', 'x²', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '^']
        ]
        
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                button = tk.Button(
                    buttons_frame,
                    text=button_text,
                    image=self.button_image,  # используем загруженное изображение
                    compound='center',  # текст поверх изображения
                    font=('Arial', 14),
                    command=lambda text=button_text: self.button_click(text)
                    )
                
                button.grid(
                    row=i, 
                    column=j, 
                    sticky='nsew', 
                    padx=2, 
                    pady=2,
                    ipadx=10,
                    ipady=10
                )
        
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)
    
    def button_click(self, text):
        if text == 'C':
            self.clear()
        elif text == '=':
            self.calculate()
        elif text == '√':
            self.square_root()
        elif text == 'x²':
            self.square()
        elif text == '^':
            self.add_operator('**')
        else:
            self.add_to_input(text)
    
    def add_to_input(self, text):
        if self.current_input == "0" and text not in ['+', '-', '*', '/', '**']:
            self.current_input = text
        else:
            self.current_input += text
        self.result_var.set(self.current_input)
    
    def add_operator(self, operator):
        if self.current_input and self.current_input[-1] not in ['+', '-', '*', '/', '.', '*']:
            self.current_input += operator
            self.result_var.set(self.current_input)
    
    def clear(self):
        self.current_input = ""
        self.result_var.set("0")
    
    def square_root(self):
        try:
            if self.current_input:
                result = math.sqrt(float(eval(self.current_input)))
                self.current_input = str(result)
                self.result_var.set(self.current_input)
            else:
                self.result_var.set("Ошибка: нет числа")
        except:
            self.result_var.set("Ошибка")
            self.current_input = ""
    
    def square(self):
        try:
            if self.current_input:
                result = float(eval(self.current_input)) ** 2
                self.current_input = str(result)
                self.result_var.set(self.current_input)
            else:
                self.result_var.set("Ошибка: нет числа")
        except:
            self.result_var.set("Ошибка")
            self.current_input = ""
    
    def calculate(self):
        try:
            result = eval(self.current_input)
            self.current_input = str(result)
            self.result_var.set(self.current_input)
        except ZeroDivisionError:
            self.result_var.set("Ошибка: деление на 0")
            self.current_input = ""
        except:
            self.result_var.set("Ошибка")
            self.current_input = ""
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()