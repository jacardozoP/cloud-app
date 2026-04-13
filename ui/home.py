import tkinter as tk
from ui.catalog import CatalogScreen
from ui.recognition import RecognitionScreen
from ui.quiz import QuizScreen
from PIL import Image, ImageTk


class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.main_frame = None


    def show(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Cargar imagen de fondo
        image = Image.open("assets/backgrounds/sky.jpg")
        image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.bg_image = ImageTk.PhotoImage(image)

        canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Overlay oscuro (mejora legibilidad)
        canvas.create_rectangle(
            0, 0,
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight(),
            fill="#0f2f44",
            stipple="gray50"
        )

        # Título
        canvas.create_text(
            600, 260,
            text="AeroCloud",
            font=("Courier New", 80, "bold"),
            fill="white"
        )

        # Subtítulo
        canvas.create_text(
            600, 335,
            text="Consulta y reconocimiento de nubes",
            font=("Courier New", 32),
            fill="#d9ecff"
        )

        # Botones
        btn_catalog = tk.Button(
            self.main_frame,
            text="Consultar nubes",
            font=("Courier New", 24, "bold"),
            bg="#2d6ea3",
            fg="white",
            bd=0,
            width=28,
            height=1,
            command=self._open_catalog
        )

        btn_recognition = tk.Button(
            self.main_frame,
            text="Reconocer nube",
            font=("Courier New", 24, "bold"),
            bg="#1f5681",
            fg="white",
            bd=0,
            width=28,
            height=1,
            command=self._open_recognition
        )

        btn_quiz = tk.Button(
            self.main_frame,
            text="Modo Quiz",
            font=("Courier New", 24, "bold"),
            bg="#3f8754",
            fg="white",
            bd=0,
            width=28,
            height=1,
            command=self._open_quiz
        )

        canvas.create_window(600, 460, window=btn_catalog)
        canvas.create_window(600, 560, window=btn_recognition)
        canvas.create_window(600, 660, window=btn_quiz)

    def destroy(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
            self.main_frame = None

    def _build_header(self):
        header = tk.Frame(self.main_frame, bg="#0b3d5c", height=110)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="AEROCLOUD SYSTEM",
            font=("Arial", 26, "bold"),
            fg="white",
            bg="#0b3d5c"
        )
        title.pack(pady=(18, 4))

        subtitle = tk.Label(
            header,
            text="Sistema de reconocimiento y consulta de nubes",
            font=("Arial", 12),
            fg="#d7ebff",
            bg="#0b3d5c"
        )
        subtitle.pack()

    def _build_center(self):
        center = tk.Frame(self.main_frame, bg="#d9ecff")
        center.pack(fill="both", expand=True)

        hero_box = tk.Frame(
            center,
            bg="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#b7d3ea"
        )
        hero_box.place(relx=0.5, rely=0.45, anchor="center", width=760, height=340)

        hero_title = tk.Label(
            hero_box,
            text="Bienvenido",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#16354a"
        )
        hero_title.pack(pady=(35, 10))

        hero_text = tk.Label(
            hero_box,
            text=(
                "Selecciona una opción para consultar información de nubes\n"
                "o realizar reconocimiento asistido a partir de imágenes."
            ),
            font=("Arial", 13),
            bg="white",
            fg="#35576e",
            justify="center"
        )
        hero_text.pack(pady=(0, 25))

        buttons_frame = tk.Frame(hero_box, bg="white")
        buttons_frame.pack(pady=10)

        consult_btn = tk.Button(
            buttons_frame,
            text="Consultar nubes",
            font=("Arial", 13, "bold"),
            width=22,
            height=2,
            bg="#2d6ea3",
            fg="white",
            activebackground="#1f5681",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self._open_catalog
        )
        consult_btn.grid(row=0, column=0, padx=15, pady=10)

        recognize_btn = tk.Button(
            buttons_frame,
            text="Reconocer nube",
            font=("Arial", 13, "bold"),
            width=22,
            height=2,
            bg="#3f8754",
            fg="white",
            activebackground="#2f6a41",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self._open_recognition
        )
        recognize_btn.grid(row=0, column=1, padx=15, pady=10)

    def _build_footer(self):
        footer = tk.Frame(self.main_frame, bg="#d9ecff", height=110)
        footer.pack(fill="x", pady=(0, 15))
        footer.pack_propagate(False)

        label = tk.Label(
            footer,
            text="Explorar por categorías",
            font=("Arial", 12, "bold"),
            bg="#d9ecff",
            fg="#16354a"
        )
        label.pack(pady=(10, 10))

        categories_frame = tk.Frame(footer, bg="#d9ecff")
        categories_frame.pack()

        categories = ["Bajas", "Medias", "Altas", "Vertical"]

        for category in categories:
            btn = tk.Button(
                categories_frame,
                text=category,
                font=("Arial", 11, "bold"),
                width=12,
                height=2,
                bg="#f4f9ff",
                fg="#21455f",
                activebackground="#d9ebfb",
                activeforeground="#16354a",
                highlightthickness=1,
                highlightbackground="#aac8df",
                bd=0,
                cursor="hand2",
                command=lambda c=category: self._show_category_info(c)
            )
            btn.pack(side="left", padx=8)

    def _open_catalog(self):
        self.destroy()
        catalog = CatalogScreen(self.root, self.show)
        catalog.show()

    def _open_recognition(self):
        self.destroy()
        recognition = RecognitionScreen(self.root, self.show)
        recognition.show()

    def _open_quiz(self):
        self.destroy()
        quiz = QuizScreen(self.root, self.show)
        quiz.pack(fill="both", expand=True)

    def _show_category_info(self, category):
        self.destroy()
        catalog = CatalogScreen(self.root, self.show)
        catalog.show()