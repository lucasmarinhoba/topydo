# Relatório da Atividade 04 — Manutenção em Projeto Existente

**Projeto de Software:** [topydo](https://github.com/topydo/topydo)  
**Repositório do Fork:** [lucasmarinhoba/topydo](https://github.com/lucasmarinhoba/topydo)  
**Branch de Trabalho:** `master`  
**Commit Inicial de Referência (Upstream):** `37eba58`  
**Autor:** Lucas Marinho  
**Disciplina:** Tópicos Avançados em Engenharia de Software — Prof. Andrei Formiga  

---

## 1. Introdução e Escopo da Manutenção

Este documento detalha o processo de desenvolvimento e entrega da **Atividade 04**, cujo objetivo foi executar a melhoria planejada na **Atividade 03** no software livre **topydo** (um gerenciador de tarefas em linha de comando baseado no padrão *todo.txt*).

### 1.1. A Melhoria Implementada
Foi adicionado ao projeto o subcomando `topydo stats`, cuja finalidade é processar o arquivo de tarefas e exibir um sumário estatístico consolidado com as seguintes métricas:
1. **Total de tarefas** cadastradas;
2. **Tarefas concluídas** (marcadas com `x`);
3. **Tarefas pendentes** (em aberto);
4. **Tarefas atrasadas (*overdue*)**: tarefas pendentes cuja data de vencimento (`due:`) seja anterior à data de referência;
5. **Distribuição de tarefas por projeto**: contagem agrupada de tarefas para cada projeto (`+projeto`).

### 1.2. Base de Dados Oficial de Testes
Todos os testes práticos e validações foram realizados com base no arquivo contido na pasta **`meus_teste_topydo/`**:
* **Arquivo Oficial:** [`meus_teste_topydo/todo.txt`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/meus_teste_topydo/todo.txt)

---

## 2. Mapa Geral de Arquivos Criados e Modificados por Fase

A tabela a seguir consolida todos os arquivos adicionados ou alterados no repositório ao longo de cada etapa do desenvolvimento:

| Fase | Descrição | Arquivos Adicionados / Criados | Arquivos Modificados |
| :--- | :--- | :--- | :--- |
| **Fase 0** | **Linha de Base (*Baseline*)** | • `atvd/Atividade03_topydo.md`<br>• `atvd/Atividade04.md`<br>• `atvd/Fase0_LinhaDeBase.md`<br>• `atvd/exemplos_testes.md`<br>• `meu_todo_teste.txt` | *(Nenhum código do projeto alterado)* |
| **Fase 1** | **Implementação do `topydo stats`** | • `topydo/commands/StatsCommand.py` | • `topydo/Commands.py`<br>• `topydo/ui/CLIApplicationBase.py` |
| **Fase 2** | **Testes Automatizados Unitários** | • `test/test_stats_command.py` | *(Nenhum)* |
| **Fase 3** | **Validações Práticas (CLI e Colunas)** | • `meus_teste_topydo/todo.txt`<br>• `meus_teste_topydo/meu_todo_teste.txt` | • `atvd/exemplos_testes.md` |
| **Fase 4** | **Documentação Consolidada e Entrega**| • `atvd/relatorio.md` | *(Consolidação no repositório)* |

---

## 3. Detalhamento das Fases do Projeto

---

### Fase 0: Linha de Base (*Baseline*) e Validação Prévia

Antes de qualquer alteração no código-fonte, estabelecemos o estado inicial de referência para garantir que nenhuma regressão fosse introduzida.

#### 📁 Arquivos desta fase:
* **Arquivos Adicionados:**
  * [`atvd/Atividade03_topydo.md`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/atvd/Atividade03_topydo.md) (documento com a definição da melhoria planejada);
  * [`atvd/Atividade04.md`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/atvd/Atividade04.md) (enunciado oficial da atividade e critérios de entrega);
  * [`atvd/Fase0_LinhaDeBase.md`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/atvd/Fase0_LinhaDeBase.md) (relatório formal de levantamento da linha de base);
  * [`atvd/exemplos_testes.md`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/atvd/exemplos_testes.md) (guia de testes manuais elaborado para a atividade);
  * [`meu_todo_teste.txt`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/meu_todo_teste.txt) (amostra inicial de dados de teste).
* **Commit Realizado:** `b104549` (`docs: registrar linha de base da Fase 0 e arquivo de testes reais`).

#### A. Verificação da Suíte de Testes Original
A suíte completa de testes unitários foi executada no ambiente oficial de referência (Linux / WSL com Python 3.10):
```bash
python -m pytest
```
* **Resultado Obtido:** **825 testes aprovados (*passed*)**, 4 ignorados (*skipped*) e **0 falhas**.
* **Critério de Aceitação:** Nenhum dos 825 testes existentes poderia quebrar após a inclusão do `stats`.

#### B. Comprovação da Ausência da Funcionalidade
Executamos o comando `stats` antes da implementação para comprovar que ele não existia:
```bash
python -m topydo.ui.UILoader stats
```
* **Saída Obtida:** O sistema não reconheceu o subcomando e exibiu o texto geral de ajuda (`topydo help`), comprovando que `stats` não estava registrado.

---

### Fase 1: Implementação do Subcomando `topydo stats`

Seguindo as orientações de arquitetura do projeto e o [CONTRIBUTING.md](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/CONTRIBUTING.md) (funções pequenas e com responsabilidade única):

#### 📁 Arquivos desta fase:
* **Arquivos Adicionados:**
  * [`topydo/commands/StatsCommand.py`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/commands/StatsCommand.py) (módulo completo com lógica de cálculo, formatação e classe do comando).
* **Arquivos Modificados:**
  * [`topydo/Commands.py`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/Commands.py) (registro do subcomando no roteador da CLI);
  * [`topydo/ui/CLIApplicationBase.py`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/ui/CLIApplicationBase.py) (configuração de comando somente leitura e inclusão no menu de ajuda global).

#### 1. Criação do Módulo Core ([StatsCommand.py](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/commands/StatsCommand.py))
O módulo foi implementado separando a lógica de negócio da apresentação:
* **`calculate_stats(p_todolist, p_reference_date=None)`**: função pura que itera sobre `p_todolist.todos()`, contabiliza totais, calcula tarefas atrasadas comparando `todo.due_date() < reference_date` e agrega a contagem por projeto. Receber uma data de referência permite testes determinísticos.
* **`format_stats(p_stats, p_lang='en')`**: função pura responsável pela formatação textual, estruturada com dicionário modular de rótulos com suporte tanto para inglês (`en`) quanto para português (`pt`).
* **Classe `StatsCommand(Command)`**: herdeira direta da classe base `Command`, implementando `execute()`, `usage()` e `help()`.

#### 2. Registro no Roteador de Subcomandos ([topydo/Commands.py](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/Commands.py))
Adicionado o mapeamento no dicionário `SUBCOMMAND_MAP`:
```python
SUBCOMMAND_MAP = {
    ...
    'sort': 'SortCommand',
    'stats': 'StatsCommand',
    'tag': 'TagCommand',
}
```

#### 3. Integração na Aplicação CLI ([topydo/ui/CLIApplicationBase.py](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/ui/CLIApplicationBase.py))
* Adicionado `'stats'` à tupla `READ_ONLY_COMMANDS` (assegura que a execução de estatísticas não gere arquivos de backup desnecessários nem altere o arquivo `todo.txt`);
* Adicionado `* stats` na listagem de comandos do `GENERIC_HELP`.

---

### Fase 2: Testes Automatizados e Não-Regressão

#### 📁 Arquivos desta fase:
* **Arquivos Adicionados:**
  * [`test/test_stats_command.py`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/test/test_stats_command.py) (suíte de testes unitários cobrindo 100% dos requisitos do novo subcomando).

#### Casos de Teste Implementados (8 testes unitários):
1. `test_stats_empty_list`: valida o comportamento em uma lista sem tarefas (zeros em todas as métricas, sem erros de divisão ou exceções);
2. `test_calculate_stats_metrics`: valida as regras de negócio de cálculo com data de referência mockada, garantindo que tarefas concluídas no passado **não** sejam contadas como atrasadas;
3. `test_stats_invalid_due_dates`: valida entradas inválidas de datas (`due:not-a-date`, `due:2026-99-99`, `due:`), garantindo que não gerem falhas nem sejam contabilizadas indevidamente como atrasadas;
4. `test_stats_execution_with_tasks`: valida a execução ponta a ponta do comando e a formatação das linhas no terminal;
5. `test_stats_help`: valida a exibição da sinopse e texto de ajuda quando invocado com `stats help` ou `help stats`;
6. `test_format_stats_portuguese`: valida o funcionamento da internacionalização modular de rótulos em português;
7. `test_format_stats_invalid_language_fallback`: valida o fallback seguro para o idioma padrão (`en`) caso um código de idioma inválido seja informado;
8. `test_stats_subcommand_registration`: valida o roteamento em `get_subcommand(["stats"])` e a marcação como somente leitura (`CLIApplicationBase.is_read_only(StatsCommand)`).

#### Execução dos Testes:
```bash
pytest test/test_stats_command.py -v
```

**Resultado Obtido:**
```text
============================= test session starts =============================
collected 8 items

test/test_stats_command.py::StatsCommandTest::test_calculate_stats_metrics PASSED [ 12%]
test/test_stats_command.py::StatsCommandTest::test_format_stats_invalid_language_fallback PASSED [ 25%]
test/test_stats_command.py::StatsCommandTest::test_format_stats_portuguese PASSED [ 37%]
test/test_stats_command.py::StatsCommandTest::test_stats_empty_list PASSED         [ 50%]
test/test_stats_command.py::StatsCommandTest::test_stats_execution_with_tasks PASSED [ 62%]
test/test_stats_command.py::StatsCommandTest::test_stats_help PASSED             [ 75%]
test/test_stats_command.py::StatsCommandTest::test_stats_invalid_due_dates PASSED [ 87%]
test/test_stats_command.py::StatsCommandTest::test_stats_subcommand_registration PASSED [100%]

============================== 8 passed in 2.67s ==============================
```

---

### Fase 3: Validação Prática sobre `meus_teste_topydo/todo.txt`

#### 📁 Arquivos desta fase:
* **Arquivos Adicionados:**
  * [`meus_teste_topydo/todo.txt`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/meus_teste_topydo/todo.txt) (base oficial enriquecida com todas as tags, projetos, dependências e contextos);
  * [`meus_teste_topydo/meu_todo_teste.txt`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/meus_teste_topydo/meu_todo_teste.txt).
* **Arquivos Modificados:**
  * [`atvd/exemplos_testes.md`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/atvd/exemplos_testes.md) (revisado para direcionar todos os 32 testes para `meus_teste_topydo/todo.txt` e detalhar a sintaxe correta no rodapé do modo colunas).

#### Teste A: Execução do Novo Comando via CLI Normal
Comando executado:
```bash
python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt stats
```

**Saída Obtida no Terminal:**
```text
Todo List Statistics:
  Total tasks: 10
  Completed:   1
  Pending:     9
  Overdue:     1

Tasks by project:
  +Faculdade: 4
  +OpenSource: 1
  +Pessoal: 3
  +Trabalho: 1
```

> **Notas de Interpretação dos Resultados:**
> 1. **Tarefas Concluídas e a Flag `-a`:** O valor `Completed: 1` reflete a conclusão de tarefa no arquivo. Para testes sem envio de concluídas para o `done.txt`, utilizou-se a flag `-a` (*do not archive*), garantindo que tarefas com `x` permaneçam em `todo.txt` e sejam contabilizadas.
> 2. **Soma dos Projetos vs. Total de Tarefas:** A soma das tarefas por projeto é 9 (4 + 1 + 3 + 1 = 9), enquanto o total de tarefas é 10. Isso decorre da especificação do padrão *todo.txt*, onde a marcação de projeto (`+projeto`) é opcional — a tarefa de rascunho interno não possui nenhum projeto associado.

#### Teste B: Consulta da Ajuda Específica
Comando executado:
```bash
python -m topydo.ui.UILoader help stats
```

**Saída Obtida:**
```text
Synopsis: stats

Displays summary statistics of the todo list.
```

#### Teste C: Execução no Modo Colunas (*Column Mode* / TUI)
O modo colunas do `topydo` fornece uma interface de terminal interativa rica (baseada na biblioteca `urwid`), onde as tarefas são distribuídas visualmente em colunas categorizadas por projeto ou contexto.

##### 1. Como Iniciar o Modo Colunas:
No ambiente com suporte a terminais ANSI (Linux / WSL com pacote `urwid` instalado):
```bash
python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt columns
```

##### 2. Interação e Atalhos Rápidos de Teclado:
* **`j` / `k`** ou **Setas para Cima/Baixo**: navega entre as tarefas da coluna atual.
* **`h` / `l`** ou **Setas Esquerda/Direita**: alterna entre as colunas do painel.
* **`x`**: marca a tarefa selecionada como concluída (`done`).
* **`d`**: exclui a tarefa selecionada.
* **`u`**: desfaz a última alteração (*undo / revert*).
* **`e`**: abre o editor para modificar a tarefa.
* **`q`**: sai do modo colunas.

##### 3. Execução de Comandos pelo Rodapé (`:`):
Pressionando a tecla **`:`** (dois pontos), a interface abre um prompt de comandos no rodapé exibindo `topydo> `.  
*(Nota: o comando deve ser digitado diretamente, sem inserir outro dois-pontos inicial)*.

Principais comandos testados e validados no rodapé do modo colunas:

| Operação | Comando no Rodapé | Comportamento e Saída Esperada |
| :--- | :--- | :--- |
| **Exibir Estatísticas** | `topydo> stats` | Abre um console sobreposto exibindo o sumário estatístico completo (tarefas, pendências, atrasadas e projetos). Pressionar `Esc` ou `Enter` fecha o console. |
| **Adicionar Tarefa** | `topydo> add (A) Revisar artigo +Faculdade @computador due:2026-11-20` | Cria a nova tarefa; a coluna de `+Faculdade` é imediatamente atualizada na tela exibindo o novo item. |
| **Alterar Prioridade** | `topydo> pri 4 B` | Atualiza a prioridade da tarefa 4 para `(B)` e a reordena na coluna. |
| **Remover Prioridade** | `topydo> depri 4` | Remove a prioridade da tarefa 4. |
| **Adicionar/Editar Tag** | `topydo> tag 4 due:2026-11-25` | Altera a data de vencimento da tarefa 4. |
| **Concluir Tarefa** | `topydo> do 4` | Conclui a tarefa 4, movendo-a ou ocultando-a da coluna ativa. |
| **Excluir Tarefa** | `topydo> del 24` | Remove a tarefa 24 da listagem com confirmação. |
| **Listar Projetos** | `topydo> lsprj` | Abre janela de console listando apenas os nomes dos projetos (sem contagens). A contagem de tarefas por projeto é exclusividade do comando `stats`. |
| **Listar Contextos** | `topydo> lscon` | Abre janela de console listando os nomes dos contextos (`@contexto`). |
| **Reordenar Arquivo** | `topydo> sort` *(ou `sort desc:priority`)* | Reordena fisicamente as linhas gravadas no arquivo `todo.txt` no disco. *(Nota: as colunas da tela já possuem ordenação visual própria configurada, por isso o efeito do `sort` ocorre no arquivo físico em disco)*. |
| **Sair da Aplicação** | `topydo> q` | Encerra a interface de colunas e retorna ao shell do terminal. |

##### 4. Atualização Automática em Tempo Real (Modo Dois Terminais):
Como o `topydo columns` utiliza a biblioteca `watchdog` para monitorar o arquivo em disco:
* **Terminal 1:** Mantém o modo colunas aberto e visível (`python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt columns`).
* **Terminal 2:** Executa comandos tradicionais da CLI (ex.: `python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt add Nova tarefa +Faculdade`).
* **Resultado:** O Terminal 1 detecta o evento de alteração em `meus_teste_topydo/todo.txt` e redesenha instantaneamente as colunas na tela em tempo real, sem necessidade de intervenção do usuário.

---

### Fase 4: Documentação Consolidada e Entrega

#### 📁 Arquivos desta fase:
* **Arquivos Adicionados:**
  * [`atvd/relatorio.md`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/atvd/relatorio.md) (este documento formal de fechamento e prestação de contas da Atividade 04).

---

## 4. Como Construir (*Build*), Configurar o Ambiente e Testar

### 4.1. Visão Geral do *Build* e Empacotamento
O `topydo` é estruturado como um pacote padrão Python configurado via `setup.py`. O processo de *build* e instalação organiza o software e suas dependências modulares em grupos (*extras*):
* `columns`: instala a biblioteca `urwid` para a interface TUI em colunas;
* `ical`: instala bibliotecas de exportação para calendários iCalendar;
* `prompt`: instala suporte para modo interativo avançado (`prompt_toolkit`);
* `test`: instala as ferramentas de teste automatizado (`pytest`, `freezegun`, etc.).

A compilação e instalação no ambiente de desenvolvimento é feita em modo de pacote via `pip install ".[columns,ical,prompt,test]" pytest`.

---

### 4.2. Fluxo Real de Inicialização do Ambiente (Windows + WSL 2 / Ubuntu)
Como o projeto utiliza a biblioteca de interface de terminal `urwid` (que exige terminal compatível com POSIX/ANSI e não opera no Windows nativo), o ambiente oficial de execução e testes utilizado no projeto foi o **WSL 2 (Windows Subsystem for Linux) com a distribuição Ubuntu**.

Abaixo está o fluxo real de comandos utilizado para inicializar a máquina de desenvolvimento:

#### 1. No PowerShell do Windows (Host):
Verificação das distribuições instaladas e inicialização da instância Ubuntu:
```powershell
(base) PS C:\Users\lucas> wsl -l -v
  NAME              STATE           VERSION
* docker-desktop    Running         2
  Ubuntu            Running         2

(base) PS C:\Users\lucas> wsl -d Ubuntu
```

#### 2. No Terminal Linux do WSL (Ubuntu):
Navegação até a pasta do repositório montada via `/mnt/c/` e ativação do ambiente virtual Python:
```bash
lucas@Lucas:/mnt/c/Users/lucas$ cd "/mnt/c/Users/lucas/OneDrive/Documentos/GitHub/topydo"
lucas@Lucas:/mnt/c/Users/lucas/OneDrive/Documentos/GitHub/topydo$ source .venv/bin/activate
(.venv) lucas@Lucas:/mnt/c/Users/lucas/OneDrive/Documentos/GitHub/topydo$
```

---

### 4.3. Instalação das Dependências (*Build* Local)
Com o ambiente virtual ativado no WSL:
```bash
# Atualizar ferramentas de empacotamento:
pip install --upgrade pip setuptools

# Instalação completa do pacote e dependências de teste:
pip install ".[columns,ical,prompt,test]" pytest
```

---

### 4.4. Executar os Testes Automatizados
```bash
# Rodar todos os 8 testes unitários do novo subcomando stats:
pytest test/test_stats_command.py -v

# Rodar a suíte completa de testes do repositório:
pytest
```

---

### 4.5. Executar o Subcomando de Estatísticas (`stats`)
```bash
# Execução direta via CLI tradicional:
python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt stats
```

---

### 4.6. Executar a Interface Interativa em Modo Colunas (*Column Mode*)
```bash
# Inicializar o modo colunas:
python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt columns

# Dentro do modo colunas:
# 1. Pressione a tecla ':' para abrir o prompt no rodapé (topydo> ).
# 2. Digite 'stats' e aperte Enter para exibir o relatório estatístico em janela sobreposta.
# 3. Pressione 'Esc' ou 'Enter' para fechar o popup e voltar à navegação das colunas.
```

---

### 4.7. Controle de Auto-Arquivamento de Tarefas Concluídas (Flag `-a`)
Por padrão, o `topydo` possui um mecanismo de **auto-arquivamento** (*auto-archive*): ao concluir uma tarefa com o comando `do`, ela é marcada com `x`, mas imediatamente transferida para o arquivo histórico `done.txt` (sendo removida do `todo.txt` para manter a lista limpa).

Para quem deseja **manter as tarefas concluídas dentro do próprio arquivo `todo.txt`** (permitindo que o `topydo stats` as contabilize continuamente no campo `Completed`), utiliza-se a flag **`-a`** (*do not archive*):

* **Na CLI tradicional (sem colunas):**
  ```bash
  # Concluir uma tarefa mantendo-a salva no todo.txt (sem mover para done.txt):
  python -m topydo.ui.UILoader -a -t meus_teste_topydo/todo.txt do <ID>

  # Em seguida, verificar a contagem de 'Completed' incrementada no stats:
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt stats
  ```

* **No Modo Colunas (*Column Mode*):**
  ```bash
  # Abrir a interface de colunas com o auto-arquivamento desativado:
  python -m topydo.ui.UILoader -a -t meus_teste_topydo/todo.txt columns
  ```
  *(Dentro da interface, qualquer `topydo> do <ID>` permanecerá no `todo.txt` e será somado no `topydo> stats`)*.

---

## 5. Relatório da Experiência com Agentes de IA

Em cumprimento aos requisitos descritos na seção 1.2 da [Atividade04.md](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/atvd/Atividade04.md):

### 5.1. O que funcionou bem
* **Compreensão da arquitetura do repositório:** O agente de IA localizou rapidamente a estrutura modular do `topydo`, identificando os arquivos de roteamento (`Commands.py` e `CLIApplicationBase.py`) e os padrões de herança da classe `Command`.
* **Separação de responsabilidades:** A separação sugerida entre cálculo puro (`calculate_stats`) e formatação (`format_stats`) tornou os testes unitários simples e determinísticos (permitindo testar tarefas atrasadas sem depender do relógio do sistema).
* **Depuração ágil de erros de execução:** Durante o primeiro teste no terminal, a interface CLI acusou `AttributeError: 'str' object has no attribute 'data'`. O agente diagnosticou imediatamente que o método `output()` esperava instâncias de `TopydoString` quando recebia listas, e corrigiu a iteração linha a linha no `StatsCommand.py`.

### 5.2. O que não funcionou / Desafios enfrentados
* **Divergências de ambiente (Windows vs. Linux/WSL):** A biblioteca de interface de colunas (`urwid`) não oferece suporte nativo ao console do Windows, gerando mensagens de restrição em PowerShell. Foi necessário esclarecer que o modo colunas opera nativamente em ambientes Unix (Linux/WSL).
* **Sintaxe no rodapé do modo colunas:** Inicialmente, a documentação continha exemplos com dois-pontos (ex.: `:tag`), fazendo com que no prompt `topydo> ` o comando ficasse `topydo> :tag`, o que impedia a execução. O problema foi identificado e corrigido para a sintaxe direta (`topydo> tag`).
* **Concorrência e travas do Git no Windows:** Durante a criação de commits, o arquivo `.git/index.lock` apresentou conflitos temporários de concorrência com o serviço de sincronização do OneDrive, sendo necessário executar comandos de escrita com elevação de sandbox.

### 5.3. O que houve de inesperado no processo
* A descoberta do mecanismo nativo de *file watching* (`watchdog`) no `topydo`: ao manter o modo colunas aberto em um terminal e executar comandos de escrita em outro, a interface gráfica se atualiza automaticamente em tempo real sem necessidade de recarregamento manual.
* O comportamento de auto-arquivamento (*auto-archive*) nativo do `topydo`: ao executar o comando `do`, as tarefas concluídas são movidas imediatamente para o arquivo histórico `done.txt` por padrão. Para manter tarefas concluídas registradas no próprio `todo.txt` e contabilizadas no `stats`, descobriu-se o papel essencial da flag `-a` (*do not archive*), tanto para uso via CLI tradicional quanto no modo colunas.
* O sistema de testes do projeto original já possuía uma classe base robusta (`CommandTest`) com captura de `stdout` e `stderr`, o que simplificou bastante a escrita dos novos testes unitários.

### 5.4. Nível de familiaridade prévio com as tecnologias
* A equipe possuía familiaridade prévia com a linguagem Python, controle de versão Git e conceitos de testes unitários.
* Não havia familiaridade prévia com a arquitetura interna do `topydo`, nem com a biblioteca `urwid` (TUI baseada em widgets de terminal), o que tornou o suporte do agente valioso para interpretar mensagens de erro e padrões internos.

### 5.5. Principais aprendizados da equipe
* **Engenharia de Manutenção:** A importância de estabelecer uma linha de base (*baseline*) sólida antes de alterar qualquer código em um projeto legado de software livre.
* **Extensibilidade e Padrões de Projeto:** O projeto utiliza o padrão *Command* e um registro desacoplado por dicionário de classes, demonstrando como uma arquitetura bem projetada permite plugar novas funcionalidades sem modificar a lógica central existente.
* **Colaboração com Agentes de Codificação:** A experiência de *pair programming* com IA mostrou-se produtiva não apenas para gerar código, mas principalmente para navegar em bases de código desconhecidas, gerar dados de teste ricos e produzir documentação técnica completa.
