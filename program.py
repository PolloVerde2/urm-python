class InterpreterException(Exception):
    def __init__(self, e):
        self.e = e

class Program:
    def __init__(self, file, init_config=None, max_iterations=-1, print_process=False, debug_mode=False, verbose=True, space=None):
        # Class parameters
        self.file = file
        self.init_config = init_config
        self.max_iterations = max_iterations
        self.print_process = print_process
        self.debug_mode = debug_mode
        self.verbose = verbose
        self.space = space

        # Public vars
        self.content = None
        self.instructions = []
        self.registry = []
        self.max_registries = 0

        # Private vars
        self._skip_to = 0
        self._parsed = False

        # Read file and load it to self.content
        self.debug(f"Opening file {self.file}")
        with open(self.file, 'r') as f:
            self.debug("Reading file content...")
            self.content = f.read().lower()
            if self.content == '':
                self.log_error(5, self.file)
    
    def debug(self, msg):
        if self.debug_mode:
            print("[DEBUG]", msg)

    def log_error(self, code, line, row=None):
        error_msg = ""
        match code:
            case 0:
                error_msg =  f"Valor numérico inválido en línea {line}"
            case 1:
                error_msg =  f"Paréntesis sin cerrar en línea {line}"
            case 2:
                error_msg = "No se encontró una configuración inicial. Asegúrate de incluir una en el archivo, o especificarla al correr este programa."
            case 3:
                error_msg = f"Instrucción inválida \"{line}\""
            case 4:
                error_msg =  f"Valor menor a 1 en línea {line}"
            case 5:
                error_msg =  f"El archivo proporcionado está vacio: {line}"
            case _:
                error_msg =  "Error"

        raise InterpreterException("Error: " + error_msg + (f" (columna {row})" if row is not None else ""))
        # print("Error: " + error_msg + (f" (columna {row})" if row is not None else ""))

    def log(self, msg, end="\n"):
        if self.verbose:
            print(msg, end=end)

    # Gets the program's initial configuration. If it doesn't exist, it will try
    # to look for it in the .urm file
    # Returns:
    #   init_config (tuple || None): Tuple containing the initial configuration,
    #                                or None if it was not found
    def get_init_config(self):
        if self.init_config is None:
            if self.parse_instructions() is None:
                return False

        return self.init_config
    
    def set_init_config(self, config):
        self.init_config = config

    # Parses instructions from a file and saves them to self.instructions
    # Returns:
    #   instructions (list): List of tuples following the format: ('I', n1, n2, n3, ...)
    #                        where I is the instruction, and n are the parameters
    def parse_instructions(self):
        self.instructions = [] # Reset instruction set

        content = self.content[self._skip_to:]
        last_inst = [None]
        inst_content = ""

        is_comment = False

        self.debug(f"Parsing instructions from file...")
        for i in range(len(content)):
            next_i = min(len(content)-1, i+1)
            char = content[i]

            if char + content[next_i] == "//":
                is_comment = True
            elif is_comment and char == '\n':
                is_comment = False
            elif not is_comment:
                # Match character with the available instruction types (p is for init. config.)
                if char in "pzsjt":
                    if last_inst[0] is not None:
                        line = len(self.content[:i+self._skip_to].split('\n'))
                        return self.log_error(1, line, row=i)

                    self.debug(f"Found instruction at index {i}: {char}")
                    last_inst[0] = char
                # Characters inside the instruction call I(...)
                elif last_inst[0] is not None and char not in "()":
                    inst_content += char
                # Match closing bracket
                elif last_inst[0] is not None and char == ")":
                    # Adding formatted instruction to a list
                    last_inst.extend([int(c) for c in inst_content.split(',')])
                    self.instructions.append(tuple(last_inst))
                    # Reset variables
                    last_inst = [None]
                    inst_content = ""
            
            # Log error in case a value less than or equal to 0 is found
            for item in inst_content.split(','):
                line = len(self.content[:i+self._skip_to].split('\n'))
                try:
                    if int(item) < 1 and last_inst[0] != 'p':
                        return self.log_error(4, line)
                    # Exception for P() instruction, as it doesn't contain registry indexes
                    elif int(item) < 0:
                        return self.log_error(4, line)
                except ValueError:
                    pass
        
        # Calculate max registry used with the instruction set
        max_reg = []
        for inst in self.instructions:
            if inst[0] == 'p': # Skip P() instruction for initial config.
                self.init_config = inst[1:]
            else:
                for i in range(1, min(3, len(inst))):
                    max_reg.append(inst[i])
        self.debug(f"Registry entries found: {max_reg}")
        self.max_registries = max(max_reg)

        if self.init_config is not None:
            init_config = ['p']
            init_config.extend(self.init_config)
            init_config = tuple(init_config)
            self.debug(f"Found init config in instructions: {init_config}")
            self.instructions.remove(init_config)

        self._parsed = True
        return self.instructions

    # Logs the current registry. Won't do anything if verbose mode is disabled in config.json
    # Parameters:
    #   space (int): Spacing between each registry value. Default is None (automatic spacing)
    #   end (str): end argument for the print() call. Default is newline
    def print_current_registry(self, end="\n"):
        if self.space is None:
            self.space = len(str(max(self.registry))) + 2
        
        # Loop through all registry values in the instruction set
        for i in range(self.max_registries):
            n = 0
            if i < len(self.registry):
                n = self.registry[i]
            # Print registry entries with consistent spacing
            self.log(str(n) + (" "*(self.space - len(str(n)))), end="")
        # Print newline
        self.log("", end=end)

    # Class method used to execute the URM program. Requires the class to
    # be initialized with a valid .urm file.
    # Returns:
    #    result: tuple(
    #       r1: int, 
    #       iterations: int
    #   )
    def execute(self):
        # Get instruction list
        if not self._parsed:
            self.parse_instructions()

        self.registry = list(self.init_config)
        # Fill missing registries with zeros
        self.registry.extend(
            [0 for _ in range(self.max_registries - len(self.registry))]
        )

        self.log("===== Inicio del programa =====")
        if self.print_process:
            self.log("    ", end="")
        self.print_current_registry(end="")
        self.log("<- Conf. inicial")

        # Throw error if no initial config is found
        if self.init_config is None:
            return self.log_error(2, 0)

        self.debug(f"Total registries: {len(self.registry)}")

        i = 0
        iterations = 0
        while i < len(self.instructions) and iterations < self.max_iterations:
            inst = self.instructions

            self.debug(f"Executing instruction {i+1}: {inst[i]}")
            # Execute current instruction
            match inst[i][0]:
                case 'z':
                    r = inst[i][1] - 1
                    self.registry[r] = 0
                case 's':
                    r = inst[i][1] - 1
                    self.registry[r] += 1
                case 't':
                    r2 = inst[i][1] - 1
                    r1 = inst[i][2] - 1

                    self.registry[r1] = self.registry[r2]
                case 'j':
                    r2 = inst[i][1] - 1
                    r1 = inst[i][2] - 1

                    if self.registry[r1] == self.registry[r2]:
                        i = inst[i][3] - 2
                case _:
                    self.log_error(3, f"{inst[i][0].upper()}{inst[i][1:]}")

            if self.print_process and i < len(self.instructions)-1:
                self.log(f"I{i+1}: ", end="")
                self.print_current_registry()

            i += 1
            iterations += 1
        
        # Log program result
        if iterations == self.max_iterations:
            self.log("Cantidad máxima de iteraciones alcanzada.")
        if self.print_process:
            self.log(f"I{i}: ", end="")
        self.print_current_registry(end="")
        self.log("<- Resultado")
        self.log("======= Fin del programa ======")

        return (self.registry[0], iterations)