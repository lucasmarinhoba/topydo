# Guia Completo de Testes das Funcionalidades Existentes do Topydo

Este documento contém um roteiro prático com **exemplos reais de teste** cobrindo **todas as funcionalidades já existentes** no projeto **topydo** (anteriormente à implementação do subcomando `stats`).

Para cada operação, você encontrará tanto o **comando normal (CLI)** quanto a **execução / visualização em formato de colunas** (*Column Mode* ou formatação tabular).

---

## 1. Preparação do Ambiente

Antes de executar os comandos, certifique-se de que o ambiente virtual está ativo e as dependências instaladas:

```bash
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1

# No Linux / WSL (Ubuntu):
source .venv/bin/activate

# Instalação das dependências do topydo:
pip install ".[columns,ical,prompt,test]" pytest
```

---

## 2. Como Usar o Modo Colunas (`topydo columns`)

Quando o modo colunas estiver aberto (`python3 -m topydo.ui.UILoader -c topydo_columns.conf -t meus_teste_topydo/todo.txt columns` no WSL/Linux):

1. **Para digitar qualquer comando:**
   * Aperte a tecla **`:`** (dois pontos) no teclado.
   * O cursor descerá para o rodapé e exibirá: `topydo> `.
   * **IMPORTANTE:** Digite o comando **diretamente sem colocar outro dois-pontos `:`**.  
     *(Exemplo correto: `topydo> add Nova tarefa`, e NÃO `topydo> :add`)*.
   * Dê **Enter**.
   * Se o comando exibir texto na tela (como `lsprj` ou `stats`), uma janela de console aparecerá sobre as colunas. Aperte **`Esc`** ou **`Enter`** para fechar essa janela e voltar à navegação das colunas.

2. **Atalhos rápidos do teclado (sem precisar do rodapé):**
   * **`x`**: conclui a tarefa selecionada.
   * **`d`**: exclui a tarefa selecionada.
   * **`u`**: desfaz a última ação (*Undo/Revert*).
   * **`e`**: edita a tarefa.
   * **`j` / `k`** ou **setas**: sobe e desce entre as tarefas.
   * **`h` / `l`** ou **setas laterais**: alterna entre as colunas.
   * **`q`**: sai do modo colunas.

---

## 3. Base de Dados de Teste Enriquecida

O arquivo [meus_teste_topydo/todo.txt](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/meus_teste_topydo/todo.txt) contém exemplos reais contemplando todos os formatos suportados pelo padrão todo.txt e pelo topydo:

```text
(A) 2026-10-01 Entregar relatório da Atividade 03 +Faculdade @computador due:2026-10-15 id:1
(B) 2026-11-01 Implementar testes e comandos no topydo +Faculdade @estudos due:2026-11-10 p:1
x 2026-10-20 2026-10-05 Estudar arquitetura de comandos do topydo +Faculdade @leitura
Comprar café e suprimentos para o laboratório +Pessoal @mercado cost:45
(C) Pagar fatura do cartão de crédito +Pessoal @financas due:2026-10-25 nota:urgente
(B) 2026-11-03 Preparar slides da apresentação +Faculdade @computador due:2026-11-25
Revisar documentação técnica do sistema +Trabalho @escritorio t:2026-11-01 due:2026-11-30 id:2
Atualizar dependências do repositório no fork +OpenSource @computador due:2026-11-15 p:2
Agendar consulta médica de rotina +Pessoal @saude
x 2026-10-15 2026-10-02 Configurar ambiente Linux no WSL +Faculdade @computador
Tarefa oculta de rascunho interno h:1
```

---

## 4. Guia Prático: Comandos Normais e Equivalentes em Coluna

---

### 4.1. Visualização e Listagem (`ls`)

#### Teste 1: Listagem padrão (apenas tarefas ativas)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls
  ```
* **No Modo Colunas:**
  * O painel de colunas já exibe as tarefas ativas organizadas nas colunas por padrão.
  * Se quiser executar via rodapé: aperte `:` e digite:
    ```text
    topydo> ls
    ```

---

#### Teste 2: Listar todas as tarefas, incluindo concluídas e ocultas (`-x`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls -x
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> ls -x
    ```
  * *(Aparecerá a listagem completa na janela de console. Aperte `Esc` para fechar).*

---

#### Teste 3: Filtrar por Contexto (`@`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls @computador
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> ls @computador
    ```

---

#### Teste 4: Filtrar por Projeto (`+`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls +Faculdade
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> ls +Faculdade
    ```

---

#### Teste 5: Filtrar por Prazos e Expressões
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls "due:<2026-11-15"
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> ls due:<2026-11-15
    ```

---

#### Teste 6: Ordenação Personalizada (`-s`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls -s due
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> ls -s due
    ```

---

#### Teste 7: Agrupamento (`-g`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls -g project
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> ls -g project
    ```

---

### 4.2. Formatos de Exportação (`ls -f`)

#### Teste 8: Exportar em formato JSON
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls -f json
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> ls -f json
    ```

#### Teste 9: Exportar em formato iCalendar (.ics)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls -f ical
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> ls -f ical
    ```

#### Teste 10: Exportar árvore de dependências em formato Graphviz DOT
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt ls -f dot
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> ls -f dot
    ```

---

### 4.3. Metadados de Contextos e Projetos

#### Teste 11: Listar todos os Projetos (`lsprj`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt lsprj
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> lsprj
    ```
  * *(Exibe a lista de projetos na janela de console. Aperte `Esc` para fechar).*

#### Teste 12: Listar todos os Contextos (`lscon`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt lscon
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> lscon
    ```
  * *(Exibe a lista de contextos na janela de console. Aperte `Esc` para fechar).*

---

### 4.4. Gerenciamento de Prioridades (`pri` e `depri`)

#### Teste 13: Definir ou alterar prioridade
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt pri 4 B
  ```
* **No Modo Colunas:**
  * **Pelo rodapé:** Aperte `:` e digite:
    ```text
    topydo> pri 4 B
    ```
  * **Ou pelo atalho de teclado:** Selecione a tarefa com `j`/`k` e aperte `prB`.

#### Teste 14: Remover a prioridade (`depri`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt depri 1
  ```
* **No Modo Colunas:**
  * **Pelo rodapé:** Aperte `:` e digite:
    ```text
    topydo> depri 1
    ```
  * **Ou pelo atalho de teclado:** Selecione a tarefa e aperte `prd`.

---

### 4.5. Prazos e Adiamento de Datas (`postpone`)

#### Teste 15: Adiar o prazo de uma tarefa por 3 dias
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt postpone 2 3d
  ```
* **No Modo Colunas:**
  * **Pelo rodapé:** Aperte `:` e digite:
    ```text
    topydo> postpone 2 3d
    ```

#### Teste 16: Adiar por 1 semana ajustando data de início (`-s`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt postpone -s 7 1w
  ```
* **No Modo Colunas:**
  * **Pelo rodapé:** Aperte `:` e digite:
    ```text
    topydo> postpone -s 7 1w
    ```

---

### 4.6. Gestão de Tags Customizadas (`tag`)

#### Teste 17: Adicionar ou atualizar uma tag
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt tag 4 responsavel lucas
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> tag 4 responsavel lucas
    ```

#### Teste 18: Remover uma tag existente
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt tag 4 cost
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> tag 4 cost
    ```

---

### 4.7. Subtarefas e Grafo de Dependências (`dep`)

#### Teste 19: Adicionar dependência entre tarefas
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt dep add 6 1
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> dep add 6 1
    ```

#### Teste 20: Inspecionar dependências
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt dep ls 2 to
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> dep ls 2 to
    ```

---

### 4.8. Manipulação e Edição de Tarefas

#### Teste 21: Adicionar uma nova tarefa (`add`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt add "(A) Nova tarefa de teste +ProjetoTeste @urgente due:2026-12-01"
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> add (A) Nova tarefa de teste +ProjetoTeste @urgente due:2026-12-01
    ```

#### Teste 22: Concluir tarefa (`do`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt do 4
  ```
* **No Modo Colunas:**
  * **Pelo atalho:** Selecione a tarefa com `j`/`k` e aperte a tecla **`x`**.
  * **Ou pelo rodapé:** Aperte `:` e digite:
    ```text
    topydo> do 4
    ```

#### Teste 23: Excluir uma tarefa (`del` / `rm`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt del 11
  ```
* **No Modo Colunas:**
  * **Pelo atalho:** Selecione a tarefa e aperte a tecla **`d`**.
  * **Ou pelo rodapé:** Aperte `:` e digite:
    ```text
    topydo> del 11
    ```

#### Teste 24: Anexar texto ao final de uma tarefa (`app` / `append`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt app 4 "urgente para entrega"
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> app 4 urgente para entrega
    ```

#### Teste 25: Modificar o conteúdo completo de uma tarefa (`mod` / `modify`)
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt mod "Agendar consulta medica geral +Pessoal @saude" 9
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> mod "Agendar consulta medica geral +Pessoal @saude" 9
    ```

---

### 4.9. Desfazer Ações e Histórico (`revert`)

#### Teste 26: Desfazer a última ação
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt revert
  ```
* **No Modo Colunas:**
  * **Pelo atalho:** Basta apertar a tecla **`u`** (*Undo*).
  * **Ou pelo rodapé:** Aperte `:` e digite:
    ```text
    topydo> revert
    ```

---

### 4.10. Organização Física do Arquivo (`sort`)

#### Teste 27: Ordenar fisicamente o arquivo todo.txt (sort)
> **Nota:** O comando sort reordena as linhas gravadas fisicamente no arquivo todo.txt em disco (usando por padrão a expressão configurada, ou uma expressão como sort desc:priority). No Modo Colunas, cada coluna já possui ordenação visual própria pré-definida em memória, portanto o efeito do sort ocorre no arquivo em disco.

* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt sort
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> sort
    ```

---

### 4.11. Novo Subcomando de Estatísticas (`stats`)

#### Teste 28: Exibir estatísticas da lista
* **Comando Normal (CLI):**
  ```bash
  python -m topydo.ui.UILoader -t meus_teste_topydo/todo.txt stats
  ```
* **No Modo Colunas:**
  * Aperte `:` e digite no rodapé:
    ```text
    topydo> stats
    ```
  * *(As estatísticas com total, pendentes, atrasadas e projetos aparecerão no console. Aperte `Esc` para voltar).*
