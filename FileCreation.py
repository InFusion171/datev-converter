import os
from tkinter import messagebox


class FileCreation:
    @staticmethod
    def create_files(gui):
        DIRECTORY_PATH = f'{os.getcwd()}/{gui.account_owner} Überweisungen'

        if os.path.exists(DIRECTORY_PATH):
            messagebox.showerror('Error', f'Ordner "{DIRECTORY_PATH}" existiert bereits') 
            return
        
        os.makedirs(DIRECTORY_PATH)

        for voluta_month, transactions in gui.transaction_by_date.items():
            with open(f'{DIRECTORY_PATH}/{voluta_month} Überweisung.txt', 'w+') as f:
                for transaction in transactions:
                    f.write(f'{transaction.create_datev_format()}\n')

        messagebox.showinfo('Erfolgreich', f'Überweisungen von {gui.account_owner} in "{os.getcwd()}" erstellt')