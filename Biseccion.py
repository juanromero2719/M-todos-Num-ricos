import tkinter as tk
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

def metodo_biseccion(funcion, _limite_inferior, _limite_superior, tolerancia):
    try:
        global raices_halladas
        raices_halladas = []

        limite_inferior = float(_limite_inferior)
        limite_superior = float(_limite_superior)
        iteracion = 0
        nuevo_limite = 0
        datos_iteraciones = []

        while True:

            limite_anterior = nuevo_limite
            funcion_evaluada_limite_inferior = eval(funcion, {"np": np, "x": limite_inferior})
            funcion_evaluada_limite_superior = eval(funcion, {"np": np, "x": limite_superior})

            nuevo_limite = (limite_inferior + limite_superior)/ 2.0

            funcion_evaluada_nuevo_limite = eval(funcion, {"np": np, "x": nuevo_limite})
            signo = funcion_evaluada_limite_inferior * funcion_evaluada_nuevo_limite

            if(signo >= 0):
                limite_inferior = nuevo_limite
            else:
                limite_superior = nuevo_limite

            iteracion += 1

            if iteracion > 1:
                error_relativo = abs((nuevo_limite - limite_anterior) / nuevo_limite) * 100
                error_relativo_almacenado = format(error_relativo, ".6f")
                datos_iteraciones.append([iteracion, limite_inferior, limite_superior, nuevo_limite,
                                          funcion_evaluada_limite_inferior, funcion_evaluada_limite_superior,
                                          funcion_evaluada_nuevo_limite, error_relativo_almacenado])
                raices_halladas.append(nuevo_limite)
                if error_relativo < tolerancia:
                    break
            else:
                datos_iteraciones.append([iteracion, limite_inferior, limite_superior, nuevo_limite,
                                          funcion_evaluada_limite_inferior, funcion_evaluada_limite_superior,
                                          funcion_evaluada_nuevo_limite, "N/A"])
                raices_halladas.append(nuevo_limite)

        tabla_iteraciones = tabulate(datos_iteraciones, headers=["Iteración", "Limite Inferior", "Limite Superior", "Nuevo Limite",
                                                                 "Func(Limite Inferior)", "Func(Limite Superior)",
                                                                 "Func(Nuevo Limite)", "Error Relativo"], tablefmt="grid")

        mostrar_resultados(tabla_iteraciones)
        boton_graficar.grid(row=4, column=1, padx=10, pady=10)

    except Exception as e:
        print(f"Error al evaluar la función: {e}")

def mostrar_resultados(tabla_iteraciones):
    resultado_label.config(text=tabla_iteraciones)

def graficar():
    x = np.linspace(float(input_limite_inferior.get()), float(input_limite_superior.get()), 400)
    y = eval(input_funcion.get(), {"np": np, "x": x})

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=input_funcion.get())
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, which='both')

    for i, raiz in enumerate(raices_halladas[:-1]):
        plt.plot(raiz, eval(input_funcion.get(), {"np": np, "x": raiz}), 'bo')

    # Graficar la última raíz con un color diferente
    if raices_halladas:
        ultima_raiz = raices_halladas[-1]
        plt.plot(ultima_raiz, eval(input_funcion.get(), {"np": np, "x": ultima_raiz}), 'ro', label='Última raíz')

    plt.title('Método de Bisección')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.show()

# Creando la ventana
root = tk.Tk()
root.title("Método de Bisección")
root.geometry("1400x800")

# Labels
label_funcion = tk.Label(root, text="Ingrese la función: ")
input_funcion = tk.Entry(root, width=40)
label_tolerancia = tk.Label(root, text="Ingrese la tolerancia: ")
input_tolerancia = tk.Entry(root, width=10)
label_limite_inferior = tk.Label(root, text="Ingrese el limite inferior: ")
input_limite_inferior = tk.Entry(root, width=10)
label_limite_superior = tk.Label(root, text="Ingrese el limite superior: ")
input_limite_superior = tk.Entry(root, width=10)
label_sugerencia = tk.Label(root, text="Para Senos 'np.sin()' Cosenos 'np.cos()' Logaritsmos 'np.log()' Elevar '**' ")
resultado_label = tk.Label(root, text="", justify=tk.LEFT, font=("Courier", 10))


# Botones
boton_evaluar = tk.Button(root, text="Evaluar función", command=lambda: metodo_biseccion(input_funcion.get(), input_limite_inferior.get(), input_limite_superior.get(), float(input_tolerancia.get())))
boton_graficar = tk.Button(root, text="Mostrar Gráfica", command=graficar)

# Grilla
label_funcion.grid(row=0, column=0, padx=10, pady=10)
input_funcion.grid(row=0, column=1, padx=10, pady=10)
label_limite_inferior.grid(row=1, column=0, padx=5, pady=10)
input_limite_inferior.grid(row=1, column=1, padx=5, pady=5)
label_limite_superior.grid(row=1, column=2, padx=5, pady=10)
input_limite_superior.grid(row=1, column=3, padx=5, pady=10)
label_tolerancia.grid(row=0, column=2, padx=10, pady=10)
input_tolerancia.grid(row=0, column=3, padx=10, pady=10)
boton_evaluar.grid(row=2, column=1, padx=10, pady=10)
resultado_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
label_sugerencia.grid(row=2, column=2, padx=10, pady=10)

# Ejecutar el bucle principal para mostrar la ventana
root.mainloop()
