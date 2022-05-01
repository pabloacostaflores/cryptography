from tkinter import CENTER, GROOVE, Entry, IntVar, Radiobutton, Tk, Frame, Label, filedialog, Button, TOP, LEFT, messagebox

from main import begin_proc

root = Tk()

global op_mode, file_selected, des_op_mode
op_mode = 0
des_op_mode = 0
mode_sel_var = IntVar()
des_mode_sel_var = IntVar()

root.geometry("900x550")
root.title("Cifrado DES")  # Titulo de la ventana

Tops = Frame(root, width=720, relief=GROOVE)  # Contenedor principal
Tops.pack(side=TOP)

f1 = Frame(root, width=720, height=420,
           relief=GROOVE)
f1.pack(side=LEFT)

# Label de titulo en la ventana
lblInfo = Label(Tops, font=('helvetica', 32, 'bold'),
                text="Practica #1. Cifrado DES", fg="Black", bd=10, anchor=CENTER)
lblInfo.grid(row=0, column=0, columnspan=4)


def handle_user_mode_selection():
    global op_mode
    op_mode = 0
    op_mode = mode_sel_var.get()


def handle_user_des_mode_selection():
    global des_op_mode
    des_op_mode = 0
    des_op_mode = des_mode_sel_var.get()


lblOpMode = Label(Tops, font=("helvetica", 18),
                  text="Selecciona el modo de operación")
lblOpMode.grid(row=1, column=0, columnspan=4, pady=8)

rbCifrar = Radiobutton(Tops, text="Cifrar texto",
                       variable=mode_sel_var, value=0, command=handle_user_mode_selection)
rbCifrar.grid(row=2, column=0, columnspan=4)

rbDescifrar = Radiobutton(Tops, text="Descifrar texto",
                          variable=mode_sel_var, value=1, command=handle_user_mode_selection)
rbDescifrar.grid(row=3, column=0, columnspan=4)

lblOpMode = Label(Tops, font=("helvetica", 18),
                  text="Selecciona el modo de operación del algoritmo DES")
lblOpMode.grid(row=4, column=0, columnspan=4, pady=8)

rbECB = Radiobutton(Tops, text="Modo ECB",
                    variable=des_mode_sel_var, value=0, command=handle_user_des_mode_selection)
rbECB.grid(row=5, column=0)

rbCBC = Radiobutton(Tops, text="Modo CBC",
                    variable=des_mode_sel_var, value=1, command=handle_user_des_mode_selection)
rbCBC.grid(row=5, column=1)

rbCFB = Radiobutton(Tops, text="Modo CFB",
                    variable=des_mode_sel_var, value=2, command=handle_user_des_mode_selection)
rbCFB.grid(row=5, column=2)

rbOFB = Radiobutton(Tops, text="Modo OFB",
                    variable=des_mode_sel_var, value=3, command=handle_user_des_mode_selection)
rbOFB.grid(row=5, column=3)

# Sección de archivo
def open_file():
    file_types = (
        ('All files', '*.*'),
        ('JPG files', '*.jpg'),
        ('JPEG files', '*.jpeg'),
        ('PNG files', '*.png'),
        ('BMP files', '*.bmp')
    )

    # Selector de archivos propio del S.O.
    f = filedialog.askopenfile(filetypes=file_types)

    if f is not None:  # Si hemos seleccionado un archivo
        global file_selected  # Reasignamos los valores de las variables globales
        # Obtenemos el nombre (que en realidad es la ruta completa)
        file_selected = f.name
    else:
        file_selected = None
        # Mostramos una advertencia en el caso de que no se haya seleccionado un archivo
        messagebox.showinfo("Advertencia", "No seleccionó ningun archivo")

lblFileSelect = Label(Tops, font=("helvetica", 18),
                      text="Selecciona el archivo a trabajar")
lblFileSelect.grid(row=6, column=0)

openFileButton = Button(Tops, text="Abrir archivo", command=open_file)
openFileButton.grid(row=6, column=1, padx=12)

lblKey = Label(Tops, text="Introduce la clave", font=("helvetica", 18))
lblKey.grid(row=7, column=0, pady=8)

txtKey = Entry(Tops, font=("helvetica", 12), width=30)
txtKey.grid(row=7, column=1, pady=8)

lblWarn = Label(Tops, text="(16 caracteres)", font=("helvetica", 12), fg="red")
lblWarn.grid(row=7, column=2, pady=8)

lblVect = Label(Tops, text="Introduce el vector de inicializacion",
               font=("helvetica", 18))
lblVect.grid(row=8, column=0, pady=8)

txtVect = Entry(Tops, font=("helvetica", 12), width=30)
txtVect.grid(row=8, column=1, pady=8)

lblWarnVect = Label(Tops, text="(8 caracteres)", font=("helvetica", 12), fg="red")
lblWarnVect.grid(row=8, column=2, pady=8)

def start_cipher():
    key = txtKey.get()
    vi = txtVect.get()

    if key == "" or vi == "" or file_selected == None:
        messagebox.showerror("Error", "La llave, vector de inicializacion y archivo deben de tener un valor")
    elif len(key) != 16 or len(vi) != 8:
        messagebox.showerror(
            "Error", "La llave o vector de inicializacion tiene una longitud incorrecta")
    else:
        if begin_proc(op_mode, des_op_mode, key, vi, file_selected):
            messagebox.showinfo("Success", "Se ha generado el archivo de salida")
        else:
            messagebox.showerror("Error", "Ha ocurrido un error al generar el archivo")

btnStart = Button(Tops, text="Aceptar", command=start_cipher)
btnStart.grid(row=9, column=2)

# keeps window alive
root.mainloop()
