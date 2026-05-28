import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import threading

from config import *
from services.validaciones_service import validar_archivo


class ValidacionView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.df_errores = pd.DataFrame()

        self.configure(
            fg_color="transparent"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.crear_header()
        self.crear_dashboard()
        self.crear_tabla()
        self.crear_footer()

    # =================================================
    # HEADER
    # =================================================

    def crear_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD,
            corner_radius=15,
            height=90
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(20, 10)
        )

        titulo = ctk.CTkLabel(
            header,
            text="Validador de Cuestionarios ENAPROCE",
            font=(FONT, 28, "bold"),
            text_color=COLOR_TEXTO
        )

        titulo.pack(anchor="w", padx=25, pady=(15, 0))

        subtitulo = ctk.CTkLabel(
            header,
            text="Instituto Nacional de Estadística y Geografía",
            font=(FONT, 14),
            text_color=COLOR_GRIS
        )

        subtitulo.pack(anchor="w", padx=25)

    # =================================================
    # DASHBOARD
    # =================================================

    def crear_dashboard(self):

        dashboard = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        dashboard.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=10
        )

        dashboard.grid_columnconfigure((0,1,2), weight=1)

        self.card_registros = self.crear_card(
            dashboard,
            "Registros",
            0,
            0
        )

        self.card_errores = self.crear_card(
            dashboard,
            "Errores",
            0,
            1
        )

        self.card_variables = self.crear_card(
            dashboard,
            "Variables con error",
            0,
            2
        )

    # =================================================
    # CARD
    # =================================================

    def crear_card(self, parent, titulo, valor, columna):

        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD,
            corner_radius=15,
            height=120
        )

        card.grid(
            row=0,
            column=columna,
            sticky="ew",
            padx=10
        )

        label_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=(FONT, 15),
            text_color=COLOR_GRIS
        )

        label_titulo.pack(anchor="w", padx=20, pady=(20, 5))

        label_valor = ctk.CTkLabel(
            card,
            text=str(valor),
            font=(FONT, 32, "bold"),
            text_color=COLOR_PRINCIPAL
        )

        label_valor.pack(anchor="w", padx=20)

        return label_valor

    # =================================================
    # TABLA
    # =================================================

    def crear_tabla(self):

        frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD,
            corner_radius=15
        )

        frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 10)
        )

        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # TOPBAR
        topbar = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        topbar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=20
        )

        # BOTON CARGAR
        btn_cargar = ctk.CTkButton(
            topbar,
            text="📂 Seleccionar Excel",
            fg_color=COLOR_PRINCIPAL,
            hover_color=COLOR_SECUNDARIO,
            height=42,
            width=220,
            font=(FONT, 14, "bold"),
            command=self.cargar_archivo
        )

        btn_cargar.pack(side="left", padx=5)

        # BOTON EXPORTAR
        btn_exportar = ctk.CTkButton(
            topbar,
            text="⬇ Descargar errores",
            fg_color="#1F6AA5",
            hover_color="#144870",
            height=42,
            width=220,
            font=(FONT, 14, "bold"),
            command=self.exportar_excel
        )

        btn_exportar.pack(side="left", padx=5)

        # BUSCADOR
        self.entry_buscar = ctk.CTkEntry(
            topbar,
            placeholder_text="Buscar variable...",
            width=250,
            height=40
        )

        self.entry_buscar.pack(side="right")

        # TABLA
        columnas = ("ID_CAT_ENCUESTAS_INFO", "vector", "variable", "mensaje")

        self.tabla = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings"
        )

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.column("ID_CAT_ENCUESTAS_INFO", width=120)
        self.tabla.column("vector", width=120)
        self.tabla.column("variable", width=220)
        self.tabla.column("mensaje", width=650)

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabla.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(20,0),
            pady=(0,10)
        )

        scrollbar.grid(
            row=1,
            column=1,
            sticky="ns",
            pady=(0,10)
        )

        # ESTADO
        self.label_estado = ctk.CTkLabel(
            frame,
            text="Esperando archivo...",
            font=(FONT, 13),
            text_color=COLOR_GRIS
        )

        self.label_estado.grid(
            row=2,
            column=0,
            sticky="w",
            padx=25,
            pady=(0,10)
        )

        # PROGRESSBAR
        self.progress = ctk.CTkProgressBar(frame)

        self.progress.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0,20)
        )

        self.progress.set(0)

    # =================================================
    # FOOTER
    # =================================================

    def crear_footer(self):

        footer = ctk.CTkLabel(
            self,
            text="INEGI • Sistema de Validación • Versión 1.0",
            font=(FONT, 12),
            text_color=COLOR_GRIS
        )

        footer.grid(
            row=3,
            column=0,
            pady=(0,10)
        )

    # =================================================
    # CARGAR ARCHIVO
    # =================================================

    def cargar_archivo(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel", "*.xlsx")]
        )

        if not ruta:
            return

        self.label_estado.configure(
            text="Procesando archivo..."
        )

        hilo = threading.Thread(
            target=self.procesar_archivo,
            args=(ruta,),
            daemon=True
        )

        hilo.start()

    # =================================================
    # PROCESAR
    # =================================================

    def procesar_archivo(self, ruta):

        try:

            df, df_errores = validar_archivo(ruta)

            self.after(
                0,
                lambda: self.finalizar_proceso(
                    df,
                    df_errores
                )
            )

        except Exception as e:

            self.after(
                0,
                lambda: messagebox.showerror(
                    "Error",
                    str(e)
                )
            )

    # =================================================
    # FINALIZAR
    # =================================================

    def finalizar_proceso(self, df, df_errores):

        self.df_errores = df_errores

        self.actualizar_tabla()

        total_registros = len(df)
        total_errores = len(df_errores)

        total_variables = 0

        if not df_errores.empty:

            total_variables = df_errores["variable"].nunique()

        self.card_registros.configure(
            text=str(total_registros)
        )

        self.card_errores.configure(
            text=str(total_errores)
        )

        self.card_variables.configure(
            text=str(total_variables)
        )

        self.progress.set(1)

        self.label_estado.configure(
            text=f"Errores encontrados: {total_errores}"
        )

        messagebox.showinfo(
            "Proceso terminado",
            f"Validación completada\nErrores encontrados: {total_errores}"
        )

    # =================================================
    # ACTUALIZAR TABLA
    # =================================================

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

    # =================================================
    # EXPORTAR
    # =================================================

    def exportar_excel(self):

        if self.df_errores.empty:

            messagebox.showwarning(
                "Sin datos",
                "No existen errores para exportar"
            )

            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")]
        )

        if not ruta:
            return

        self.df_errores.to_excel(
            ruta,
            index=False
        )

        messagebox.showinfo(
            "Exportado",
            "Archivo exportado correctamente"
        )