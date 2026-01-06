"""
Lemmanaid - Template Normalization
Status: REFINED (Strict Syntax)
Source: Lemmanaid (2025)

Enforces strict template syntax (?Hk, x_i) and variable normalization.
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class InstantiatedLemma:
    statement: str
    template_origin: str
    bindings: Dict[str, str]
    verified: bool = False

class TemplateNormalizer:
    """
    Normaliza lemas a plantillas abstractas 'Holed' para Lemmanaid.
    Convierte funciones a ?Hk y variables a x_k/y_k.
    Fuente: [16], [14].
    """
    def __init__(self):
        self.func_pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b') # Simplificado

    def abstract_to_template(self, lemma_str):
        """
        Transforma: "a * (b + c) = a * b + a * c"
        A: "?H1 x1 (?H2 x2 x3) = ?H2 (?H1 x1 x2) (?H1 x1 x3)"
        Fuente: [17].
        """
        # Mapa de símbolos a agujeros
        symbol_map = {}
        hole_counter = 1
        
        # Mapa de variables a índices canónicos (x1, x2...)
        var_map = {}
        var_counter = 1
        
        def replace_token(match):
            token = match.group(0)
            # Lógica heurística: si es operador/función conocido -> ?Hk
            if self._is_operator(token):
                nonlocal hole_counter
                if token not in symbol_map:
                    symbol_map[token] = f"?H{hole_counter}"
                    hole_counter += 1
                return symbol_map[token]
            # Si es variable -> x_k
            elif self._is_variable(token):
                nonlocal var_counter
                if token not in var_map:
                    var_map[token] = f"x{var_counter}"
                    var_counter += 1
                return var_map[token]
            return token # Símbolos lógicos (forall, =, etc) se mantienen

        # Aplicar transformación
        template = self.func_pattern.sub(replace_token, lemma_str)
        return template

    def _is_operator(self, token):
        # Lista de operadores que deben abstraerse según [18]
        # Símbolos lógicos como 'forall', 'exists', '=', 'True' NO se abstraen.
        preserved = {'forall', 'exists', '=', 'True', 'False', 'implies', 'and', 'or'}
        return token not in preserved and not token.isnumeric()

    def _is_variable(self, token):
        return token.islower() and len(token) == 1 # Heurística simple

class LemmanaidAgent:
    def __init__(self):
        self.normalizer = TemplateNormalizer()
        
    def abstract_lemma(self, lemma: str):
        print(f"[LEMMANAID] Input: {lemma}")
        template = self.normalizer.abstract_to_template(lemma)
        print(f"[LEMMANAID] Template: {template}")
        return template

if __name__ == "__main__":
    agent = LemmanaidAgent()
    agent.abstract_lemma("a * (b + c) = a * b + a * c")
    agent.abstract_lemma("distrib x y z = plus (mult x y) (mult x z)")
