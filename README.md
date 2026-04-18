# Controle de Estoque (Mini Projeto)

Aplicacao desktop simples para cadastro de produto e processamento de venda, com foco em organizacao de codigo e interface amigavel.

## Funcionalidades

- Cadastro de produto (nome, preco, estoque inicial)
- Listagem de produtos cadastrados
- Filtro de listagem: `Todos` ou `Somente em estoque`
- Processamento de venda com validacao de estoque insuficiente
- Botoes dedicados para `Limpar venda` e `Novo cadastro`
- Exibicao do resultado no formato da regra de negocio

Exemplo de saida:

![Saída](images/saida.png)

```text
Produto: Notebook
Preco: R$ 4.500,00
Estoque antes da Venda : 5 unidades
Venda realizada: 2 unidades
Estoque atualizado: 3 unidades
```

Quando a venda for maior que o estoque:

```text
Estoque insuficiente para realizar a venda.
```

Depois de cada venda, a tela tambem mostra automaticamente os produtos em estoque.

## Fluxo de uso

1. Cadastre um produto preenchendo nome, preco e estoque inicial, depois clique em `Cadastrar produto`.
2. Informe a quantidade vendida e clique em `Processar venda` para exibir o resultado da operacao.
3. Use `Listar produtos` para consultar a lista e escolha o filtro `Todos` ou `Somente em estoque`.
4. Clique em `Limpar venda` para limpar apenas a venda atual e em `Novo cadastro` para iniciar outro cadastro do zero.

## Estrutura

- `src/models/produto.py`: entidade de dominio
- `src/services/estoque_service.py`: regras de negocio
- `src/ui/main_window.py`: interface grafica
- `src/main.py`: ponto de entrada da aplicacao
- `tests/test_estoque_service.py`: testes unitarios da regra de negocio

## Requisitos

- Python 3.10+

## Como executar

No Prompt de Comando (Windows), a partir da raiz do projeto:

```bat
python -m src.main
```

Opcao PowerShell (recomendada neste projeto):

```powershell
.\run.ps1
```

Opcao explicita para abrir a aplicacao:

```powershell
.\run.ps1 -App
```

## Como executar os testes

```bat
python -m unittest discover -s tests -v
```

Opcao PowerShell:

```powershell
.\run.ps1 -Tests
```

