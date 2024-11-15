import tkinter as tk
from tkinter import ttk, filedialog
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # Importa pandas para trabajar con Excel

# Configuración de la ventana principal
root = tk.Tk()
root.title("Calculadora de Distribución Normal")

# Configuración de estilo para mejorar la estética
style = ttk.Style()
style.configure("TLabel", padding=(5, 2))
style.configure("TButton", padding=(5, 2))
style.configure("TEntry", padding=(5, 2))

# Etiquetas y entradas para los parámetros de la distribución
ttk.Label(root, text="Media (μ):").grid(column=0, row=0, sticky="e", padx=(10, 5), pady=5)
mean_entry = tk.Entry(root)
mean_entry.grid(column=1, row=0, sticky="w", padx=(0, 10), pady=5)

ttk.Label(root, text="Desviación Estándar (σ):").grid(column=0, row=1, sticky="e", padx=(10, 5), pady=5)
std_dev_entry = tk.Entry(root)
std_dev_entry.grid(column=1, row=1, sticky="w", padx=(0, 10), pady=5)

# Opciones de cálculo
options = ["Probabilidad P(X < x)", "Probabilidad P(X > x)", "Probabilidad P(a < X < b)"]
ttk.Label(root, text="Seleccione el tipo de cálculo:").grid(column=0, row=2, sticky="e", padx=(10, 5), pady=5)
calculation_type = ttk.Combobox(root, values=options)
calculation_type.grid(column=1, row=2, sticky="w", padx=(0, 10), pady=5)

# Entradas para valores específicos según el cálculo seleccionado
ttk.Label(root, text="Valor de X o límites (a, b):").grid(column=0, row=3, sticky="e", padx=(10, 5), pady=5)
x_value_entry = tk.Entry(root)
x_value_entry.grid(column=1, row=3, sticky="w", padx=(0, 10), pady=5)

# Etiqueta para mostrar la ruta del archivo cargado
file_path_label = ttk.Label(root, text="")
file_path_label.grid(column=0, row=4, columnspan=2, pady=(5, 10))

# Función para cargar datos desde Excel
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        data = pd.read_excel(file_path)  # Lee el archivo Excel
        column = data.columns[0]  # Usa la primera columna por defecto
        mean = data[column].mean()
        std_dev = data[column].std()

        # Actualiza las entradas con los valores calculados
        mean_entry.delete(0, tk.END)
        mean_entry.insert(0, str(mean))
        std_dev_entry.delete(0, tk.END)
        std_dev_entry.insert(0, str(std_dev))
        
        # Mostrar la ruta del archivo
        file_path_label.config(text=f"Archivo cargado: {file_path}")

# Función para borrar la ruta del archivo
def clear_file_path():
    file_path_label.config(text="")  # Limpia la etiqueta de la ruta del archivo
    mean_entry.delete(0, tk.END)
    std_dev_entry.delete(0, tk.END)
    x_value_entry.delete(0, tk.END)
    calculation_type.set('')
    result_label.config(text="")

# Botón para cargar datos desde Excel
load_button = ttk.Button(root, text="Cargar Datos desde Excel", command=load_data)
load_button.grid(column=0, row=5, sticky="w", padx=(10, 0), pady=5)

# Botón para borrar la ruta del archivo
clear_button = ttk.Button(root, text="Borrar Ruta", command=clear_file_path)
clear_button.grid(column=1, row=5, sticky="w", padx=(0, 10), pady=5)

# Función para ejecutar el cálculo y mostrar resultados
def calculate():
    mean = float(mean_entry.get())
    std_dev = float(std_dev_entry.get())
    calculation = calculation_type.get()
    x_value = x_value_entry.get()
    
    if calculation == "Probabilidad P(X < x)":
        x = float(x_value)
        prob = norm.cdf(x, mean, std_dev)
        result_text = f"P(X < {x}) = {prob:.4f} ({prob:.2%})"
        result_label.config(text=result_text)
        generate_plot(mean, std_dev, x, calculation, prob)
        
    elif calculation == "Probabilidad P(X > x)":
        x = float(x_value)
        prob = 1 - norm.cdf(x, mean, std_dev)
        result_text = f"P(X > {x}) = {prob:.4f} ({prob:.2%})"
        result_label.config(text=result_text)
        generate_plot(mean, std_dev, x, calculation, prob)
        
    elif calculation == "Probabilidad P(a < X < b)":
        a, b = map(float, x_value.split(','))
        prob = norm.cdf(b, mean, std_dev) - norm.cdf(a, mean, std_dev)
        result_text = f"P({a} < X < {b}) = {prob:.4f} ({prob:.2%})"
        result_label.config(text=result_text)
        generate_plot(mean, std_dev, None, calculation, prob, a, b)

# Botón para calcular
calculate_button = ttk.Button(root, text="Calcular", command=calculate)
calculate_button.grid(column=1, row=6, sticky="w", padx=(0, 10), pady=10)

# Etiqueta para mostrar resultados
result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=7, columnspan=2, pady=(10, 5))

# Función para generar la gráfica
def generate_plot(mean, std_dev, x=None, calculation=None, prob=None, a=None, b=None):
    plt.clf()
    x_values = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
    y_values = norm.pdf(x_values, mean, std_dev)
    plt.plot(x_values, y_values, label="Distribución Normal")

    if calculation == "Probabilidad P(X < x)" and x is not None:
        plt.fill_between(x_values, 0, y_values, where=(x_values < x), color='skyblue', alpha=0.5)
        plt.text(x - std_dev/2, max(y_values)/4, f"{prob:.2%}", ha='center', color="black")

    elif calculation == "Probabilidad P(X > x)" and x is not None:
        plt.fill_between(x_values, 0, y_values, where=(x_values > x), color='skyblue', alpha=0.5)
        plt.text(x + std_dev/2, max(y_values)/4, f"{prob:.2%}", ha='center', color="black")

    elif calculation == "Probabilidad P(a < X < b)" and a is not None and b is not None:
        plt.fill_between(x_values, 0, y_values, where=(x_values > a) & (x_values < b), color='skyblue', alpha=0.5)
        plt.text((a + b) / 2, max(y_values)/4, f"{prob:.2%}", ha='center', color="black")

    plt.xlabel("Valores de X")
    plt.ylabel("Densidad de Probabilidad")
    plt.title("Distribución Normal")
    plt.legend()
    plt.show()

# Iniciar la aplicación
root.mainloop()
