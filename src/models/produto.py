from dataclasses import dataclass


@dataclass
class Produto:
    nome: str
    preco: float
    estoque: int

    def __post_init__(self) -> None:
        self.nome = self.nome.strip()
        if not self.nome:
            raise ValueError("O nome do produto e obrigatorio.")
        if self.preco < 0:
            raise ValueError("O preco nao pode ser negativo.")
        if self.estoque < 0:
            raise ValueError("O estoque inicial nao pode ser negativo.")

    def preco_formatado(self) -> str:
        valor = f"{self.preco:,.2f}"
        valor = valor.replace(",", "#").replace(".", ",").replace("#", ".")
        return f"R$ {valor}"

