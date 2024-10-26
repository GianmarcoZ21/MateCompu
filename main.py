#Modificación
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

global matriz, matrizAux, caminosPreferidos
global flujoMax
global bordesEliminados
global pesoMax

flujoMax = 0
matriz = None
caminosPreferidos = []
bordesEliminados = []
pesoMax = 0

global caminos_izq, caminos_der
caminos_izq = [1, 3, 5, 8, 10, 12, 14]
caminos_der = [2, 4, 6, 9, 11, 13, 15]


def alerta(tipo_alerta):
    global matriz, matrizAux, pesoMax

    if tipo_alerta == 'peso':
        if pesoMax < 7:
            ventana_alerta = Tk()
            ventana_alerta.title("Alerta")
            ventana_alerta.geometry("350x150")

            alerta_label = Label(ventana_alerta, font=("Arial", 12, "bold"), fg="red")
            alerta_label.pack(pady=20)
            alerta_label.config(text="Peso máximo inválido.")
            btn_aceptar = Button(ventana_alerta, text="Aceptar", command=ventana_alerta.destroy)
            btn_aceptar.pack(pady=10)
            ventana_alerta.mainloop()
        else:
            return

    elif tipo_alerta == 'matriz':
        if matriz is None or matrizAux is None:
            ventana_alerta = Tk()
            ventana_alerta.title("Alerta")
            ventana_alerta.geometry("350x150")
            alerta_label = Label(ventana_alerta, font=("Arial", 12, "bold"), fg="red")
            alerta_label.pack(pady=20)
            alerta_label.config(text="No se ha creado la matriz.")
            btn_aceptar = Button(ventana_alerta, text="Aceptar", command=ventana_alerta.destroy)
            btn_aceptar.pack(pady=10)
            ventana_alerta.mainloop()
        else:
            return

def menu():
    ventana_menu = Tk()
    ventana_menu.title("Presentación")
    ventana_menu.geometry("500x500")

    ventana_menu.configure(bg='#ef8383')

    label = Label(ventana_menu, text="Presentación", font=("Arial Black", 25), bg='#ef8383')
    label.pack(pady=20)

    frmP = Frame(ventana_menu, bg='#ef8383')
    frmC = Frame(frmP, bg='#ef8383')

    frmP.pack(padx=10, pady=10)
    frmC.pack(padx=10, pady=10)

    lblUniversidad = Label(frmC, text="Universidad Peruana de Ciencias\nTB1\n\n", font=("Arial", 15, "bold"),
                           bg='#ef8383')
    lblA1 = Label(frmC, text="César Augusto Aróstegui Alzamora - U202114548", font=("Arial", 15), bg='#ef8383')
    lblA2 = Label(frmC, text="Gianmarco Fabian Jiménez Guerra - U202123843", font=("Arial", 15), bg='#ef8383')
    lblA3 = Label(frmC, text="Alessandra Nicole Becerra Tejeda - U202318947", font=("Arial", 15), bg='#ef8383')
    lblA4 = Label(frmC, text="Diego Mateo Collantes Carrillo - U202311823", font=("Arial", 15), bg='#ef8383')
    lblA5 = Label(frmC, text="Stefany Alexandra Peña Castro - U20231D360", font=("Arial", 15), bg='#ef8383')
    lblUniversidad.pack()
    lblA1.pack()
    lblA2.pack()
    lblA3.pack()
    lblA4.pack()
    lblA5.pack()

    ventana_menu.after(3000, lambda: ventana_menu.destroy())
    ventana_menu.mainloop()

# Se limpia la memoria de los valores de matriz, flujoMax, etc
def reiniciarTodo():
    global matriz, matrizAux, flujoMax, caminosPreferidos, bordesEliminados, pesoMax
    matriz = None
    matrizAux = None
    flujoMax = 0
    pesoMax = 0
    caminosPreferidos = []
    bordesEliminados = []

    for widget in root.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()

    tipoMatrizVar.set('')
    tamanioMatrizVar.set(8)

    reiniciar_confirmacion = Toplevel(root)
    reiniciar_confirmacion.geometry("300x150")
    reiniciar_confirmacion.title("Reinicio Completo")
    Label(reiniciar_confirmacion, text="La aplicación ha sido reiniciada.", font=("Arial", 12)).pack(pady=30)
    Button(reiniciar_confirmacion, text="Cerrar", command=reiniciar_confirmacion.destroy).pack(pady=10)


def verMatriz():
    global matrizAux
    alerta('matriz')
    mostrar_Matriz = Toplevel(root)
    mostrar_Matriz.title("Matriz adyacente")
    mostrar_Matriz.geometry("610x400")
    label_matriz = Label(mostrar_Matriz, font=("Courier", 14), justify=LEFT, bg="white", relief="solid")
    label_matriz.pack(padx=20, pady=20)

    matriz_str = "   " + "  ".join([chr(97 + x) for x in range(len(matrizAux))]) + "\n"

    for x in range(len(matrizAux)):
        fila = chr(97 + x) + "  "
        for val in matrizAux[x]:

            if val >= 10:
                fila += str(int(val)) + " "
            else:
                fila += str(int(val)) + "  "

        matriz_str += fila + "\n"

    label_matriz.config(text=matriz_str)
    pass


def reiniciarMatriz():
    global matriz, caminosPreferidos
    matriz = None
    caminosPreferidos = []


def estiloBotones(button):
    button.configure(
        bg='#007BFF',
        fg='white',
        activebackground='#0056b3',
        activeforeground='white',
        font=("Arial", 12, "bold"),
        bd=5,
        relief="raised",
        padx=5,
        pady=5
    )


def estiloCombobox(combobox):
    combobox.configure(
        font=("Arial", 12),
        state="readonly"
    )


# Función que genera una matriz aleatoria con restricciones

def crearMatrizAleatoria(n, probabilidad=0.3):
    global matriz
    global matrizAux
    global caminos_izq
    global caminos_der
    global pesoMax
    reiniciarMatriz()
    matriz = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == 0 and j == 7:
                continue
            if (i in caminos_izq) and (j in caminos_izq):
                continue
            if i == 0 and (j in caminos_der):
                continue
            if (i in caminos_izq) and j == 7:
                continue
            if (i in caminos_der) and (j in caminos_der):
                continue
            if i == 0 and (j in caminos_izq):
                matriz[i][j] = np.random.randint(1, pesoMax - 5)
            if (i in caminos_der) and j == 7:
                matriz[i][j] = np.random.randint(1, pesoMax - 5)
            if (i in caminos_izq) and (j in caminos_der) and (np.random.rand() < 0.8) and np.count_nonzero(
                    matriz[i]) <= 3:
                matriz[i][j] = np.random.randint(3, pesoMax + 1)

    matrizAux = matriz.copy()
    return matriz


def crearMatrizManual(n):
    global matriz
    global matrizAux
    global pesoMax
    reiniciarMatriz()
    matriz = np.zeros((n, n))

    new_window = Toplevel(root)
    new_window.title("Crear Matriz Manual")
    new_window.geometry("1400x900")

    frame = Frame(new_window)
    frame.pack(side=LEFT, padx=10, pady=10)

    for j in range(n):
        label = Label(frame, text=chr(97 + j), font=("Arial", 12, "bold"))
        label.grid(row=0, column=j + 1, padx=5, pady=5)

    for i in range(n):
        label = Label(frame, text=chr(97 + i), font=("Arial", 12, "bold"))
        label.grid(row=i + 1, column=0, padx=5, pady=5)

    widgets = []

    for i in range(n):
        row = []
        for j in range(n):
            #
            if i == j:
                value = "0"
                widget = Entry(frame, width=5, state="disabled", bg="#ffcccc")
                widget.insert(0, value)
            elif i == 0 and j == 7:
                value = "0"
                widget = Entry(frame, width=5, state="disabled", bg="#ffcccc")
                widget.insert(0, value)
            elif (i in caminos_izq) and (j in caminos_izq):
                value = "0"
                widget = Entry(frame, width=5, state="disabled", bg="#ffcccc")
                widget.insert(0, value)
            elif i == 0 and (j in caminos_der):
                value = "0"
                widget = Entry(frame, width=5, state="disabled", bg="#ffcccc")
                widget.insert(0, value)
            elif (i in caminos_izq) and j == 7:
                value = "0"
                widget = Entry(frame, width=5, state="disabled", bg="#ffcccc")
                widget.insert(0, value)
            elif (i in caminos_der) and (j in caminos_der):
                value = "0"
                widget = Entry(frame, width=5, state="disabled", bg="#ffcccc")
                widget.insert(0, value)
            elif j == 0:
                value = "0"
                widget = Entry(frame, width=5, state="disabled", bg="#ffcccc")
                widget.insert(0, value)
            elif i == 7:
                value = "0"
                widget = Entry(frame, width=5, state="disabled", bg="#ffcccc")
                widget.insert(0, value)
            elif (i in caminos_izq) and (j in caminos_der):
                valores = [str(x) for x in range(pesoMax + 1)]
                widget = ttk.Combobox(frame, values=valores, width=5, state="readonly")
                widget.current(0)
                widget.configure(background="white")

            else:
                valores = [str(x) for x in range(pesoMax + 1)]
                widget = ttk.Combobox(frame, values=valores, width=5, state="readonly")
                widget.current(0)
                widget.configure(background="white")

            widget.grid(row=i + 1, column=j + 1, padx=5, pady=5)
            row.append(widget)
        widgets.append(row)

    graph_frame = Frame(new_window)
    graph_frame.pack(side=RIGHT, padx=10, pady=10)

    def actualizar_grafo():
        nonlocal graph_frame
        for widget in graph_frame.winfo_children():
            widget.destroy()

        G = nx.DiGraph()
        for i in range(n):
            for j in range(n):
                if matriz[i][j] > 0:
                    G.add_edge(chr(97 + i), chr(97 + j), weight=matriz[i][j])

        fig, ax = plt.subplots(figsize=(5, 5))
        pos = {
            'a': (-4, 4),
            'b': (2, 10),
            'c': (6, 10),
            'd': (2, 6),
            'e': (6, 6),
            'f': (2, 2),
            'g': (6, 2),
            'h': (10, 4),
            'i': (2, -2),
            'j': (6, -2),
            'k': (2, -6),
            'l': (6, -6),
            'm': (2, -10),
            'n': (6, -10),
            'o': (2, -14),
            'p': (6, -14),
        }
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='orange', font_size=10, ax=ax)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def guardar_valores():
        global matriz, matrizAux
        for i in range(n):
            for j in range(n):
                widget = widgets[i][j]
                if isinstance(widget, ttk.Combobox):
                    valor = widget.get()
                    matriz[i][j] = int(valor) if valor.isdigit() else 0
                else:
                    matriz[i][j] = 0

        matrizAux = matriz.copy()
        actualizar_grafo()

    button_done = Button(new_window, text="Guardar", command=guardar_valores, bg='#007BFF', fg='white', font=("Arial", 12, "bold"), width=25)
    button_done.pack(pady=10)

    return matriz


def crearMatriz():
    global matriz
    global flujoMax
    global bordesEliminados, pesoMax

    n = int(tamanioMatrizVar.get())
    tipo = tipoMatrizVar.get()

    if pesoMax<7:
        alerta('peso')
        return
    if tipo == 'a':
        matriz = crearMatrizAleatoria(n)
    elif tipo == 'm':
        matriz = crearMatrizManual(n)
    else:
        alerta('matriz')


def grafoMatrizInicial(n):
    global matrizAux
    edgesL = []
    dicV = {i: chr(97 + i) for i in range(n)}

    for i in range(n):
        for j in range(n):
            if matrizAux[i][j] != 0:
                edgesL.append((dicV[i], dicV[j], matrizAux[i][j]))
    return edgesL, dicV


def grafoMatriz(n):
    global matriz
    edgesL = []
    dicV = {i: chr(97 + i) for i in range(n)}

    for i in range(n):
        for j in range(n):
            if matriz[i][j] != 0:
                edgesL.append((dicV[i], dicV[j], matriz[i][j]))
    return edgesL, dicV


def verGrafoInicial():
    global matrizAux
    alerta('matriz')

    n = len(matrizAux)
    new_window = Toplevel(root)
    new_window.title("Visualización del Grafo")
    new_window.geometry("1000x1000")

    bordes, dicV = grafoMatrizInicial(n)

    G = nx.DiGraph()
    G.add_weighted_edges_from(bordes)

    fig, ax = plt.subplots(figsize=(5, 5))

    pos = {
        'a': (-4, 4),
        'b': (2, 10),
        'c': (6, 10),
        'd': (2, 6),
        'e': (6, 6),
        'f': (2, 2),
        'g': (6, 2),
        'h': (10, 4),
        'i': (2, -2),
        'j': (6, -2),
        'k': (2, -6),
        'l': (6, -6),
        'm': (2, -10),
        'n': (6, -10),
        'o': (2, -14),
        'p': (6, -14),
    }

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='orange', font_size=10, font_weight='bold', ax=ax)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)


def verGrafo():
    global matriz, bordesEliminados, flujoMax
    alerta('matriz')

    n = len(matriz)
    new_window = Toplevel(root)
    new_window.title("Visualización del Grafo")
    new_window.geometry("1000x1000")
    labelFlujoMax = Label(new_window, text=f"Flujo Máximo: |f| = {flujoMax}",
                          font=("Arial", 14))
    labelFlujoMax.pack(pady=20)

    bordes, dicV = grafoMatriz(n)

    G = nx.DiGraph()
    G.add_nodes_from(dicV.values())
    G.add_weighted_edges_from(bordes)

    fig, ax = plt.subplots(figsize=(5, 5))

    pos = {
        'a': (-4, 4),
        'b': (2, 10),
        'c': (6, 10),
        'd': (2, 6),
        'e': (6, 6),
        'f': (2, 2),
        'g': (6, 2),
        'h': (10, 4),
        'i': (2, -2),
        'j': (6, -2),
        'k': (2, -6),
        'l': (6, -6),
        'm': (2, -10),
        'n': (6, -10),
        'o': (2, -14),
        'p': (6, -14),
    }

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='orange', font_size=10, font_weight='bold', ax=ax)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

    nx.draw_networkx_edges(G, pos, edgelist=bordesEliminados, edge_color='blue', width=2, style='dashed', ax=ax)

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)


class VisualizarGrafo:
    def __init__(self, root, paths, current_index=0):
        self.root = root
        self.root.geometry("900x1000")
        self.paths = paths
        self.current_index = current_index

        self.label = Label(root,
                           text=f"Mostrando el Camino {current_index + 1}: {' -> '.join(self.paths[self.current_index])}",
                           font=("Arial", 14, "bold"))
        self.label.pack(pady=20)

        self.restriction_button = Button(root, text="Aplicar restricción de pesos",
                                         command=self.aplicarRestriccionPeso,
                                         bg='#007BFF',
                                         fg='white',
                                         font=("Arial", 12, "bold"))

        self.restriction_button.pack(pady=20)

        self.next_button = Button(root, text="Siguiente", command=self.siguientePaso,
                                  bg='#a1de3c',
                                  fg='black',
                                  font=("Arial", 12, "bold"))
        self.next_button.pack(pady=20)

        self.matriz_button = Button(root, text="Ver Matriz", command=self.verMatriz,
                                    bg='#3cbede',
                                    fg='black',
                                    font=("Arial", 12, "bold"))
        self.matriz_button.pack(pady=20)

        self.canvas = None
        self.dibujarGrafo(self.paths[self.current_index])

    def verMatriz(self):
        global matriz
        if matrizAux is None:
            alerta('matriz')
            return

        new_window = Toplevel()
        new_window.title("Matriz Actual")
        new_window.geometry("610x600")

        label_matriz = Label(new_window, font=("Courier", 12), justify=LEFT, bg="white", relief="solid")
        label_matriz.pack(padx=20, pady=20)

        matriz_str = "   " + "  ".join([chr(97 + x) for x in range(len(matriz))]) + "\n"

        for x in range(len(matriz)):
            fila = chr(97 + x) + "  "
            for val in matriz[x]:
                if val >= 10:
                    fila += str(int(val)) + " "
                else:
                    fila += str(int(val)) + "  "
            matriz_str += fila + "\n"

        label_matriz.config(text=matriz_str)

    def dibujarGrafo(self, path):
        global matriz, bordesEliminados, pesoMax
        bordes, dicV = grafoMatriz(len(matriz))

        G = nx.DiGraph()
        G.add_nodes_from(dicV.values())
        G.add_weighted_edges_from(bordes)

        pos = {
            'a': (-4, 4),
            'b': (2, 10),
            'c': (6, 10),
            'd': (2, 6),
            'e': (6, 6),
            'f': (2, 2),
            'g': (6, 2),
            'h': (10, 4),
            'i': (2, -2),
            'j': (6, -2),
            'k': (2, -6),
            'l': (6, -6),
            'm': (2, -10),
            'n': (6, -10),
            'o': (2, -14),
            'p': (6, -14),
        }

        flujo_por_nodo = {}

        for i in range(1, len(path)):
            anterior = path[i - 1]
            actual = path[i]
            flujo = matriz[ord(anterior) - 97][ord(actual) - 97]
            flujo_por_nodo[actual] = (anterior, flujo)

        fig, ax = plt.subplots(figsize=(16, 16))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='orange', font_size=10, font_weight='bold', ax=ax)

        labels = nx.get_edge_attributes(G, 'weight')

        edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=3, ax=ax, arrows=True,
                               arrowsize=20)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=10)

        nx.draw_networkx_edges(G, pos, edgelist=bordesEliminados, edge_color='blue', width=2, style='dashed', ax=ax)

        pesoMinCamino = pesoMax + 1
        etiquetas_personalizadas = {}
        etiquetas_personalizadas[path[0]] = "(-, ∞)"
        for nodo in path[1:]:
            if nodo in flujo_por_nodo:
                anterior, flujo = flujo_por_nodo[nodo]
                pesoMinCamino = min(pesoMinCamino, flujo)
                etiquetas_personalizadas[nodo] = f"({anterior}+,{pesoMinCamino})"

        pos_labels = {nodo: (x, y + 1) for nodo, (x, y) in pos.items()}
        nx.draw_networkx_labels(G, pos_labels, labels=etiquetas_personalizadas, font_size=12, font_color='#551dde',
                                ax=ax, font_weight="bold")

        x_values, y_values = zip(*pos.values())
        ax.set_xlim([min(x_values) - 1, max(x_values) + 1])
        ax.set_ylim([min(y_values) - 2, max(y_values) + 2])

        if self.canvas is not None:
            self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def aplicarRestriccionPeso(self):
        global matriz, flujoMax, bordesEliminados
        path = self.paths[self.current_index]

        min_weight = min([matriz[ord(path[i]) - 97][ord(path[i + 1]) - 97] for i in range(len(path) - 1)])
        if (min_weight > 0):
            flujoMax += min_weight
        for i in range(len(path) - 1):
            nodo_origen = ord(path[i]) - 97
            nodo_destino = ord(path[i + 1]) - 97
            matriz[nodo_origen][nodo_destino] -= min_weight

            if matriz[nodo_origen][nodo_destino] == 0:
                bordesEliminados.append((path[i], path[i + 1]))

        peso_min_root = Tk()
        peso_min_root.geometry("600x200")

        labelPesoMin = Label(peso_min_root, text=f"Peso mínimo encontrado: {min_weight}",
                             font=("Arial", 14))
        labelCamino = Label(peso_min_root, text=f"Camino {self.current_index + 1} actualizado: {' -> '.join(path)}",
                            font=("Arial", 14, "bold"))
        labelPesoMin.pack(pady=20)
        labelCamino.pack(pady=20)

        peso_min_root.mainloop()

    def siguientePaso(self):
        global matriz, caminosPreferidos, flujoMax

        self.root.destroy()

        bordes, dicV = grafoMatriz(len(matriz))
        G = nx.DiGraph()
        G.add_nodes_from(dicV.values())
        G.add_weighted_edges_from(bordes)
        try:
            caminosPreferidos = list(nx.all_simple_paths(G, source='a', target='h'))
        except nx.NodeNotFound as e:
            print(f"Error: {e}")
            return
        if len(caminosPreferidos) > 0 and self.current_index < len(caminosPreferidos):
            new_root = Tk()
            VisualizarGrafo(new_root, caminosPreferidos, self.current_index)
            new_root.mainloop()

            self.current_index += 1
        elif len(caminosPreferidos) == 0:
            flujo_máximo_root = Tk()
            flujo_máximo_root.geometry("500x200")

            labelFlujo = Label(flujo_máximo_root,
                               text=f"Todos los caminos han sido mostrados\nFlujo máximo: | f | = {flujoMax}",
                               font=("Arial", 14, "bold"))
            labelFlujo.pack(pady=20)

            flujo_máximo_root.mainloop()


def mostrarCaminos():
    global matriz, caminosPreferidos
    alerta('matriz')

    n = len(matriz)
    bordes, dicV = grafoMatriz(n)

    G = nx.DiGraph()
    G.add_weighted_edges_from(bordes)

    caminosPreferidos = list(nx.all_simple_paths(G, source='a', target='h'))

    if caminosPreferidos:
        root = Tk()
        VisualizarGrafo(root, caminosPreferidos)
        root.mainloop()
    else:
        print("No hay caminos posibles entre 'a' y 'h'.")


def elegirPesoMax():
    global pesoMax
    ventana_peso = Tk()
    ventana_peso.title("Selección de Peso máximo")
    ventana_peso.geometry("650x250")

    label = Label(ventana_peso, text="Elegir un entero mayor o igual que 7 para el peso máximo: ", font=("Arial Black", 14))
    label.pack(pady=20)

    peso_entry = Entry(ventana_peso, font=("Arial", 12))
    peso_entry.pack(pady=10)
    peso_label = Label(ventana_peso)

    def confirmarPeso():
        global pesoMax
        try:
            pesoMax = int(peso_entry.get())
            if(pesoMax<7):
                peso_label.config(text=f"El valor del peso debe ser mayor o igual que 7", font=("Arial", 12), fg="red")
            else:
                peso_label.config(text=f"El valor de su peso máximo es {pesoMax}", font=("Arial", 12), fg="blue")
        except ValueError:
            peso_label.config(text="Por favor, ingrese un número entero válido.", font=("Arial", 12), fg="red")
            pesoMax=0

        peso_label.pack(pady=10)

    confirmar_peso = Button(ventana_peso, text="Confirmar", command=confirmarPeso, bg='#007BFF', fg='white',
                           font=("Arial", 12, "bold"))
    confirmar_peso.pack(pady=20)


# Ventana principal
menu()
root = Tk()
root.title("Problema del Flujo Máximo")
root.geometry("800x700")
root.configure(bg='#d1f497')

tamanioMatrizVar = IntVar()
tipoMatrizVar = StringVar()

titulo_principal = Label(root, text="Problema del flujo máximo", font=("Arial Black", 25), bg='#d1f497')
titulo_principal.pack(pady=10)

frmP = Frame(root, bg='#d1f497')
frmC = Frame(frmP, bg='#d1f497')
frmP.pack(padx=10, pady=10)
frmC.pack(padx=10, pady=10)

lblTamanioMatriz = Label(frmC, text="Seleccione el tamaño de la matriz (entre 8 y 16):", bg='#d1f497',
                         font=("Arial", 12))
lblTipoMatriz = Label(frmC, text="¿Cómo desea generar la matriz?", bg='#d1f497', font=("Arial", 12))

cboTamanioMatriz = ttk.Combobox(frmC, textvariable=tamanioMatrizVar, values=[i for i in range(8, 17)], state="readonly")
cboTamanioMatriz.current(0)
estiloCombobox(cboTamanioMatriz)

rbAleatorio = Radiobutton(frmC, text="Aleatorio", variable=tipoMatrizVar, value="a", bg='#d1f497', font=("Arial", 12))
rbManual = Radiobutton(frmC, text="Manual", variable=tipoMatrizVar, value="m", bg='#d1f497', font=("Arial", 12))

btnElegirPesoMax = Button(frmC, text="Elegir peso máximo", command=elegirPesoMax)
btnCrearMatriz = Button(frmC, text="Crear Matriz", command=crearMatriz)
btnVerGrafoInicial = Button(frmC, text="Ver Grafo Inicial", command=verGrafoInicial)
btnVerGrafo = Button(frmC, text="Ver Grafo Final", command=verGrafo)
btnVerMatriz = Button(frmC, text="Ver Matriz", command=verMatriz)
btnCaminosPosibles = Button(frmC, text="Ver Caminos Posibles", command=mostrarCaminos)
btnReiniciarTodo = Button(frmC, text="Reiniciar Todo", command=reiniciarTodo)

estiloBotones(btnElegirPesoMax)
estiloBotones(btnReiniciarTodo)
estiloBotones(btnVerMatriz)
estiloBotones(btnCrearMatriz)
estiloBotones(btnVerGrafoInicial)
estiloBotones(btnVerGrafo)
estiloBotones(btnCaminosPosibles)

btnReiniciarTodo.configure(bg='#a24912')

lblTamanioMatriz.grid(row=3, column=1, padx=5, pady=5, sticky=W)
lblTipoMatriz.grid(row=4, column=1, padx=5, pady=5, sticky=W)

cboTamanioMatriz.grid(row=3, column=2, padx=5, pady=5, sticky=W)

rbAleatorio.grid(row=5, column=1, padx=5, pady=5, sticky=W)
rbManual.grid(row=5, column=2, padx=5, pady=5, sticky=W)

btnElegirPesoMax.grid(row=6, column=1, padx=5, pady=5, sticky=W)
btnCrearMatriz.grid(row=7, column=1, padx=5, pady=5, sticky=W)
btnVerMatriz.grid(row=7, column=2, padx=5, pady=5, sticky=W)
btnVerGrafoInicial.grid(row=8, column=1, padx=5, pady=5, sticky=W)
btnVerGrafo.grid(row=9, column=1, padx=5, pady=5, sticky=W)
btnCaminosPosibles.grid(row=8, column=2, padx=5, pady=5, sticky=W)
btnReiniciarTodo.grid(row=9, column=2, padx=5, pady=5, sticky=W)

root.mainloop()
