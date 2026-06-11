import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import threading
import tkinter as tk

from config import *
from services.validaciones_service import validar_archivo
from services.app_state import AppState


class ValidacionView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.df_errores = pd.DataFrame()

        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.crear_header()
        self.crear_dashboard()
        self.crear_tabla()
        self.crear_footer()

        if AppState.resultados_actuales is not None:
            self.df_errores = AppState.resultados_actuales
            self.actualizar_tabla()

        self.card_registros.configure(text=str(AppState.total_registros))

        self.card_errores.configure(text=str(AppState.total_errores))

        self.card_variables.configure(text=str(AppState.total_variables))

        self.cargando = False
        self.progress.set(1)
        self.label_estado.configure(text=f"Errores encontrados: {AppState.total_errores}")

    # =========================
    # BUSCADOR
    # =========================
    def filtrar(self, texto):

        if AppState.resultados_actuales is None:
            return

        df = AppState.resultados_actuales
        base = "E_ENAPROCE_"

        if not texto.startswith(base):
            texto = base
            self.entry_buscar.delete(0, "end")
            self.entry_buscar.insert(0, texto)

        if texto.strip() == base:
            self.cargar_tabla(df)
            return

        df_filtrado = df[
            df["Nombre Vector"].astype(str).str.contains(texto, case=False, na=False)
        ]

        self.cargar_tabla(df_filtrado)

    def crear_header(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text="Validador de Vectores para Enaproce 2026",
            font=(FONT, 24, "bold"),
            text_color=COLOR_TITULOS,
            
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Carga el archivo vaciado de Excel para validar los vectores",
            font=("Arial", 18),
            text_color=COLOR_TITULOS
        ).pack(anchor="w")

    def crear_dashboard(self):

        dashboard = ctk.CTkFrame(self, fg_color="transparent")
        dashboard.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 10))

        dashboard.grid_columnconfigure((0, 1, 2), weight=1)

        self.card_registros = self.crear_card(dashboard, "Registros", 0, 0)
        self.card_errores = self.crear_card(dashboard, "Errores", 0, 1)
        self.card_variables = self.crear_card(dashboard, "Variables", 0, 2)

    def crear_card(self, parent, titulo, valor, columna):

        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=12)
        card.grid(row=0, column=columna, sticky="ew", padx=8, pady=5)

        ctk.CTkLabel(card,
        text=titulo,
        font=("Arial", 24),
        text_color=COLOR_TEXTO ).pack(expand=True, pady=(15, 0))

        label_valor = ctk.CTkLabel(
        card,
        text=str(valor),
        font=("Arial", 20),
        text_color=COLOR_PRINCIPAL)
        label_valor.pack(expand=True, pady=(5, 15))

        return label_valor

    def crear_tabla(self):

        frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 10))

        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        topbar = ctk.CTkFrame(frame, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew", padx=15, pady=12)

        ctk.CTkButton(topbar, text="Seleccionar Excel",
                      width=180, height=36,
                      fg_color=COLOR_PRINCIPAL,
                      command=self.cargar_archivo).pack(side="left", padx=5)

        ctk.CTkButton(topbar, text="Exportar",
                      width=120, height=36,
                      fg_color=COLOR_ACENTO,
                      command=self.exportar_excel).pack(side="left", padx=5)

        self.entry_buscar = ctk.CTkEntry(topbar, width=220, height=34)
        self.entry_buscar.insert(0, "E_ENAPROCE_")
        self.entry_buscar.pack(side="right")

        self.entry_buscar.bind(
            "<KeyRelease>",
            lambda e: self.filtrar(self.entry_buscar.get())
        )

        columnas = ("ID", "Nombre Vector", "Variables Involucradas", "Procedimiento")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(
                col,
                text=col,
                command=lambda c=col: self.mostrar_filtro(c)
            )

        self.tabla.column("ID", width=120)
        self.tabla.column("Nombre Vector", width=140)
        self.tabla.column("Variables Involucradas", width=300)
        self.tabla.column("Procedimiento", width=700)

        self.tabla.grid(row=1, column=0, sticky="nsew", padx=(15, 0), pady=(0, 10))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 10))
        self.tabla.configure(yscrollcommand=scrollbar.set)

        bottom = ctk.CTkFrame(frame, fg_color="transparent")
        bottom.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))

        self.label_estado = ctk.CTkLabel(bottom, text="Esperando archivo...")
        self.label_estado.pack(side="left")

        self.progress = ctk.CTkProgressBar(bottom)
        self.progress.pack(side="right", fill="x", expand=True, padx=10)
        self.progress.set(0)

    def mostrar_filtro(self, columna):

        if AppState.resultados_actuales is None:
            return

        df = AppState.resultados_actuales

        mapa = {
            "ID": "ID_CAT_ENCUESTAS_INFO",
            "Nombre Vector": "NOMBRE VECTOR",
            "Variables Involucradas": "VARIABLES INVOLUCRADAS",
            "Procedimiento": "PROCEDIMIENTO"
        }

        col_real = mapa[columna]
        valores = sorted(df[col_real].astype(str).unique())

        menu = tk.Menu(self, tearoff=0)
        vars_checks = {}

        def limpiar():
                self.cargar_tabla(df)

        menu.add_command(label="(Todos)", command=lambda: self.cargar_tabla(df))
        menu.add_separator()

        for v in valores:
            var = tk.BooleanVar(value=False)
            vars_checks[v] = var

            menu.add_checkbutton(
                label=str(v),
                variable=var
            )

        menu.add_separator()

        def aplicar():

            seleccionados = [v for v, var in vars_checks.items() if var.get()]

            if not seleccionados:
                self.cargar_tabla(df)
            else:
                filtrado = df[df[col_real].astype(str).isin(seleccionados)]
                self.cargar_tabla(filtrado)

        menu.add_command(label="Aplicar", command=aplicar)

        try:
            x = self.winfo_pointerx()
            y = self.winfo_pointery()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    def finalizar_proceso(self, df, df_errores):

        self.df_errores = df_errores
        AppState.resultados_actuales = df_errores
        AppState.total_registros =len(df)
        AppState.total_errores =len(df_errores)
        AppState.total_variables = df_errores["Variables Involucradas"].nunique() if not df_errores.empty else 0

        self.actualizar_tabla()

        self.card_registros.configure(text=str(len(df)))
        self.card_errores.configure(text=str(len(df_errores)))

        total_vars = df_errores["Variables Involucradas"].nunique() if not df_errores.empty else 0
        self.card_variables.configure(text=str(total_vars))

        self.cargando = False
        self.progress.stop()
        self.progress.set(1)

    def actualizar_tabla(self):

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for _, fila in self.df_errores.iterrows():
            self.tabla.insert("", "end", values=(
                fila["ID_CAT_ENCUESTAS_INFO"],
                fila["Nombre Vector"],
                fila["Variables Involucradas"],
                (str(fila["Procedimiento"]) [:120] + "..." if len(str(fila["Procedimiento"])) > 120 else str(fila["Procedimiento"]))
            ))

    def cargar_tabla(self, df):

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for _, fila in df.iterrows():
            self.tabla.insert("", "end", values=(
                fila["ID_CAT_ENCUESTAS_INFO"],
                fila["Nombre Vector"],
                fila["Variables Involucradas"],
                (str(fila["Procedimiento"]) [:120] + "..." if len(str(fila["Procedimiento"])) > 120 else str(fila["Procedimiento"]))
            ))

    # =========================
    def cargar_archivo(self):

        ruta = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])

        if not ruta:
            return

        self.label_estado.configure(text="Procesando archivo...")
        self.cargando = True
        self.progress.set(0)
        self.progress.start()

        threading.Thread(
            target=self.procesar_archivo,
            args=(ruta,),
            daemon=True
        ).start()

    def procesar_archivo(self, ruta):

        df, df_errores = validar_archivo(ruta)

        self.after(0, lambda:
        self.progress.set(0.6))
        self.after(0, lambda:
        self.finalizar_proceso(df, df_errores))
        

    def exportar_excel(self):

        if self.df_errores.empty:
            messagebox.showwarning("Sin datos", "No hay errores")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx")

        if ruta:
            self.df_errores.to_excel(ruta, index=False)
            messagebox.showinfo("Exportado", "Archivo exportado correctamente")     

    def crear_footer(self):

        ctk.CTkLabel(
            self,
            text="INEGI • Sistema de Validación v1.0"
        ).grid(row=3, column=0, pady=(0, 8))
