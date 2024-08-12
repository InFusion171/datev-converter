import os
import tkinter as tk
from tkinter import Button, Entry, Label, filedialog as fd
from tkinter import messagebox

import chardet

from FileCreation import FileCreation
from Transaction import Transaction

class Gui:
    def __init__(self, title):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.resizable(False, False)

        Label(self.window, text='IBAN des gegebenen Kontos').grid(row=0)
        Label(self.window, text='BIC des gegebenen Kontos').grid(row=1)

        self.iban_input = Entry(self.window, width=30)
        self.iban_input.grid(row=0, column=1)

        self.bic_input = Entry(self.window, width=30)
        self.bic_input.grid(row=1, column=1)

        self.pick_file_button = Button(self.window, text='Datei auswählen', command=self.select_file)
        self.pick_file_button.grid(row=2, columnspan=2, pady=10, sticky='ew')

        self.filename_lable = Label(self.window, text='Bitte eine Datei auswählen')
        self.filename_lable.grid(row=3, columnspan=2, sticky='ew')

        self.generate_button = Button(self.window, text='Generieren', command=self.generate)
        self.generate_button.grid(row=4, columnspan=2, pady=(10, 0), sticky='ew')

        self.account_owner = ''
        self.content = ''

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

        try:
           self.account_owner, self.transaction_by_date = Transaction.parse(self.iban_input.get(), self.bic_input.get(), self.content)
           
        except AttributeError:
            messagebox.showerror("Error", "Zuerst eine Datei auswählen") 
            return
        except Exception:
            messagebox.showerror("Error", "Das Format der Datei stimmt nicht") 
            return

        FileCreation.create_files(self)
            

    def select_file(self):
        path:str = fd.askopenfilename(
            title='Datei auswählen',
            initialdir=f'{os.getcwd()}',
            filetypes=[('Spardabank Überweisungs export', '*.csv'), ('Spardabank Überweisungs export', '*.txt')])
        
        if len(path) == 0:
            return
        
        filename = path.split('/')[len(path.split('/')) - 1]

        self.filename_lable['text'] = filename

        with open(path, 'rb') as file:
            raw_data = file.read()

    
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    
        if encoding is None:
            messagebox.showerror("Error", "Das Encoding der Datei konnte nicht erkannt werden")
            return
    
        self.content = raw_data.decode(encoding)