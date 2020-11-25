import os
from tkinter.filedialog import asksaveasfilename
import tkinter as tk
from turtle import RawTurtle

from nxc import NXCBuilder

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.filepath = os.path.join(os.path.expanduser("~"), "kod.nxc")
        
        self.power_var = tk.IntVar()
        self.forward_wait_var = tk.IntVar()
        self.degrees_var = tk.IntVar()
        self.wait_wait_var = tk.IntVar()
        
        self.power_var.set(50)
        self.forward_wait_var.set(1000)
        self.degrees_var.set(90)
        self.wait_wait_var.set(1000)
        
        self.create_widgets()
        self.connect_widgets()
        
        self.nxc = NXCBuilder(self.draw)
        
    def create_widgets(self):
        tk.Label(self.parent, text="Robot Driver Inc.", font = ('Arial' , 25)).grid(row = 0, column = 0, columnspan=6)
        self.forward_btn = tk.Button(self.parent, text="Jazda do przodu")
        self.rotate_btn = tk.Button(self.parent, text="Obrót")
        self.wait_btn = tk.Button(self.parent, text="Czekaj")
        self.undo_btn = tk.Button(self.parent, text="Cofnij")
        self.generate_btn = tk.Button(self.parent, text="Generuj kod")
        self.canvas = tk.Canvas(self.parent, width=640, height=480)
        self.draw = RawTurtle(self.canvas)

        self.forward_btn.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.rotate_btn.grid(row=2, column=0, sticky=tk.E+tk.W)
        self.wait_btn.grid(row=3, column=0, sticky=tk.E+tk.W)
        self.undo_btn.grid(row=4, column=0, sticky=tk.E+tk.W)
        self.generate_btn.grid(row=5, column=0, sticky=tk.E+tk.W)
        self.canvas.grid(row=6, column=0, columnspan=6)
        
        tk.Label(self.parent, text="Moc:").grid(row=1, column=1)
        self.power_input = tk.Entry(self.parent, textvariable=self.power_var)
        
        tk.Label(self.parent, text="Czas:").grid(row=1, column=3)
        self.forward_wait_input = tk.Entry(self.parent, textvariable=self.forward_wait_var)
        
        tk.Label(self.parent, text="Stopnie:").grid(row=2, column=1)
        self.rotate_input = tk.Entry(self.parent, textvariable=self.degrees_var)
        
        tk.Label(self.parent, text="Czas:").grid(row=3, column=1)
        self.wait_wait_input = tk.Entry(self.parent, textvariable=self.wait_wait_var)
        
        tk.Label(self.parent, text="Ścieżka:").grid(row=4, column=1, rowspan=2)
        self.filepath_label = tk.Label(self.parent, text=self.filepath, wraplength=150, justify='center')
        
        self.filepath_btn = tk.Button(self.parent, text="Wybierz")
        
        self.power_input.grid(row=1, column=2)
        self.forward_wait_input.grid(row=1, column=4)
        self.rotate_input.grid(row=2, column=2)
        self.wait_wait_input.grid(row=3, column=2)
        self.filepath_label.grid(row=4, column=2, rowspan=2)
        self.filepath_btn.grid(row=5, column=3, columnspan=2, sticky=tk.E+tk.W)
        
    def connect_widgets(self):
        self.forward_btn.bind('<Button-1>', lambda x: self.on_forward_btn_pressed())
        self.rotate_btn.bind('<Button-1>', lambda x: self.on_rotate_btn_pressed())
        self.wait_btn.bind('<Button-1>', lambda x: self.on_wait_btn_pressed())
        self.generate_btn.bind('<Button-1>', lambda x: self.on_generate_btn_pressed())
        self.undo_btn.bind('<Button-1>', lambda x: self.on_undo_btn_pressed())
        self.filepath_btn.bind('<Button-1>', lambda x: self.on_filepath_btn_pressed())
    
    def on_forward_btn_pressed(self):
        #self.draw.forward(10)
        print("Fwd: Power:", self.power_var.get(), ", Wait time:", self.forward_wait_var.get())
        self.nxc.add_forward_command(self.power_var.get(), self.forward_wait_var.get())
    
    def on_rotate_btn_pressed(self):
        #self.draw.right(45)
        print("Rotate: Degrees:", self.degrees_var.get())
        self.nxc.add_rotate_command(self.degrees_var.get())
    
    def on_wait_btn_pressed(self):
        #print("Wait:", self.wait_wait_var.get())
        print("Wait:", self.wait_wait_var.get())
        self.nxc.add_wait_command(self.wait_wait_var.get())
    
    def on_generate_btn_pressed(self):
        print(self.filepath)
        self.nxc.generate_code(self.filepath)

    def on_undo_btn_pressed(self):
        print("Undo")
        self.nxc.undo_last_command()
    
    def on_filepath_btn_pressed(self):
        self.filepath = asksaveasfilename(initialdir=os.path.expanduser("~"),
                                          filetypes=(("NXC File", "*.nxc"), ("TXT File", "*.txt")))
        self.filepath_label['text'] = self.filepath

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).grid()
    root.mainloop()