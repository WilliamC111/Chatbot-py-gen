import json
import os
from difflib import get_close_matches
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

def cargar_corpus_desde_archivo(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            corpus_json = json.load(file)
            corpus = {item['pregunta']: item['respuesta'] for item in corpus_json['dialogos']}
            print("Corpus cargado exitosamente.")
            return corpus
    except FileNotFoundError as e:
        print(f"Error: Archivo no encontrado - {e}")
        return None
    except json.JSONDecodeError as e:
        print("Error al decodificar JSON:", str(e))
        return None

def obtener_respuesta(corpus, pregunta_usuario):
    respuesta = corpus.get(pregunta_usuario, "Lo siento, no tengo información sobre eso. ¿Puedes preguntar de otra manera?")
    respuesta = '\n'.join([respuesta[i:i + 70] for i in range(0, len(respuesta), 70)])
    return respuesta

def obtener_respuesta_gui():
    if combo_archivos.get():
        entrada_usuario = entrada_pregunta.get()
        matches = get_close_matches(entrada_usuario, list(corpus.keys()), n=1, cutoff=0.6)
        if matches:
            respuesta = obtener_respuesta(corpus, matches[0])
            respuesta_label.config(text=respuesta)
        else:
            messagebox.showerror("Error", "Lo siento, no tengo información sobre eso.")
    else:
        messagebox.showerror("Error", "Por favor, elija un tema del Combobox.")
      
def seleccionar_archivo(event):
    selected_index = combo_archivos.current()
    file_ids = [
        "chat_vers.json",
        "Procesadores.json",
        "universidad.json",
        "yogurt.json"
    ]
    file_path = os.path.join(files_folder, file_ids[selected_index])
    global corpus
    corpus = cargar_corpus_desde_archivo(file_path)

def cerrar_aplicacion():
    root.destroy()

root = tk.Tk()
root.title("Chatbot")


background_image = "ChatbotW\Fondos\Fondo (1).jpg"

img = Image.open(background_image)
img = img.resize((600, 600))
background_image = ImageTk.PhotoImage(img)

background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

files_folder = "ChatbotW/corpus"

root.geometry("600x600")
root.resizable(False, False)

label_text = tk.Label(root, text="Elige un tema")
label_text.place(relx=0.5, rely=0.16, anchor=tk.CENTER)

file_options = [
    "Chat Versatil",
    "Procesadores",
    "Universidad UPTC",
    "Recetas"
]

combo_archivos = ttk.Combobox(root, values=file_options)
combo_archivos.current(0)  # Selección inicial
combo_archivos.bind('<<ComboboxSelected>>', seleccionar_archivo)
combo_archivos.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

title_label = tk.Label(root, text="Mi MateBot", font=("Arial", 15))
title_label.config(bg="grey", fg="white", width=10)
title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

entrada_pregunta = tk.Entry(root, width=50)
entrada_pregunta.insert(0, "Ingrese una pregunta") 
entrada_pregunta.config(fg='grey')
entrada_pregunta.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

def limpiar_texto(event):
    if entrada_pregunta.get() == "Ingrese una pregunta":
        entrada_pregunta.delete(0, tk.END)
        entrada_pregunta.config(fg='black')



def rellenar_texto(event):
    if not entrada_pregunta.get():
        entrada_pregunta.insert(0, "Ingrese una pregunta")
        entrada_pregunta.config(fg='grey')

entrada_pregunta.bind("<FocusIn>", limpiar_texto)
entrada_pregunta.bind("<FocusOut>", rellenar_texto)

boton_enviar = tk.Button(root, text="Enviar", command=obtener_respuesta_gui)
boton_enviar.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

respuesta_label = tk.Label(root, text="", justify='left', wraplength=580)
respuesta_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

boton_salir = tk.Button(root, text="Salir", command=cerrar_aplicacion)
boton_salir.place(relx=0, rely=0, anchor='nw')

root.mainloop()
