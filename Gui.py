import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox

import chardet

from FileCreation import FileCreation
from Transaction import Transaction

class Gui:
    def __init__(self, title):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.resizable(False, False)

        style = ttk.Style(self.window)
        style.theme_use('clam') 
        
        style.configure('TLabel', font=('Arial', 12), padding=5)
        style.configure('TButton', font=('Arial', 12), padding=5)
        style.configure('TEntry', font=('Arial', 12), padding=5)

        ttk.Label(self.window, text='IBAN des gegebenen Kontos').grid(row=0, sticky='w')
        ttk.Label(self.window, text='BIC des gegebenen Kontos').grid(row=1, sticky='w')

        self.iban_input = ttk.Entry(self.window, width=30)
        self.iban_input.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        self.bic_input = ttk.Entry(self.window, width=30)
        self.bic_input.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        self.pick_file_button = ttk.Button(self.window, text='Datei auswählen', command=self.select_file)
        self.pick_file_button.grid(row=2, columnspan=2, pady=10, padx=10, sticky='ew')

        self.pick_output_dir_button = ttk.Button(self.window, text='Ausgabepfad auswählen', command=self.select_output_directory)
        self.pick_output_dir_button.grid(row=3, columnspan=2, pady=(0, 10), padx=10, sticky='ew')

        # Box (Frame) für die Labels
        self.label_frame = ttk.Frame(self.window, borderwidth=2, relief="groove")
        self.label_frame.grid(row=4, columnspan=2, pady=10, padx=10, sticky='ew')

        # Spalten des Frames konfigurieren, um die Labels zu zentrieren
        self.label_frame.grid_columnconfigure(0, weight=1)

        self.filename_label = ttk.Label(self.label_frame, text='Bitte eine Datei auswählen', anchor='center')
        self.filename_label.grid(row=0, column=0, pady=5, padx=10, sticky='ew')

        self.output_path_label = ttk.Label(self.label_frame, text='Bitte Zielordner auswählen', anchor='center')
        self.output_path_label.grid(row=1, column=0, pady=5, padx=10, sticky='ew')

        self.generate_button = ttk.Button(self.window, text='Generieren', command=self.generate)
        self.generate_button.grid(row=5, columnspan=2, pady=10, padx=10, sticky='ew')

        self.account_owner = ''
        self.content = ''
        self.output_path = ''

    def run(self):
        self.window.mainloop()

    def generate(self):
        if len(self.content) == 0:
            messagebox.showerror("Error", "Zuerst eine Datei auswählen")
            return

        if len(self.iban_input.get()) == 0:
            messagebox.showerror("Error", "IBAN Feld ist leer")
            return

        if len(self.bic_input.get()) == 0:
            messagebox.showerror("Error", "BIC Feld ist leer")
            return

        if len(self.output_path) == 0:
            messagebox.showerror("Error", "Bitte den Zielpfad auswählen")
            return

        try:
            self.account_owner, self.transaction_by_date = Transaction.parse(self.iban_input.get(), self.bic_input.get(), self.content)

        except AttributeError:
            messagebox.showerror("Error", "Zuerst eine Datei auswählen")
            return
        except Exception:
            messagebox.showerror("Error", "Das Format der Datei stimmt nicht")
            return

        FileCreation.create_files(self.transaction_by_date, self.account_owner, self.output_path)

    def select_output_directory(self):
        path = fd.askdirectory(title='Zielpfad auswählen')

        self.output_path = path
        self.output_path_label['text'] = f'Ausgabepfad: {path}'

    def select_file(self):
        path = fd.askopenfilename(
            title='Datei auswählen',
            filetypes=[('Spardabank Überweisungs export', '*.csv'), ('Spardabank Überweisungs export', '*.txt')]
        )

        if not path:
            return

        filename = os.path.basename(path)
        self.filename_label['text'] = f'Datei: {filename}'

        with open(path, 'rb') as file:
            raw_data = file.read()

        result = chardet.detect(raw_data)
        encoding = result['encoding']

        if encoding is None:
            messagebox.showerror("Error", "Das Encoding der Datei konnte nicht erkannt werden")
            return

        self.content = raw_data.decode(encoding)

