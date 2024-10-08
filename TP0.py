import tkinter as tk
from tkinter import filedialog, Label, messagebox
import random as R
from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import imageio.v2 as imageio
from PIL import Image, ImageTk

import os

class Application(tk.Frame):
    global url_image
    url_image =""
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Frame que contendrá los dos cuadros y los botones
        self.squares_frame = tk.Frame(self)
        self.squares_frame.pack(side="top", fill="both", expand=True)

        # Cuadro 1 de 500x500 píxeles
        self.square1 = tk.Frame(self.squares_frame, width=500, height=500, bg="lightblue")
        self.square1.pack(side="left", padx=10, pady=10)

        # Frame para los botones entre los cuadros
        self.buttons_frame = tk.Frame(self.squares_frame)
        self.buttons_frame.pack(side="left", padx=10, pady=10)

        # Botón 1
        self.button1 = tk.Button(self.buttons_frame, text="Guardar", height=2, width=20, command=self.save_image)
        self.button1.pack(pady=5)

        # Botón 2
        self.button2 = tk.Button(self.buttons_frame, text="Procesar", height=2, width=20)
        self.button2.pack(pady=5)
        saturacion='0'
        saturaciones = ['10*10','20*20','50*50','100*100']
        self.select= ttk.Combobox(self, textvariable=saturacion,values=saturaciones,height=12,width=20)
        self.select.pack(pady=5)
        self.select.set(saturacion)
        self.seleccionado=tk.Label(self,textvariable=saturacion)
        self.seleccionado.pack(pady=5)

        # Botón 3
        self.button3 = tk.Button(self.buttons_frame, command=self.processImageRGB, text="Botón RGB", height=2, width=20)
        
        self.button3.pack(pady=5)

        # Cuadro 2 de 500x500 píxeles con borde de líneas de trazos
        self.square2 = tk.Canvas(self.squares_frame, width=500, height=500, bg="white")
        self.square2.pack(side="left", padx=10, pady=10)
        
        # Dibujar el borde con líneas de trazos
        self.square2.create_rectangle(
            5, 5, 495, 495,
            outline="gray",
            width=2,
            dash=(5, 2)
        )

        # Frame para los botones inferiores
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side="bottom", fill="x")

        # Botón para subir imagen
        self.button = tk.Button(self.bottom_frame, command=self.upload_image, text='Subir Imagen', height=2, width=28)
        self.button.pack(side="left", padx=10)

        # Botón para salir
        self.out = tk.Button(self.bottom_frame, text="Salir", command=self.close, height=2, width=28)
        self.out.pack(side="right", padx=10)


    def upload_image(self):
        global url_image
        url_image = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        print(f"Upload de imagen seleccionada: {url_image}")
        
        if url_image: 
            self.show_image(url_image)

    def show_image(self, url_image):
        print(f"Show de imagen seleccionada: {url_image}")

        imgIO = imageio.imread(url_image)
        img=Image.fromarray(imgIO)
        new_img = img.resize((500, 500))  # Cambiado para que la imagen se ajuste al tamaño del cuadro
        imagen_tk = ImageTk.PhotoImage(new_img)
        img1 = Label(self.square1, image=imagen_tk)
        img1.image = imagen_tk
        img1.pack()
        self.loaded_image = img 

    def close(self):
        response = messagebox.askquestion("Salir", "¿Desea salir de la interfaz?")
        if response == 'yes':
            self.master.destroy()

    def save_image(self):
        if self.loaded_image:
            save_path = os.path.join(os.getcwd(), 'imagen_guardada.png')  # Guarda en la carpeta de ejecución
            self.loaded_image.save(save_path)
            messagebox.showinfo("Imagen guardada", f"Imagen guardada en {save_path}")
            self.url_image = save_path  # Actualiza la ruta de la imagen guardada

    def processImageRGB(self):
        global url_image
        #if not self.url_image:
         #   messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
           # return
        print(f"Ruta de imagen seleccionada: {url_image}")
        #im = imageio.v2.imread(self.url_image.split('\\').reverse)
        im = imageio.imread(url_image)

        print(im.shape, im.dtype)

        titles = ['Rojo','Verde','Azul']
        chanels = ['Reds','Greens','Blues']

        for i in range(3):
            plt.subplot(1,3,i+1)
            plt.imshow(im[:,:,i], cmap=chanels[i])
            plt.title(titles[i])
            plt.axis('off')
        plt.show()

    def processImageYIQ(self):
        im = imageio.imread(url_image)
        print(im.shape, im.dtype)

        # we are working in float numbers [0,1] in image processing:

        im = np.clip(im/255,0.,1.)
        # print(im.shape,im.dtype)
        YIQ=np.zeros(im.shape)
        Y=im[:,:,0]
        I=im[:,:,1]
        Q=im[:,:,2]
        YIQ[:,:,0] = np.clip((Y*0.299 +  I *0.587 + Q*0.114),0.,1.)
        print(im.shape,im.dtype)
        YIQ[:,:,1] = np.clip(Y*0.595 +  I *(-0.274) + Q*(-0.321),-0.59,0.59)
        print(im.shape,im.dtype)
        YIQ[:,:,2] = np.clip(Y*0.211 +  I *(-0.522) + Q*(0.311),-0.52,0.52)
        # print(im.shape,im.dtype)


        plt.imshow(YIQ[:,:,1],"gray")
        plt.show()
        

root = tk.Tk()
root.geometry('1300x800')  # Ajuste del tamaño de la ventana para acomodar los cuadros y botones
app = Application(master=root)
app.mainloop()
