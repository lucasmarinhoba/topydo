# Exemplos de Teste no Estado Atual do Projeto (Linha de Base)

Este documento contém um roteiro prático com **exemplos reais de teste** para serem executados no estado atual do projeto **topydo**, antes de iniciar a implementação do subcomando `stats`.

O objetivo é garantir que o ambiente esteja funcionando corretamente e estabelecer a linha de base (*baseline*) de funcionamento.

---

## 1. Preparação do Ambiente

Antes de executar os testes, certifique-se de que o ambiente virtual está ativo e as dependências instaladas:

```bash
# Se estiver no Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Se estiver no Linux ou WSL (Ubuntu):
source .venv/bin/activate

# Instalação das dependências necessárias para testes:
pip install ".[columns,ical,prompt,test]" pytest
```

> [!NOTE]
> Conforme documentado na [Atividade03_topydo.md](file:///c:/Users/lucas/OneDrive/Documentos/GitHub/topydo/atvd/Atividade03_topydo.md), o ambiente de referência oficial é **Linux / WSL**, onde **825 testes passam e nenhum falha**. No Windows nativo, diferenças de quebra de linha (`\r\n` vs `\n`) em testes de I/O podem gerar falhas em alguns testes de formatação.

---

## 2. Testes Automatizados (Suíte de Testes)

### 2.1. Execução Completa com Pytest (Ambiente de Referência)
Executa toda a suíte de testes do repositório:

```bash
pytest
```
**Resultado esperado (no Linux/WSL):**
```text
======================== 825 passed, 4 skipped in ~10s ========================
```

---

### 2.2. Execução de Módulos Específicos (Compatíveis com Windows e Linux)
Você pode rodar testes de módulos focados na resolução de comandos e configurações:

#### Exemplo A: Teste do despachante de comandos (`get_subcommand`)
Testa se o sistema reconhece os comandos existentes e lida com aliases:
```bash
pytest test/test_get_sub_command.py -v
```
**Saída esperada:**
```text
test/test_get_sub_command.py::GetSubCommandTest::test_get_subcommand_add PASSED
test/test_get_sub_command.py::GetSubCommandTest::test_get_subcommand_alias PASSED
test/test_get_sub_command.py::GetSubCommandTest::test_get_subcommand_invalid PASSED
...
============================== 12 passed in 0.15s ==============================
```

#### Exemplo B: Teste de parser e leitura de configurações
```bash
pytest test/test_config.py -v
```
**Saída esperada:**
```text
test/test_config.py::ConfigTest::test_config_file PASSED
test/test_config.py::ConfigTest::test_aliases PASSED
...
============================== 25 passed in 0.20s ==============================
```

---

### 2.3. Execução com o Runner `green` (Documentado no CONTRIBUTING.md)
```bash
green -r
```

---

## 3. Testes Manuais com a CLI e Arquivo `todo.txt` Real

Para testar as funcionalidades do CLI sem alterar seus arquivos pessoais, crie um arquivo temporário de testes com tarefas reais.

### Passo 1: Criar o arquivo `meu_todo_teste.txt`
Crie um arquivo na raiz do repositório chamado `meu_todo_teste.txt` com o seguinte conteúdo:

```text
(A) 2026-10-01 Entregar relatório da Atividade 03 +Faculdade @computador due:2026-10-15
(B) 2026-11-01 Implementar testes no topydo +Faculdade @estudos due:2026-11-10
x 2026-10-20 Estudar estrutura de comandos do topydo +Faculdade @leitura
Comprar café e lanche +Pessoal @mercado
(C) Pagar fatura do cartão +Pessoal @financas due:2026-10-25
```

---

### Passo 2: Executar Comandos de Consulta

#### Teste 1: Listar todas as tarefas ativas (`ls`)
```bash
python -m topydo.ui.UILoader -t meu_todo_teste.txt ls
```
*Ou simplesmente `topydo -t meu_todo_teste.txt ls` se estiver instalado no path do ambiente.*

**Saída esperada:**
Exibe as tarefas pendentes ordenadas por prioridade:
```text
(A) 2026-10-01 Entregar relatório da Atividade 03 +Faculdade @computador due:2026-10-15
(B) 2026-11-01 Implementar testes no topydo +Faculdade @estudos due:2026-11-10
(C) Pagar fatura do cartão +Pessoal @financas due:2026-10-25
Comprar café e lanche +Pessoal @mercado
```
*(A tarefa concluída iniciada com `x` é ocultada na listagem padrão).*

---

#### Teste 2: Listar apenas projetos (`lsprj`)
```bash
python -m topydo.ui.UILoader -t meu_todo_teste.txt lsprj
```
**Saída esperada:**
```text
Faculdade
Pessoal
```

---

#### Teste 3: Adicionar uma nova tarefa (`add`)
```bash
python -m topydo.ui.UILoader -t meu_todo_teste.txt add "(A) Nova tarefa de teste +ProjetoTeste @urgente due:2026-12-01"
```
**Saída esperada:**
A nova tarefa é inserida no arquivo `meu_todo_teste.txt`.

---

#### Teste 4: Concluir uma tarefa (`do`)
```bash
python -m topydo.ui.UILoader -t meu_todo_teste.txt do "Comprar café"
```
**Saída esperada:**
A tarefa é marcada como concluída com `x YYYY-MM-DD`.

---

## 4. Teste de Ausência do `stats` (Validação de Pré-requisito)

Como verificação fundamental antes de iniciar a Atividade 04, confirme que o subcomando `stats` **ainda não existe**:

```bash
python -m topydo.ui.UILoader -t meu_todo_teste.txt stats
```

**Resultado esperado atual:**
O comando não é reconhecido, exibindo o texto geral de ajuda do `topydo` (`Synopsis: topydo ... Available commands: ...`), confirmando que `stats` não está registrado.

Ao consultar ajuda específica:
```bash
python -m topydo.ui.UILoader help stats
```
**Resultado esperado atual:**
Redireciona para a ajuda geral ou indica comando desconhecido.

---

## 5. Verificação de Linter e Análise Estática

Para validar se o código atual está em conformidade com as regras do projeto:

```bash
python -m pylint --errors-only topydo test
```
**Resultado esperado:**
Nenhum erro crítico retornado pelo pylint.
