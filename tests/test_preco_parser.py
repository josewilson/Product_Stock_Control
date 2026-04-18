import unittest

from src.ui.main_window import parse_preco


class PrecoParserTestCase(unittest.TestCase):
    def test_deve_aceitar_formato_brasileiro_com_milhar(self) -> None:
        self.assertEqual(4500.00, parse_preco("4.500,00"))

    def test_deve_aceitar_formato_brasileiro_sem_milhar(self) -> None:
        self.assertEqual(4500.00, parse_preco("4500,00"))

    def test_deve_aceitar_formato_internacional(self) -> None:
        self.assertEqual(4500.00, parse_preco("4500.00"))

    def test_deve_aceitar_inteiro(self) -> None:
        self.assertEqual(4500.00, parse_preco("4500"))

    def test_deve_rejeitar_preco_vazio(self) -> None:
        with self.assertRaises(ValueError):
            parse_preco("")

    def test_deve_rejeitar_preco_invalido(self) -> None:
        with self.assertRaises(ValueError):
            parse_preco("abc")


if __name__ == "__main__":
    unittest.main()

