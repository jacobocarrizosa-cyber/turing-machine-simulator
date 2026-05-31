# -*- coding: utf-8 -*-

class TuringMachineSimulator:
    def __init__(self, tm_data, input_string="", max_steps=10000):
        """
        Inicializa el simulador con los datos parseados y la cadena de entrada.
        """
        self.states = tm_data['states']
        self.tape_alphabet = tm_data['tape_alphabet']
        self.blank_symbol = tm_data['blank_symbol']
        self.final_states = tm_data['final_states']
        self.transitions = tm_data['transitions']
        
        # Implementación de cinta infinita usando un diccionario
        self.tape = {}
        for i, char in enumerate(input_string):
            self.tape[i] = char
            
        self.head_position = 0
        self.current_state = tm_data['initial_state']
        self.steps_count = 0
        self.max_steps = max_steps
        self.status = "Ejecutando"
        self.history = []

    def get_tape_content(self):
        """Devuelve la cinta como una cadena de texto."""
        if not self.tape:
            return self.blank_symbol
        
        min_idx = min(self.tape.keys())
        max_idx = max(self.tape.keys())
        return "".join(self.tape.get(i, self.blank_symbol) for i in range(min_idx, max_idx + 1))

    def get_state_snapshot(self):
        """Captura el estado actual para la visualización paso a paso."""
        return {
            'tape': self.get_tape_content(),
            'head_position': self.head_position - (min(self.tape.keys()) if self.tape else 0),
            'current_state': self.current_state,
            'steps': self.steps_count,
            'status': self.status
        }

    def step(self):
        """Ejecuta un único paso de la máquina de Turing."""
        if self.status != "Ejecutando":
            return False

        # Guardar historial antes de cambiar
        self.history.append(self.get_state_snapshot())

        # Condición de aceptación
        if self.current_state in self.final_states:
            self.status = "Aceptada"
            return False

        current_symbol = self.tape.get(self.head_position, self.blank_symbol)
        transition_key = (self.current_state, current_symbol)

        # Condición de rechazo (no hay transición definida)
        if transition_key not in self.transitions:
            self.status = "Rechazada"
            return False

        # Aplicar transición
        next_state, write_symbol, direction = self.transitions[transition_key]
        
        self.tape[self.head_position] = write_symbol
        self.current_state = next_state
        
        # Mover cabezal
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
            
        self.steps_count += 1
        
        # Condición de límite de pasos (evitar bucles infinitos)
        if self.steps_count >= self.max_steps:
            self.status = "No Termina"
            return False
            
        return True

    def run_full(self):
        """Ejecuta la máquina hasta que se detenga."""
        while self.status == "Ejecutando":
            self.step()
            
        # Guardar el estado final en el historial
        self.history.append(self.get_state_snapshot())
        return self.status