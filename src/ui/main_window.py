from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from src.models.produto import Produto
from src.services.estoque_service import EstoqueService
from src.services.estoque_service import VendaResultado


def parse_preco(valor: str) -> float:
    texto = valor.strip().replace(" ", "")
    if not texto:
        raise ValueError("O preco e obrigatorio.")

    if any(char not in "0123456789,." for char in texto):
        raise ValueError("Formato de preco invalido.")

    ultimo_ponto = texto.rfind(".")
    ultima_virgula = texto.rfind(",")

    if ultimo_ponto != -1 and ultima_virgula != -1:
        # Usa o ultimo separador como decimal e remove o outro como milhar.
        if ultima_virgula > ultimo_ponto:
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", "")
    elif "," in texto:
        texto = texto.replace(",", ".")

    try:
        return float(texto)
    except ValueError as erro:
        raise ValueError("Formato de preco invalido.") from erro


def montar_saida_venda(produto: Produto, resultado: VendaResultado) -> str:
    texto = [
        f"Produto: {produto.nome}",
        f"Pre\u00e7o: {produto.preco_formatado()}",
        f"Estoque antes da Venda : {resultado.estoque_antes} unidades",
    ]

    if resultado.sucesso:
        unidade_label = "unidade" if resultado.quantidade_vendida == 1 else "unidades"
        texto.append(f"Venda realizada: {resultado.quantidade_vendida} {unidade_label}")
    else:
        texto.append(resultado.mensagem)

    texto.append(f"Estoque atualizado: {resultado.estoque_depois} unidades")
    return "\n".join(texto)


def montar_lista_produtos(produtos: list[Produto], somente_em_estoque: bool = False) -> str:
    if somente_em_estoque:
        produtos_filtrados = [produto for produto in produtos if produto.estoque > 0]
        titulo = "Produtos em estoque"
    else:
        produtos_filtrados = list(produtos)
        titulo = "Produtos cadastrados"

    if not produtos_filtrados:
        return f"{titulo}: nenhum produto para exibir."

    linhas = [f"{titulo}:"]
    for produto in produtos_filtrados:
        linhas.append(f"- {produto.nome} | {produto.preco_formatado()} | Estoque: {produto.estoque}")
    return "\n".join(linhas)


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Controle de Estoque")
        self.geometry("560x460")
        self.resizable(False, False)

        self.produto: Optional[Produto] = None
        self.produtos: list[Produto] = []
        self.filtro_listagem_var = tk.StringVar(value="Todos")

        self._criar_componentes()

    def _criar_componentes(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Cadastro do Produto", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        ttk.Label(frame, text="Nome do produto:").grid(row=1, column=0, sticky="w", pady=4)
        self.nome_entry = ttk.Entry(frame, width=36)
        self.nome_entry.grid(row=1, column=1, sticky="w", pady=4)

        ttk.Label(frame, text="Preco (R$):").grid(row=2, column=0, sticky="w", pady=4)
        self.preco_entry = ttk.Entry(frame, width=36)
        self.preco_entry.grid(row=2, column=1, sticky="w", pady=4)

        ttk.Label(frame, text="Estoque inicial:").grid(row=3, column=0, sticky="w", pady=4)
        self.estoque_entry = ttk.Entry(frame, width=36)
        self.estoque_entry.grid(row=3, column=1, sticky="w", pady=4)

        cadastro_botoes = ttk.Frame(frame)
        cadastro_botoes.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 16))
        cadastro_botoes.columnconfigure((0, 1), weight=1)

        ttk.Button(cadastro_botoes, text="Cadastrar produto", command=self.cadastrar_produto).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(cadastro_botoes, text="Listar produtos", command=self.listar_produto).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

        ttk.Label(cadastro_botoes, text="Filtro da listagem:").grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        self.filtro_listagem_combo = ttk.Combobox(
            cadastro_botoes,
            textvariable=self.filtro_listagem_var,
            values=("Todos", "Somente em estoque"),
            state="readonly",
            width=28,
        )
        self.filtro_listagem_combo.grid(row=1, column=1, sticky="ew", pady=(8, 0))

        ttk.Label(frame, text="Venda", font=("Segoe UI", 11, "bold")).grid(
            row=5, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        ttk.Label(frame, text="Quantidade vendida:").grid(row=6, column=0, sticky="w", pady=4)
        self.venda_entry = ttk.Entry(frame, width=36)
        self.venda_entry.grid(row=6, column=1, sticky="w", pady=4)

        botoes_frame = ttk.Frame(frame)
        botoes_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(8, 12))
        botoes_frame.columnconfigure((0, 1, 2), weight=1)

        ttk.Button(botoes_frame, text="Processar venda", command=self.processar_venda).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(botoes_frame, text="Limpar venda", command=self.limpar_venda).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )
        ttk.Button(botoes_frame, text="Novo cadastro", command=self.novo_cadastro).grid(
            row=0, column=2, sticky="ew", padx=(6, 0)
        )

        ttk.Label(frame, text="Saida", font=("Segoe UI", 11, "bold")).grid(
            row=8, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )

        self.output_text = tk.Text(frame, height=10, width=60, state="disabled")
        self.output_text.grid(row=9, column=0, columnspan=2, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(9, weight=1)

    def cadastrar_produto(self) -> None:
        try:
            nome = self.nome_entry.get().strip()
            preco = parse_preco(self.preco_entry.get())
            estoque = int(self.estoque_entry.get().strip())
            novo_produto = Produto(nome=nome, preco=preco, estoque=estoque)
        except ValueError as erro:
            messagebox.showerror("Erro de validacao", str(erro))
            return

        indice_existente = next(
            (indice for indice, produto in enumerate(self.produtos) if produto.nome.lower() == novo_produto.nome.lower()),
            None,
        )
        if indice_existente is None:
            self.produtos.append(novo_produto)
            self.produto = novo_produto
        else:
            self.produtos[indice_existente] = novo_produto
            self.produto = self.produtos[indice_existente]

        self._set_output(
            "Produto cadastrado com sucesso.\n"
            "Preencha a quantidade vendida e clique em 'Processar venda'.\n\n"
            + montar_lista_produtos(self.produtos, somente_em_estoque=False)
        )

    def listar_produto(self) -> None:
        if not self.produtos:
            messagebox.showwarning("Produto nao cadastrado", "Cadastre um produto antes de listar.")
            return

        somente_em_estoque = self.filtro_listagem_var.get() == "Somente em estoque"
        self._set_output(montar_lista_produtos(self.produtos, somente_em_estoque=somente_em_estoque))

    def processar_venda(self) -> None:
        if self.produto is None:
            messagebox.showwarning("Produto nao cadastrado", "Cadastre um produto antes de vender.")
            return

        try:
            quantidade = int(self.venda_entry.get().strip())
            resultado = EstoqueService.processar_venda(self.produto, quantidade)
        except ValueError as erro:
            messagebox.showerror("Erro de validacao", str(erro))
            return

        self._set_output(
            montar_saida_venda(self.produto, resultado)
            + "\n\n"
            + montar_lista_produtos(self.produtos, somente_em_estoque=True)
        )

    def limpar_venda(self) -> None:
        self.venda_entry.delete(0, tk.END)
        self._set_output("")

    def novo_cadastro(self) -> None:
        self.nome_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.estoque_entry.delete(0, tk.END)
        self.venda_entry.delete(0, tk.END)
        self.produto = None
        self._set_output("")

    # Mantido por compatibilidade com chamada antiga do botao Limpar.
    def limpar_campos(self) -> None:
        self.limpar_venda()

    def _set_output(self, texto: str) -> None:
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", texto)
        self.output_text.configure(state="disabled")

