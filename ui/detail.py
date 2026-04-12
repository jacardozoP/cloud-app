import os
import tkinter as tk
from PIL import Image, ImageTk
from ui.examples import ExamplesScreen



class DetailScreen:
    def __init__(self, root, cloud, go_back_callback, open_catalog_callback):
        self.root = root
        self.cloud = cloud
        self.go_back_callback = go_back_callback
        self.open_catalog_callback = open_catalog_callback
        self.main_frame = None
        self.header_image = None

    def show(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.root, bg="#eef6ff")
        self.main_frame.pack(fill="both", expand=True)

        self._build_header()
        self._build_body()

    def destroy(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
            self.main_frame = None

    def _build_header(self):
        header = tk.Frame(self.main_frame, bg="#16354a", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=self.cloud["name"],
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#16354a"
        ).pack(pady=(16, 4))

        tk.Label(
            header,
            text="Ficha descriptiva de la nube seleccionada",
            font=("Arial", 11),
            fg="#d9ecff",
            bg="#16354a"
        ).pack()

    def _build_body(self):
        body = tk.Frame(self.main_frame, bg="#eef6ff")
        body.pack(fill="both", expand=True, padx=20, pady=20)

        top_bar = tk.Frame(body, bg="#eef6ff")
        top_bar.pack(fill="x", pady=(0, 12))

        tk.Button(
            top_bar,
            text="Volver al catálogo",
            font=("Arial", 11, "bold"),
            width=18,
            height=2,
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self._go_back
        ).pack(side="left")

        content = tk.Frame(body, bg="#eef6ff")
        content.pack(fill="both", expand=True)

        left_panel = tk.Frame(
            content,
            bg="white",
            width=420,
            highlightthickness=1,
            highlightbackground="#c8deed"
        )
        left_panel.pack(side="left", fill="y", padx=(0, 18))
        left_panel.pack_propagate(False)

        right_panel = tk.Frame(
            content,
            bg="white",
            highlightthickness=1,
            highlightbackground="#c8deed"
        )
        right_panel.pack(side="left", fill="both", expand=True)

        self._build_image_panel(left_panel)
        self._build_info_panel(right_panel)

    def _build_image_panel(self, parent):
        tk.Label(
            parent,
            text="Imagen de referencia",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#16354a"
        ).pack(pady=(18, 12))

        viewer = tk.Frame(
            parent,
            width=360,
            height=280,
            bg="#f4f9ff",
            highlightthickness=1,
            highlightbackground="#d8e8f5"
        )
        viewer.pack(padx=20, pady=(0, 18))
        viewer.pack_propagate(False)

        image_label = tk.Label(
            viewer,
            bg="#f4f9ff",
            text="Sin imagen",
            font=("Arial", 12),
            fg="#537089"
        )
        image_label.place(relx=0.5, rely=0.5, anchor="center")

        image_path = self.cloud.get("image", "")
        loaded = self._load_detail_image(image_path, 360, 280)
        if loaded is not None:
            image_label.config(image=loaded, text="")
            image_label.image = loaded
            self.header_image = loaded

        info_box = tk.Frame(
            parent,
            bg="#f8fbff",
            highlightthickness=1,
            highlightbackground="#d8e8f5"
        )
        info_box.pack(fill="x", padx=20, pady=(0, 16))

        tk.Label(
            info_box,
            text=f"Código: {self.cloud.get('code', '-')}",
            font=("Arial", 11, "bold"),
            bg="#f8fbff",
            fg="#35576e"
        ).pack(anchor="w", padx=14, pady=(12, 4))

        tk.Label(
            info_box,
            text=f"Categoría: {self.cloud.get('category', '-').capitalize()}",
            font=("Arial", 11, "bold"),
            bg="#f8fbff",
            fg="#35576e"
        ).pack(anchor="w", padx=14, pady=(0, 12))

        tk.Button(
            parent,
            text="Ver más de esta categoría",
            font=("Arial", 11, "bold"),
            width=24,
            height=2,
            bg="#2d6ea3",
            fg="white",
            activebackground="#1f5681",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self._show_same_category
        ).pack(pady=(0, 20))

        tk.Button(
            parent,
            text="Ver más ejemplos de esta nube",
            font=("Arial", 11, "bold"),
            width=24,
            height=2,
            bg="#3f8754",
            fg="white",
            activebackground="#2f6a41",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self._show_examples
        ).pack(pady=(0, 20))

    def _build_info_panel(self, parent):
        canvas = tk.Canvas(parent, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        sections = [
            ("Definición", self.cloud.get("definition", "")),
            ("Altitud", self.cloud.get("altitude", "")),
            ("Aspecto", self.cloud.get("appearance", "")),
            ("Composición", self.cloud.get("composition", "")),
            ("Qué indican", self.cloud.get("weather_meaning", "")),
            ("Dato interesante", self.cloud.get("interesting_fact", "")),
            ("Por qué pertenece a esta categoría", self.cloud.get("category_reason", ""))
        ]

        for title, content in sections:
            block = tk.Frame(
                scroll_frame,
                bg="#f9fcff",
                highlightthickness=1,
                highlightbackground="#d6e7f3"
            )
            block.pack(fill="x", padx=20, pady=10)

            tk.Label(
                block,
                text=title,
                font=("Arial", 14, "bold"),
                bg="#f9fcff",
                fg="#16354a"
            ).pack(anchor="w", padx=16, pady=(14, 6))

            tk.Label(
                block,
                text=content,
                font=("Arial", 12),
                bg="#f9fcff",
                fg="#35576e",
                wraplength=650,
                justify="left"
            ).pack(anchor="w", padx=16, pady=(0, 14))

    def _load_detail_image(self, image_path, target_width, target_height):
        if not image_path or not os.path.exists(image_path):
            return None

        try:
            image = Image.open(image_path).convert("RGB")

            img_width, img_height = image.size
            scale = max(target_width / img_width, target_height / img_height)

            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            image = image.resize((new_width, new_height), Image.LANCZOS)

            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height

            image = image.crop((left, top, right, bottom))

            return ImageTk.PhotoImage(image)
        except Exception:
            return None

    def _show_same_category(self):
        from ui.catalog import CatalogScreen

        self.destroy()
        catalog = CatalogScreen(
            self.root,
            self.go_back_callback,
            category_filter=self.cloud["category"]
        )
        catalog.show()

    def _go_back(self):
        self.destroy()
        self.go_back_callback()

    def _show_examples(self):
        self.destroy()
        examples = ExamplesScreen(self.root, self.cloud, lambda: self._reopen_self())
        examples.show()

    def _reopen_self(self):
        detail = DetailScreen(
            self.root,
            self.cloud,
            self.go_back_callback,
            self.open_catalog_callback
        )
        detail.show()