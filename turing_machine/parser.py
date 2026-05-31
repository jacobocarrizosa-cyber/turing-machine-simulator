# -*- coding: utf-8 -*-

class MTValidationError(Exception):
    pass

class TuringMachineParser:
    def __init__(self, file_content):
        self.raw_lines = file_content.splitlines()
        self.states = []
        self.input_alphabet = []
        self.tape_alphabet = []
        self.initial_state = ""
        self.final_states = []
        self.blank_symbol = ""
        self.transitions = {}

    def parse(self):
        parsing_transitions = False

        for line in self.raw_lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Transiciones:"):
                parsing_transitions = True
                continue

            if not parsing_transitions:
                self._parse_definition(line)
            else:
                self._parse_transition(line)

        self._validate()

        return {
            "states": self.states,
            "input_alphabet": self.input_alphabet,
            "tape_alphabet": self.tape_alphabet,
            "initial_state": self.initial_state,
            "final_states": self.final_states,
            "blank_symbol": self.blank_symbol,
            "transitions": self.transitions
        }

    def _parse_definition(self, line):
        if ":" not in line:
            return
        
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()

        if key == "estados":
            self.states = [s.strip() for s in value.split(",")]
        elif key == "alfabeto entrada":
            self.input_alphabet = [s.strip() for s in value.split(",")]
        elif key == "alfabeto_cinta" or key == "alfabeto cinta":
            self.tape_alphabet = [s.strip() for s in value.split(",")]
        elif key == "inicial":
            self.initial_state = value
        elif key == "finales":
            self.final_states = [s.strip() for s in value.split(",")]
        elif key == "blanco":
            self.blank_symbol = value

    def _parse_transition(self, line):
        if "->" not in line:
            return
            
        left, right = line.split("->")
        current_state, read_symbol = [x.strip() for x in left.split(",")]
        next_state, write_symbol, direction = [x.strip() for x in right.split(",")]
        
        direction = direction.upper()
        if direction == 'I': 
            direction = 'L'

        self.transitions[(current_state, read_symbol)] = (next_state, write_symbol, direction)

    def _validate(self):
        if self.blank_symbol not in self.tape_alphabet:
            raise MTValidationError("El símbolo blanco debe pertenecer al alfabeto de cinta.")
        
        if self.initial_state not in self.states:
            raise MTValidationError("El estado inicial no está en el conjunto de estados.")
        
        for state in self.final_states:
            if state not in self.states:
                raise MTValidationError(f"El estado final '{state}' no pertenece a los estados.")

        for (curr_st, read_sym), (next_st, write_sym, dir) in self.transitions.items():
            if curr_st not in self.states or next_st not in self.states:
                raise MTValidationError("Las transiciones contienen estados no definidos.")
            if read_sym not in self.tape_alphabet or write_sym not in self.tape_alphabet:
                raise MTValidationError("Las transiciones contienen símbolos que no están en el alfabeto de cinta.")
            if dir not in ['L', 'R', 'S']:
                raise MTValidationError("La dirección debe ser L, R o S.")