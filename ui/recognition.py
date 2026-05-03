import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from data.cloud_repository import get_cloud_by_name
from ui.components import TopMenuBar
from logic.ai_predictor import predict_cloud


class RecognitionScreen:
    def __init__(self, root, go_home_callback):
        self.root = root
        self.go_home_callback = go_home_callback
        self.main_frame = None
        self.image_label = None
        self.result_label = None
        self.selected_image_path = None
        self.image_preview = None

        self.density_var = tk.StringVar(value="")
        self.vertical_var = tk.StringVar(value="")
        self.coverage_var = tk.StringVar(value="")
        self.shape_var = tk.StringVar(value="")
        self.high_thin_var = tk.StringVar(value="")

    def _go_catalog(self):
        from ui.catalog import CatalogScreen
        self.destroy()
        catalog = CatalogScreen(self.root, self.go_home_callback)
        catalog.show()

    def _go_quiz(self):
        from ui.quiz import QuizScreen

        self.destroy()
        quiz = QuizScreen(self.root, self.go_home_callback)
        quiz.pack(fill="both", expand=True)

    def _refresh_recognition(self):
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
            on_catalog=self._go_catalog,
            on_recognition=self._refresh_recognition,
            on_quiz=self._go_quiz
        )
        menu.pack(fill="x")

        self._build_header()
        self._build_body()

    def destroy(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
            self.main_frame = None

    def _build_header(self):
        header = tk.Frame(self.main_frame, bg="#1d4d6e", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="RECONOCIMIENTO ASISTIDO",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1d4d6e"
        ).pack(pady=(18, 4))

        tk.Label(
            header,
            text="Carga una imagen y responde algunas preguntas visuales",
            font=("Arial", 11),
            fg="#dceefe",
            bg="#1d4d6e"
        ).pack()

    def _build_body(self):
        body = tk.Frame(self.main_frame, bg="#eef6ff")
        body.pack(fill="both", expand=True, padx=30, pady=25)

        left_panel = tk.Frame(
            body,
            bg="white",
            highlightthickness=1,
            highlightbackground="#bfd9ec"
        )
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))

        right_panel = tk.Frame(
            body,
            bg="white",
            highlightthickness=1,
            highlightbackground="#bfd9ec"
        )
        right_panel.pack(side="left", fill="y")

        tk.Label(
            left_panel,
            text="Imagen seleccionada",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#16354a"
        ).pack(pady=(20, 15))

        self.viewer_frame = tk.Frame(
            left_panel,
            width=760,
            height=380,
            bg="#f7fbff",
            highlightthickness=1,
            highlightbackground="#c7dceb"
        )
        self.viewer_frame.pack(padx=25, pady=10)
        self.viewer_frame.pack_propagate(False)

        self.image_label = tk.Label(
            self.viewer_frame,
            text="Aquí aparecerá la imagen cargada",
            font=("Arial", 14),
            bg="#f7fbff",
            fg="#4b6a7f",
            justify="center"
        )
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(
            left_panel,
            text="Cargar imagen",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            bg="#2d6ea3",
            fg="white",
            activebackground="#1f5681",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self._load_image
        ).pack(pady=15)

        self.result_frame = tk.Frame(
            left_panel,
            bg="white",
            highlightthickness=1,
            highlightbackground="#cfe3f1"
        )
        self.result_frame.pack(fill="x", padx=25, pady=(10, 20))

        self.result_title = tk.Label(
            self.result_frame,
            text="Resultado del reconocimiento",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#16354a"
        )
        self.result_title.pack(anchor="w", padx=15, pady=(10, 5))

        self.result_content = tk.Text(
            self.result_frame,
            height=9,
            font=("Arial", 11),
            bg="white",
            fg="#35576e",
            wrap="word",
            bd=0
        )
        self.result_content.pack(fill="x", padx=15, pady=(0, 15))

        self.result_content.insert("1.0", "Aún no se ha realizado el reconocimiento.")
        self.result_content.config(state="disabled")

        tk.Label(
            right_panel,
            text="Guía visual",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#16354a"
        ).pack(pady=(20, 18))

        self._create_question_block(
            right_panel,
            "¿La nube se ve densa y oscura?",
            self.density_var
        )

        self._create_question_block(
            right_panel,
            "¿Tiene gran desarrollo vertical?",
            self.vertical_var
        )

        self._create_question_block(
            right_panel,
            "¿Cubre gran parte del cielo como capa?",
            self.coverage_var

        )

        self._create_question_block(
            right_panel,
            "¿Tiene bordes definidos o forma clara?",
            self.shape_var
        )

        self._create_question_block(
            right_panel,
            "¿Se ve alta y delgada como pluma?",
            self.high_thin_var
        )

        tk.Button(
            right_panel,
            text="Analizar",
            font=("Arial", 12, "bold"),
            width=18,
            height=2,
            bg="#3f8754",
            fg="white",
            activebackground="#2f6a41",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self._analyze_cloud
        ).pack(pady=(15, 6))

        tk.Button(
            right_panel,
            text="Comparar con IA",
            font=("Arial", 12, "bold"),
            width=18,
            height=2,
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self._compare_with_ai
        ).pack(pady=(0, 6))

        tk.Button(
            right_panel,
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
        ).pack(pady=(0, 10))

    def _create_question_block(self, parent, question_text, variable):
        block = tk.Frame(parent, bg="#f8fbff", highlightthickness=1, highlightbackground="#d7e8f5")
        block.pack(fill="x", padx=20, pady=8)

        tk.Label(
            block,
            text=question_text,
            font=("Arial", 11, "bold"),
            bg="#f8fbff",
            fg="#35576e",
            wraplength=250,
            justify="left"
        ).pack(anchor="w", padx=12, pady=(10, 6))

        options = tk.Frame(block, bg="#f8fbff")
        options.pack(anchor="w", padx=12, pady=(0, 10))

        tk.Radiobutton(
            options, text="Sí", variable=variable, value="si",
            bg="#f8fbff", font=("Arial", 10)
        ).pack(side="left", padx=(0, 15))

        tk.Radiobutton(
            options, text="No", variable=variable, value="no",
            bg="#f8fbff", font=("Arial", 10)
        ).pack(side="left")

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

        try:
            image = Image.open(file_path)

            viewer_width = 760
            viewer_height = 380
            padding = 16

            max_width = viewer_width - padding
            max_height = viewer_height - padding

            img_width, img_height = image.size
            ratio = min(max_width / img_width, max_height / img_height)

            new_width = max(1, int(img_width * ratio))
            new_height = max(1, int(img_height * ratio))

            image = image.resize((new_width, new_height), Image.LANCZOS)

            self.image_preview = ImageTk.PhotoImage(image)

            self.image_label.config(image=self.image_preview, text="")
            self.image_label.image = self.image_preview
            self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cargar la imagen.\n{error}")


    def _analyze_cloud(self):
        if not self.selected_image_path:
            messagebox.showwarning("Falta imagen", "Primero debes cargar una imagen.")
            return

        density = self.density_var.get()
        vertical = self.vertical_var.get()
        coverage = self.coverage_var.get()
        shape = self.shape_var.get()
        high_thin = self.high_thin_var.get()

        if not density or not vertical or not coverage or not shape or not high_thin:
            messagebox.showwarning("Faltan datos", "Debes responder todas las preguntas.")
            return
        
        
        result = self._get_suggestion(density, vertical, coverage, shape, high_thin)
        cloud_name = result["name"]

        cloud = get_cloud_by_name(cloud_name)

        if cloud:
            text = f"Nube probable: {cloud['name']}\n"
            text += f"Confianza: {result['confidence']}\n"
            text += f"Razón: {result['reason']}\n\n"
            if result["alternatives"]:
                text += f"También podría parecerse a: {', '.join(result['alternatives'])}\n"

            text += "\n"
            text += f"Definición: {cloud['definition']}\n\n"
            text += f"Apariencia: {cloud.get('appearance', 'No disponible')}\n\n"
            text += f"Altitud: {cloud['altitude']}"
        else:
            text = f"Nube probable: {cloud_name}\n"
            text += f"Confianza: {result['confidence']}\n"
            text += f"Razón: {result['reason']}\n\n"
            if result["alternatives"]:
                text += f"También podría parecerse a: {', '.join(result['alternatives'])}\n"

            text += "\n"
            text += "No hay datos específicos disponibles para esta combinación."

        self.result_content.config(state="normal")
        self.result_content.delete("1.0", "end")
        self.result_content.insert("1.0", text)
        self.result_content.config(state="disabled")

    def _compare_with_ai(self):
        if not self.selected_image_path:
            messagebox.showwarning("Falta imagen", "Primero debes cargar una imagen.")
            return

        try:
            result = predict_cloud(self.selected_image_path)

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
            confidence_percent = result["confidence"] * 100

            ai_text = (
                "\n\n--- Comparación con IA ---\n"
                f"Resultado IA: {cloud_name} ({result['code']})\n"
                f"Confianza IA: {confidence_percent:.2f}%"
            )

            self.result_content.config(state="normal")
            self.result_content.insert("end", ai_text)
            self.result_content.config(state="disabled")

        except Exception as error:
            messagebox.showerror("Error IA", f"No se pudo comparar con IA.\n{error}")

    def _get_suggestion(self, density, vertical, coverage, shape, high_thin):
        scores = {
            "Cumulonimbus": 0,
            "Cumulus": 0,
            "Cirrus": 0,
            "Nimbostratus": 0,
            "Stratus": 0,
            "Altocumulus": 0,
            "Stratocumulus": 0
        }

        reasons = {
            "Cumulonimbus": [],
            "Cumulus": [],
            "Cirrus": [],
            "Nimbostratus": [],
            "Stratus": [],
            "Altocumulus": [],
            "Stratocumulus": []
        }

        if density == "si":
            scores["Cumulonimbus"] += 2
            scores["Nimbostratus"] += 2
            scores["Stratocumulus"] += 1
            reasons["Cumulonimbus"].append("se ve densa u oscura")
            reasons["Nimbostratus"].append("se ve densa u oscura")

        if vertical == "si":
            scores["Cumulonimbus"] += 3
            scores["Cumulus"] += 3
            reasons["Cumulonimbus"].append("tiene desarrollo vertical")
            reasons["Cumulus"].append("tiene desarrollo vertical")

        if coverage == "si":
            scores["Nimbostratus"] += 3
            scores["Stratus"] += 3
            scores["Stratocumulus"] += 2
            reasons["Nimbostratus"].append("cubre gran parte del cielo")
            reasons["Stratus"].append("cubre gran parte del cielo")

        if shape == "si":
            scores["Cumulus"] += 2
            scores["Altocumulus"] += 2
            scores["Stratocumulus"] += 1
            reasons["Cumulus"].append("presenta forma o bordes definidos")
            reasons["Altocumulus"].append("presenta elementos definidos")

        if high_thin == "si":
            scores["Cirrus"] += 5
            reasons["Cirrus"].append("se ve alta y delgada, tipo pluma")

        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        main_name = ranked[0][0]
        main_score = ranked[0][1]

        if main_score >= 5:
            confidence = "Alta"
        elif main_score >= 3:
            confidence = "Media"
        else:
            confidence = "Baja"

        main_reasons = reasons.get(main_name, [])
        reason_text = ", ".join(main_reasons) if main_reasons else "coincide parcialmente con las respuestas dadas"

        alternatives = [name for name, score in ranked[1:4] if score > 0]

        return {
            "name": main_name,
            "confidence": confidence,
            "reason": reason_text,
            "alternatives": alternatives
        }
    def _go_home(self):
        self.destroy()
        self.go_home_callback()