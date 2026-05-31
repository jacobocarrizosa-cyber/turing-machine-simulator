# -*- coding: utf-8 -*-
from django.test import TestCase
from .parser import TuringMachineParser
from .simulator import TuringMachineSimulator

class TuringMachineTests(TestCase):
    def run_simulation(self, mt_definition, input_string, max_steps=1000):
        """Método auxiliar para parsear y simular rápidamente en las pruebas."""
        parser = TuringMachineParser(mt_definition)
        tm_data = parser.parse()
        simulator = TuringMachineSimulator(tm_data, input_string, max_steps=max_steps)
        status = simulator.run_full()
        
        # Obtenemos la cinta y le quitamos los espacios Blancos (B) de los extremos 
        # para que la comparación de los resultados sea más limpia.
        clean_tape = simulator.get_tape_content().strip('B')
        return status, clean_tape

    def test_0n1n(self):
        """1. Prueba de Lenguaje no regular (0^n 1^n)"""
        mt_def = "Estados: q0,q1,q2,q3,qf\nAlfabeto entrada: 0,1\nAlfabeto_cinta: 0,1,B,X\nInicial: q0\nFinales: qf\nBlanco: B\nTransiciones:\nq0,0->q1,X,R\nq1,0->q1,0,R\nq1,1->q2,1,R\nq2,1->q2,1,R\nq2,B->q3,B,L\nq3,1->q3,1,L\nq3,0->q0,0,R\nq0,X->q0,X,R\nq0,B->qf,B,S"
        
        # Prueba obligatoria: "0011" -> Aceptada
        status, _ = self.run_simulation(mt_def, "0011")
        self.assertEqual(status, "Aceptada")
        
        # Prueba obligatoria: "011" -> Rechazada
        status, _ = self.run_simulation(mt_def, "011")
        self.assertEqual(status, "Rechazada")

    def test_palindromo_binario(self):
        """2. Prueba de Palíndromo binario"""
        mt_def = "Estados: q0,q1,q2,qf\nAlfabeto_entrada: 0,1\nAlfabeto_cinta: 0,1,B\nInicial: q0\nFinales: qf\nBlanco: B\nTransiciones:\nq0,0->q1,B,R\nq0,1->q2,B,R\nq0,B->qf,B,S\nq1,0->q1,0,R\nq1,1->q1,1,R\nq1,B->q0,B,L\nq2,0->q2,0,R\nq2,1->q2,1,R\nq2,B->q0,B,L"
        
        # Prueba obligatoria: "101" -> Aceptada
        status, _ = self.run_simulation(mt_def, "101")
        self.assertEqual(status, "Aceptada")
        
        # Prueba obligatoria: "10" -> Rechazada
        status, _ = self.run_simulation(mt_def, "10")
        self.assertEqual(status, "Rechazada")

    def test_duplicadora_unos(self):
        """3. Prueba de Duplicadora de unos (unario)"""
        mt_def = "Estados: q0,q1,q2,qf\nAlfabeto_entrada: 1\nAlfabeto_cinta: 1,B\nInicial: q0\nFinales: qf\nBlanco: B\nTransiciones:\nq0,1->q1,B,R\nq1,1->q1,1,R\nq1,B->q2,1,L\nq2,1->q2,1,L\nq2,B->q0,1,R\nq0,B->qf,B,S"
        
        # Prueba obligatoria: "111" -> Cinta final "111111" (Aceptada)
        status, tape = self.run_simulation(mt_def, "111")
        self.assertEqual(status, "Aceptada")
        self.assertEqual(tape, "111111")

    def test_termina_en_aa(self):
        """4. Prueba de cadena que termina en 'aa'"""
        mt_def = "Estados: q0,q1,qf\nAlfabeto_entrada: a,b\nAlfabeto_cinta: a,b,B\nInicial: q0\nFinales: qf\nBlanco: B\nTransiciones:\nq0,a->q1,a,R\nq0,b->q0,b,R\nq1,a->qf,a,R\nq1,b->q0,b,R\nqf,a->qf,a,R\nqf,b->qf,b,R"
        
        # Pruebas adicionales exigidas en PDF
        status, _ = self.run_simulation(mt_def, "baa")
        self.assertEqual(status, "Aceptada")
        
        status, _ = self.run_simulation(mt_def, "ba")
        self.assertEqual(status, "Rechazada")

    def test_duplicadora_binaria(self):
        """5. Prueba de Duplicadora binaria (separador #)"""
        mt_def = "Estados: q0,q1,q2,q3,q4,qf\nAlfabeto_entrada: 0,1\nAlfabeto_cinta: 0,1,#,B,X,Y\nInicial: q0\nFinales: qf\nBlanco: B\nTransiciones:\nq0,0->q1,X,R\nq0,1->q2,Y,R\nq0,B->q3,B,L\nq1,0->q1,0,R\nq1,1->q1,1,R\nq1,#->q1,#,R\nq1,B->q3,0,L\nq2,0->q2,0,R\nq2,1->q2,1,R\nq2,#->q2,#,R\nq2,B->q3,1,L\nq3,0->q3,0,L\nq3,1->q3,1,L\nq3,X->q0,X,R\nq3,Y->q0,Y,R\nq3,#->q4,#,R\nq4,0->q4,0,R\nq4,1->q4,1,R\nq4,B->qf,B,S"
        
        # Prueba adicional: "10" debe ser aceptada 
        status, _ = self.run_simulation(mt_def, "10")
        self.assertEqual(status, "Aceptada")

    def test_suma_unario(self):
        """6. Prueba de Suma de dos números en unario"""
        mt_def = "Estados: q0,q1,q2,qf\nAlfabeto_entrada: 1,#\nAlfabeto_cinta: 1,#,B\nInicial: q0\nFinales: qf\nBlanco: B\nTransiciones:\nq0,1->q0,1,R\nq0,#->q1,#,R\nq1,1->q1,1,R\nq1,B->q2,1,L\nq2,1->q2,1,L\nq2,#->qf,B,R"
        
        # Prueba adicional: "11#111" -> Cinta final con 5 unos
        status, tape = self.run_simulation(mt_def, "11#111")
        self.assertEqual(status, "Aceptada")
        # El algoritmo reemplaza el #, verificamos que en la cinta queden 5 unos
        self.assertEqual(tape.count('1'), 5)

    def test_limite_de_pasos_bucle(self):
        """7. Prueba límite (No_termina) por bucle infinito"""
        # Diseñamos una máquina que se mueve a la derecha infinitamente
        mt_def = "Estados: q0,qf\nAlfabeto_entrada: 0\nAlfabeto_cinta: 0,B\nInicial: q0\nFinales: qf\nBlanco: B\nTransiciones:\nq0,B->q0,B,R\nq0,0->q0,0,R"
        
        # Max_steps muy bajo para forzar el quiebre del bucle rápido
        status, _ = self.run_simulation(mt_def, "0", max_steps=20)
        self.assertEqual(status, "No Termina")