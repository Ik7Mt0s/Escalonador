# Sistema de Escalonamento de Processos

## 📋 Informações Acadêmicas
- **Disciplina**: Algoritmo e Estruturas de Dados I
- **Professor**: Dimmy Magalhões
- **Instituição**: iCEV - Instituto de Ensino Superior
- **Semestre**: 2025.2
- **Período**: 2°

## 👨‍💻 Desenvolvido por
- **Nome**: Ícaro Matos Castelo Branco
- **Matrícula**: 000292
- **Email**: icaro_castelo.branco@somosicev.com

## 🎯 Descrição do Projeto
Implementação de um escalonador de processos utilizando listas encadeadas implementadas "do zero" em Python. O sistema gerencia múltiplas filas de prioridade com prevenção de inanição e controle de recursos.

### ⚡ Funcionalidades
- ✅ Múltiplas filas de prioridade (Alta, Média, Baixa)
- ✅ Prevenção de inanição (starvation prevention)
- ✅ Gerenciamento de recursos (bloqueio/desbloqueio)
- ✅ Leitura de processos via arquivo CSV
- ✅ Simulação completa de ciclos de CPU
- ✅ Interface de linha de comando intuitiva

## 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python
- **Estruturas de Dados**: Listas Encadeadas Simples implementadas manualmente funcionando como fila
- **Entrada/Saída**: Arquivos CSV (onde a função principal de leitura do arquivo CSV foi feita por IA)
- **Controle de Versão**: Git/GitHub

## 🎯 Como usar

### 📥 1. Pré-requisitos
- Ter instalado: Visual Studio Code e Python

### 📦 2. Configuração do Projeto
- Abra o VS Code
- Crie uma pasta de arquivo exclusiva para o Scheduler
- Na pasta em que se encontra o Scheduler, crie um arquivo "processos.csv"
- O arquivo Scheduler e o arquivo "processos.csv" **devem** estar na mesma pasta, mostrando apenas eles na área lateral esquerda do VS Code, caso o contrário, o arquivo python não achará "processos.csv" e retornará: "Arquivo 'processos.csv' não encontrado!""Certifique-se de que o arquivo está na mesma pasta do programa"

### 📝 3. Preparação do Arquivo de Processos
- Crie o arquivo "processos.csv" com este formato ou siga o formato do arquivo exemplo no repositório:
- """
- id,nome,prioridade,ciclos_necessarios,recurso_necessario
- 1,Chrome,1,5,
- 2,Word,2,3,
- 3,Backup,3,10,DISCO
- 4,Photoshop,1,8,
- 5,Antivirus,2,6,
- """

### 🚀 4. Execução do Programa
- Aperte o Run em formato de seta no canto superior direito do VS Code

### 📊 5. Exemplo de Saída
- Carregando processos do arquivo...
- Processos carregados!
______
- CICLO 1
- Executando: Chrome
- Processo Chrome volta para fila (4 ciclos restantes)
______
- CICLO 2
- Processo Backup bloqueado (DISCO)
______
- CICLO 3
- Processo Backup desbloqueado
- Executando: Word
______
- 🎉 TODOS OS PROCESSOS TERMINARAM!
