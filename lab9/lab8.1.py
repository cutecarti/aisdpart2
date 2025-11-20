import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import csv


class RentalAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("lab8")
        self.root.geometry("900x600")
        
        self.contracts = []
        
        # Создаем меню
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Открыть файл", command=self.load_data_from_file)
        menubar.add_cascade(label="Файл", menu=file_menu)
        root.config(menu=menubar)
        
        # Создаем вкладки
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка для анализа по оборудованию
        self.create_equipment_tab()
        
        # Вкладка для анализа по датам
        self.create_dates_tab()
        
        # Вкладка для просмотра данных
        self.create_data_view_tab()

    def create_equipment_tab(self):
        """Вкладка анализа по типам оборудования"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Анализ по оборудованию")
        
        tk.Button(tab, text="Построить диаграмму", 
                 command=self.show_equipment_stats).pack(pady=10)
        
        self.equipment_frame = tk.Frame(tab)
        self.equipment_frame.pack(fill=tk.BOTH, expand=True)
        
        # Место для круговой диаграммы
        self.equipment_fig = Figure(figsize=(5, 4), dpi=100)
        self.equipment_canvas = FigureCanvasTkAgg(self.equipment_fig, master=self.equipment_frame)
        self.equipment_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_dates_tab(self):
        """Вкладка анализа по датам"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Анализ по датам")
        
        # Поле для ввода года
        tk.Label(tab, text="Год для анализа:").pack(side=tk.LEFT, padx=5)
        self.year_entry = tk.Entry(tab, width=8)
        self.year_entry.pack(side=tk.LEFT, padx=5)
        self.year_entry.insert(0, datetime.now().year)
        
        tk.Button(tab, text="Построить диаграмму", 
                command=self.show_dates_stats).pack(side=tk.LEFT, padx=10)
        
        self.dates_frame = tk.Frame(tab)
        self.dates_frame.pack(fill=tk.BOTH, expand=True)
        
        # Место для столбчатой диаграммы
        self.dates_fig = Figure(figsize=(5, 4), dpi=100)
        self.dates_canvas = FigureCanvasTkAgg(self.dates_fig, master=self.dates_frame)
        self.dates_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_data_view_tab(self):
        """Вкладка для просмотра загруженных данных"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Просмотр данных")
        
        self.data_tree = ttk.Treeview(tab, columns=(
            "ID", "Client", "Equipment", "Date", "Days", "Price"
        ), show="headings")
        
        # Настраиваем колонки
        self.data_tree.heading("ID", text="Номер")
        self.data_tree.heading("Client", text="Клиент")
        self.data_tree.heading("Equipment", text="Оборудование")
        self.data_tree.heading("Date", text="Дата")
        self.data_tree.heading("Days", text="Дней")
        self.data_tree.heading("Price", text="Цена")
        
        self.data_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(tab, textvariable=self.status_var, bd=1, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X)

    def load_data_from_file(self):
        """Загрузка данных из CSV файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл с данными",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        
        if not file_path:
            return
        
        self.contracts = []
        error_count = 0
        line_count = 0
        
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # Пропускаем заголовок
                
                for row in reader:
                    line_count += 1
                    try:
                        if len(row) != 6:
                            raise ValueError("Неверное количество полей")
                        
                        # Проверяем корректность данных
                        contract_id = row[0]
                        client_name = row[1]
                        equipment_type = row[2]
                        start_date = row[3]
                        duration_days = int(row[4])
                        price = float(row[5])
                        
                        # Проверка даты
                        datetime.strptime(start_date, "%Y-%m-%d")
                        
                        # Добавляем договор
                        self.contracts.append({
                            "id": contract_id,
                            "client": client_name,
                            "equipment": equipment_type,
                            "date": start_date,
                            "days": duration_days,
                            "price": price
                        })
                        
                    except Exception as e:
                        error_count += 1
                        print(f"Ошибка в строке {line_count}: {str(e)}")
            
            # Обновляем статус
            self.status_var.set(
                f"Загружено {len(self.contracts)} договоров. Ошибок: {error_count}"
            )
            
            # Обновляем таблицу
            self.update_data_view()
            
            messagebox.showinfo("Успех", "Данные успешно загружены")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")

    def update_data_view(self):
        """Обновление таблицы с данными"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        for contract in self.contracts:
            self.data_tree.insert("", tk.END, values=(
                contract["id"],
                contract["client"],
                contract["equipment"],
                contract["date"],
                contract["days"],
                contract["price"]
            ))

    def show_equipment_stats(self):
        """Анализ по типам оборудования"""
        if not self.contracts:
            messagebox.showwarning("Ошибка", "Нет данных для анализа")
            return
        
        equipment_stats = {}
        for contract in self.contracts:
            eq_type = contract["equipment"]
            equipment_stats[eq_type] = equipment_stats.get(eq_type, 0) + 1
        
        # Строим круговую диаграмму
        self.equipment_fig.clear()
        ax = self.equipment_fig.add_subplot(111)
        
        labels = list(equipment_stats.keys())
        sizes = list(equipment_stats.values())
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title("Распределение по типам оборудования")
        self.equipment_canvas.draw()

    def show_dates_stats(self):
        """Анализ по месяцам выбранного года"""
        if not self.contracts:
            messagebox.showwarning("Ошибка", "Нет данных для анализа")
            return
        
        try:
            year = int(self.year_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return
        
        monthly_stats = {month: 0 for month in range(1, 13)}
        
        for contract in self.contracts:
            try:
                date_obj = datetime.strptime(contract["date"], "%Y-%m-%d")
                if date_obj.year == year:
                    month = date_obj.month
                    monthly_stats[month] += 1
            except:
                continue
        
        # Строим столбчатую диаграмму
        self.dates_fig.clear()
        ax = self.dates_fig.add_subplot(111)
        
        months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
                 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
        counts = list(monthly_stats.values())
        
        ax.bar(months, counts)
        ax.set_xlabel("Месяц")
        ax.set_ylabel("Количество договоров")
        ax.set_title(f"Распределение по месяцам {year} года")
        self.dates_canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = RentalAnalyzer(root)
    root.mainloop()