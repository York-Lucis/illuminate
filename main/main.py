import time
import threading
from core import start_illuminate
from core import Illuminate
import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import ttk, filedialog

current_progress_bar_value = 0

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Illuminate - PDF Enhancer")
        self.iconbitmap('program_icon.ico')
        self.geometry("300x200")
        
        self.style = ttkb.Style(theme='lumen')
        
        self.create_widgets()

    def create_widgets(self):
        frame = ttkb.Frame(self)
        frame.pack(fill='both', expand=True)

        self.pdf_label = ttkb.Label(frame, text="PDF File:")
        self.pdf_label.pack()

        self.pdf_entry = ttkb.Entry(frame)
        self.pdf_entry.pack(fill='x', expand=True)

        self.browse_button = ttkb.Button(frame, text="Browse", command=self.browse_pdf)
        self.browse_button.pack()

        self.output_label = ttkb.Label(frame, text="Output Directory:")
        self.output_label.pack()

        self.output_entry = ttkb.Entry(frame)
        self.output_entry.pack(fill='x', expand=True)

        self.browse_button = ttkb.Button(frame, text="Browse", command=self.browse_output)
        self.browse_button.pack()

        self.run_button = ttkb.Button(frame, text="Run", command=self.run)
        self.run_button.pack()

        # Create a progress bar and hide it initially
        self.progress = ttkb.Progressbar(frame, length=200, mode='determinate')
        self.progress.pack_forget()

    def update_progress_bar(self, value):
        # Update the progress bar to a certain value
        self.progress['value'] = value
        self.update_idletasks()

    def browse_pdf(self):
        self.pdf_entry.delete(0, 'end')
        self.pdf_entry.insert(0, filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")]))

    def browse_output(self):
        self.output_entry.delete(0, 'end')
        self.output_entry.insert(0, filedialog.askdirectory())

    def run(self):
        pdf_path = self.pdf_entry.get()
        output_path = self.output_entry.get()
        # Start a new thread to run the operation and update the progress bar
        threading.Thread(target=self.start_operation, args=(pdf_path, output_path)).start()

    def start_operation(self, pdf_path, output_path):
        illuminate = Illuminate(pdf_path, output_path)
        start_illuminate(illuminate)

    def close_window(self):
        self.destroy()

def main():
    app = Application()
    app.mainloop()

if __name__ == '__main__':
    main()
