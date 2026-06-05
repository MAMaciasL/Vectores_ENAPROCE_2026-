import customtkinter as ctk

from views.login_view import LoginView

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()

app.title("Validador ENAPROCE")
app.geometry("650x520")

try:
    app.iconbitmap("assets/icons/Designer.ico")
except:
    pass

login = LoginView(app)
login.pack(fill="both", expand=True)

app.mainloop()