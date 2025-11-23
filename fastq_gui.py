import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastq_reader import FastqReader


class FastqGUI:
    """Графический интерфейс для работы с FASTQ файлами"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FASTQ File Analyzer")
        self.root.geometry("1200x800")
        
        self.reader = None
        self.current_file = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Создание интерфейса"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Open FASTQ File", 
                  command=self.open_file).grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        stats_frame = ttk.LabelFrame(main_frame, text="File Statistics", padding="10")
        stats_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_text = tk.Text(stats_frame, height=6, width=80, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=scrollbar.set)
        
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)
        
        plot_frame = ttk.LabelFrame(main_frame, text="Visualizations", padding="10")
        plot_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(1, weight=1)
        
        button_frame = ttk.Frame(plot_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(button_frame, text="Per Base Quality", 
                  command=self.show_quality_plot).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Sequence Content", 
                  command=self.show_content_plot).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Length Distribution", 
                  command=self.show_length_plot).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Clear Plots", 
                  command=self.clear_plot).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Export Stats", 
                  command=self.export_statistics).pack(side=tk.LEFT)
        
        plot_container = ttk.Frame(plot_frame)
        plot_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        plot_container.columnconfigure(0, weight=1)
        plot_container.rowconfigure(0, weight=1)
        
        self.canvas_frame = ttk.Frame(plot_container)
        self.canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.canvas_frame.columnconfigure(0, weight=1)
        
        plot_scrollbar = ttk.Scrollbar(plot_container, orient=tk.VERTICAL)
        plot_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.plot_canvas = tk.Canvas(self.canvas_frame, yscrollcommand=plot_scrollbar.set)
        plot_scrollbar.config(command=self.plot_canvas.yview)
        
        self.plot_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)
        
        self.plot_frame = ttk.Frame(self.plot_canvas)
        self.plot_canvas_window = self.plot_canvas.create_window((0, 0), window=self.plot_frame, anchor="nw")
        
        self.plot_frame.bind("<Configure>", self._on_frame_configure)
        self.plot_canvas.bind("<Configure>", self._on_canvas_configure)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def _on_frame_configure(self, event):
        """Update scrollregion when plot frame size changes"""
        self.plot_canvas.configure(scrollregion=self.plot_canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Update canvas window width when canvas size changes"""
        self.plot_canvas.itemconfig(self.plot_canvas_window, width=event.width)
    
    def open_file(self):
        """Открытие файла через диалоговое окно"""
        file_types = [
            ("FASTQ files", "*.fastq *.fq"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select FASTQ File",
            filetypes=file_types
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """Загрузка и анализ FASTQ файла"""
        try:
            self.status_var.set("Loading file...")
            self.root.update()
            
            self.reader = FastqReader(file_path)
            self.reader.read()
            self.current_file = file_path
            
            file_name = os.path.basename(file_path)
            self.file_label.config(text=f"Loaded: {file_name}")
            
            self.show_statistics()
            
            self.status_var.set(f"File loaded successfully: {self.reader.count_sequences()} sequences")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            self.status_var.set("Error loading file")
    
    def show_statistics(self):
        """Отображение статистики файла"""
        if not self.reader:
            return
        
        stats_text = f"""File: {os.path.basename(self.current_file)}
Total sequences: {self.reader.count_sequences():,}
Total length: {self.reader.total_length:,} bp
Average sequence length: {self.reader.get_average_sequence_len():.2f} bp
"""
        
        if self.reader.seq_dict:
            sample_ids = list(self.reader.seq_dict.keys())[:3]
            stats_text += "\nSample sequences quality:\n"
            for seq_id in sample_ids:
                avg_quality = self.reader.get_average_quality(seq_id)
                length = self.reader.get_sequence_length(seq_id)
                stats_text += f"  {seq_id}: length={length} bp, avg_quality={avg_quality:.2f}\n"
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state=tk.DISABLED)
    
    def clear_plot(self):
        """Очистка области с графиком"""
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        self.plot_canvas.configure(scrollregion=self.plot_canvas.bbox("all"))
    
    def show_quality_plot(self):
        """Отображение графика качества последовательностей"""
        if not self.validate_reader():
            return
        
        try:
            self.status_var.set("Generating quality plot...")
            self.root.update()
            
            fig = plt.Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            import io
            import contextlib
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            
            temp_canvas = FigureCanvasAgg(fig)
            
            self.reader.per_base_sequence_quality()
            
            current_fig = plt.gcf()
            
            canvas = FigureCanvasTkAgg(current_fig, master=self.plot_frame)
            canvas.draw()
            
            widget = canvas.get_tk_widget()
            widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            self.plot_canvas.configure(scrollregion=self.plot_canvas.bbox("all"))
            
            self.status_var.set("Quality plot generated")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate quality plot: {str(e)}")
            self.status_var.set("Error generating plot")
    
    def show_content_plot(self):
        """Отображение графика содержания последовательностей"""
        if not self.validate_reader():
            return
        
        try:
            self.status_var.set("Generating sequence content plot...")
            self.root.update()
            
            self.reader.per_base_sequence_content()
            current_fig = plt.gcf()
            canvas = FigureCanvasTkAgg(current_fig, master=self.plot_frame)
            canvas.draw()
            
            widget = canvas.get_tk_widget()
            widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            self.plot_canvas.configure(scrollregion=self.plot_canvas.bbox("all"))
            self.status_var.set("Sequence content plot generated")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate content plot: {str(e)}")
            self.status_var.set("Error generating plot")
    
    def show_length_plot(self):
        """Отображение графика распределения длин последовательностей"""
        if not self.validate_reader():
            return
        
        try:
            self.status_var.set("Generating length distribution plot...")
            self.root.update()
            
            self.reader.sequence_length_distribution()
            current_fig = plt.gcf()
            canvas = FigureCanvasTkAgg(current_fig, master=self.plot_frame)
            canvas.draw()
            
            widget = canvas.get_tk_widget()
            widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            self.plot_canvas.configure(scrollregion=self.plot_canvas.bbox("all"))
            self.status_var.set("Length distribution plot generated")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate length plot: {str(e)}")
            self.status_var.set("Error generating plot")
    
    def export_statistics(self):
        """Экспорт статистики в файл"""
        if not self.validate_reader():
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.stats_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Statistics exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export statistics: {str(e)}")
    
    def validate_reader(self):
        """Проверка наличия загруженного файла"""
        if not self.reader:
            messagebox.showwarning("Warning", "Please load a FASTQ file first")
            return False
        return True


def main():
    """Основная функция запуска графического интерфейса"""
    root = tk.Tk()
    app = FastqGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()