from dataclasses import dataclass

from src.models.produto import Produto


@dataclass
class VendaResultado:
    sucesso: bool
    mensagem: str
    quantidade_vendida: int
    estoque_antes: int
    estoque_depois: int


class EstoqueService:
    @staticmethod
    def processar_venda(produto: Produto, quantidade_vendida: int) -> VendaResultado:
        if quantidade_vendida <= 0:
            raise ValueError("A quantidade vendida deve ser maior que zero.")

        estoque_antes = produto.estoque
        if quantidade_vendida > produto.estoque:
            return VendaResultado(
                sucesso=False,
                mensagem="Estoque insuficiente para realizar a venda.",
                quantidade_vendida=quantidade_vendida,
                estoque_antes=estoque_antes,
                estoque_depois=produto.estoque,
            )

        produto.estoque -= quantidade_vendida
        return VendaResultado(
            sucesso=True,
            mensagem="Venda realizada com sucesso.",
            quantidade_vendida=quantidade_vendida,
            estoque_antes=estoque_antes,
            estoque_depois=produto.estoque,
        )

