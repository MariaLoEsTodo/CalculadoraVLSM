import tkinter as tk

root=tk.Tk()
root.title("Looping of entry box")
root.geometry("500x600")

def applyToLabel():
    xx=size.get()
    for i in range(xx):
        element = box_list[i].get() # Get value from corresponding Entry
        ArrayLabel=tk.Label(root,text="Array Element: " + element)
        ArrayLabel.pack()

box_list = []   # Create list of Entrys
def Boxes():
    xx=size.get()
    for i in range(xx):        
        box=tk.Entry(root)
        box.pack()
        box_list.append(box)    # Append current Entry to list
    ApplytoLabel1=tk.Button(root,text="Calcular",command=applyToLabel).place(x=17,y=180)
    ApplytoLabel1.pack()

Array = tk.Frame(root)
Array.pack()

font = "Arial 10 bold"

text0=tk.Label(Array,text="Dirección IP:",
            font=font,fg="blue")
text0.grid(row=1,column=0,sticky="w")

size0=tk.IntVar()

ArraySize1=tk.Entry(Array,textvariable=size0)
ArraySize1.grid(row=1,column=1,sticky="w")

text1=tk.Label(Array,text="Prefijo de red:",
            font=font,fg="blue")
text1.grid(row=2,column=0,sticky="w")

size1=tk.IntVar()

ArraySize1=tk.Entry(Array,textvariable=size1)
ArraySize1.grid(row=2,column=1,sticky="w")


text2=tk.Label(Array,text="Número de sub redes:",
            font=font,fg="blue")
text2.grid(row=3,column=0,sticky="w")

size=tk.IntVar()

ArraySize=tk.Entry(Array,textvariable=size)
ArraySize.grid(row=3,column=1,sticky="w")

SizeofArray=tk.Button(Array,text="Aplicar",command=Boxes)
SizeofArray.grid(row=3,column=2,sticky="w")


root.mainloop()