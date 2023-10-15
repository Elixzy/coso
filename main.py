import tkinter
from tkinter import Tk, Frame, Button, Label, ttk, StringVar
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#creacion del espacio 3d
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111, projection='3d')

window=Tk()
window.geometry("895x720")
window.wm_title("Fuerzas entre cargas")
window.minsize(width=895, height=720)
window.resizable(0,0)
frame = Frame(window, bg="gray22", bd=3)
frame.grid(column=0, row=0)

#seleccion de rango de unidades
combo = ttk.Combobox(frame, width=13, font=("Bahnschrift", 11),state="readonly",values=["C", "mC", "uC", "pC"])
combo.grid(column=0, row=3, pady=3)
combo.current(0)
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(column=0, row=0, columnspan=5, padx=5, pady=5)
carga = Label(frame, width=15, bg="gray22", text="CARGA", fg="white", font=("Bahnschrift", 11))
carga.grid(column=0, row=1, pady=5)
axisx = Label(frame, width=15, bg="gray22", text="X", fg="white", font=("Bahnschrift", 11))
axisx.grid(column=1, row=1, pady=5)
axisy = Label(frame, width=15, bg="gray22", text="Y", fg="white", font=("Bahnschrift", 11))
axisy.grid(column=2, row=1, pady=5)
axisz = Label(frame, width=15, bg="gray22", text="Z", fg="white", font=("Bahnschrift", 11))
axisz.grid(column=3, row=1, pady=5)
#entradas de texto para el usuario
entry0 = ttk.Entry(frame, font=("Bahnschrift", 11), width=15)
entry0.grid(column=0, row=2, pady=1)
entry1 = ttk.Entry(frame, font=("Bahnschrift", 11), width=15)
entry1.grid(column=1, row=2, pady=1)
entry2 = ttk.Entry(frame, font=("Bahnschrift", 11), width=15)
entry2.grid(column=2, row=2, pady=1)
entry3 = ttk.Entry(frame, font=("Bahnschrift", 11), width=15)
entry3.grid(column=3, row=2, pady=1)
resultado = StringVar()

#label donde se muestra el resultado
resultados = Label(frame, width=90, height=10, bg="gray22", textvariable=resultado, fg="white",font=("Bahnschrift", 9))
resultados.grid(column=1, row=3,columnspan=3, rowspan=2, pady=5)

cargas0 = []
fuerzas = []
count=True

#funcion para obtener los valores de los entry
def getvalue():
    global count
    cargas=[]
    if count:  
        ax.scatter(float(entry1.get()),float(entry2.get()),float(entry3.get()), c="green")
    else:
        ax.scatter(float(entry1.get()),float(entry2.get()),float(entry3.get()), c="red")
    count=False
    fig.canvas.draw()
    fig.canvas.flush_events()
    if combo.get()=="C":
        unity = 1
    elif combo.get()=="mC":
        unity = 0.001
    elif combo.get()=="uC":
        unity = 0.000001
    elif combo.get()=="nC":
        unity= 0.000000001

    cargas.append(float(entry0.get())*unity)
    cargas.append(float(entry1.get()))
    cargas.append(float(entry2.get()))
    cargas.append(float(entry3.get()))
    cargas0.append(cargas)
    entry0.delete(0, tkinter.END)
    entry1.delete(0, tkinter.END)
    entry2.delete(0, tkinter.END)
    entry3.delete(0, tkinter.END)

#funcion de calculo que utiliza los datos obtenidos en la funcion anterior
def calculo():
    if len(cargas0)>1:
        resul = ""
        x=0
        y=0
        z=0
        for i in range(len(cargas0)-1):   
            x_f=cargas0[i+1][1]-cargas0[0][1]
            y_f=cargas0[i+1][2]-cargas0[0][2]
            z_f=cargas0[i+1][3]-cargas0[0][3]
            #ley de coulomb
            c_f=(cargas0[i+1][0]*cargas0[0][0]*9000000000)/(((x_f**2+y_f**2+z_f**2)**(1/2))**3)

            #sentido o dirección del vector
            if cargas0[0][0]>0 and cargas0[i+1][0]>0:
                Direction = -1
            elif cargas0[0][0]<0 or cargas0[i+1][0]<0:
                Direction = 1
            #fuerza en termino vectorial                                  
            fuerza = [round(x_f*c_f*Direction, 6), round(y_f*c_f*Direction,6),round(z_f*c_f*Direction,6)]
            #modulo del vector
            Magnitud = ((x_f*c_f)**2+ (y_f*c_f)**2 + (z_f*c_f)**2)**(1/2)
            resul = resul+f"F1{i+2} = <{round(x_f*c_f*Direction, 6)},  {round(y_f*c_f*Direction,6)},  {round(z_f*c_f*Direction,6)}>  ||F1{i+1}||= {Magnitud} N\n"
            fuerzas.append(fuerza)
            #trazado de vectores
            ax.quiver(cargas0[0][1], cargas0[0][2], cargas0[0][3], x_f, y_f, z_f, length=1, arrow_length_ratio=0.01)

            fig.canvas.draw()
            fig.canvas.flush_events()

        for i in fuerzas:
            x=x+i[0]
            y=y+i[1]
            z=z+i[2]
        #fuerza total
        FTotal= (x**2+y**2+z**2)**(1/2)
        resul=resul+f"FT = <{x}, {y}, {z} >  ||FT||= {FTotal} N"
        resultado.set(resul)

button = Button(frame, text="OK", width=15, bg="magenta", fg="white", command=getvalue, font=("Bahnschrift", 11))
button.grid(column=4, row=2, pady=5)
button = Button(frame, text="CALCULAR", width=15, bg="magenta", fg="white", command=calculo, font=("Bahnschrift", 11))
button.grid(column=4, row=3, pady=5)

window.mainloop()