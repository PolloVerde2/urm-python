import os, json
from program import Program, InterpreterException

# Abrir archivo de configuración
with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
    config = json.load(config_file)

base_dir = config["search_in"]

if base_dir == './':
    base_dir = os.path.dirname(__file__)

# Dirección de la carpeta de programas
program_path = os.path.join(base_dir, 'programas')

# Crear carpeta de programas en caso de no existir
if not os.path.exists(program_path):
    os.mkdir(program_path)

files = os.listdir(program_path)
list_program = []

# Filtrar archivos en la carpeta programas
for file in files:
    if file.endswith('.urm'):
        list_program.append(file)

# Program
def main():
    # Imprimir lista de programas disponibles
    index = 0
    if len(list_program) > 1:
        print("Tienes varios programas. Escoge uno: ")
        for i in range(len(list_program)):
            print(f"  {i+1}) {list_program[i]}")
        
        while True:
            try:
                index = int(input("> ")) - 1
                break
            except ValueError:
                continue

    # Seleccionar programa de la lista
    if len(list_program) >= 1:
        program_file = os.path.join(program_path, list_program[index])

        try:
            # Inicializar interprete del programa
            program = Program(
                program_file, 
                max_iterations=config["max_iterations"], 
                print_process=config["print_process"],
                debug_mode=config["debug"],
                verbose=config["verbose"],
                space=4
            )

            # Solicitar configuración inicial
            if program.get_init_config() is None or not config["use_file_config"]:
                if config["use_file_config"]:
                    print("El programa no incluye una configuración inicial. Deberás proporcionar una.")
                else:
                    print("Necesitas proporcionar una configuración inicial. (Para usar la que incluye el programa, cambia \"use_file_config\" a \"true\" en config.json)")
                print("Ingresa los valores para cada registro, separados por comas: (ej.: 1, 3, 5)")
                program.set_init_config([int(i) for i in input("> ").strip().split(',')])

            # Ejecutar programa
            result = program.execute()
            print(f"Resultado: {result[0]}")
            print(f"Iteraciones: {result[1]}")

        except InterpreterException as e:
            print(e.args[0])

    else:
        print("No se encontró ningun programa. Para iniciar, crea un archivo .urm en la carpeta \"programas\"")

if __name__ == "__main__":
    main()

    print("\nFin del programa. Hecho por: Demian Galindo Vazquez")
    input("Presiona ENTER para salir.")