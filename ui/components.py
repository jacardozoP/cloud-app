import tkinter as tk
from tkinter import messagebox



class TopMenuBar(tk.Frame):
    def __init__(self, parent, on_home, on_catalog, on_recognition):
        super().__init__(parent, bg="#0f2f44", height=54)
        self.pack_propagate(False)

        left = tk.Frame(self, bg="#0f2f44")
        left.pack(side="left", fill="y", padx=14)

        logo = tk.Label(
            left,
            text="☁ AeroCloud",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#0f2f44"
        )
        logo.pack(side="left", pady=10)

        right = tk.Frame(self, bg="#0f2f44")
        right.pack(side="right", fill="y", padx=10)

        self._make_button(right, "Inicio", on_home).pack(side="left", padx=6, pady=8)
        self._make_button(right, "Consultar nubes", on_catalog).pack(side="left", padx=6, pady=8)
        self._make_button(right, "Reconocimiento", on_recognition).pack(side="left", padx=6, pady=8)
        self._make_button(right, "Acerca de", self._show_about).pack(side="left", padx=6, pady=8)

    def _make_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            font=("Arial", 10, "bold"),
            bg="#1d4d6e",
            fg="white",
            activebackground="#2a668f",
            activeforeground="white",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=command
        )

    def _show_about(self):
        messagebox.showinfo(
            "Acerca de",
            "AeroCloud\n\nAplicación de escritorio en Python para consulta y reconocimiento asistido de nubes."
        )