"""
Maestro Schrodinger plugin which enables user to take screenshots of workspace and save them in the selected directory.
"""

#Name: CNNdock_maestro_plugin
#Command: pythonrun CNNdock_maestro_plugin.main

import tkinter as tk
from tkinter import filedialog
import os
from pathlib import Path
import pandas as pd
import schrodinger.ui.qt.entryselector
from schrodinger.maestro import maestro

def main():
    root = tk.Tk()

    def func_dir():
        directory_path = filedialog.askdirectory(title="Select directory")
        if directory_path:
            root.destroy() 
        return directory_path

    def main_logic(directory_path):
        entries_list = schrodinger.ui.qt.entryselector.get_entries()
        df = pd.DataFrame(entries_list)
        df_list = df[df.columns[0]].to_list()

        if not directory_path:
            print("No directory selected")
            return  

        pt = maestro.project_table_get()
        for entry in df_list:

            os.makedirs(Path(f'{directory_path}/{entry}'), exist_ok=True)
            maestro.command(f'changedirectory "{directory_path}/{entry}"')
            maestro.command(f'entrywsincludeonly entry {entry}')
            maestro.command(f'entryselectonly entry {entry}')

            for row in pt.selected_rows:
                nazwa = row.property['s_m_title']
                os.rename(f'{directory_path}/{entry}', f'{directory_path}/{nazwa}_{entry}')

            iterator_y = 1
            while iterator_y <= 4:
                maestro.command(f"rotate y=90")
                maestro.command(f"saveimage image_{nazwa}_{entry}_{str(iterator_y)}.png")
                iterator_y += 1

            iterator_x = 5
            while iterator_x <= 7:
                maestro.command(f"rotate x=90")
                maestro.command(f"saveimage image_{nazwa}_{entry}_{str(iterator_x)}.png")
                iterator_x += 1

            maestro.command(f"rotate x=90") 
    
    def start_process():
        directory_path = func_dir()
        if directory_path:
            main_logic(directory_path)

    b1 = tk.Button(root, text='Select directory', command=start_process)
    b1.pack(expand=True)

    root.title("CNNdock plugin")
    root.geometry('300x200')
    root.mainloop()

main()
