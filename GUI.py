import tkinter as tk


gui = tk.Tk()
gui.title('YouTube Downloader')
gui.geometry('800x600')
# gui.configure(background='#ffffff')

input_text = tk.Text(gui, height=5, width=20)
input_text.pack()

lbl = tk.Label(gui, text='Hello')
lbl.pack()
gui.mainloop()
