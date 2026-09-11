import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox


class NexaProject:
    REQUIRED_FOLDERS = (
        "models",
        "textures",
        "scenes",
        "scripts",
    )

    def __init__(self):
        self.path = None

    def is_valid(self, folder):
        if not folder:
            return False

        folder = os.path.abspath(folder)

        return all(
            os.path.isdir(os.path.join(folder, name))
            for name in self.REQUIRED_FOLDERS
        )

    def open(self, folder):
        if not self.is_valid(folder):
            return False

        self.path = os.path.abspath(folder)
        return True

    def choose(self):
        root = tk.Tk()
        root.withdraw()

        folder = filedialog.askdirectory(
            title="Nexa-Projekt öffnen"
        )

        root.destroy()

        if not folder:
            return False

        if not self.open(folder):
            root = tk.Tk()
            root.withdraw()

            messagebox.showerror(
                "Nexa App",
                "Kein gültiges Nexa-Projekt.\n\n"
                "Benötigt werden:\n"
                "models/\n"
                "textures/\n"
                "scenes/\n"
                "scripts/"
            )

            root.destroy()
            return False

        print("Nexa-Projekt geöffnet:")
        print(self.path)

        return True

    def export_zip(self):
        if not self.path:
            return False

        root = tk.Tk()
        root.withdraw()

        destination = filedialog.asksaveasfilename(
            title="Nexa-Projekt exportieren",
            defaultextension=".zip",
            filetypes=[
                ("Nexa-Projekt", "*.zip"),
                ("ZIP-Datei", "*.zip"),
            ],
        )

        root.destroy()

        if not destination:
            return False

        with zipfile.ZipFile(
            destination,
            "w",
            zipfile.ZIP_DEFLATED,
        ) as archive:

            for folder_name in self.REQUIRED_FOLDERS:
                folder = os.path.join(
                    self.path,
                    folder_name,
                )

                for current_root, _, files in os.walk(folder):
                    for filename in files:
                        full_path = os.path.join(
                            current_root,
                            filename,
                        )

                        relative_path = os.path.relpath(
                            full_path,
                            self.path,
                        )

                        archive.write(
                            full_path,
                            relative_path,
                        )

        print("Nexa-Projekt exportiert:")
        print(destination)

        return True


project = NexaProject()
