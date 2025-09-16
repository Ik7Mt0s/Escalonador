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
    
    def status(self):
        if self.lista_vazia():
            return "Lista de Processos: Vazia"
        else:
            return f"Lista de Processos: {self.tamanho} processo(s)"
        
    def adicionar_final(self, processo):
        novo_no = Node(processo)
        if self.lista_vazia():
            self.cabeca = novo_no
            self.cauda = novo_no
        else:
            self.cauda.proximo = novo_no
            self.cauda = novo_no
        self.tamanho += 1

    def remover_inicio(self):
        if self.lista_vazia():
            return None
        else:
            processo_removido = self.cabeca.processo
            self.cabeca = self.cabeca.proximo
            if self.cabeca is None:
                self.cauda = None
            self.tamanho -= 1
            return processo_removido
        
    def __str__(self):
        if self.lista_vazia():
            return "Lista vazia"
        else:
            elementos = []
            atual = self.cabeca
            while atual:
                elementos.append(str(atual.processo))
                atual = atual.proximo
            return "->".join(elementos)
        
class Scheduler:
    def __init__(self):
        self.lista_alta_prioridade = ListaProcessos()
        self.lista_media_prioridade = ListaProcessos()
        self.lista_baixa_prioridade = ListaProcessos()
        self.lista_bloqueados = ListaProcessos()
        self.contador_alta_prioridade = 0

    def adicionar_processo(self, processo):
        if processo.prioridade == 1:
            self.lista_alta_prioridade.adicionar_final(processo)
        elif processo.prioridade == 2:
            self.lista_media_prioridade.adicionar_final(processo)
        elif processo.prioridade == 3:
            self.lista_baixa_prioridade.adicionar_final(processo)
        else:
            return "Processo não pode entrar"
        
    def executar(self):
        if not self.lista_bloqueados.lista_vazia():
            processo_desbloqueado = self.lista_bloqueados.remover_inicio()
            self.adicionar_processo(processo_desbloqueado)
            print(f"Processo {processo_desbloqueado} desbloqueado")

        processo = None

        if self.contador_alta_prioridade >= 5:
            if not self.lista_media_prioridade.lista_vazia():
                processo = self.lista_media_prioridade.remover_inicio()
            elif not self.lista_baixa_prioridade.lista_vazia():
                processo = self.lista_baixa_prioridade.remover_inicio()
            self.contador_alta_prioridade = 0
            print(f"Anti-inanição executada")

        if processo is None:
            if not self.lista_alta_prioridade.lista_vazia():
                processo = self.lista_alta_prioridade.remover_inicio()
                self.contador_alta_prioridade += 1
            elif not self.lista_media_prioridade.lista_vazia():
                processo = self.lista_media_prioridade.remover_inicio()
            elif not self.lista_baixa_prioridade.lista_vazia():
                processo = self.lista_baixa_prioridade.remover_inicio()
            else: 
                print("Nenhum processo para executar")

        if processo is not None and processo.recurso_necessario == "DISCO":
            self.lista_bloqueados.adicionar_final(processo)
            print(f"Processo {processo.nome} bloqueado")
            return
        
        print(f"Excutando: {processo.nome}")
        processo.ciclos_necessarios -= 1

        if processo.ciclos_necessarios <= 0:
            print(f"Processo {processo.nome} finalizado")
        else:
            self.adicionar_processo(processo)
            print(f"Processo {processo.nome} volta para fila ({processo.ciclos_necessarios} ciclos restantes)")