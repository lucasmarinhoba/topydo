# Relatório da Fase 0 — Estabelecimento da Linha de Base (*Baseline*)

**Projeto:** topydo  
**Repositório (Fork):** [lucasmarinhoba/topydo](https://github.com/lucasmarinhoba/topydo)  
**Branch:** `master`  
**Commit de Referência:** `37eba58`  
**Atividade:** Atividade 04 – Manutenção em Projeto Existente  

---

## 1. Objetivo da Fase 0

A **Fase 0** consiste em avaliar, testar e registrar o estado inicial do projeto antes de qualquer intervenção no código-fonte. Seu propósito é:
1. Validar que o ambiente de execução e a suíte de testes original estão íntegros;
2. Definir a linha de base de testes para garantia de não-regressão;
3. Criar os dados reais de teste para validações manuais;
4. Comprovar formalmente que a funcionalidade planejada (`topydo stats`) **não existe** no projeto atual.

---

## 2. Linha de Base dos Testes Automatizados

Conforme verificado no ambiente oficial de referência (Linux / WSL com extras `columns`, `ical`, `prompt` e `test`):

```bash
python -m pytest
```

### Resultado Obtido:
* **Total de testes:** 829
* **Testes aprovados (*passed*):** 825
* **Testes ignorados (*skipped*):** 4
* **Falhas (*failed* / *errors*):** 0

> [!IMPORTANT]
> **Critério de Não-Regressão para a Fase 1:**  
> Após a implementação do comando `stats`, os **825 testes originais devem continuar passando sem falhas**.

---

## 3. Dados Reais de Teste Criados

Foi criado na raiz do repositório o arquivo [`meu_todo_teste.txt`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/meu_todo_teste.txt) com cenários diversificados para testar os subcomandos atuais e servir de base para o futuro `stats`:

```text
(A) 2026-10-01 Entregar relatório da Atividade 03 +Faculdade @computador due:2026-10-15
(B) 2026-11-01 Implementar testes no topydo +Faculdade @estudos due:2026-11-10
x 2026-10-20 Estudar estrutura de comandos do topydo +Faculdade @leitura
Comprar café e lanche +Pessoal @mercado
(C) Pagar fatura do cartão +Pessoal @financas due:2026-10-25
```

### Características dos dados de teste:
* **Total de tarefas:** 5
* **Concluídas:** 1 (iniciada com `x 2026-10-20`)
* **Pendentes:** 4
* **Tarefas com vencimento no passado (atrasadas em relação a nov/2026):**
  * `due:2026-10-15` (tarefa A, pendente -> atrasada)
  * `due:2026-10-25` (tarefa C, pendente -> atrasada)
* **Tarefas com vencimento futuro:**
  * `due:2026-11-10` (tarefa B, pendente -> dentro do prazo)
* **Projetos identificados:**
  * `+Faculdade`: 3 tarefas
  * `+Pessoal`: 2 tarefas

---

## 4. Validação Manual dos Comandos Existentes

### 4.1. Listagem de tarefas ativas (`ls`)
Comando executado:
```bash
topydo -t meu_todo_teste.txt ls
```
**Comportamento observado:**  
Exibe apenas as 4 tarefas pendentes, ordenadas por prioridade `(A)`, `(B)`, `(C)` e sem prioridade. A tarefa concluída com `x` é ocultada, conforme o comportamento padrão do `topydo`.

### 4.2. Listagem de projetos (`lsprj`)
Comando executado:
```bash
topydo -t meu_todo_teste.txt lsprj
```
**Comportamento observado:**  
Lista corretamente os nomes únicos dos projetos em ordem alfabética:
```text
Faculdade
Pessoal
```

---

## 5. Comprovação da Ausência do Subcomando `stats`

### 5.1. No código-fonte:
* **Mapeamento em `topydo/Commands.py`:**
  O dicionário `SUBCOMMAND_MAP` foi inspecionado e **não contém** o subcomando `'stats'`:
  ```python
  SUBCOMMAND_MAP = {
      'add': 'AddCommand',
      'app': 'AppendCommand',
      'append': 'AppendCommand',
      'del': 'DeleteCommand',
      'dep': 'DepCommand',
      'depri': 'DepriCommand',
      'do': 'DoCommand',
      'edit': 'EditCommand',
      'exit': 'ExitCommand',
      'ls': 'ListCommand',
      'lscon': 'ListContextCommand',
      'lsprj': 'ListProjectCommand',
      'mod': 'ModifyCommand',
      'modify': 'ModifyCommand',
      'postpone': 'PostponeCommand',
      'pri': 'PriorityCommand',
      'quit': 'ExitCommand',
      'revert': 'RevertCommand',
      'rm': 'DeleteCommand',
      'sort': 'SortCommand',
      'tag': 'TagCommand',
  }
  ```
* **Ausência de módulo:** O arquivo `topydo/commands/StatsCommand.py` não existe no diretório.

### 5.2. Na execução via CLI:
Ao tentar executar:
```bash
topydo -t meu_todo_teste.txt stats
```
O sistema não reconhece o subcomando e exibe o menu de ajuda geral (`topydo help`).

---

## 6. Conclusão da Fase 0

* [x] Linha de base de testes estabelecida (825 passed, 0 failures).
* [x] Massa de dados real de teste criada (`meu_todo_teste.txt`).
* [x] Funcionamento dos comandos existentes validado.
* [x] Ausência da funcionalidade `stats` confirmada no código e no CLI.
* [x] Repositório pronto na branch `master` para início da **Fase 1 (Implementação de `StatsCommand.py`)**.
