import tkinter as tk
from tkinter import messagebox

def hello():
    messagebox.showinfo("Hello", "Hello, world!")

def main():
    root = tk.Tk()
    root.title("Interface Gráfica")
    
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)
    
    hello_button = tk.Button(frame, text="Say Hello", command=hello)
    hello_button.pack(padx=5, pady=5)
    
    quit_button = tk.Button(frame, text="Quit", command=root.quit)
    quit_button.pack(padx=5, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
