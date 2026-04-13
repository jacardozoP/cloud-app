import tkinter as tk
from ui.home import HomeScreen
from ui.quiz import QuizScreen



def main():
    root = tk.Tk()
    root.title("AeroCloud System")
    root.state("zoomed")  # pantalla completa en Windows
    root.configure(bg="#d9ecff")

    app = HomeScreen(root)
    app.show()

    root.mainloop()


if __name__ == "__main__":
    main()