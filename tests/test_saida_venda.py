import unittest

from src.models.produto import Produto
from src.services.estoque_service import VendaResultado
from src.ui.main_window import montar_lista_produtos
from src.ui.main_window import montar_saida_venda


class SaidaVendaTestCase(unittest.TestCase):
    def test_deve_formatar_saida_quando_venda_sucesso(self) -> None:
        produto = Produto(nome="Notebook", preco=4500.00, estoque=3)
        resultado = VendaResultado(
            sucesso=True,
            mensagem="Venda realizada com sucesso.",
            quantidade_vendida=2,
            estoque_antes=5,
            estoque_depois=3,
        )

        texto = montar_saida_venda(produto, resultado)

        esperado = "\n".join(
            [
                "Produto: Notebook",
                "Pre\u00e7o: R$ 4.500,00",
                "Estoque antes da Venda : 5 unidades",
                "Venda realizada: 2 unidades",
                "Estoque atualizado: 3 unidades",
            ]
        )
        self.assertEqual(esperado, texto)

    def test_deve_listar_apenas_produtos_com_estoque(self) -> None:
        produtos = [
            Produto(nome="Notebook", preco=4500.00, estoque=3),
            Produto(nome="Mouse", preco=100.00, estoque=0),
            Produto(nome="Teclado", preco=250.00, estoque=7),
        ]

        texto = montar_lista_produtos(produtos, somente_em_estoque=True)

        esperado = "\n".join(
            [
                "Produtos em estoque:",
                "- Notebook | R$ 4.500,00 | Estoque: 3",
                "- Teclado | R$ 250,00 | Estoque: 7",
            ]
        )
        self.assertEqual(esperado, texto)

    def test_deve_listar_todos_os_produtos_cadastrados(self) -> None:
        produtos = [
            Produto(nome="Notebook", preco=4500.00, estoque=3),
            Produto(nome="Mouse", preco=100.00, estoque=0),
        ]

        texto = montar_lista_produtos(produtos, somente_em_estoque=False)

        esperado = "\n".join(
            [
                "Produtos cadastrados:",
                "- Notebook | R$ 4.500,00 | Estoque: 3",
                "- Mouse | R$ 100,00 | Estoque: 0",
            ]
        )
        self.assertEqual(esperado, texto)

    def test_deve_formatar_saida_quando_estoque_insuficiente(self) -> None:
        produto = Produto(nome="Notebook", preco=4500.00, estoque=5)
        resultado = VendaResultado(
            sucesso=False,
            mensagem="Estoque insuficiente para realizar a venda.",
            quantidade_vendida=8,
            estoque_antes=5,
            estoque_depois=5,
        )

        texto = montar_saida_venda(produto, resultado)

        esperado = "\n".join(
            [
                "Produto: Notebook",
                "Pre\u00e7o: R$ 4.500,00",
                "Estoque antes da Venda : 5 unidades",
                "Estoque insuficiente para realizar a venda.",
                "Estoque atualizado: 5 unidades",
            ]
        )
        self.assertEqual(esperado, texto)


if __name__ == "__main__":
    unittest.main()

