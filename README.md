📊 Validador de Vectores ENAPROCE 2026
Sistema de validación automatizada para los datos del cuestionario ENAPROCE 2026, diseñado para detectar inconsistencias estructurales, semánticas y de reglas en archivos Excel de vaciado.
________________________________________
🚀 Descripción
Este proyecto permite validar registros de la encuesta ENAPROCE mediante un motor de reglas combinado con técnicas de validación semántica.
El sistema:
•	✅ Valida consistencia entre variables
•	✅ Detecta errores en campos tipo “Otros (especifique)”
•	✅ Identifica textos redundantes usando similitud semántica
•	✅ Aplica reglas provenientes de vectores definidos externamente
•	✅ Presenta resultados en una interfaz gráfica interactiva
________________________________________
🧠 Características principales
🔹 1. Validación estructural
•	Campos requeridos
•	Formatos incorrectos
•	Relación entre variables
________________________________________
🔹 2. Validación de “Otros (Especifique)”
Detecta errores como:
•	❌ Se seleccionó “Otro” pero no se especificó texto
•	❌ Se escribió texto sin haber seleccionado “Otro” (extensible)
________________________________________
🔹 3. Validación semántica (IA ligera)
Usa embeddings con sentence-transformers para:
•	Detectar textos similares a opciones de catálogo
•	Evitar uso incorrecto de “Otros”
📌 Ejemplo:
Entrada	Resultado
"Banco" en campo "Otro"	❌ Error (debió usar catálogo)
"Inversionista extranjero"	✅ Válido
________________________________________
🔹 4. Motor de reglas dinámico
Las validaciones adicionales se ejecutan con base en un archivo externo:
Vectores_Enaproce_2026_220526.xlsx
Esto permite:
•	Escalabilidad
•	Configuración sin modificar código
•	Validaciones mantenibles
________________________________________
🔹 5. Interfaz gráfica (UI)
Desarrollada con CustomTkinter:
•	Carga de archivos Excel
•	Visualización de errores
•	Dashboard con métricas: 
o	Total de registros
o	Total de errores
o	Porcentaje de error
•	Exportación de resultados
________________________________________
🏗️ Arquitectura del proyecto
El sistema sigue una arquitectura por capas:
Vectores_ENAPROCE_2026/
│
├── views/
│   └── validacion_view.py      # Interfaz gráfica (UI)
│
├── services/
│   ├── validaciones_service.py # Orquestación del proceso
│   │
│   ├── rules/
│   │   ├── loader.py          # Carga de vectores
│   │   └── engine.py          # Motor de validación
│   │
│   ├── validators/
│   │   └── semantic.py        # Validación semántica
│   │
│   └── app_state.py           # Estado global de la app
│
├── data/
│   └── Vectores_Enaproce_2026.xlsx
│
└── main.py                    # Punto de entrada
________________________________________
🔧 Instalación
1. Clonar repositorio
Shell
git clone https://github.com/MAMaciasL/Vectores_ENAPROCE_2026-.git

Mostrar más líneas
________________________________________
2. Crear entorno virtual (opcional)
Shell
python -m venv venv
venv\Scripts\activate
Mostrar más líneas
________________________________________
3. Instalar dependencias
Shell
pip install pandas customtkinter sentence-transformers torch
Mostrar más líneas
________________________________________
▶️ Uso
Ejecuta el sistema:
Shell
python main.py
Mostrar más líneas
________________________________________
📂 Flujo de uso
1.	Seleccionar archivo Excel (vaciado ENAPROCE)
2.	Ejecutar validación
3.	Visualizar errores en tabla
4.	Exportar resultados (opcional)
________________________________________
📊 Tipos de validaciones implementadas
Tipo	Descripción
Estructural	Validación de integridad
Otros	Campos dependientes
Semántica	Similitud con catálogo
Reglas	Basadas en vectores
________________________________________
🧪 Ejemplo de validación semántica
Python
es_similar, opcion, score = es_semanticamente_similar(
"banco",
FUENTES_CAPITAL
)
Mostrar más líneas
Resultado:
(True, "Banco", 0.87)
________________________________________
⚙️ Configuración de catálogos
Los catálogos utilizados en validación semántica se definen como listas:
Python
FUENTES_CAPITAL = [
"Recursos propios",
"Banco",
"Familiares"
]
Mostrar más líneas
Y se asocian a variables:
Python
CATALOGOS_OTROS = {
"P2_9X": FUENTES_CAPITAL
}
Mostrar más líneas
________________________________________
📈 Métricas del sistema
El sistema calcula:
•	Total de registros
•	Total de errores
•	Porcentaje de error
•	Historial de validaciones
________________________________________
🧩 Posibles mejoras
•	✅ Autocorrección inteligente (Normalización)
•	✅ Sugerencias automáticas de catálogo
•	✅ Validación bidireccional en “Otros”
•	✅ Procesamiento batch
•	✅ Exportación enriquecida (reportes)
________________________________________
⚠️ Consideraciones
•	Los modelos de lenguaje se cargan una sola vez para eficiencia
•	La validación semántica puede ser costosa en datasets grandes
•	Se recomienda optimización futura con embeddings precargados
________________________________________
👨‍💻 Autor
Martin Alejandro Macías Lara
Enlace de Integración Estadística “C”
Cristina Sanchez Lara
Enlace de Integración Estadística "B”
________________________________________
📄 Licencia
Uso interno / INEGI
________________________________________
🚀 Conclusión
Este proyecto implementa un sistema completo de validación de datos estadísticos que combina:
•	reglas tradicionales
•	lógica de negocio
•	y técnicas modernas de NLP
para mejorar la calidad de la información capturada.

