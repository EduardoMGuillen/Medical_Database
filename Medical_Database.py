import tkinter
from tkinter import *
import datetime
from tkinter import messagebox, ttk
import sqlite3


def selection():
    selected_item = tree.focus()
    details = tree.item(selected_item)
    idx = details.get('values')[0]
    nombre = details.get('values')[1]
    edad = details.get('values')[2]
    peso = details.get('values')[3]
    presion = details.get('values')[4]
    sintomas = details.get('values')[5]
    receta = details.get('values')[6]
    telefono = details.get('values')[7]
    fecha = details.get('values')[8]
    hora = details.get('values')[9]
    motivo = details.get('values')[10]
    diagnosis = details.get('values')[11]

    entry_summary.configure(state='normal')
    entry_summary.delete(0.1, END)
    entry_summary.insert(END, f'-' * 89 + '\n')
    entry_summary.insert(END, f'Identificador en base de datos: {idx}\nFecha: {fecha}\nHora: {hora}\n')
    entry_summary.insert(END, f'-' * 89 + '\n')
    entry_summary.insert(END, f'Datos del paciente\n')
    entry_summary.insert(END, f'Nombre del paciente: {nombre}\n')
    entry_summary.insert(END, f'Numero de telefono: {telefono}\n')
    entry_summary.insert(END, f'Edad: {edad}\n')
    entry_summary.insert(END, f'Peso: {peso}\n')
    entry_summary.insert(END, f'Presion Arterial: {presion}\n')
    entry_summary.insert(END, f'-' * 89 + '\n')
    entry_summary.insert(END, f'Motivo de consulta: \t{motivo}\n\n')
    entry_summary.insert(END, f'Historial Clinico: \t{sintomas}\n\n')
    entry_summary.insert(END, f'Diagnostico: \t{diagnosis}\n\n')
    entry_summary.insert(END, f'Tratamiento:\t{receta}\n\n')
    entry_summary.insert(END, f'-' * 89 + '\n')
    entry_summary.configure(state='disabled')


def add():
    date = datetime.datetime.now()
    if int(date.minute) < 10:
        timex = f'{date.hour}:0{date.minute}'
    else:
        timex = f'{date.hour}:{date.minute}'

    name = f'\t{entry_name.get(1.0, END)}'.replace("\t", '')
    phone = f'\t{entry_phone.get(1.0, END)}'.replace("\t", '')
    simptoms = f'\t{entry_simptoms.get(1.0, END)}'.replace("\t", '')
    weight = f'\t{entry_weight.get(1.0, END)}'.replace("\t", '')
    preasure = f'\t{entry_preasure.get(1.0, END)}'.replace("\t", '')
    age = f'\t{entry_age.get(1.0, END)}'.replace("\t", '')
    recipe = f'\t{entry_recipe.get(1.0, END)}'.replace("\t", '')
    datex = f'\t{date.day}/{date.month}/{date.year}'.replace("\t", '')
    timey = timex.replace("\t", '')
    motive = f'\t{entry_motive.get(1.0, END)}'.replace("\t", '')
    diagnosis = f'\t{entry_diagnosis.get(1.0, END)}'.replace("\t", '')
    clean()

    # Create Database
    conn = sqlite3.connect('medical_db.db')

    # Create Cursos
    c = conn.cursor()

    # Insert into table
    if len(name) <= 1:
        messagebox.showinfo('Informacion', 'ERROR: Casilla de Nombre vacia')
    else:
        c.execute(
            "INSERT INTO CITAS(Nombre,Edad,Peso,Presion,Sintomas,Receta,Telefono,Fecha,Hora,Motivo,Diagnosis) VALUES "
            "(?,?,?,?,?,?,?,?,?,?,?)",
            (name.replace('\n', '').replace('\t', ''), age.replace('\n', '').replace('\t', ''),
             weight.replace('\n', '').replace('\t', ''), preasure.replace('\n', '').replace('\t', ''),
             simptoms.replace('\t', ''), recipe.replace('\t', ''),
             phone.replace('\n', '').replace('\t', ''), datex.replace('\n', '').replace('\t', ''),
             timey.replace('\n', '').replace('\t', ''), motive.replace('\t', ''), diagnosis.replace('\t', '')))
        messagebox.showinfo('Informacion', 'El paciente se ha anadido a la base de datos')
    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()

    # Update view
    app.update()


def view():
    for i in tree.get_children():
        tree.delete(i)
    # Create Database
    conn = sqlite3.connect('medical_db.db')

    # Create Cursos
    c = conn.cursor()

    # Qery the database
    c.execute("SELECT * FROM CITAS ORDER BY id DESC LIMIT 100")
    records = c.fetchall()

    tree.tag_configure('even', background='white')
    tree.tag_configure('odd', background='lightblue')

    count = 0

    # Loop through results
    for record in records:
        if count % 2 == 0:
            my_tag = 'even'
            tree.insert("", END, values=record, tags=my_tag)
        else:
            my_tag = 'odd'
            tree.insert("", END, values=record, tags=my_tag)
        count += 1
    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()

    # Update view
    app.update()


def search():
    for i in tree.get_children():
        tree.delete(i)
    # Create Database
    conn = sqlite3.connect('medical_db.db')

    # Create Cursos
    c = conn.cursor()

    # Key word
    search_name = f'\t{entry_search.get(1.0, END)}'.replace("\t", '').replace('\n', '')

    # Qery the database
    c.execute("SELECT * FROM CITAS WHERE Nombre like ? ORDER BY id DESC LIMIT 100", ("%" + search_name + "%",))
    records = c.fetchall()

    count = 0
    # Loop through results
    for record in records:
        if count % 2 == 0:
            my_tag = 'even'
            tree.insert("", END, values=record, tags=my_tag)
        else:
            my_tag = 'odd'
            tree.insert("", END, values=record, tags=my_tag)
        count += 1

    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()

    # Update view
    app.update()

    entry_search.delete(0.1, END)


def delete_entry():
    # Create Database
    conn = sqlite3.connect('medical_db.db')

    # Create Cursos
    c = conn.cursor()

    # Delete a record
    idx = f'\t{entry_delete.get(1.0, END)}'.replace("\t", '').replace('\n', '')

    if idx == '':
        messagebox.showinfo('Informacion', f'ERROR: No se ha introducido numero de ID')
    else:
        c.execute("DELETE from CITAS WHERE ID=?", (idx,))
        messagebox.showinfo('Informacion', f'Se ha eliminado el paciente {idx} de la base de datos')

    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()

    # Update view
    app.update()

    # Clean Text Box
    entry_delete.delete(0.1, END)


def clean():
    entry_name.delete(0.1, END)
    entry_age.delete(0.1, END)
    entry_weight.delete(0.1, END)
    entry_preasure.delete(0.1, END)
    entry_simptoms.delete(0.1, END)
    entry_recipe.delete(0.1, END)
    entry_phone.delete(0.1, END)
    entry_search.delete(0.1, END)
    entry_delete.delete(0.1, END)
    entry_diagnosis.delete(0.1, END)
    entry_motive.delete(0.1, END)
    entry_summary.configure(state='normal')
    entry_summary.delete(0.1, END)
    entry_summary.configure(state='disabled')

    app.update()


# Create Database
conn = sqlite3.connect('medical_db.db')

# Create Cursos
c = conn.cursor()

# Create Table
c.execute(""" CREATE TABLE  IF NOT EXISTS CITAS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre text,
            Edad text,
            Peso text,
            Presion text,
            Sintomas text,
            Receta text,
            Telefono text,
            Fecha text,
            Hora text,
            Motivo text,
            diagnosis text
        ) """)

# Commit Changes
conn.commit()

# Close Connection
conn.close()

# Run tkinter
app = Tk()
style = ttk.Style()

# Window Size
app.geometry("1920x1080+0+0")

# Fixed size
# app.resizable(0, 0)

# Window Title
app.title("Guiro IT Service - Base de datos")
# app.attributes("-transparentcolor", "red")

# Add image file
bg = PhotoImage(file="Medical_bg.png")

# Create Canvas
canvas1 = Canvas(app, width=1920, height=1080)
canvas1.pack(fill="both", expand=True)

canvas1.create_image(0, 0, image=bg, anchor=NW)

# Create Buttons
reset = Button(app, text="Limpiar", width=20, height=1, command=clean, borderwidth=1, font=('Dosis', 10, 'bold'))
add_db = Button(app, text="Anadir", width=20, height=1, command=add, borderwidth=1, font=('Dosis', 10, 'bold'))
refresh_db = Button(app, text="Refrescar", width=20, height=1, command=view, borderwidth=1, font=('Dosis', 10, 'bold'))
delete_from_db = Button(app, text="Eliminar", width=20, height=1, command=delete_entry, borderwidth=1,
                        font=('Dosis', 10, 'bold'))
search_db = Button(app, text="Buscar", width=20, height=1, command=search, borderwidth=1, font=('Dosis', 10, 'bold'))
get_selection = Button(app, text="Cargar Cita", width=20, height=1, command=selection, borderwidth=1,
                       font=('Dosis', 10, 'bold'))

# Add Text
canvas1.create_text(270, 30, text="Datos del Paciente", font=('Dosis', 20, 'bold'))
canvas1.create_text(270, 215 - 150, text="Nombre", font=('Dosis', 10, 'bold'))
canvas1.create_text(125, 300 - 180, text="Edad", font=('Dosis', 10, 'bold'))
canvas1.create_text(270, 300 - 180, text="Peso", font=('Dosis', 10, 'bold'))
canvas1.create_text(415, 300 - 180, text="Presion Arterial", font=('Dosis', 10, 'bold'))
canvas1.create_text(270, 370 - 190, text="Motivo de consulta", font=('Dosis', 10, 'bold'))
canvas1.create_text(270, 370 - 140, text="Historia Clinica", font=('Dosis', 10, 'bold'))
canvas1.create_text(270, 370 - 70, text="Diagnostico", font=('Dosis', 10, 'bold'))
canvas1.create_text(270, 485 - 115, text="Tratamiento", font=('Dosis', 10, 'bold'))
canvas1.create_text(270, 575 - 130, text="Numero de Telefono", font=('Dosis', 10, 'bold'))

# Create Table
style.theme_use('default')
style.configure("Treeview", bg="#BFF9EB", foreground="black", rowheigth=25, fieldbackground="F1FFFC")
style.map("Treeview", background=[('selected', "#347083")])
style.configure('Treeview', rowheight=22)

tree = ttk.Treeview(app,
                    columns=(
                        "ID", "Nombre", "Edad", "Peso", "Presion Arterial", "Sintomas", "Tratamiento",
                        "Numero de Telefono",
                        "Fecha", "hora"), show="headings", selectmode=tkinter.BROWSE)
# tree.tag_configure(alternating_row_color='#97FFFF')
tree.tag_configure("even", background='#BFF9EB')
tree.bind('<Motion>', 'break')

tree.column("#1", anchor=tkinter.CENTER, minwidth=0, width=75)
tree.heading("#1", text="ID")

tree.column("#2", anchor=tkinter.CENTER, minwidth=0, width=200)
tree.heading("#2", text="Nombre")

tree.column("#3", anchor=tkinter.CENTER, minwidth=0, width=100)
tree.heading("#3", text="Edad")

tree.column("#4", anchor=tkinter.CENTER, minwidth=0, width=100)
tree.heading("#4", text="Peso")

tree.column("#5", anchor=tkinter.CENTER, minwidth=0, width=100)
tree.heading("#5", text="Presion Arterial")

tree.column("#6", anchor=tkinter.CENTER, minwidth=0, width=200)
tree.heading("#6", text="Motivo de consulta")

tree.column("#7", anchor=tkinter.CENTER, minwidth=0, width=200)
tree.heading("#7", text="Tratamiento")

tree.column("#8", anchor=tkinter.CENTER, minwidth=0, width=150)
tree.heading("#8", text="Numero de Telefono")

tree.column("#9", anchor=tkinter.CENTER, minwidth=0, width=100)
tree.heading("#9", text="Fecha")

tree.column("#10", anchor=tkinter.CENTER, minwidth=0, width=100)
tree.heading("#10", text="Hora")

sb = ttk.Scrollbar(app, orient="vertical", command=tree.yview)
canvas1.create_window(1870, 500, window=sb, height=900)

tree.pack()
canvas1.create_window(1200, 500, window=tree, height=900)

# Create an input on canvas
entry_name = Text(app, width=40, height=1, font=('Dosis', 12))
canvas1.create_window(270, 240 - 150, window=entry_name)

entry_age = Text(app, width=7, height=1, font=('Dosis', 12))
canvas1.create_window(125, 325 - 180, window=entry_age)

entry_weight = Text(app, width=7, height=1, font=('Dosis', 12))
canvas1.create_window(270, 325 - 180, window=entry_weight)

entry_preasure = Text(app, width=7, height=1, font=('Dosis', 12))
canvas1.create_window(415, 325 - 180, window=entry_preasure)

entry_motive = Text(app, width=50, height=1, font=('Dosis', 12))
canvas1.create_window(270, 425 - 220, window=entry_motive)

entry_simptoms = Text(app, width=50, height=2, font=('Dosis', 12))
canvas1.create_window(270, 425 - 160, window=entry_simptoms)

entry_diagnosis = Text(app, width=50, height=2, font=('Dosis', 12))
canvas1.create_window(270, 425 - 90, window=entry_diagnosis)

entry_recipe = Text(app, width=50, height=2, font=('Dosis', 12))
canvas1.create_window(270, 525 - 120, window=entry_recipe)

entry_phone = Text(app, width=20, height=1, font=('Dosis', 12))
canvas1.create_window(270, 600 - 130, window=entry_phone)

entry_search = Text(app, width=30, height=1, borderwidth=1, font=('Dosis', 12))
canvas1.create_window(1555, 30, window=entry_search)

entry_delete = Text(app, width=6, height=1, borderwidth=1, font=('Dosis', 12))
canvas1.create_window(1665, 970, window=entry_delete)

entry_summary = Text(app, width=50, height=22, borderwidth=1, font=('Dosis', 12), state='disabled')
canvas1.create_window(270, 750, window=entry_summary)

# Display Buttons
button1_canvas = canvas1.create_window(170, 725 - 210,
                                       window=add_db)

button2_canvas = canvas1.create_window(625, 30,
                                       window=refresh_db)

button3_canvas = canvas1.create_window(370, 725 - 210,
                                       window=reset)

button4_canvas = canvas1.create_window(1790, 970,
                                       window=delete_from_db)

button5_canvas = canvas1.create_window(1790, 30,
                                       window=search_db)

button6_canvas = canvas1.create_window(800, 30,
                                       window=get_selection)
# Keep Window Open
app.mainloop()
