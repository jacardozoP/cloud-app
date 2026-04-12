import os
import tkinter as tk
from PIL import Image, ImageTk


class ExamplesScreen:
    def __init__(self, root, cloud, go_back_callback):
        self.root = root
        self.cloud = cloud
        self.go_back_callback = go_back_callback
        self.main_frame = None
        self.thumb_images = []

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
            text=f"Ejemplos de {self.cloud['name']}",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#16354a"
        ).pack(pady=(16, 4))

        tk.Label(
            header,
            text=f"Código: {self.cloud['code']}",
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
            text="Volver a la ficha",
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

        content_frame = tk.Frame(
            body,
            bg="white",
            highlightthickness=1,
            highlightbackground="#c5dcec"
        )
        content_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        self.grid_frame = tk.Frame(canvas, bg="white")

        self.grid_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._populate_examples()

    def _populate_examples(self):
        image_paths = self._get_example_paths()

        if not image_paths:
            tk.Label(
                self.grid_frame,
                text="No se encontraron ejemplos para esta nube.",
                font=("Arial", 14),
                bg="white",
                fg="#35576e"
            ).pack(pady=40)
            return

        self.root.update_idletasks()
        container_width = self.root.winfo_width()

        thumb_width = 260
        thumb_height = 180
        columns = max(2, container_width // (thumb_width + 50))

        for index, image_path in enumerate(image_paths):
            row = index // columns
            col = index % columns

            card = tk.Frame(
                self.grid_frame,
                bg="white",
                width=thumb_width,
                height=thumb_height,
                highlightthickness=0,
                bd=0,
                cursor="hand2"
            )
            card.grid(row=row, column=col, padx=18, pady=18)
            card.grid_propagate(False)

            canvas = tk.Canvas(
                card,
                width=thumb_width,
                height=thumb_height,
                highlightthickness=0,
                bd=0,
                cursor="hand2"
            )
            canvas.pack(fill="both", expand=True)

            thumb = self._load_cover_image(image_path, thumb_width, thumb_height)
            if thumb is not None:
                canvas.create_image(0, 0, anchor="nw", image=thumb)
                self.thumb_images.append(thumb)
            else:
                canvas.configure(bg="#dcecf8")
                canvas.create_text(
                    thumb_width // 2,
                    thumb_height // 2,
                    text="Sin imagen",
                    font=("Arial", 14, "bold"),
                    fill="#4b6a7f"
                )

            def open_example(event, path=image_path):
                self.destroy()
                detail = ExampleDetailScreen(
                    self.root,
                    path,
                    self.cloud,
                    lambda: self.show()
                )
                detail.show()

            canvas.bind("<Button-1>", open_example)
            card.bind("<Button-1>", open_example)

    def _get_example_paths(self):
        code = self.cloud["code"]
        folder = os.path.join("dataset_app", code)

        if not os.path.exists(folder):
            return []

        files = []
        for name in os.listdir(folder):
            lower = name.lower()
            if lower.endswith(".jpg") or lower.endswith(".jpeg") or lower.endswith(".png") or lower.endswith(".webp"):
                files.append(os.path.join(folder, name))

        files.sort()
        return files[:20]

    def _load_cover_image(self, image_path, target_width, target_height):
        if not os.path.exists(image_path):
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

    def _go_back(self):
        self.destroy()
        self.go_back_callback()


class ExampleDetailScreen:
    def __init__(self, root, image_path, cloud, go_back_callback):
        self.root = root
        self.image_path = image_path
        self.cloud = cloud
        self.go_back_callback = go_back_callback
        self.main_frame = None
        self.image_ref = None

    def show(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.root, bg="#eef6ff")
        self.main_frame.pack(fill="both", expand=True)

        self._build_header()
        self._build_body()

    def destroy(self):
        if self.main_frame:
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

    def _build_body(self):
        body = tk.Frame(self.main_frame, bg="#eef6ff")
        body.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Button(
            body,
            text="Volver",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            bd=0,
            command=self._go_back
        ).pack(anchor="w", pady=(0, 10))

        # Imagen grande
        img = Image.open(self.image_path).convert("RGB")
        img.thumbnail((800, 500))
        self.image_ref = ImageTk.PhotoImage(img)

        tk.Label(body, image=self.image_ref, bg="#eef6ff").pack(pady=10)

        # Descripción simple (temporal)
        tk.Label(
            body,
            text=self._generate_description(),
            font=("Arial", 13),
            bg="#eef6ff",
            fg="#35576e",
            wraplength=800,
            justify="left"
        ).pack(pady=20)

    def _generate_description(self):
        code = self.cloud["code"]

        templates = {
            "Cu": "Se observan cúmulos con bordes definidos y aspecto algodonoso.",
            "As": "Capa nubosa uniforme característica de altostratos.",
            "Ci": "Nubes altas, delgadas y fibrosas típicas de cirros.",
            "Sc": "Nubes agrupadas en capas, propias de estratocúmulos.",
            "St": "Capa uniforme grisácea característica de estratos.",
            "Cb": "Nube con desarrollo vertical intenso, típica de tormenta.",
        }

        return templates.get(code, "Ejemplo representativo de esta nube.")

    def _go_back(self):
        self.destroy()
        self.go_back_callback()