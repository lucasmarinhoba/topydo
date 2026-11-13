---
marp: true
theme: default
paginate: true
header: "Topydo — Implementação do Subcomando `stats` | Atividade 04"
footer: "Lucas Marinho — Engenharia de Software"
---

# 📊 Implementação do Subcomando `topydo stats`
## Manutenção de Software Livre e Engenharia de Software com IA

**Projeto:** [topydo](https://github.com/topydo/topydo) (Python / todo.txt)  
**Autor:** Lucas Marinho  
**Disciplina:** Tópicos Avançados em Engenharia de Software  
**Professor:** Andrei Formiga  

---

## 🎯 1. Contexto e Objetivo da Atividade

* **Projeto Escolhido:** `topydo` — Gerenciador CLI/TUI de tarefas em Python baseado no padrão mundial *todo.txt*.
* **Desafio da Atividade 04:** Executar na prática a melhoria de software planejada na Atividade 03, mantendo integridade total do sistema legado.
* **A Melhoria:** Criação do subcomando **`stats`**, fornecendo um sumário analítico e métricas em tempo real sobre a lista de tarefas.
* **Metodologia:** Desenvolvimento assistido por agente inteligente de IA, com rigorosa cobertura de testes unitários e respeito aos padrões arquiteturais do projeto.

> 🗣️ **O que falar:** *"O topydo é um projeto consolidado de software livre que gerencia tarefas complexas. Na Atividade 03 identificamos que não havia nenhum comando nativo para resumir métricas. Na Atividade 04, implementamos e testamos essa solução de ponta a ponta."*

---

## 🔍 2. O Problema: Ausência de Visão Consolidada

* O `topydo` possuía comandos de listagem avançados (`ls`, `ls -x`, `ls -f json/ical/dot`), filtros por prioridade e visualização em colunas.
* **Limitações encontradas:**
  1. O comando `lsprj` lista apenas os *nomes* dos projetos cadastrados, sem quantificar tarefas.
  2. Não havia resposta rápida para: *"Quantas tarefas faltam?"*, *"Quantas estão atrasadas?"*, *"Como meus projetos estão distribuídos?"*.
  3. O usuário precisava inspecionar listas longas manualmente ou recorrer a scripts externos.

> 🗣️ **O que falar:** *"Embora o topydo fosse excelente para organizar itens, faltava um dashboard rápido de produtividade. Foi essa lacuna que o comando stats veio preencher."*

---

## 🚀 3. A Nova Funcionalidade: `topydo stats`

O novo subcomando calcula e exibe de forma clara:
1. **Total de tarefas** (`Total tasks`);
2. **Tarefas concluídas** (`Completed`, marcadas com `x`);
3. **Tarefas pendentes** (`Pending`);
4. **Tarefas atrasadas (*Overdue*)**: pendências com `due:` anterior à data de hoje;
5. **Distribuição por projeto (`+projeto`)**: contagem ordenada alfabeticamente.

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

---

## 🏗️ 4. Arquitetura e Boas Práticas

Seguindo as diretrizes do `CONTRIBUTING.md` do repositório original:
* **Funções pequenas com responsabilidade única:**
  * `calculate_stats(p_todolist, p_reference_date=None)`: Função pura de negócio. Receber data de referência permite testes determinísticos sem depender do relógio do sistema.
  * `format_stats(p_stats, p_lang='en')`: Função pura de apresentação com dicionário modular `LABELS` (suporte a inglês e português com fallback seguro).
* **Padrão Command:** Classe `StatsCommand(Command)` plugada de forma desacoplada.
* **Integração no Ecossistema:**
  * Registrado em `SUBCOMMAND_MAP` ([Commands.py](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/Commands.py)).
  * Classificado como comando de leitura em `READ_ONLY_COMMANDS` ([CLIApplicationBase.py](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/topydo/ui/CLIApplicationBase.py)).

---

## 🧪 5. Estratégia de Testes Automatizados

* **Linha de Base Preservada:** Todos os **825 testes pré-existentes** continuam passando sem qualquer regressão.
* **Nova Suíte de Testes:** Criado `test/test_stats_command.py` com **8 testes unitários** sem alterar nenhum arquivo de teste original:
  1. Lista vazia (`test_stats_empty_list`);
  2. Cálculo puro de métricas e tarefas atrasadas (`test_calculate_stats_metrics`);
  3. Tratamento robusto de datas inválidas sem lançar exceções (`test_stats_invalid_due_dates`);
  4. Execução ponta a ponta e ordenação case-insensitive (`test_stats_execution_with_tasks`);
  5. Consulta de ajuda do comando (`test_stats_help`);
  6. Internacionalização em português (`test_format_stats_portuguese`);
  7. Fallback seguro para idiomas desconhecidos (`test_format_stats_invalid_language_fallback`);
  8. Roteamento do subcomando (`test_stats_subcommand_registration`).

---

## 🖥️ 6. Preparação para a Demonstração ao Vivo

O modo colunas do `topydo` utiliza a biblioteca `urwid` (interface de terminal rica em POSIX/ANSI).

### Como inicializar o ambiente de apresentação (no WSL 2 / Ubuntu):
```bash
# 1. Navegar até a pasta do projeto:
cd "/mnt/c/Users/lucas/OneDrive/Documentos/GitHub/topydo"

# 2. Ativar o ambiente virtual:
source .venv/bin/activate

# 3. Iniciar o modo colunas com a base oficial de testes:
python -m topydo.ui.UILoader -a -t meus_teste_topydo/todo.txt columns
```

> 💡 **Nota sobre a flag `-a`:** Desativa o auto-arquivamento imediato para `done.txt`, permitindo que as tarefas concluídas durante a demo permaneçam visíveis no `stats`.

---

## 🕹️ 7. Navegação e Comandos no Modo Colunas

Na interface gráfica em colunas:
* **Navegação rápida:** Setas ou teclas `j`/`k` (sobe/desce) e `h`/`l` (troca de coluna).
* **Para digitar comandos:** Pressione a tecla **`:`** (dois pontos).
  * O rodapé abrirá o prompt: `topydo> `
  * **Atenção:** Digite os comandos diretamente (sem digitar outro `:` inicial).
  * Quando o comando abre um popup (como o `stats`), pressione **`Esc`** ou **`Enter`** para fechar e voltar às colunas.

---

## 🎬 8. Demonstração Prática 1: Executando o `stats`

### Passo a passo no rodapé do modo colunas:
1. Pressione **`:`**
2. Digite:
   ```text
   topydo> stats
   ```
3. Pressione **Enter**.

### O que mostrar na tela:
* Uma janela sobreposta (*popup*) se abrirá exibindo o resumo estatístico consolidado:
  * Total de tarefas, pendências e tarefas atrasadas;
  * A distribuição de cada projeto (`+Faculdade`, `+Pessoal`, `+Trabalho`, etc.).
* Pressione **`Esc`** para fechar a janela.

---

## 🎬 9. Demonstração Prática 2: Adicionando Tarefa Atrasada

### Passo a passo no rodapé:
1. Pressione **`:`**
2. Adicione uma tarefa urgente com prazo vencido:
   ```text
   topydo> add (A) Revisar artigo do simpósio +Faculdade @estudos due:2026-10-01
   ```
3. Pressione **Enter**.
4. Abra o `stats` novamente (`:` → `stats` → Enter):
   * O total de tarefas incrementou (+1).
   * O contador **`Overdue`** subiu em 1.
   * O projeto **`+Faculdade`** aumentou a contagem imediatamente.

---

## 🎬 10. Demonstração Prática 3: Concluindo Tarefa (`do`)

### Passo a passo no rodapé:
1. Selecione ou identifique o ID da tarefa atrasada.
2. Pressione **`:`** e conclua a tarefa:
   ```text
   topydo> do <ID>
   ```
   *(Ou simplesmente posicione o cursor sobre ela e aperte a tecla de atalho **`x`**)*.
3. Consulte as estatísticas atualizadas (`:` → `stats` → Enter):
   * **`Completed`** subiu em 1.
   * **`Pending`** diminuiu em 1.
   * **`Overdue`** diminuiu em 1 (comprovando que tarefas concluídas **não** são computadas como atrasadas!).

---

## 💡 11. Desafios Arquiteturais Superados

1. **Auto-Arquivamento Nativo (*Auto-Archive*):**
   * Por padrão, o `topydo do` transfere concluídas para o `done.txt`. Descobrimos o papel da flag `-a` para persistir os itens no `todo.txt` e refletir em `Completed`.
2. **Grafo de Dependências (`id:` e `p:`):**
   * Tarefas que possuem dependências pendentes são ocultadas da tela pelo `DependencyFilter` até que os filhos sejam concluídos.
3. **Tratamento de Exceções de Console:**
   * Ajuste do método `execute()` para iterar sobre linhas individuais, respeitando a integração com `TopydoString` da CLI.

---

## 🤖 12. Relatório da Experiência com Agentes de IA

* **O que funcionou muito bem:**
  * Leitura e compreensão ágil de um repositório legado desconhecido.
  * Estruturação de testes unitários determinísticos e isolamento de efeitos colaterais.
  * Agilidade na elaboração de datasets realistas e documentação formal.
* **Lições Aprendidas:**
  * O papel do engenheiro é guiar o agente nas decisões de negócio, validar os casos de teste e questionar divergências reais de comportamento.
  * *Pair programming* com IA acelerou a entrega sem comprometer a qualidade do design de software.

---

## 🏁 13. Conclusão

* **Requisitos Atendidos:**
  * ✅ Subcomando `stats` implementado com sucesso.
  * ✅ Separação nítida entre lógica de cálculo e formatação.
  * ✅ 100% de aprovação na suíte de testes (legada e nova).
  * ✅ Compatibilidade total com a CLI tradicional e com o **Modo Colunas**.
  * ✅ Relatório técnico e documentação entregues no repositório.

**Repositório do Fork:** [github.com/lucasmarinhoba/topydo](https://github.com/lucasmarinhoba/topydo)

---

# ❓ Perguntas & Respostas

### Obrigado pela atenção!
**Dúvidas ou comentários?**
