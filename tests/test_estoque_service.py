import unittest

from src.models.produto import Produto
from src.services.estoque_service import EstoqueService


class EstoqueServiceTestCase(unittest.TestCase):
    def test_deve_reduzir_estoque_quando_venda_valida(self) -> None:
        produto = Produto(nome="Notebook", preco=3500.00, estoque=5)

        resultado = EstoqueService.processar_venda(produto, 2)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(5, resultado.estoque_antes)
        self.assertEqual(3, resultado.estoque_depois)
        self.assertEqual(3, produto.estoque)

    def test_nao_deve_reduzir_quando_estoque_insuficiente(self) -> None:
        produto = Produto(nome="Notebook", preco=3500.00, estoque=5)

        resultado = EstoqueService.processar_venda(produto, 8)

        self.assertFalse(resultado.sucesso)
        self.assertEqual("Estoque insuficiente para realizar a venda.", resultado.mensagem)
        self.assertEqual(5, resultado.estoque_depois)
        self.assertEqual(5, produto.estoque)

    def test_deve_falhar_com_quantidade_invalida(self) -> None:
        produto = Produto(nome="Notebook", preco=3500.00, estoque=5)

        with self.assertRaises(ValueError):
            EstoqueService.processar_venda(produto, 0)


if __name__ == "__main__":
    unittest.main()

