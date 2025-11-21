# Intérprete de Máquinas de Registros (URM)

Este es un programa hecho en Python para ejecutar instrucciones de URM.
Una URM (Por sus siglas en inglés: Unlimited Register Machine) consiste en una cantidad infinita de registros R₁, R₂, R₃, ... que contienen cada uno un número rₙ >= 0 entero.

_Para mas información: [Máquina de registro (Wikipedia)](https://es.wikipedia.org/wiki/M%C3%A1quina_de_registro)_

## Como usar

Descarga el repositorio usando:
```bash
git clone https://github.com/PolloVerde2/urm-python.git
```
A continuación, crea un archivo dentro de la carpeta `programas` con extensión `.urm` (Por ejemplo: `mi_programa.urm`)

Una vez creado el programa, ejecuta `run.py`:
```bash
python run.py
```

Dentro del archivo `.urm` puedes escribir instrucciones, donde `n` es el registro Rₙ:
- **Z(n):** Asigna el valor `0` en el registro `rₙ`.
- **S(n):** Cambia `rₙ` por `rₙ + 1`.
- **T(m, n):** Cambia el registro `rₙ` por el valor de `rₘ`.
- **J(m, n, q):** Si `rₘ = rₙ`, salta a la q-ésima instrucción, en caso contrario, pasa a la siguiente
_Nota: solo se pueden asignar valores enteros >= 1_

Es opcional, pero puedes incluir una primer instrucción `P(a₁, a₂, a₃, ...)` para proporcionar una configuración inicial. _Siempre_ deberá ser la primera y solo puedes poner una.
También puedes añadir comentarios usando `//`.

El programa termina cuando:
1. Se ejecutan todas las instrucciones.
2. No existe la q-ésima instrucción en un salto `J(m, n, q)`.
3. Se alcanza el límite de iteraciones (especificado en `config.json`)

## Configuración
Dentro del mismo directorio de `run.py`, se encuentra el archivo de configuración `config.json`, el cual se verá así:
```jsonc
{
	"max_iterations":  500,   // Cantidad máxima de iteraciones
	"print_process":  false,  // Imprime el registro en cada instrucción
	"use_file_config":  true, // Utiliza la conf. inicial proporcionada en el archivo
	"debug":  false,          // Modo depurar, útil para diagnosticar problemas
	"search_in":  "./",       // Directorio donde se buscarán programas .urm
	"verbose":  true          // Imprime datos del programa en consola.
}
```
## Ejemplos
Programa para calcular el producto de dos números `P(m, n) = mn`:
```c
// Configuración inicial
P(5, 5)

// Instrucciones
J(2, 4, 5)
S(3)
S(4)
J(1, 1, 1)
Z(4)
S(5)
J(1, 5, 9)
J(1, 1, 1)
T(3, 1)
```

Programa para restar `P(m, n) = m-n`:
```c
// Configuración inicial
P(9, 7)

// Instrucciones
J(1, 2, 6)
S(2)
S(3)
J(1, 2, 6)
J(1, 1, 2)
T(3, 1)
```