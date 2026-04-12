import os
import tkinter as tk
from ui.detail import DetailScreen
from ui.components import TopMenuBar
from ui.recognition import RecognitionScreen

from PIL import Image, ImageTk

from data.cloud_repository import get_all_clouds, get_clouds_by_category


class CatalogScreen:
    def __init__(self, root, go_home_callback, category_filter=None):
        self.root = root
        self.go_home_callback = go_home_callback
        self.category_filter = category_filter
        self.main_frame = None
        self.card_images = []

    def _refresh_catalog(self):
        self.destroy()
        new_screen = CatalogScreen(self.root, self.go_home_callback, None)
        new_screen.show()

    def _go_recognition(self):
        self.destroy()
        recognition = RecognitionScreen(self.root, self.go_home_callback)
        recognition.show()

    def show(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.root, bg="#eef6ff")
        self.main_frame.pack(fill="both", expand=True)
        menu = TopMenuBar(
            self.main_frame,
            on_home=self._go_home,
            on_catalog=self._refresh_catalog,
            on_recognition=self._go_recognition
        )
        menu.pack(fill="x")

        self._build_header()
        self._build_body()

    def destroy(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
            self.main_frame = None

    def _build_header(self):
        header = tk.Frame(self.main_frame, bg="#16354a", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="CATÁLOGO DE NUBES",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#16354a"
        )
        title.pack(pady=(18, 4))

        subtitle_text = "Selecciona una nube para consultar su información"
        if self.category_filter:
            subtitle_text = f"Mostrando categoría: {self.category_filter.capitalize()}"

        subtitle = tk.Label(
            header,
            text=subtitle_text,
            font=("Arial", 11),
            fg="#d9ecff",
            bg="#16354a"
        )
        subtitle.pack()

    def _build_body(self):
        body = tk.Frame(self.main_frame, bg="#eef6ff")
        body.pack(fill="both", expand=True, padx=20, pady=20)

        top_bar = tk.Frame(body, bg="#eef6ff")
        top_bar.pack(fill="x", pady=(0, 12))

        back_btn = tk.Button(
            top_bar,
            text="Volver al inicio",
            font=("Arial", 11, "bold"),
            width=18,
            height=2,
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self._go_home
        )
        back_btn.pack(side="left")

        content_frame = tk.Frame(
            body,
            bg="white",
            highlightthickness=1,
            highlightbackground="#c5dcec"
        )
        content_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            content_frame,
            bg="white",
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        self.cards_container = tk.Frame(canvas, bg="white")

        self.cards_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.cards_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._populate_cards()

    def _populate_cards(self):
        if self.category_filter:
            clouds = get_clouds_by_category(self.category_filter)
        else:
            clouds = get_all_clouds()

        self.root.update_idletasks()
        container_width = self.root.winfo_width()

        card_width = 330
        card_height = 230

        columns = max(2, container_width // (card_width + 40))
        image_width = card_width
        image_height = card_height

        for index, cloud in enumerate(clouds):
            row = index // columns
            col = index % columns

            card = tk.Frame(
                self.cards_container,
                bg="#f9fcff",
                width=card_width,
                height=card_height,
                highlightthickness=1,
                highlightbackground="#c8deed",
                cursor="hand2"
            )
            card.grid(row=row, column=col, padx=18, pady=18)
            card.grid_propagate(False)

            image_canvas = tk.Canvas(
                card,
                width=image_width,
                height=image_height,
                highlightthickness=0,
                bd=0,
                cursor="hand2"
            )
            image_canvas.pack(fill="both", expand=True)

            image_path = cloud.get("image", "")
            loaded_image = self._load_cover_image(image_path, image_width, image_height)

            if loaded_image is not None:
                image_canvas.create_image(0, 0, anchor="nw", image=loaded_image)
                self.card_images.append(loaded_image)
            else:
                image_canvas.configure(bg="#dcecf8")
                image_canvas.create_text(
                    image_width // 2,
                    image_height // 2,
                    text="Sin imagen",
                    font=("Arial", 14, "bold"),
                    fill="#4b6a7f"
                )

            # sombra del texto
            image_canvas.create_text(
                16, 22,
                anchor="nw",
                text=cloud["name"],
                font=("Arial", 16, "bold"),
                fill="#1a1a1a"
            )

            # texto principal
            image_canvas.create_text(
                14, 20,
                anchor="nw",
                text=cloud["name"],
                font=("Arial", 16, "bold"),
                fill="#f7fbff"
            )

            # click en toda la tarjeta
            card.bind("<Button-1>", lambda e, c=cloud: self._open_cloud(c))
            image_canvas.bind("<Button-1>", lambda e, c=cloud: self._open_cloud(c))

    def _load_cover_image(self, image_path, target_width, target_height):
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

    def _open_cloud(self, cloud):
        self.destroy()
        detail = DetailScreen(
            self.root,
            cloud,
            self.show,
            self.show
        )
        detail.show()

    def _go_home(self):
        self.destroy()
        self.go_home_callback()