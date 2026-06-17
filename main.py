import customtkinter as ctk
from app.ui.login_view import LoginView
from app.utils.path_utils import resource_path
import sys
sys.setrecursionlimit(10000)


def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("Validador ENAPROCE")
    app.geometry("650x520")

    try:
        app.iconbitmap(resource_path("assets/icons/Designer.ico"))
    except:
        pass

    login = LoginView(app)
    login.pack(fill="both", expand=True)

    app.mainloop()


if __name__ == "__main__":
    main()