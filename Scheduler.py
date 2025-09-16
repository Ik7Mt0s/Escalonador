class Processo():
    def __init__(self, id, nome, prioridade, ciclos_necessarios, recurso_necessario):
        self.id = id
        self.nome = nome
        self.prioridade = prioridade
        self.ciclos_necessarios = ciclos_necessarios
        self.recurso_necessario = recurso_necessario

    def __str__(self):
        return f"{self.nome} (ID: {self.id}, Prioridade: {self.prioridade})"
    
class Node:
    def __init__(self, processo):
        self.processo = processo
        self.proximo = None

class ListaProcessos:
    def __init__(self):
        self.cabeca = None
        self.cauda = None
        self.tamanho = 0

    def lista_vazia(self):
        return self.cabeca is None