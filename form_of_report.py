import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from faker import Faker

class PatientManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления пациентами")
        self.root.geometry("1200x800")
        
        self.patients = []
        self.data_file = "patients_data.json"
        self.faker = Faker('ru_RU')
        
        self.load_data()
        
        self.create_widgets()
        
    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)
        
        self.tab_patients = ttk.Frame(tab_control)
        tab_control.add(self.tab_patients, text='Пациенты')
        
        self.tab_stats = ttk.Frame(tab_control)
        tab_control.add(self.tab_stats, text='Статистика')
        
        tab_control.pack(expand=1, fill='both')
        
        self.create_patients_tab()
        self.create_stats_tab()
    
    def create_patients_tab(self):
        button_frame = ttk.Frame(self.tab_patients)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Добавить пациента", 
                  command=self.add_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Редактировать", 
                  command=self.edit_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", 
                  command=self.delete_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Сгенерировать тестовые данные", 
                  command=self.generate_test_data).pack(side=tk.LEFT, padx=5)
        
        columns = ('ФИО', 'Возраст', 'Пол', 'Рост', 'Вес', 'ИМТ')
        self.tree = ttk.Treeview(self.tab_patients, columns=columns, show='headings')
    
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.update_table()
    
    def create_stats_tab(self):
        ttk.Button(self.tab_stats, text="Обновить статистику", 
                  command=self.show_statistics).pack(pady=10)
        
        self.stats_frame = ttk.Frame(self.tab_stats)
        self.stats_frame.pack(expand=True, fill='both', padx=10, pady=10)
    
    def calculate_bmi(self, weight, height):
        """Расчет индекса массы тела"""
        if height > 0:
            return round(weight / ((height / 100) ** 2), 2)
        return 0
    
    def generate_test_data(self):
        """Генерация тестовых данных с помощью Faker"""
        count = simpledialog.askinteger("Генерация данных", "Сколько пациентов сгенерировать?", 
                                       initialvalue=10, minvalue=1, maxvalue=100)
        if count:
            for _ in range(count):
                gender = self.faker.random_element(['Мужской', 'Женский'])
                if gender == 'Мужской':
                    name = self.faker.last_name_male() + " " + self.faker.first_name_male() + " " + self.faker.middle_name_male()
                    height = self.faker.random_int(165, 195)
                    weight = self.faker.random_int(65, 110)
                else:
                    name = self.faker.last_name_female() + " " + self.faker.first_name_female() + " " + self.faker.middle_name_female()
                    height = self.faker.random_int(155, 180)
                    weight = self.faker.random_int(50, 85)
                
                age = self.faker.random_int(18, 80)
                
                patient_data = {
                    'ФИО': name,
                    'Возраст': age,
                    'Пол': gender,
                    'Рост': height,
                    'Вес': weight,
                    'ИМТ': self.calculate_bmi(weight, height)
                }
                self.patients.append(patient_data)
            
            self.save_data()
            self.update_table()
            messagebox.showinfo("Успех", f"Сгенерировано {count} тестовых пациентов")
    
    def add_patient(self):
        """Добавление нового пациента"""
        dialog = PatientDialog(self.root, "Добавить пациента")
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            patient_data = dialog.result
            patient_data['ИМТ'] = self.calculate_bmi(patient_data['Вес'], patient_data['Рост'])
            self.patients.append(patient_data)
            self.save_data()
            self.update_table()

    def edit_patient(self):
        """Редактирование выбранного пациента"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пациента для редактирования")
            return
        
        index = self.tree.index(selected[0])
        patient = self.patients[index]
        
        dialog = PatientDialog(self.root, "Редактировать пациента", patient)
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            updated_data = dialog.result
            updated_data['ИМТ'] = self.calculate_bmi(updated_data['Вес'], updated_data['Рост'])
            self.patients[index] = updated_data
            self.save_data()
            self.update_table()
        
    def delete_patient(self):
        """Удаление выбранного пациента"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пациента для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить пациента?"):
            index = self.tree.index(selected[0])
            del self.patients[index]
            self.save_data()
            self.update_table()
    
    def update_table(self):
        """Обновление таблицы пациентов"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for patient in self.patients:
            self.tree.insert('', 'end', values=(
                patient['ФИО'],
                patient['Возраст'],
                patient['Пол'],
                patient['Рост'],
                patient['Вес'],
                patient['ИМТ']
            ))
    
    def show_statistics(self):
        """Отображение статистики"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if not self.patients:
            ttk.Label(self.stats_frame, text="Нет данных для отображения статистики").pack(pady=20)
            return
        
        self.create_gender_distribution()
        self.create_age_distribution()
        self.create_bmi_by_gender()
        self.create_bmi_by_age()
    
    def create_gender_distribution(self):
        """Распределение пациентов по полу"""
        genders = [p['Пол'] for p in self.patients]
        male_count = genders.count('Мужской')
        female_count = genders.count('Женский')
        
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.pie([male_count, female_count], labels=['Мужской', 'Женский'], autopct='%1.1f%%')
        ax.set_title('Распределение пациентов по полу')
        
        canvas = FigureCanvasTkAgg(fig, self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    
    def create_age_distribution(self):
        """Распределение пациентов по возрасту"""
        ages = [p['Возраст'] for p in self.patients]
        
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.hist(ages, bins=10, edgecolor='black', alpha=0.7)
        ax.set_xlabel('Возраст')
        ax.set_ylabel('Количество пациентов')
        ax.set_title('Распределение пациентов по возрасту')
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    
    def create_bmi_by_gender(self):
        """Распределение ИМТ с учётом пола"""
        male_bmi = [p['ИМТ'] for p in self.patients if p['Пол'] == 'Мужской']
        female_bmi = [p['ИМТ'] for p in self.patients if p['Пол'] == 'Женский']
        
        fig, ax = plt.subplots(figsize=(6, 4))
        data = [male_bmi, female_bmi]
        labels = ['Мужской', 'Женский']
        ax.boxplot(data, labels=labels)
        ax.set_ylabel('ИМТ')
        ax.set_title('Распределение ИМТ по полу')
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    
    def create_bmi_by_age(self):
        """Зависимость ИМТ от возраста"""
        ages = [p['Возраст'] for p in self.patients]
        bmis = [p['ИМТ'] for p in self.patients]
        genders = [p['Пол'] for p in self.patients]
        
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ['blue' if g == 'Мужской' else 'red' for g in genders]
        ax.scatter(ages, bmis, c=colors, alpha=0.6)
        ax.set_xlabel('Возраст')
        ax.set_ylabel('ИМТ')
        ax.set_title('Зависимость ИМТ от возраста')
        ax.grid(True, alpha=0.3)
        
        ax.scatter([], [], c='blue', label='Мужской', alpha=0.6)
        ax.scatter([], [], c='red', label='Женский', alpha=0.6)
        ax.legend()
        
        canvas = FigureCanvasTkAgg(fig, self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    
    def save_data(self):
        """Сохранение данных в файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.patients, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def load_data(self):
        """Загрузка данных из файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.patients = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
                self.patients = []

class PatientDialog:
    def __init__(self, parent, title, patient=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        ttk.Label(self.dialog, text="ФИО:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.name_entry = ttk.Entry(self.dialog)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(self.dialog, text="Возраст:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.age_entry = ttk.Entry(self.dialog)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(self.dialog, text="Пол:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.gender_var = tk.StringVar()
        self.gender_combo = ttk.Combobox(self.dialog, textvariable=self.gender_var, 
                                        values=['Мужской', 'Женский'], state='readonly')
        self.gender_combo.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(self.dialog, text="Рост (см):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.height_entry = ttk.Entry(self.dialog)
        self.height_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(self.dialog, text="Вес (кг):").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.weight_entry = ttk.Entry(self.dialog)
        self.weight_entry.grid(row=4, column=1, padx=5, pady=5, sticky='we')
    
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Сохранить", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        if patient:
            self.name_entry.insert(0, patient['ФИО'])
            self.age_entry.insert(0, str(patient['Возраст']))
            self.gender_combo.set(patient['Пол'])
            self.height_entry.insert(0, str(patient['Рост']))
            self.weight_entry.insert(0, str(patient['Вес']))
        
        self.dialog.columnconfigure(1, weight=1)
        self.dialog.bind('<Return>', lambda e: self.save())
    
    def save(self):
        """Сохранение данных пациента"""
        try:
            name = self.name_entry.get().strip()
            age = int(self.age_entry.get())
            gender = self.gender_var.get()
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            
            if not name or not gender:
                messagebox.showwarning("Предупреждение", "Заполните все обязательные поля")
                return
            
            if age <= 0 or height <= 0 or weight <= 0:
                messagebox.showwarning("Предупреждение", "Возраст, рост и вес должны быть положительными числами")
                return
            
            self.result = {
                'ФИО': name,
                'Возраст': age,
                'Пол': gender,
                'Рост': height,
                'Вес': weight
            }
            
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность введенных числовых значений")

def main():
    root = tk.Tk()
    app = PatientManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()