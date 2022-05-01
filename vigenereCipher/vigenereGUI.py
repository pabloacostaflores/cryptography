from cgitb import text
import os
from tkinter import CENTER, END, GROOVE, Entry, IntVar, Radiobutton, Text, Tk, Frame, Label, filedialog,Button, TOP, LEFT, messagebox
from vigenere import cipher_message, uncipher_message

root = Tk()

# Definiciones globales para las variables de modo de operacion y archivo seleccionado
global op_mode, file_selected
op_mode = 0
file_selected = ""

root.geometry("720x720")
root.title("Cifrado Vigenere") # Titulo de la ventana

Tops = Frame(root, width = 720, relief = GROOVE) # Contenedor principal
Tops.pack(side = TOP)

f1 = Frame(root, width = 720, height = 720,
							relief = GROOVE)
f1.pack(side = LEFT)

# Label de titulo en la ventana
lblInfo = Label(Tops, font = ('helvetica', 32, 'bold'), text = "Practica #0. Cifrado Vigenere", fg = "Black", bd = 10, anchor=CENTER)					
lblInfo.grid(row = 0, column = 0, columnspan=3)

## Seccion de configuracion del usuario

# Opcion de texto para el usuario
lblTextToWork = Label(Tops, font = ("helvetica", 18), text="Introduce el texto a trabajar")
lblTextToWork.grid(row=1, column=0)

lblFileSelect = Label(Tops, font=("helvetica", 18), text="Seleccionar un archivo")
lblFileSelect.grid(row=1, column=1, columnspan=2)

txtBoxMessage = Text(Tops, font=("helvetica", 14), height=8, fg="Black", relief=GROOVE, width=42, insertborderwidth=1)
txtBoxMessage.grid(row=2, column=0,pady=12)

# Sección del selector de archivos
def open_file():
	file_types = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

	# Selector de archivos propio del S.O.
	f = filedialog.askopenfile(filetypes=file_types) 

	if f is not None: # Si hemos seleccionado un archivo
		global file_selected # Reasignamos los valores de las variables globales
		file_selected = f.name #Obtenemos el nombre (que en realidad es la ruta completa)
		txtBoxMessage.delete("1.0", END) # Limpiamos la caja de texto del mensaje
		txtBoxMessage.insert("1.0", f.read()) # Insertamos los valores del archivo
	else:
		# Mostramos una advertencia en el caso de que no se haya seleccionado un archivo
		messagebox.showinfo("Advertencia", "No seleccionó ningun archivo") 
		
openFileButton = Button(Tops, text="Abrir archivo", command=open_file)
openFileButton.grid(row=2, column=1, columnspan=2)

# Mensaje de informacion

lblInfoFile = Label(Tops,  font=("helvetica", 12), text="** Al seleccionar un archivo el texto en la caja se reescribirá **", fg="Red")
lblInfoFile.grid(row=3, column=0)

# Selector de modo
# 0 para cifrar, 1 para descifrar
lblOpMode = Label(Tops, font=("helvetica", 18), text="Selecciona el modo de operación")
lblOpMode.grid(row=4, column=0, columnspan=3, pady=8)

def handle_user_selection():
	global op_mode
	op_mode = 0
	op_mode = mode_sel_var.get()

mode_sel_var = IntVar()
rbCifrar = Radiobutton(Tops, text="Cifrar texto", variable=mode_sel_var, value=0, command=handle_user_selection)
rbCifrar.grid(row=5, column=0, columnspan=3)

rbDescifrar = Radiobutton(Tops, text="Descifrar texto",
                       variable=mode_sel_var, value=1, command=handle_user_selection)
rbDescifrar.grid(row=6, column=0, columnspan=3)

lblKey = Label(Tops, text="Introduce la clave", font=("helvetica", 18))
txtKey = Entry(Tops, font=("helvetica", 12), width=30)
lblKey.grid(row=7, column=0, pady=8)
txtKey.grid(row=7, column=1, pady=8)

# Seccion de resultados
lblResult = Label(Tops, text="Resultado", font=("helvetica", 18))
lblResult.grid(row=8, column=0, columnspan=3)

txtResult = Text(Tops, font=("helvetica", 12), width=64, height=12)
txtResult.grid(row=9, column=0, columnspan=3, pady=8)

# Guardar el texto a un archivo
def save_to_file():
	files = [
		('All Files', '*.*'),
        ('Text Document', '*.txt')
	]

 	# Nombre por default del archivo, esto se da cuando el usuario no abrió algun archivo o hizo un intento sin seleccionar el archivo
	save_file_name = "vigenere_prog"

	if file_selected != "": # Si hemos seleccionado un archivo previamente
		file_comps = file_selected.split(os.path.sep)  # Dividimos la ruta del archivo por sus componentes del path
		file_name = file_comps[len(file_comps)-1] #Obtenemos el ultimo valor, que es el nombre + extension
		exact_name = file_name.split(".")[0] # Separamos el nombre de la extensión
		if op_mode == 1:
			exact_name += "_D" # Agregamos D de descifrado
		else:
			exact_name += "_C" # Agregamos C de cifrado

		save_file_name = exact_name # Guardamos este nuevo valor en la variable del nombre del archivo

	# Solicitamos que se cree el archivo con los parametros establecidos, sin embargo, se crea vacio
	file = filedialog.asksaveasfile(filetypes = files, defaultextension = files, initialfile=save_file_name)
	# Escribimos los datos obtenidos de la operacion
	file.write(txtResult.get("1.0", END))
	file.close() # Cerramos el archivo para confirmar la escritura
	

btnSaveToFile = Button(Tops, text="Guardar salida", command=save_to_file)
btnSaveToFile.grid(row=10, column=0)

# Funcion que permite iniciar el proceso de cifrado o descifrado
def start_cipher():
	message_to_op = txtBoxMessage.get("1.0", END) # Obtenemos el valor del mensaje
	key = txtKey.get() # Obtebemos el valor de la llave
	message_to_op = message_to_op.strip() # Limpiamos los espacios en blanco al inicio y final
	key = key.strip()
	if message_to_op == "" or key == "": 
		#Mostramos un error si el mensaje o llave están en blanco
		messagebox.showerror(
			"Error", "Los campos de mensaje y llave no pueden quedar en blanco")
	else:
		if op_mode == 1:  # Descifrar
			msg_plain = uncipher_message(key, message_to_op) # Llamamos a la función auxiliar de descifrado
			txtResult.delete("1.0", END) # Limpiamos la caja de texto del resultado
			txtResult.insert("1.0", msg_plain) # Insertamos el texto obtenido
		else:
			msg_cipher = cipher_message(key, message_to_op) # Llamamos a la funcion auxiliar de cifrado
			txtResult.delete("1.0", END)  # Limpiamos la caja de texto del resultado
			txtResult.insert("1.0", msg_cipher)  # Insertamos el texto obtenido


btnStart = Button(Tops, text="Iniciar", command=start_cipher)
btnStart.grid(row=7, column=2, padx=12, pady=8)

# keeps window alive
root.mainloop()
