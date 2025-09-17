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

    # Cria uma instância do escalonador
    scheduler = Scheduler()
    
    print("Carregando processos do arquivo...")

    try:
        # Abre o arquivo CSV para leitura
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            # Cria um leitor CSV para processar o arquivo
            leitor = csv.reader(arquivo)
            next(leitor)  # Pula a primeira linha (cabeçalho do CSV)
            
            # Processa cada linha do arquivo CSV
            for linha in leitor:
                # Verifica se a linha tem pelo menos 5 colunas (dados completos)
                if len(linha) >= 5:
                    try:
                        # Converte e extrai os dados de cada coluna:
                        id = int(linha[0])           # Coluna 0: ID (convertido para inteiro)
                        nome = linha[1]              # Coluna 1: Nome do processo
                        prioridade = int(linha[2])   # Coluna 2: Prioridade (1-3)
                        ciclos = int(linha[3])       # Coluna 3: Ciclos necessários
                        # Coluna 4: Recurso necessário (None se vazio)
                        recurso = linha[4] if linha[4] != "" else None
                        
                        # Cria um objeto Processo com os dados extraídos
                        processo = Processo(id, nome, prioridade, ciclos, recurso)
                        
                        # Adiciona o processo ao escalonador na fila de prioridade correta
                        scheduler.adicionar_processo(processo)
                        
                    except ValueError:
                        # Ignora linhas com erro de conversão (dados inválidos)
                        continue
        
        print("Processos carregados!")
        
        # Exibe o estado inicial do escalonador após carregamento
        scheduler.status()
        
        # EXECUÇÃO PRINCIPAL DO ESCALONADOR
        # Executa ciclos continuamente até que todos os processos terminem
        ciclo = 1  # Contador de ciclos executados
        
        while True:
            print(f"\n🎯 CICLO {ciclo}")
            
            # Executa um ciclo completo de escalonamento
            scheduler.executar()
            
            # VERIFICAÇÃO DE TÉRMINO
            # Verifica se TODAS as listas do escalonador estão vazias:
            if (scheduler.lista_alta_prioridade.lista_vazia() and
                scheduler.lista_media_prioridade.lista_vazia() and
                scheduler.lista_baixa_prioridade.lista_vazia() and
                scheduler.lista_bloqueados.lista_vazia()):
                
                print("🎉 TODOS OS PROCESSOS TERMINARAM!")
                break  # Sai do loop quando não há mais processos
                
            ciclo += 1  # Incrementa contador de ciclos
            
    except FileNotFoundError:
        # Trata erro caso o arquivo CSV não seja encontrado
        print("Arquivo 'processos.csv' não encontrado!")
        print("Certifique-se de que o arquivo está na mesma pasta do programa")
        
    except Exception as e:
        # Trata qualquer outro erro inesperado
        print(f"Erro inesperado: {e}")

# Ponto de entrada do programa
# Executa a função main() apenas se este arquivo for executado diretamente
if __name__ == "__main__":
    main()