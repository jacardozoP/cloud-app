import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
from io import BytesIO


class QuizScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#0f172a")
        self.app = app
        self.use_web = True  # cambiar a True cuando quieras usar Supabase/web
        self.web_dataset_cache = None
        self.next_question_cache = None
        self.image_cache = {}
        self.preloaded_image_cache = {}
        self.cloud_types = ["Ac", "As", "Cb", "Cc", "Ci", "Cs", "Ct", "Cu", "Ns", "Sc", "St"]

        self.type_map = {
            "Ac": "Altocumulus",
            "As": "Altostratus",
            "Cb": "Cumulonimbus",
            "Cc": "Cirrocumulus",
            "Cs": "Cirrostratus",
            "Ci": "Cirrus",
            "Ct": "Cirrus (Contrails)",
            "Cu": "Cumulus",
            "Ns": "Nimbostratus",
            "Sc": "Stratocumulus",
            "St": "Stratus"
        }

        self.cloud_info = {
            "Ac": "Altocumulus: nubes medias en parches o bandas, con elementos redondeados y cierta sombra.",
            "As": "Altostratus: capa media uniforme, grisácea, que cubre gran parte del cielo.",
            "Cb": "Cumulonimbus: nube de gran desarrollo vertical, asociada a tormentas y precipitación intensa.",
            "Cc": "Cirrocumulus: pequeñas nubes altas en patrón granular o aborregado, sin sombras marcadas.",
            "Ci": "Cirrus: nubes altas, delgadas y fibrosas, formadas principalmente por cristales de hielo.",
            "Cs": "Cirrostratus: velo fino y alto que puede producir halo alrededor del Sol o la Luna.",
            "Ct": "Cirrus homogenitus (contrails): estelas de condensación producidas por aeronaves a gran altitud, compuestas por cristales de hielo.",
            "Cu": "Cumulus: nube de desarrollo vertical, bordes definidos y aspecto algodonoso.",
            "Ns": "Nimbostratus: nube densa y extensa, asociada a precipitación continua.",
            "Sc": "Stratocumulus: nubes bajas en bloques, capas o rodillos con textura marcada.",
            "St": "Stratus: capa baja uniforme, de aspecto gris, que suele cubrir gran parte del cielo."
        }

        self.cloud_features = {
            "Ac": [
                "nubes medias",
                "aparecen en parches o bandas",
                "elementos redondeados",
                "pueden mostrar sombras"
            ],
            "As": [
                "capa media uniforme",
                "extensión amplia del cielo",
                "tono grisáceo",
                "aspecto continuo"
            ],
            "Cb": [
                "gran desarrollo vertical",
                "estructura densa y potente",
                "asociada a tormentas",
                "puede producir precipitación intensa"
            ],
            "Cc": [
                "nubes altas muy pequeñas",
                "patrón granular o aborregado",
                "sin sombras marcadas",
                "elementos muy finos"
            ],
            "Ci": [
                "nubes altas",
                "aspecto fibroso o filamentoso",
                "muy delgadas",
                "formadas por cristales de hielo"
            ],
            "Cs": [
                "velo fino y alto",
                "aspecto lechoso o transparente",
                "puede generar halo",
                "cubre gran parte del cielo"
            ],
            "Ct": [
                "estela producida por aeronaves",
                "trazo lineal en altura",
                "formada por cristales de hielo",
                "corresponde a cirrus homogenitus"
            ],
            "Cu": [
                "desarrollo vertical",
                "bordes bien definidos",
                "aspecto algodonoso",
                "nube individual o aislada"
            ],
            "Ns": [
                "nube densa y extensa",
                "cielo cubierto",
                "precipitación continua",
                "aspecto gris oscuro"
            ],
            "Sc": [
                "nubes bajas",
                "estructura en bloques o capas",
                "textura marcada",
                "cobertura fragmentada o en bancos"
            ],
            "St": [
                "capa baja uniforme",
                "aspecto gris continuo",
                "poca textura",
                "cielo cubierto sin desarrollo vertical"
            ]
        }

        # Ruta base del dataset del quiz
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dataset_path = os.path.join(base_dir, "dataset_original", "train")

        # Lista fija de clases esperadas
        self.cloud_types = ["Ac", "As", "Cb", "Cc", "Ci", "Cs", "Ct", "Cu", "Ns", "Sc", "St"]

        # Estado actual
        self.current_question = None
        self.current_image_tk = None
        self.answered = False

        self.build_ui()
        self.after(100, self.load_next_question)

    def load_web_dataset_cache(self):
        import requests

        if self.web_dataset_cache is not None:
            return self.web_dataset_cache

        url = "https://yuslpcidllsexfbncqpb.supabase.co/rest/v1/cloud_images"

        headers = {
            "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1c2xwY2lkbGxzZXhmYm5jcXBiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcyNDQyMzcsImV4cCI6MjA5MjgyMDIzN30.55AemrekkJznuHcFKHjhMh9dEYhabgi_C5B0BTfXCFk",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1c2xwY2lkbGxzZXhmYm5jcXBiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcyNDQyMzcsImV4cCI6MjA5MjgyMDIzN30.55AemrekkJznuHcFKHjhMh9dEYhabgi_C5B0BTfXCFk"
        }

        params = {
            "select": "cloud_type,image_url"
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        dataset = {}

        for row in data:
            cloud_type = row["cloud_type"]
            image_url = row["image_url"]

            if cloud_type not in dataset:
                dataset[cloud_type] = []

            dataset[cloud_type].append(image_url)

        self.web_dataset_cache = dataset
        return dataset

    def build_ui(self):
        title = tk.Label(
            self,
            text="Modo Quiz",
            font=("Arial", 22, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=(20, 10))

        subtitle = tk.Label(
            self,
            text="¿Qué tipo de nube es esta?",
            font=("Arial", 14),
            bg="#0f172a",
            fg="#cbd5e1"
        )
        subtitle.pack(pady=(0, 15))

        self.image_label = tk.Label(self, bg="#0f172a")
        self.image_label.config(
            text="Preparando quiz...",
            fg="white",
            font=("Arial", 12)
        )
        self.image_label.pack(pady=10)

        self.options_frame = tk.Frame(self, bg="#0f172a")
        self.options_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.options_frame,
                text="",
                font=("Arial", 11, "bold"),
                width=25,
                height=3,
                wraplength=180,
                justify="center",
                bg="#1e293b",
                fg="white",
                activebackground="#334155",
                activeforeground="white",
                relief="flat",
                command=lambda: None
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.option_buttons.append(btn)

        self.feedback_label = tk.Label(
            self,
            text="",
            font=("Arial", 1),
            bg="#0f172a",
            fg="#0f172a"
        )
        self.feedback_label.pack(pady=(0, 0))

        buttons_frame = tk.Frame(self, bg="#0f172a")
        buttons_frame.pack(pady=10)

        self.next_button = tk.Button(
            buttons_frame,
            text="Siguiente",
            font=("Arial", 12, "bold"),
            width=15,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            command=self.load_next_question,
            state="disabled"
        )

        self.back_button = tk.Button(
            buttons_frame,
            text="Volver",
            font=("Arial", 12, "bold"),
            width=15,
            bg="#475569",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            command=self.go_back
        )
        self.back_button.grid(row=0, column=0, padx=10)

    def go_back(self):
        self.destroy()
        if callable(self.app):
            self.app()
        else:
            messagebox.showinfo("Volver", "No se pudo regresar al menú principal.")

    def get_available_classes(self):
        valid_classes = []

        if not os.path.isdir(self.dataset_path):
            return valid_classes

        for cloud_type in self.cloud_types:
            class_path = os.path.join(self.dataset_path, cloud_type)
            if os.path.isdir(class_path):
                images = self.get_images_from_folder(class_path)
                if images:
                    valid_classes.append(cloud_type)

        return valid_classes
    
    def get_available_classes_web(self):
        dataset = self.load_web_dataset_cache()
        return list(dataset.keys())
    
    def get_images_by_class_web(self, cloud_type):
        dataset = self.load_web_dataset_cache()
        return dataset.get(cloud_type, [])

    def get_images_from_folder(self, folder_path):
        valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
        try:
            files = [
                f for f in os.listdir(folder_path)
                if f.lower().endswith(valid_extensions)
            ]
            return files
        except Exception:
            return []

    def generate_question(self):
        if self.use_web:
            available_classes = self.get_available_classes_web()
        else:
            available_classes = self.get_available_classes()

        if len(available_classes) < 4:
            return None

        correct_type = random.choice(available_classes)

        if self.use_web:
            images = self.get_images_by_class_web(correct_type)

            if not images:
                return None

            image_path = random.choice(images)

        else:
            class_folder = os.path.join(self.dataset_path, correct_type)

            images = self.get_images_from_folder(class_folder)
            if not images:
                return None

            image_file = random.choice(images)
            image_path = os.path.join(class_folder, image_file)

        wrong_options = random.sample(
            [c for c in available_classes if c != correct_type],
            3
        )

        options = [correct_type] + wrong_options
        random.shuffle(options)

        return {
            "image_path": image_path,
            "correct_type": correct_type,
            "options": options
        }
    
    def format_features(self, cloud_type):
        features = self.cloud_features.get(cloud_type, [])
        if not features:
            return "Sin rasgos definidos."
        return "\n".join([f"• {feature}" for feature in features[:3]])

    def build_feedback_text(self, selected_option, correct_type):
        correct_name = self.type_map.get(correct_type, correct_type)
        selected_name = self.type_map.get(selected_option, selected_option)

        correct_info = self.cloud_info.get(correct_type, "")
        correct_features = self.format_features(correct_type)

        if selected_option == correct_type:
            return (
                f"Correcto.\n"
                f"{correct_name}\n\n"
                f"{correct_info}\n\n"
                f"Rasgos clave:\n{correct_features}"
            )

        selected_features = self.format_features(selected_option)

        return (
            f"Incorrecto.\n"
            f"Elegiste: {selected_name}\n"
            f"Correcta: {correct_name}\n\n"
            f"¿Por qué la correcta es {correct_name}?\n"
            f"{correct_info}\n\n"
            f"Rasgos de la correcta:\n{correct_features}\n\n"
            f"Tu opción ({selected_name}) suele mostrar:\n{selected_features}"
        )
    
    def show_feedback_popup(self, selected_option, correct_type):
        popup = tk.Toplevel(self)
        popup.title("Resultado")
        popup.configure(bg="#0f172a")
        popup_width = 700
        popup_height = 500

        self.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (popup_width // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (popup_height // 2)

        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        correct_name = self.type_map.get(correct_type, correct_type)
        selected_name = self.type_map.get(selected_option, selected_option)

        feedback_text = self.build_feedback_text(selected_option, correct_type)

        title_text = "Correcto" if selected_option == correct_type else "Incorrecto"
        title_color = "#22c55e" if selected_option == correct_type else "#f87171"

        title_label = tk.Label(
            popup,
            text=title_text,
            font=("Arial", 20, "bold"),
            bg="#0f172a",
            fg=title_color
        )
        title_label.pack(pady=(20, 10))

        text_label = tk.Label(
            popup,
            text=feedback_text,
            font=("Arial", 12),
            bg="#0f172a",
            fg="white",
            wraplength=620,
            justify="left"
        )
        text_label.pack(padx=25, pady=15)

        continue_btn = tk.Button(
            popup,
            text="Siguiente pregunta",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            width=20,
            height=2,
            command=lambda: self.close_popup_and_continue(popup)
        )
        continue_btn.pack(pady=(20, 15))

        if self.app is not None:
            back_btn = tk.Button(
                popup,
                text="Cerrar",
                font=("Arial", 11, "bold"),
                bg="#475569",
                fg="white",
                activebackground="#334155",
                activeforeground="white",
                relief="flat",
                width=14,
                height=1,
                command=popup.destroy
            )
            back_btn.pack(pady=(0, 20))

    
    def close_popup_and_continue(self, popup):
        popup.destroy()
        self.load_next_question()

    def load_image(self, image_path):
        self.image_label.config(
            image="",
            text="Cargando imagen...",
            fg="white",
            font=("Arial", 12),
            bg="#0f172a"
        )

        if image_path.startswith("http"):

            if image_path in self.preloaded_image_cache:
                img = self.preloaded_image_cache.pop(image_path)
                self.image_cache[image_path] = img
                self.set_loaded_image(img)
                return
            # 🔥 CACHE
            if image_path in self.image_cache:
                self.set_loaded_image(self.image_cache[image_path])
                return

            thread = threading.Thread(
                target=self.load_image_from_url_thread,
                args=(image_path,),
                daemon=True
            )
            thread.start()
        else:
            self.load_image_from_local(image_path)

    def load_image_from_local(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((700, 450))
            self.current_image_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_image_tk, text="")
        except Exception as e:
            self.show_image_error(e)
    
    def load_image_from_url_thread(self, image_url):
        try:
            import requests

            response = requests.get(image_url, timeout=10)
            response.raise_for_status()

            img_data = BytesIO(response.content)

            with Image.open(img_data) as img:
                img = img.convert("RGB")
                img.thumbnail((700, 450))
                img_copy = img.copy()

            self.image_cache[image_url] = img_copy
            self.after(0, lambda: self.set_loaded_image(img_copy))

        except Exception as e:
            self.after(0, lambda: self.show_image_error(e))

    def preload_image(self, image_url):
        if not image_url.startswith("http"):
            return

        if image_url in self.image_cache:
            return

        if image_url in self.preloaded_image_cache:
            return

        def worker():
            try:
                import requests

                response = requests.get(image_url, timeout=10)
                response.raise_for_status()

                img_data = BytesIO(response.content)

                with Image.open(img_data) as img:
                    img = img.convert("RGB")
                    img.thumbnail((700, 450))
                    img_copy = img.copy()

                self.preloaded_image_cache[image_url] = img_copy

            except Exception:
                pass

        threading.Thread(target=worker, daemon=True).start()
    
    def set_loaded_image(self, img):
        self.current_image_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.current_image_tk, text="")
    
    def show_image_error(self, error):
        self.image_label.config(
            image="",
            text=f"No se pudo cargar la imagen.\n{error}",
            fg="white",
            font=("Arial", 12),
            bg="#0f172a"
        )

    def load_next_question(self):
        if self.next_question_cache:
            self.current_question = self.next_question_cache
        else:
            self.current_question = self.generate_question()

        # preparar la siguiente en segundo plano
        threading.Thread(target=self.preload_next_question, daemon=True).start()

        if not self.current_question:
            messagebox.showerror(
                "Error",
                "No se pudo generar una pregunta.\nRevisa que dataset_original/train tenga carpetas válidas con imágenes."
            )
            return

        self.answered = False
        self.feedback_label.config(text="", fg="#f8fafc")
        self.next_button.config(state="disabled")

        self.load_image(self.current_question["image_path"])

        for btn, option in zip(self.option_buttons, self.current_question["options"]):
            display_name = self.type_map.get(option, option)

            btn.option_code = option

            btn.config(
                text=display_name,
                state="normal",
                bg="#1e293b",
                fg="white",
                command=lambda opt=option: self.check_answer(opt)
            )

    def preload_next_question(self):
        try:
            question = self.generate_question()
            self.next_question_cache = question

            if question:
                self.preload_image(question["image_path"])

        except:
            self.next_question_cache = None

    def check_answer(self, selected_option):
        if self.answered:
            return

        self.answered = True
        correct_type = self.current_question["correct_type"]

        for btn in self.option_buttons:
            btn.config(state="disabled")

            btn_code = getattr(btn, "option_code", None)

            if btn_code == correct_type:
                btn.config(bg="#15803d")  # verde
            elif btn_code == selected_option and selected_option != correct_type:
                btn.config(bg="#b91c1c")  # rojo

        self.show_feedback_popup(selected_option, correct_type)

        self.next_button.config(state="normal")