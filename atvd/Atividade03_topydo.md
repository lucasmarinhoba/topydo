# Atividade 03 – Manutenção em Projeto Existente

*Definição do projeto e da melhoria planejada*

## 1. Projeto escolhido

| | |
|---|---|
| **Projeto** | topydo |
| **Repositório** | https://github.com/topydo/topydo |
| **Linguagem** | Python |
| **Licença** | GPLv3 (software livre, código aberto) |
| **Descrição** | Gerenciador de tarefas em linha de comando que usa o formato todo.txt, com suporte a prioridades, projetos, contextos, datas de vencimento, recorrência e dependências. |
| **Manutenção** | Repositório ativo: houve commits recentes nas pastas de código e de testes. |

## 2. Verificações realizadas

- Clonamos o repositório (com histórico do git), instalamos o programa e listamos os comandos existentes com `topydo help`: add, append, del, dep, depri, do, edit, ls, listcon, listprojects, modify, postpone, pri, revert, sort e tag.
- Verificamos a ajuda dos comandos `ls`, `sort` e `postpone`. O `ls` já exporta em JSON, iCal e Dot, mas nenhum comando resume os dados.
- Buscamos no código-fonte por "stats" e "statistic": não há nenhum resultado, ou seja, a funcionalidade escolhida não existe.
- Executamos a suíte de testes em ambiente Linux (Ubuntu no WSL), com as mesmas dependências do CI do projeto (extras columns, ical, prompt e test) e o executor `pytest`. Resultado: **825 testes passam, 4 são ignorados e nenhum falha** (829 no total). Essa é a linha de base da Atividade 04.
- No Windows, 318 testes falharam apenas por diferença de quebra de linha (`\r\n` contra `\n`). O CI do projeto roda somente em Linux, por isso adotamos o ambiente Linux como referência.

## 3. Melhoria planejada

Novo subcomando `topydo stats`, que resume a lista de tarefas mostrando:

- total de tarefas, concluídas e pendentes;
- tarefas atrasadas (data de vencimento no passado);
- contagem de tarefas por projeto (+projeto).

## 4. Justificativa

O `ls -f json` permite exportar os dados, mas não há como resumi-los. O comando é independente dos demais, segue o padrão do projeto de um arquivo por comando em `topydo/commands/` e permite separar o cálculo das estatísticas da impressão do texto, o que facilita os testes. O escopo é pequeno o bastante para a Atividade 04.

## 5. Plano para a Atividade 04

1. Trabalhar em uma branch separada (`feature-stats`), mantendo o código original intacto.
2. Criar `StatsCommand.py` em `topydo/commands/`, com uma função que calcula os números e outra que formata a saída, e registrar o subcomando.
3. Escrever testes em `test/` com várias entradas, incluindo casos inválidos e lista vazia, sem alterar os testes existentes.
4. Rodar `python -m pytest` a cada etapa. Critério de aceitação: os 825 testes atuais continuam passando, os testes novos passam e não surgem falhas nem avisos novos.
5. Seguir as orientações do CONTRIBUTING.md (funções curtas, que fazem uma coisa só) e usar o agente de codificação com essas regras no prompt.

## 6. Observação

Conforme o enunciado, o código gerado pelo agente não será enviado ao projeto original. Após a Atividade 04, o grupo poderá consultar os mantenedores se desejarem receber a melhoria.
