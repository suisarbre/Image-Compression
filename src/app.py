import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from core import *

class SVDCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title = ("SVD Image Compressor")
        
        self.original_image = None
        self.compressed_matrix = None
        #SVD matrices
        self.U = None
        self.sigma = None
        self.Vt = None
        self.k = tk.IntVar(value = 50) #default k = 50
        
        #Setup UI
        self.create_widgets()
        
    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        #load image button
        load_button = ttk.Button(control_frame,text="Load Image",command = self.load_and_convert)
        load_button.grid(row=0, column=0, padx=5)
        
        # "Save" button next to the "Load" button
        self.save_btn = ttk.Button(
            control_frame, 
            text="Save Compressed", 
            command=self.save_compressed_image,  
            state="disabled"  # Disabled until compression happens
        )
        self.save_btn.grid(row=0, column=4, padx=5)
        
        #slider for k
        slider_label = ttk.Label(control_frame,text = "k (Singular Values):")
        slider_label.grid(row = 0,column=1,padx=5)
        
        self.slider = ttk.Scale(control_frame,
                                from_= 1,
                                to = 300 ,
                                variable = self.k,
                                command = self.update_compression)
        self.slider.grid(row = 0, column = 2, padx = 5)
        
        k_value_label = ttk.Label(control_frame,textvariable=int(self.k.get()))
        k_value_label.grid(row = 0, column = 3, padx = 5)
        
        image_frame = ttk.Frame(self.root)
        image_frame.pack(fill = tk.BOTH,expand = True)
        
        #Original Image
        self.original_label = ttk.Label(image_frame)
        self.original_label.grid(row=0,column = 0,padx = 10, pady = 10)
        
        #compressed image
        self.compressed_label = ttk.Label(image_frame)
        self.compressed_label.grid(row = 0, column = 1, padx=10, pady=10)
        
    
    def load_and_convert(self):
        filepath = filedialog.askopenfilename(
            filetypes = [("Image Files","*.jpg *.jpeg *.png")]
            
        )
        if not filepath:
            return
        
        #load
        matrix = load_image(filepath)
        if matrix is None:
            messagebox.showerror("Error","Failed to load image!")
            return
        
        #compute and update SVD
        
        try:
            self.U, self.sigma, self.Vt = compute_svd(matrix)
            self.original_image = matrix
            self.update_compression()
            
        except Exception as e:
            messagebox.showerror("Error",f"SVD computation failed : {e}")
                
    def update_compression(self,*args):
        if self.original_image is None:
            return
        
        k = int(self.k.get())
        print(k)
        try:
            compressed = compress(self.U,self.sigma,self.Vt,k)
            self.compressed_matrix = compressed
            self.save_btn.config(state = "normal")
            #Display images
            self.display_image(self.original_image,self.original_label,"Original")
            self.display_image(compressed,self.compressed_label, f"Compressed (k = {k})")
        except Exception as e:
            messagebox.showerror("Error", f"Compression failed : {e}")
            
    def display_image(self,matrix,label,title):
        
        #convert matrix to PIL image
        image = Image.fromarray(matrix)
        image.thumbnail((400,400)) #Resize for display
        
        tk_image = ImageTk.PhotoImage(image)
        
        #update label
        label.config(image = tk_image, text = title, compound = tk.TOP)
        label.image = tk_image #Keep reference to avoid garbage collection
        
    def save_compressed_image(self):
        if self.compressed_matrix is None:
            messagebox.showerror("Error", "No compressed image to save!")
            return

        # Open file dialog to choose save location
        filepath = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("All Files", "*.*")
            ]
        )

        if not filepath:
            return  # User canceled

        try:
            # Convert the compressed matrix to PIL Image
            compressed_pil = Image.fromarray(self.compressed_matrix)
            compressed_pil.save(filepath)
            messagebox.showinfo("Success", f"Saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
        
def main():
    root = tk.Tk()
    app = SVDCompressorGUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()