import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import threading

from config import *
from services.validaciones_service import validar_archivo
from services.historial_service import guardar_historial


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

    # =========================
    # HEADER
    # =========================
    def crear_header(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text="Validador Vectores ENAPROCE",
            font=(FONT, 28, "bold"),
            text_color=COLOR_TITULOS
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Carga un archivo de Excel para validar los vectores y variables",
            font=(FONT, 18, "arial"),
            text_color=COLOR_TITULOS
        ).pack(anchor="w")

    # =========================
    # DASHBOARD
    # =========================
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

        ctk.CTkLabel(
            card,
            text=titulo,
            font=(FONT, 13),
            text_color=COLOR_GRIS
        ).pack(anchor="w", padx=15, pady=(10, 2))

        label_valor = ctk.CTkLabel(
            card,
            text=str(valor),
            font=(FONT, 26, "bold"),
            text_color=COLOR_PRINCIPAL
        )
        label_valor.pack(anchor="w", padx=15, pady=(0, 10))

        return label_valor

    # =========================
    # TABLA
    # =========================
    def crear_tabla(self):

        frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 10))

        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # TOPBAR
        topbar = ctk.CTkFrame(frame, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew", padx=15, pady=12)

        # BOTONES
        ctk.CTkButton(
            topbar,
            text="Seleccionar Excel",
            width=180,
            height=36,
            fg_color=COLOR_PRINCIPAL,
            hover_color=COLOR_SECUNDARIO,
            command=self.cargar_archivo
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            topbar,
            text="Exportar",
            width=120,
            height=36,
            fg_color=COLOR_ACENTO,
            hover_color="#144870",
            command=self.exportar_excel
        ).pack(side="left", padx=5)

        # BUSCADOR
        self.entry_buscar = ctk.CTkEntry(
            topbar,
            placeholder_text="Buscar...",
            width=220,
            height=34
        )
        self.entry_buscar.pack(side="right")

        # TABLA
        columnas = ("ID", "Vector", "Variable", "Mensaje")

        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.column("ID", width=120)
        self.tabla.column("Vector", width=120)
        self.tabla.column("Variable", width=200)
        self.tabla.column("Mensaje", width=500)

        self.tabla.grid(row=1, column=0, sticky="nsew", padx=(15, 0), pady=(0, 10))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 10))

        self.tabla.configure(yscrollcommand=scrollbar.set)

        # FOOTER INTERNO
        bottom = ctk.CTkFrame(frame, fg_color="transparent")
        bottom.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))

        self.label_estado = ctk.CTkLabel(
            bottom,
            text="Esperando archivo...",
            font=(FONT, 12),
            text_color=COLOR_GRIS
        )
        self.label_estado.pack(side="left")

        self.progress = ctk.CTkProgressBar(bottom)
        self.progress.pack(side="right", fill="x", expand=True, padx=10)
        self.progress.set(0)

    # =========================
    # FOOTER
    # =========================
    def crear_footer(self):

        ctk.CTkLabel(
            self,
            text="INEGI • Sistema de Validación V1.0",
            font=(FONT, 11),
            text_color=COLOR_GRIS
        ).grid(row=3, column=0, pady=(0, 8))

    # =========================
    # CARGAR ARCHIVO
    # =========================
    def cargar_archivo(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel", "*.xlsx")]
        )

        if not ruta:
            return

        self.label_estado.configure(text="Procesando archivo...")
        self.progress.set(0.3)

        hilo = threading.Thread(
            target=self.procesar_archivo,
            args=(ruta,),
            daemon=True
        )
        hilo.start()

    # =========================
    # PROCESAR
    # =========================
    def procesar_archivo(self, ruta):

        try:
            df, df_errores = validar_archivo(ruta)

            self.after(0, lambda: self.finalizar_proceso(df, df_errores))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))

    # =========================
    # FINALIZAR
    # =========================
    def finalizar_proceso(self, df, df_errores):

        self.df_errores = df_errores
        self.actualizar_tabla()

        self.card_registros.configure(text=str(len(df)))
        self.card_errores.configure(text=str(len(df_errores)))

        total_vars = df_errores["variable"].nunique() if not df_errores.empty else 0
        self.card_variables.configure(text=str(total_vars))

        self.progress.set(1)
        self.label_estado.configure(text=f"Errores encontrados: {len(df_errores)}")

    # =========================
    # TABLA
    # =========================
    def actualizar_tabla(self):

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for _, fila in self.df_errores.iterrows():
            self.tabla.insert(
                "",
                "end",
                values=(
                    fila["ID_CAT_ENCUESTAS_INFO"],
                    fila["vector"],
                    fila["variable"],
                    fila["mensaje"]
                )
            )

    # =========================
    # EXPORTAR
    # =========================
    def exportar_excel(self):

        if self.df_errores.empty:
            messagebox.showwarning("Sin datos", "No hay errores")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx")

        if not ruta:
            return

        self.df_errores.to_excel(ruta, index=False)
        messagebox.showinfo("Exportado", "Archivo exportado correctamente")