
import os
import sys
import math
import importlib
import importlib.util
import customtkinter as ctk
from tkinter import messagebox

RUTA_BACKEND = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Jacobi-Gauss-Seidel"
)

RUTA_INIT = os.path.join(RUTA_BACKEND, "__init__.py")

if not os.path.isfile(RUTA_INIT):
    raise FileNotFoundError(
        f"No se encontró el archivo __init__.py en: {RUTA_INIT}"
    )

NOMBRE_PAQUETE = "jacobi_gauss_seidel"

spec = importlib.util.spec_from_file_location(
    NOMBRE_PAQUETE,
    RUTA_INIT,
    submodule_search_locations=[RUTA_BACKEND]
)

if spec is None or spec.loader is None:
    raise ImportError("No se pudo cargar el paquete del backend.")

paquete = importlib.util.module_from_spec(spec)
sys.modules[NOMBRE_PAQUETE] = paquete
spec.loader.exec_module(paquete)

ver = importlib.import_module(f"{NOMBRE_PAQUETE}.verificacion")
conv = importlib.import_module(f"{NOMBRE_PAQUETE}.conversiones")
op = importlib.import_module(f"{NOMBRE_PAQUETE}.operaciones")
sol = importlib.import_module(f"{NOMBRE_PAQUETE}.solucion")
vis = importlib.import_module(f"{NOMBRE_PAQUETE}.visualizacion")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AppCalculadoraJacobiGaussSeidel(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Calculadora Jacobi y Gauss-Seidel")
        self.geometry("1150x800")
        self.minsize(900, 650)

        self.campos_matriz = []
        self.campos_b = []
        self.campos_x0 = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.crear_interfaz()
        self.generar_campos()

    def crear_interfaz(self):
        self.frame_superior = ctk.CTkFrame(self)
        self.frame_superior.grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 10),
            sticky="ew"
        )

        self.frame_superior.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_superior,
            text="CALCULADORA DE MÉTODOS ITERATIVOS",
            font=ctk.CTkFont(size=22, weight="bold")
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            self.frame_superior,
            text="Dimensión del sistema:"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        self.entrada_dimension = ctk.CTkEntry(
            self.frame_superior,
            width=100,
            justify="center"
        )
        self.entrada_dimension.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky="w"
        )
        self.entrada_dimension.insert(0, "3")

        ctk.CTkButton(
            self.frame_superior,
            text="Generar matriz",
            command=self.generar_campos
        ).grid(
            row=1,
            column=2,
            padx=10,
            pady=10
        )

        self.frame_central = ctk.CTkScrollableFrame(
            self,
            label_text="Datos del sistema de ecuaciones"
        )
        self.frame_central.grid(
            row=1,
            column=0,
            padx=15,
            pady=5,
            sticky="nsew"
        )

        self.frame_inferior = ctk.CTkFrame(self)
        self.frame_inferior.grid(
            row=2,
            column=0,
            padx=15,
            pady=10,
            sticky="ew"
        )

        self.frame_inferior.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1
        )

        ctk.CTkLabel(
            self.frame_inferior,
            text="Método:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=(12, 5)
        )

        self.menu_metodo = ctk.CTkOptionMenu(
            self.frame_inferior,
            values=["Jacobi", "Gauss-Seidel"],
            width=150
        )
        self.menu_metodo.grid(
            row=1,
            column=0,
            padx=10,
            pady=(5, 12)
        )

        ctk.CTkLabel(
            self.frame_inferior,
            text="Formato:"
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=(12, 5)
        )

        self.menu_formato = ctk.CTkOptionMenu(
            self.frame_inferior,
            values=["Decimal", "Fracción"],
            width=150
        )
        self.menu_formato.grid(
            row=1,
            column=1,
            padx=10,
            pady=(5, 12)
        )

        ctk.CTkLabel(
            self.frame_inferior,
            text="Tolerancia:"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=(12, 5)
        )

        self.entrada_tolerancia = ctk.CTkEntry(
            self.frame_inferior,
            width=150,
            justify="center"
        )
        self.entrada_tolerancia.grid(
            row=1,
            column=2,
            padx=10,
            pady=(5, 12)
        )
        self.entrada_tolerancia.insert(0, "0.000001")

        ctk.CTkLabel(
            self.frame_inferior,
            text="Máximo de iteraciones:"
        ).grid(
            row=0,
            column=3,
            padx=10,
            pady=(12, 5)
        )

        self.entrada_iteraciones = ctk.CTkEntry(
            self.frame_inferior,
            width=150,
            justify="center"
        )
        self.entrada_iteraciones.grid(
            row=1,
            column=3,
            padx=10,
            pady=(5, 12)
        )
        self.entrada_iteraciones.insert(0, "100")

        self.frame_botones = ctk.CTkFrame(self)
        self.frame_botones.grid(
            row=3,
            column=0,
            padx=15,
            pady=(5, 10),
            sticky="nsew"
        )

        self.frame_botones.grid_columnconfigure(0, weight=1)
        self.frame_botones.grid_rowconfigure(1, weight=1)

        self.frame_acciones = ctk.CTkFrame(
            self.frame_botones,
            fg_color="transparent"
        )
        self.frame_acciones.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        ctk.CTkButton(
            self.frame_acciones,
            text="Calcular",
            width=150,
            command=self.calcular
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        ctk.CTkButton(
            self.frame_acciones,
            text="Limpiar",
            width=150,
            fg_color="#555555",
            hover_color="#333333",
            command=self.limpiar
        ).grid(
            row=0,
            column=1,
            padx=10
        )

        self.salida = ctk.CTkTextbox(
            self.frame_botones,
            wrap="word",
            font=ctk.CTkFont(family="Consolas", size=13)
        )
        self.salida.grid(
            row=1,
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="nsew"
        )

    def generar_campos(self):
        try:
            dimension = int(self.entrada_dimension.get())

            if dimension < 2 or dimension > 10:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Dimensión inválida",
                "Introduce una dimensión entera entre 2 y 10."
            )
            return

        for widget in self.frame_central.winfo_children():
            widget.destroy()

        self.campos_matriz = []
        self.campos_b = []
        self.campos_x0 = []

        ctk.CTkLabel(
            self.frame_central,
            text="Matriz de coeficientes A",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(
            row=0,
            column=0,
            columnspan=dimension,
            padx=10,
            pady=10
        )

        for i in range(dimension):
            fila = []

            for j in range(dimension):
                entrada = ctk.CTkEntry(
                    self.frame_central,
                    width=85,
                    justify="center"
                )
                entrada.grid(
                    row=i + 1,
                    column=j,
                    padx=4,
                    pady=4
                )
                fila.append(entrada)

            self.campos_matriz.append(fila)

        columna_b = dimension + 1
        columna_x0 = dimension + 2

        ctk.CTkLabel(
            self.frame_central,
            text="Vector independiente b",
            font=ctk.CTkFont(size=15, weight="bold")
        ).grid(
            row=0,
            column=columna_b,
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            self.frame_central,
            text="Vector inicial x₀",
            font=ctk.CTkFont(size=15, weight="bold")
        ).grid(
            row=0,
            column=columna_x0,
            padx=10,
            pady=10
        )

        for i in range(dimension):
            entrada_b = ctk.CTkEntry(
                self.frame_central,
                width=100,
                justify="center"
            )
            entrada_b.grid(
                row=i + 1,
                column=columna_b,
                padx=10,
                pady=4
            )
            self.campos_b.append(entrada_b)

            entrada_x0 = ctk.CTkEntry(
                self.frame_central,
                width=100,
                justify="center"
            )
            entrada_x0.grid(
                row=i + 1,
                column=columna_x0,
                padx=10,
                pady=4
            )
            entrada_x0.insert(0, "0")
            self.campos_x0.append(entrada_x0)

        self.salida.delete("1.0", "end")
        self.salida.insert(
            "end",
            "Introduce los coeficientes de la matriz A, el vector b y el vector inicial x₀."
        )

    def obtener_valor(self, entrada):
        valor = conv.convertir_a_decimal(entrada.get())

        if valor is None or not math.isfinite(valor):
            raise ValueError(
                "Todos los campos deben contener números válidos y finitos."
            )

        return valor

    def obtener_datos(self):
        matriz = [
            [
                self.obtener_valor(entrada)
                for entrada in fila
            ]
            for fila in self.campos_matriz
        ]

        vector_b = [
            self.obtener_valor(entrada)
            for entrada in self.campos_b
        ]

        vector_inicial = [
            self.obtener_valor(entrada)
            for entrada in self.campos_x0
        ]

        if not ver.verificar_dimensiones_sistema(
            matriz,
            vector_b,
            vector_inicial
        ):
            raise ValueError(
                "Las dimensiones de la matriz y los vectores no coinciden."
            )

        if not ver.verificar_diagonal_no_nula(matriz):
            raise ValueError(
                "La diagonal principal no puede contener ceros."
            )

        return matriz, vector_b, vector_inicial

    def calcular(self):
        try:
            matriz, vector_b, vector_inicial = self.obtener_datos()

            tolerancia = conv.convertir_a_decimal(
                self.entrada_tolerancia.get()
            )

            if tolerancia is None or not math.isfinite(tolerancia) or tolerancia <= 0:
                raise ValueError(
                    "La tolerancia debe ser un número finito mayor que cero."
                )

            try:
                max_iteraciones = int(self.entrada_iteraciones.get())
            except ValueError:
                raise ValueError(
                    "El máximo de iteraciones debe ser un número entero."
                )

            if max_iteraciones <= 0:
                raise ValueError(
                    "El máximo de iteraciones debe ser mayor que cero."
                )

            metodo = self.menu_metodo.get()
            formato = (
                "fraccion"
                if self.menu_formato.get() == "Fracción"
                else "decimal"
            )

            if metodo == "Jacobi":
                resultado = sol.resolver_jacobi(
                    matriz,
                    vector_b,
                    vector_inicial,
                    tolerancia,
                    max_iteraciones
                )
            else:
                resultado = sol.resolver_gauss_seidel(
                    matriz,
                    vector_b,
                    vector_inicial,
                    tolerancia,
                    max_iteraciones
                )

            texto = vis.mostrar_procedimiento(
                resultado,
                formato
            )

            if not op.verificar_valores_finitos(resultado["solucion"]):
                raise ValueError(
                    "El cálculo produjo valores no finitos. Revisa los datos del sistema."
                )

            self.salida.delete("1.0", "end")
            self.salida.insert("end", texto)

            if not ver.verificar_diagonal_dominante(matriz):
                messagebox.showwarning(
                    "Advertencia de convergencia",
                    "La matriz no es diagonalmente dominante. "
                    "No se garantiza la convergencia del método."
                )

            if not resultado["convergio"]:
                messagebox.showwarning(
                    "Resultado",
                    "Se alcanzó el máximo de iteraciones sin cumplir la tolerancia."
                )

        except (ValueError, ZeroDivisionError, OverflowError) as error:
            messagebox.showerror(
                "Error de cálculo",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                f"Ocurrió un error durante el cálculo:\n{error}"
            )

    def limpiar(self):
        for fila in self.campos_matriz:
            for entrada in fila:
                entrada.delete(0, "end")

        for entrada in self.campos_b:
            entrada.delete(0, "end")

        for entrada in self.campos_x0:
            entrada.delete(0, "end")
            entrada.insert(0, "0")

        self.entrada_tolerancia.delete(0, "end")
        self.entrada_tolerancia.insert(0, "0.000001")

        self.entrada_iteraciones.delete(0, "end")
        self.entrada_iteraciones.insert(0, "100")

        self.salida.delete("1.0", "end")


if __name__ == "__main__":
    aplicacion = AppCalculadoraJacobiGaussSeidel()
    aplicacion.mainloop()
