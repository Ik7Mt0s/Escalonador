class Processo():
    """
    Classe que representa um processo no sistema
    """
    def __init__(self, id, nome, prioridade, ciclos_necessarios, recurso_necessario):
        self.id = id
        self.nome = nome
        self.prioridade = prioridade
        self.ciclos_necessarios = ciclos_necessarios
        self.recurso_necessario = recurso_necessario
        self.recurso_solicitado = False

    def __str__(self):
        """Representação em string do processo para exibição"""
        return f"{self.nome} (ID: {self.id}, Prioridade: {self.prioridade})"
    
class Node:
    """
    Classe que representa um nó na lista encadeada
    Cada nó contém um processo e uma referência para o próximo nó
    """
    def __init__(self, processo):
        self.processo = processo
        self.proximo = None

class ListaProcessos:
    """
    Implementação de lista encadeada simples para gerenciar processos
    """
    def __init__(self):
        self.cabeca = None
        self.cauda = None
        self.tamanho = 0

    def lista_vazia(self):
        """Verifica se a lista está vazia"""
        return self.cabeca is None
    
    def status(self):
        """Retorna string com status da lista"""
        if self.lista_vazia():
            return "Lista de Processos: Vazia"
        else:
            return f"Lista de Processos: {self.tamanho} processo(s)"
        
    def adicionar_final(self, processo):
        """
        Adiciona um processo no final da lista
        Complexidade: O(1)
        """
        novo_no = Node(processo)
        if self.lista_vazia():
            self.cabeca = novo_no
            self.cauda = novo_no
        else:
            self.cauda.proximo = novo_no
            self.cauda = novo_no
        self.tamanho += 1

    def remover_inicio(self):
        """
        Remove e retorna o processo do início da lista
        Complexidade: O(1)
        """
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
        """Retorna representação em string de toda a lista"""
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
    """
    Classe principal do escalonador
    Gerencia múltiplas filas de prioridade e implementa políticas de escalonamento
    """
    def __init__(self):
        self.lista_alta_prioridade = ListaProcessos()
        self.lista_media_prioridade = ListaProcessos()
        self.lista_baixa_prioridade = ListaProcessos()
        self.lista_bloqueados = ListaProcessos()
        self.contador_alta_prioridade = 0

    def adicionar_processo(self, processo):
        """
        Adiciona processo na fila de prioridade correta
        """
        if processo.prioridade == 1:
            self.lista_alta_prioridade.adicionar_final(processo)
        elif processo.prioridade == 2:
            self.lista_media_prioridade.adicionar_final(processo)
        elif processo.prioridade == 3:
            self.lista_baixa_prioridade.adicionar_final(processo)
        else:
            return "Processo não pode entrar"
        
    def executar(self):
        """
        Executa um ciclo completo de escalonamento
        Segue as regras: desbloqueio → anti-inanição → prioridades → execução
        """
        # 1. FASE DE DESBLOQUEIO: Libera processos bloqueados se houver
        if not self.lista_bloqueados.lista_vazia():
            processo_desbloqueado = self.lista_bloqueados.remover_inicio()
            processo_desbloqueado.recurso_solicitado = True
            self.adicionar_processo(processo_desbloqueado)
            print(f"Processo {processo_desbloqueado} desbloqueado")

        processo = None # Processo selecionado para execução neste ciclo

        # 2. VERIFICAÇÃO ANTI-INANIÇÃO: Previne starvation de processos de baixa prioridade
        if self.contador_alta_prioridade >= 5:
            if not self.lista_media_prioridade.lista_vazia():
                processo = self.lista_media_prioridade.remover_inicio()
            elif not self.lista_baixa_prioridade.lista_vazia():
                processo = self.lista_baixa_prioridade.remover_inicio()
            self.contador_alta_prioridade = 0
            print(f"Anti-inanição executada")

        # 3. SELEÇÃO POR PRIORIDADE: Ordem normal de escalonamento
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

        # 4. VERIFICAÇÃO DE BLOQUEIO: Se processo precisa de recurso especial
        if processo is not None and processo.recurso_necessario == "DISCO" and not processo.recurso_solicitado:
            self.lista_bloqueados.adicionar_final(processo)
            print(f"Processo {processo.nome} bloqueado")
            return
        
        # 5. EXECUÇÃO DO PROCESSO: Se chegou aqui, processo pode ser executado
        print(f"Excutando: {processo.nome}")
        processo.ciclos_necessarios -= 1

        # 6. VERIFICAÇÃO DE TÉRMINO: Processo completou sua execução?
        if processo.ciclos_necessarios <= 0:
            print(f"Processo {processo.nome} finalizado") # Processo terminou
        else:
            # Processo não terminou - recoloca no final da fila de prioridade
            self.adicionar_processo(processo)
            print(f"Processo {processo.nome} volta para fila ({processo.ciclos_necessarios} ciclos restantes)")

    def status(self):
        """
        Exibe o estado atual de todas as filas do escalonador
        """
        print("\n" + "="*50)
        print("ESTADO DO ESCALONADOR")
        print("="*50)
        print(f"Alta: {self.lista_alta_prioridade}")
        print(f"Média: {self.lista_media_prioridade}")
        print(f"Baixa: {self.lista_baixa_prioridade}")
        print(f"Bloqueados: {self.lista_bloqueados}")
        print(f"Contador anti-inanição: {self.contador_alta_prioridade}/5")
        print("="*50)

import csv

def main():
    """
    Função principal do programa
    Responsável por carregar processos de arquivo CSV e executar o escalonador
    """
    # Nome do arquivo CSV que contém os processos
    nome_arquivo = "processos.csv"