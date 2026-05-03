import tkinter as tk
from ui.components import TopMenuBar
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from logic.ai_predictor import predict_cloud


class AIScreen:
    def __init__(self, root, go_home_callback):
        self.root = root
        self.go_home_callback = go_home_callback
        self.main_frame = None
        self.selected_image_path = None
        self.image_preview = None
        self.image_label = None
        self.result_label = None

    def show(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.root, bg="#eef6ff")
        self.main_frame.pack(fill="both", expand=True)

        menu = TopMenuBar(
            self.main_frame,
            on_home=self._go_home,
            on_catalog=self._go_catalog,
            on_recognition=self._go_recognition,
            on_quiz=self._go_quiz
        )
        menu.pack(fill="x")

        title = tk.Label(
            self.main_frame,
            text="Reconocimiento por IA",
            font=("Arial", 28, "bold"),
            bg="#eef6ff",
            fg="#16354a"
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            self.main_frame,
            text="Este módulo estará destinado al reconocimiento automático de nubes mediante inteligencia artificial.",
            font=("Arial", 14),
            bg="#eef6ff",
            fg="#35576e",
            wraplength=700,
            justify="center"
        )
        subtitle.pack(pady=5)



        self.image_label = tk.Label(
            self.main_frame,
            text="Carga una imagen para analizarla con IA",
            font=("Arial", 13),
            bg="#f7fbff",
            fg="#4b6a7f"
        )
        self.image_label.pack(pady=5)

        tk.Button(
            self.main_frame,
            text="Cargar imagen",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            bd=0,
            width=18,
            height=2,
            command=self._load_image
        ).pack(pady=5)

        tk.Button(
            self.main_frame,
            text="Analizar con IA",
            font=("Arial", 12, "bold"),
            bg="#7c3aed",
            fg="white",
            bd=0,
            width=18,
            height=2,
            command=self._analyze_with_ai
        ).pack(pady=5)

        self.result_label = tk.Label(
            self.main_frame,
            text="Resultado IA: pendiente",
            font=("Arial", 13, "bold"),
            bg="#eef6ff",
            fg="#16354a",
            justify="left"
        )
        self.result_label.pack(pady=10)

    def _load_image(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.webp"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not file_path:
            return

        self.selected_image_path = file_path

        image = Image.open(file_path).convert("RGB")

        # 🔥 MISMO tamaño que Recognition (ajústalo si ahí usas otro)
        image.thumbnail((800, 500))

        self.image_preview = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.image_preview, text="")

    def _analyze_with_ai(self):
        if not self.selected_image_path:
            messagebox.showwarning("Falta imagen", "Primero carga una imagen.")
            return

        try:
            result = predict_cloud(self.selected_image_path)

            confidence_percent = result["confidence"] * 100

            cloud_names = {
                "Ac": "Altocúmulos",
                "As": "Altostratos",
                "Cb": "Cumulonimbos",
                "Cc": "Cirrocúmulos",
                "Ci": "Cirros",
                "Cs": "Cirrostratos",
                "Ct": "Estelas de condensación",
                "Cu": "Cúmulos",
                "Ns": "Nimbostratos",
                "Sc": "Estratocúmulos",
                "St": "Estratos"
            }

            cloud_name = cloud_names.get(result["code"], result["code"])

            top_text = "Top 3 IA:\n"

            for i, prediction in enumerate(result["top_3"], start=1):
                code = prediction["code"]
                name = cloud_names.get(code, code)
                confidence = prediction["confidence"] * 100

                top_text += f"{i}. {name} ({code}) - {confidence:.2f}%\n"

            self.result_label.config(text=top_text)

        except Exception as error:
            messagebox.showerror("Error IA", f"No se pudo analizar la imagen.\n{error}")

    def destroy(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
            self.main_frame = None

    def _go_home(self):
        self.destroy()
        self.go_home_callback()

    def _go_catalog(self):
        from ui.catalog import CatalogScreen
        self.destroy()
        catalog = CatalogScreen(self.root, self.go_home_callback)
        catalog.show()

    def _go_recognition(self):
        from ui.recognition import RecognitionScreen
        self.destroy()
        recognition = RecognitionScreen(self.root, self.go_home_callback)
        recognition.show()

    def _go_quiz(self):
        from ui.quiz import QuizScreen
        self.destroy()
        quiz = QuizScreen(self.root, self.go_home_callback)
        quiz.pack(fill="both", expand=True)