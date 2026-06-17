import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import threading
import time
from config import *
from app.services.validaciones_service import procesar_archivo_completo
from app.services.app_state import AppState
from app.repositories.historial_repo import guardar_historial


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

        columnas = ("Nombre Vector", "Variables Involucradas", "Procedimiento")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="tree headings")
        self.tabla.heading("#0", text="ID")
        self.tabla.column("#0", width=100)

        
        self.tabla.column("Nombre Vector", width=120, stretch=False)
        self.tabla.column("Variables Involucradas", width=180, stretch=False)
        self.tabla.column("Procedimiento", width=500, stretch=True)


        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.grid(row=1, column=0, sticky="nsew", padx=(15,0), pady=(0,10))

        bottom = ctk.CTkFrame(frame, fg_color="transparent")
        bottom.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))

        bottom.grid_columnconfigure(1, weight=1)
        
        scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(xscrollcommand=scroll_x.set)
        scroll_x.grid(row=3, column=0, sticky="ew", padx=(15,0))

        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_detalle)


        self.label_estado = ctk.CTkLabel(bottom, text="Esperando archivo...")
        self.label_estado.grid(row=0, column=0, sticky="w")

        self.progress = ctk.CTkProgressBar(bottom)
        self.progress.grid(row=0, column=1, sticky="ew", padx=10)
        self.progress.set(0)

    def finalizar_proceso(self, resultado):

        df = resultado["df"]
        df_errores = resultado["df_errores"]
        total_registros = resultado["total_registros"]
        total_errores = resultado["total_errores"]
        porcentaje_error = resultado["porcentaje_error"]

        self.df_errores = df_errores
        AppState.resultados_actuales = df_errores

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

        self.update_idletasks()
        
        self.label_estado.configure(
            text=f"✅ Finalizado | Registros: {total_registros} | Errores: {total_errores}"
        )


    def actualizar_tabla(self):

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        if self.df_errores.empty:
            return

        df = self.df_errores.sort_values(
            by=["ID_CAT_ENCUESTAS_INFO", "Nombre Vector"]
        )

        grupos = {}

        for _, fila in df.iterrows():

            id_val = fila["ID_CAT_ENCUESTAS_INFO"]

            if id_val not in grupos:
                grupos[id_val] = self.tabla.insert(
                    "",
                    "end",
                    text=f"ID: {id_val}",
                    values=("", "", "")
                )

            self.tabla.insert(
                grupos[id_val],
                "end",
                text="",
                values=(
                    fila["Nombre Vector"],
                    fila["Variables Involucradas"],
                    fila["Procedimiento"]
                )
            )

        for item in self.tabla.get_children():
            self.tabla.item(item, open=True)


    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])

        if not ruta:
            return

        self.label_estado.configure(text="Procesando archivo...")
        self.progress.set(0.2)
        self.progress.start()

        self.update_idletasks()

        self.inicio_tiempo = time.time()
        AppState.archivo_actual = ruta.split("/")[-1]

        threading.Thread(
            target=self.procesar_archivo,
            args=(ruta,),
            daemon=True
        ).start()
    def procesar_archivo(self, ruta):
    
        resultado = procesar_archivo_completo(ruta)
    
        self.after(0, lambda: self.finalizar_proceso(resultado))
    

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

    def mostrar_detalle(self, event):

        selected = self.tabla.selection()

        if not selected:
            return

        item = selected[0]

        valores = self.tabla.item(item, "values")

        if not valores or all(v == "" for v in valores):
            return
        
        id = valores[0]
        nombre = valores[1]
        variables = valores[2]
        procedimiento = valores[3]

        ventana = ctk.CTkToplevel(self)
        ventana.title("Detalle del error")
        ventana.geometry("600x400")

        ctk.CTkLabel(
            ventana, text="ID", font=(FONT, 14, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 0))

        ctk.CTkLabel(
            ventana, text=id, wraplength=550
        ).pack(anchor="w", padx=10)

        ctk.CTkLabel(
            ventana, text="Nombre Vector", font=(FONT, 14, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 0))

        ctk.CTkLabel(
            ventana, text=nombre, wraplength=550
        ).pack(anchor="w", padx=10)

        ctk.CTkLabel(
            ventana, text="Variables", font=(FONT, 14, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 0))

        ctk.CTkLabel(
            ventana, text=variables, wraplength=550
        ).pack(anchor="w", padx=10)

        ctk.CTkLabel(
            ventana, text="Procedimiento", font=(FONT, 14, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 0))

        textbox = ctk.CTkTextbox(ventana, width=580, height=200)
        textbox.pack(padx=10, pady=5)

        textbox.insert("1.0", procedimiento)
        textbox.configure(state="disabled")