---
marp: true
theme: default
paginate: true
header: "Topydo — Filosofia, Arquitetura e Subcomando `stats` | Atividade 04"
footer: "Tópicos Avançados em Ciência da Computação — Prof. Andrei Formiga"
---

# 📊 Topydo & Novo Subcomando `stats`
## Manutenção em Software Livre e Engenharia de Software com IA

**Projeto:** [topydo](https://github.com/topydo/topydo) (Python / padrão *todo.txt*)  
**Fork do Trabalho:** [lucasmarinhoba/topydo](https://github.com/lucasmarinhoba/topydo)  
**Grupo:** Guilherme Peixoto Gurgel, João Pedro Figueiredo Chaves, Lucas Marinho Basilio de Sousa, Yuri Silva Bezerra de Lima  
**Disciplina:** Tópicos Avançados em Ciência da Computação — Prof. Andrei Formiga  

---

## 🧩 1. O que é o `topydo` e a Filosofia *todo.txt*

* **Software Livre em Python (GPLv3):** Gerenciador de tarefas leve, extensível e focado em produtividade via terminal.
* **Padrão `todo.txt` (Texto Puro):**
  * Sem banco de dados binário ou proprietário — toda a base cabe em um arquivo `.txt`.
  * **Legível por humanos** em qualquer editor de texto e **versionável** com Git.
  * Portável entre sistemas e ferramentas.
* **Três Modos de Operação:**
  1. **CLI Tradicional:** Comandos pontuais no shell (`topydo ls`, `topydo add`, `topydo stats`).
  2. **Prompt Interativo:** Shell contínuo (`topydo prompt`) com histórico e autocompletar.
  3. **Modo Colunas (TUI):** Painel visual estilo Kanban no terminal com `urwid` e atualização em tempo real via `watchdog` (ao editar o arquivo em outro terminal, as colunas atualizam sozinhas).

> 🗣️ **O que falar:** *"Antes de mostrar o que criamos, vale entender o topydo: ele segue a filosofia todo.txt, onde todo o banco de dados é texto puro. Mesmo sendo texto simples, ele entrega uma interface avançada em colunas com atualização automática em tempo real."*

---

## 🔬 2. Anatomia de uma Tarefa no `topydo`

Cada linha do arquivo `todo.txt` carrega metadados estruturados de forma legível:

```text
x 2026-11-18 (A) 2026-11-01 Entregar relatório +Faculdade @computador due:2026-11-10 id:1
```

* **`x YYYY-MM-DD`:** Marca a tarefa como concluída e registra a data de conclusão.
* **`(A)`, `(B)`, `(C)`:** Níveis de prioridade (de A até Z).
* **`+Projeto`:** Agrupamento temático / projeto (ex.: `+Faculdade`, `+Trabalho`, `+Pessoal`).
* **`@Contexto`:** Local, ferramenta ou situação de execução (ex.: `@computador`, `@financas`).
* **Tags estendidas (`chave:valor`) nativas do `topydo`:**
  * `due:YYYY-MM-DD`: Data de vencimento (aceita datas relativas como `tod`, `tom`, `1w`).
  * `t:YYYY-MM-DD`: Data de início (*threshold*) — oculta a tarefa até chegar a data.
  * `rec:1w` / `rec:1m`: Recorrência automática ao concluir.
  * `id:N` e `p:N`: Grafo de dependências entre tarefas pai e subtarefas.
  * `h:1`: Marcação de **tarefa oculta** (*hidden*) para rascunhos internos.

---

## ⚙️ 3. Mecanismos Internos Importantes do `topydo`

Para compreender como o sistema se comporta ao vivo, dois conceitos internos são essenciais:

### A. Auto-Arquivamento (`done.txt`) vs. Flag `-a`
* Por padrão, ao concluir uma tarefa (`do`), o `topydo` marca com `x` e a **remove do `todo.txt`**, arquivando-a em `done.txt` para manter a lista limpa.
* Ao iniciar com a flag **`-a`** (*do not archive*), as tarefas concluídas permanecem no `todo.txt`, permitindo contabilizá-las continuamente no `stats`.

### B. Filtros Automáticos do Modo Colunas
Por padrão, cada coluna aplica 3 filtros internos sobre a lista bruta:
1. **`RelevanceFilter`:** Oculta tarefas já concluídas (`x`) e tarefas futuras (`t:` maior que hoje).
2. **`DependencyFilter`:** Oculta tarefas pai (`id:N`) enquanto existirem subtarefas (`p:N`) pendentes.
3. **`HiddenTagFilter`:** Oculta tarefas com a tag **`h:1`** da visualização padrão (só visíveis via `ls -x`).

---

## 🔍 4. O Problema e a Motivação do `topydo stats`

* O `topydo` possuía filtros e exportadores (`ls -f json`, `ical`, `dot`), mas **nenhum resumo quantitativo**.
* **Limitações identificadas na Atividade 03:**
  * O comando nativo `lsprj` exibe apenas os *nomes* dos projetos (sem quantidade de tarefas).
  * Não havia comando para responder rapidamente: *"Quantas tarefas estão concluídas?"*, *"Quantas estão atrasadas?"*, *"Qual o peso de cada projeto?"*.
* **Solução Planejada e Implementada:** Criar o subcomando **`topydo stats`** seguindo rigorosamente a arquitetura original de comandos do projeto.

---

## 🚀 5. A Nova Funcionalidade (`topydo stats`) e Arquitetura

### Saída Padronizada do Comando
```text
Todo List Statistics:
  Total tasks: 6
  Completed:   1
  Pending:     5
  Overdue:     2

Tasks by project:
  +Faculdade: 3
  +Pessoal: 1
  +Trabalho: 1
```

### Design Modular (seguindo o `CONTRIBUTING.md`)
* **[`topydo/commands/StatsCommand.py`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/commands/StatsCommand.py):**
  * `_is_overdue` e `_count_projects`: funções auxiliares curtas e de responsabilidade única.
  * `calculate_stats(p_todolist, p_reference_date=None)`: lógica pura e determinística (aceita data de referência para testes sem depender do relógio).
  * `format_stats(p_stats, p_lang='en')`: apresentação desacoplada com dicionário `LABELS` (inglês e português com fallback).
  * `StatsCommand(Command)`: classe de comando seguindo a interface base do `topydo`.
* **Integração:** Registrado em [`SUBCOMMAND_MAP`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/Commands.py#L47) e marcado em [`READ_ONLY_COMMANDS`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/ui/CLIApplicationBase.py#L30) (não altera arquivos nem cria backups).

---

## 🧪 6. Qualidade e Testes Automatizados (`pytest`)

* **Zero Regressão na Linha de Base:** Todos os **825 testes originais** do repositório permanecem passando no ambiente Linux/WSL.
* **Nova Suíte em [`test/test_stats_command.py`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/test/test_stats_command.py) (8/8 aprovados):**
  1. `test_stats_empty_list` — lista vazia (`Total tasks: 0`, `Projects: none`);
  2. `test_calculate_stats_metrics` — total, concluídas, pendentes, atrasadas e projetos (com data fixa);
  3. `test_stats_invalid_due_dates` — tolerância a datas malformadas sem lançar exceções;
  4. `test_stats_execution_with_tasks` — execução ponta a ponta e ordenação case-insensitive;
  5. `test_stats_help` — saída de ajuda `stats help`;
  6. `test_format_stats_portuguese` — formatação com `lang='pt'`;
  7. `test_format_stats_invalid_language_fallback` — fallback seguro para inglês;
  8. `test_stats_subcommand_registration` — validação do roteador `get_subcommand` e `is_read_only`.

---

## 🖥️ 7. Preparação da Demo ao Vivo (Modo Colunas no WSL)

O modo colunas usa `urwid` (POSIX/ANSI), executado via **WSL 2 (Ubuntu)**:

### Passo 0 — Abrir o terminal Ubuntu correto no PowerShell:
> ⚠️ Digite sempre `wsl -d Ubuntu` (se digitar só `wsl`, pode cair na distro padrão `docker-desktop` em `/mnt/host/c/` onde o `.venv` não existe).
```powershell
wsl -d Ubuntu
```

### Passo 1 — Entrar no projeto e iniciar o Modo Colunas com `-a`:
```bash
cd "/mnt/c/Users/lucas/OneDrive/Documentos/GitHub/topydo"
source .venv/bin/activate
python -m topydo.ui.UILoader -a -t meus_teste_topydo/todo.txt columns
```

### Como operar os comandos dentro do Modo Colunas:
* **Navegação:** Setas ou `j`/`k` (vertical) e `h`/`l` (entre colunas) | **`x`**: conclui tarefa | **`q`**: sai.
* **Rodapé de comandos:** Pressione **`:`** para abrir `topydo> ` e digite o comando **sem repetir o `:`**.
* **Popups de saída (`stats`, `ls -x`):** Pressione **`Esc`** ou **`Enter`** para fechar o console e voltar às colunas.

---

## 🎬 8. Demo — Ato 1: Visão Inicial e Primeiro `stats`

O arquivo limpo [`meus_teste_topydo/todo.txt`](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/meus_teste_topydo/todo.txt) começa com **6 tarefas**:
* Coluna **"All tasks"**: exibe **4 tarefas visíveis**.
* Coluna **"Overdue tasks"**: exibe **2 tarefas atrasadas** (`due:2026-11-10` e `due:2026-11-05`).

### No rodapé das colunas, pressione `:` e execute:
```text
topydo> stats
```

### Saída exibida no popup:
```text
Todo List Statistics:
  Total tasks: 6
  Completed:   1
  Pending:     5
  Overdue:     2

Tasks by project:
  +Faculdade: 3
  +Pessoal: 1
  +Trabalho: 1
```

> 🗣️ **O que destacar:** *"Reparem em duas curiosidades: (1) A soma dos projetos dá 5 porque uma tarefa não tem `+projeto` (no todo.txt é opcional); (2) O `stats` acusa **5 pendentes**, mas na coluna só vemos **4**. Guardem esse detalhe para o final!"*

*(Pressione `Esc` para voltar às colunas).*

---

## 🎬 9. Demo — Ato 2: Adicionando Tarefa Atrasada (+Novo Projeto)

### No rodapé das colunas, pressione `:` e execute:
```text
topydo> add (A) Entregar slides finais +Apresentacao @faculdade due:2026-10-01
```

* O cartão aparece **imediatamente** tanto na coluna **"All tasks"** quanto na coluna **"Overdue tasks"**.

### Consulte as estatísticas novamente (`:` → `stats` → Enter):
```text
Todo List Statistics:
  Total tasks: 7
  Completed:   1
  Pending:     6
  Overdue:     3

Tasks by project:
  +Apresentacao: 1
  +Faculdade: 3
  +Pessoal: 1
  +Trabalho: 1
```

* **Total** subiu para `7`, **Pending** para `6`, **Overdue** para `3`, e **`+Apresentacao: 1`** surgiu automaticamente em ordem alfabética!

*(Pressione `Esc` para voltar às colunas).*

---

## 🎬 10. Demo — Ato 3: Alterando Prioridades e Navegando

Além de consultar estatísticas, todos os comandos do `topydo` funcionam no rodapé do modo colunas e refletem na hora:

### No rodapé, pressione `:` e eleve a prioridade da tarefa 4 para `(A)`:
```text
topydo> pri 4 A
```

* A tarefa **`Revisar documentação técnica +Trabalho`** recebe prioridade `(A)` e se reposiciona no topo da coluna de acordo com a ordenação visual.

---

## 🎬 11. Demo — Ato 4: Concluindo Todas as Tarefas Visíveis

Agora vamos limpar todas as tarefas visíveis na tela!

### Escolha uma das duas formas nas colunas:
* **Pelo atalho de teclado:** Selecione cada uma das **5 tarefas visíveis** na coluna `"All tasks"` usando `j`/`k` e pressione **`x`** em cada uma.
* **Ou pelo rodapé em um só comando** (`:` → Enter):
  ```text
  topydo> do 1 2 3 4 7
  ```

### Resultado Visual na Tela:
* Todas as colunas (**"All tasks"**, **"Due today"** e **"Overdue tasks"**) ficam **100% vazias**!

> 🗣️ **O que falar:** *"Olhando para a interface visual, parece que finalizamos 100% do nosso trabalho do dia, certo? Vamos confirmar no `stats`!"*

---

## 🕵️ 12. Demo — Ato 5 (Gran Finale): O Mistério da Tarefa Oculta (`h:1`)

Com a tela aparentemente vazia, pressione **`:`** e execute:
```text
topydo> stats
```

### Saída surpreendente no popup:
```text
Todo List Statistics:
  Total tasks: 7
  Completed:   6
  Pending:     1
  Overdue:     0
```

* **Por que ainda existe `Pending: 1` se a tela está vazia?** Porque há uma tarefa marcada com a tag **`h:1`** (*hidden*), ocultada automaticamente pelo `HiddenTagFilter` das colunas! *(Pressione `Esc` para fechar o popup).*

### Vamos revelar e concluir essa tarefa oculta ao vivo:
1. **Prove onde ela está** listando inclusive tarefas ocultas/concluídas (`:` → Enter → `Esc`):
   ```text
   topydo> ls -x
   ```
   *(Mostra a linha `6: Rascunho oculto de melhorias futuras h:1`)*.
2. **Remova a tag de ocultação `h:1`** pelo rodapé (`:` → Enter → `Esc`):
   ```text
   topydo> tag 6 h
   ```
   *(A tarefa aparece **instantaneamente** na coluna `"All tasks"` que estava vazia!)*.
3. **Conclua a tarefa** apertando **`x`** sobre ela e rode `:` → `stats`:
   * Resultado final: **`Total tasks: 7 | Completed: 7 | Pending: 0 | Overdue: 0`**!

---

## 🤖 13. Desafios Superados e Experiência com IA

### Principais Desafios Técnicos Descobertos e Resolvidos
1. **Integração com `TopydoString` na CLI:** O `output()` esperava objetos `TopydoString` quando recebia listas; corrigimos iterando linha por linha no `StatsCommand.py`.
2. **Comportamento do Auto-Archive:** Compreendemos que `do` arquiva no `done.txt` por padrão e documentamos a flag `-a` para manter estatísticas históricas em `todo.txt`.
3. **Sintaxe do Modo Colunas & Ambiente:** Identificamos que o rodapé `topydo> ` dispensa o `:` extra e que o `urwid` requer Linux/WSL (`wsl -d Ubuntu`).

### Experiência de *Pair Programming* com Agente de IA
* **Ganhos:** Leitura rápida de código legado, separação limpa entre negócio e formatação, criação de suíte determinística de 8 testes e agilidade na depuração.
* **Papel Humano:** Validar cenários reais no modo colunas, identificar divergências visuais (`lsprj`, `sort`, tarefas ocultas/bloqueadas) e orientar as decisões arquiteturais.

---

## 🏁 14. Conclusão

* ✅ Subcomando **`topydo stats`** entregue seguindo os padrões e estilo do projeto original.
* ✅ Arquitetura testável com cálculo desacoplado da formatação e suporte multilíngue (`en`/`pt`).
* ✅ **825 testes originais** intactos + **8 novos testes unitários** 100% aprovados.
* ✅ Compatibilidade total validada via **CLI** e ao vivo no **Modo Colunas**.

**Obrigado pela atenção! Perguntas?**
