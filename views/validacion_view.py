import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import threading
import time

from config import *
from services.validaciones_service import validar_archivo
from services.app_state import AppState, guardar_historial


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
        self.aplicar_estado_actual()

        

        self.cargando = False
        self.progress.set(1)
        self.label_estado.configure(text=f"Errores encontrados: {AppState.total_errores}")

    # =========================
    def filtrar(self, texto):

        if AppState.resultados_actuales is None:
            return

        df = AppState.resultados_actuales
        base = "E_ENAPROCE_"

        if texto.strip() == "" or texto.strip() == base:
            self.df_errores = df
            self.actualizar_tabla()
            return

        if not texto.startswith(base):
            texto = base
            self.entry_buscar.delete(0, "end")
            self.entry_buscar.insert(0, texto)

        if texto.strip() == base:
            self.df_errores = df
            self.actualizar_tabla()
            return

        df_filtrado = df[
            df["Nombre Vector"].astype(str).str.contains(texto, case=False, na=False)
        ]

        self.df_errores = df_filtrado
        self.actualizar_tabla()

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
        self.card_porcentaje = self.crear_card(dashboard, "% Error", "0%", 2)

    def crear_card(self, parent, titulo, valor, columna):

        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=12)
        card.grid(row=0, column=columna, sticky="ew", padx=8, pady=5)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 24),
            text_color=COLOR_TEXTO
        ).pack(expand=True, pady=(15, 0))

        label_valor = ctk.CTkLabel(
            card,
            text=str(valor),
            font=("Arial", 20),
            text_color=COLOR_PRINCIPAL
        )
        label_valor.pack(expand=True, pady=(5, 15))

        return label_valor

    def crear_tabla(self):
        frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 10))

        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        topbar = ctk.CTkFrame(frame, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew", padx=15, pady=12)

        ctk.CTkButton(
            topbar,
            text="Seleccionar Excel",
            command=self.cargar_archivo
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            topbar,
            text="Exportar",
            command=self.exportar_excel
        ).pack(side="left", padx=5)

        self.entry_buscar = ctk.CTkEntry(topbar)
        self.entry_buscar.insert(0, "E_ENAPROCE_")
        self.entry_buscar.pack(side="right")

        self.entry_buscar.bind(
            "<KeyRelease>",
            lambda e: self.filtrar(self.entry_buscar.get())
        )

        columnas = ("ID", "Nombre Vector", "Variables Involucradas", "Procedimiento")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.grid(row=1, column=0, sticky="nsew", padx=(15,0), pady=(0,10))

        bottom = ctk.CTkFrame(frame, fg_color="transparent")
        bottom.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))

        bottom.grid_columnconfigure(1, weight=1)

        self.label_estado = ctk.CTkLabel(bottom, text="Esperando archivo...")
        self.label_estado.grid(row=0, column=0, sticky="w")

        self.progress = ctk.CTkProgressBar(bottom)
        self.progress.grid(row=0, column=1, sticky="ew", padx=10)
        self.progress.set(0)

    def finalizar_proceso(self, df, df_errores):

        self.df_errores = df_errores
        AppState.resultados_actuales = df_errores

        total_registros = len(df)
        total_errores = len(df_errores)

        if total_registros > 0:
            porcentaje_error = (total_errores / total_registros) * 100
        else:
            porcentaje_error = 0

        AppState.total_registros = total_registros
        AppState.total_errores = total_errores
        AppState.porcentaje_error = porcentaje_error
        self.actualizar_tabla()

        self.card_registros.configure(text=str(total_registros))
        self.card_errores.configure(text=str(total_errores))

        self.aplicar_estado_actual()

        self.cargando = False
        self.progress.stop()
        self.progress.set(1)

        fin = time.time()

        if not hasattr(AppState, "historial_reportes"):
            AppState.historial_reportes = []

        AppState.historial_reportes.append({
            "fecha": time.strftime("%d/%m/%Y %H:%M"),
            "archivo": AppState.archivo_actual,
            "registros": total_registros,
            "errores": total_errores,
            "correctos": total_registros - total_errores,
            "tiempo": round(fin - self.inicio_tiempo, 2)
        })

        guardar_historial(AppState.historial_reportes)
        self.update_idletasks()

    def actualizar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for _, fila in self.df_errores.iterrows():
            self.tabla.insert("", "end", values=(
                fila["ID_CAT_ENCUESTAS_INFO"],
                fila["Nombre Vector"],
                fila["Variables Involucradas"],
                str(fila["Procedimiento"])
            ))

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])

        if not ruta:
            return

        self.label_estado.configure(text="Procesando archivo...")

        self.inicio_tiempo = time.time()
        AppState.archivo_actual = ruta.split("/")[-1]

        threading.Thread(
            target=self.procesar_archivo,
            args=(ruta,),
            daemon=True
        ).start()

    def procesar_archivo(self, ruta):
        df, df_errores = validar_archivo(ruta)

        self.after(0, lambda: self.finalizar_proceso(df, df_errores))

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
        ).grid(row=3, column=0)

    def aplicar_estado_actual(self):

        total_registros = AppState.total_registros
        total_errores = AppState.total_errores
        porcentaje_error = getattr(AppState, "porcentaje_error", 0)

        # actualizar cards
        self.card_registros.configure(text=str(total_registros))
        self.card_errores.configure(text=str(total_errores))

        # color
        if porcentaje_error < 1:
            color = "#28a745"
        elif porcentaje_error < 5:
            color = "#ffc107"
        else:
            color = "#dc3545"

        self.card_porcentaje.configure(
            text=f"{porcentaje_error:.2f}%",
            text_color=color
        )

