from datetime import date, datetime, timedelta
import random
from decimal import Decimal

from sqlalchemy import text

from src.database.connection import SessionLocal
from src.database.models.cliente import Cliente
from src.database.models.item_pedido import ItemPedido
from src.database.models.pedido import Pedido
from src.database.models.produto import Produto


def limpar_banco(db):
    """
    Limpa os dados existentes para permitir que o seed
    seja executado várias vezes sem gerar conflitos de
    chave única ou IDs inconsistentes.
    """

    print("Limpando dados existentes...")

    db.execute(
        text(
            """
            TRUNCATE TABLE
                item_pedido,
                pedido,
                produto,
                cliente
            RESTART IDENTITY CASCADE
            """
        )
    )

    db.flush()

    print("Banco limpo com sucesso.")

def criar_clientes(db):
    clientes = [
        Cliente(
            nome="Anderson Tecnologia",
            cpf_cnpj="10000000001",
            email="anderson@exemplo.com",
            telefone="21999990001",
            endereco="Rua das Flores, 100",
            cidade="Rio de Janeiro",
            estado="RJ",
            cep="23000001",
        ),
        Cliente(
            nome="Maria Silva",
            cpf_cnpj="10000000002",
            email="maria@exemplo.com",
            telefone="21999990002",
            endereco="Rua das Palmeiras, 200",
            cidade="Rio de Janeiro",
            estado="RJ",
            cep="23000002",
        ),
        Cliente(
            nome="João Santos",
            cpf_cnpj="10000000003",
            email="joao@exemplo.com",
            telefone="21999990003",
            endereco="Rua do Comércio, 300",
            cidade="Rio de Janeiro",
            estado="RJ",
            cep="23000003",
        ),
        Cliente(
            nome="Carlos Oliveira",
            cpf_cnpj="10000000004",
            email="carlos@exemplo.com",
            telefone="21999990004",
            endereco="Rua Central, 400",
            cidade="Rio de Janeiro",
            estado="RJ",
            cep="23000004",
        ),
        Cliente(
            nome="Fernanda Costa",
            cpf_cnpj="10000000005",
            email="fernanda@exemplo.com",
            telefone="21999990005",
            endereco="Rua Brasil, 500",
            cidade="Rio de Janeiro",
            estado="RJ",
            cep="23000005",
        ),
        Cliente(
            nome="Ricardo Souza",
            cpf_cnpj="10000000006",
            email="ricardo@exemplo.com",
            telefone="21999990006",
            endereco="Rua do Sol, 600",
            cidade="Niterói",
            estado="RJ",
            cep="24000006",
        ),
        Cliente(
            nome="Juliana Almeida",
            cpf_cnpj="10000000007",
            email="juliana@exemplo.com",
            telefone="21999990007",
            endereco="Rua das Acácias, 700",
            cidade="Niterói",
            estado="RJ",
            cep="24000007",
        ),
        Cliente(
            nome="Pedro Martins",
            cpf_cnpj="10000000008",
            email="pedro@exemplo.com",
            telefone="21999990008",
            endereco="Rua Principal, 800",
            cidade="Nova Iguaçu",
            estado="RJ",
            cep="26000008",
        ),
        Cliente(
            nome="Patricia Gomes",
            cpf_cnpj="10000000009",
            email="patricia@exemplo.com",
            telefone="21999990009",
            endereco="Rua do Bosque, 900",
            cidade="Nova Iguaçu",
            estado="RJ",
            cep="26000009",
        ),
        Cliente(
            nome="Bruno Ferreira",
            cpf_cnpj="10000000010",
            email="bruno@exemplo.com",
            telefone="21999990010",
            endereco="Rua da Paz, 1000",
            cidade="São Gonçalo",
            estado="RJ",
            cep="24400010",
        ),
    ]

    db.add_all(clientes)
    db.flush()

    return clientes

def criar_produtos(db):
    produtos_data = [
        ("Notebook Dell", "Informática", "Notebook", "3500.00", "2800.00", 30),
        ("Notebook Lenovo", "Informática", "Notebook", "3200.00", "2500.00", 25),
        ("Monitor 24", "Informática", "Monitor", "899.90", "650.00", 40),
        ("Monitor 27", "Informática", "Monitor", "1299.90", "950.00", 35),
        ("Teclado Mecânico", "Informática", "Teclado", "350.00", "220.00", 50),
        ("Teclado USB", "Informática", "Teclado", "120.00", "70.00", 80),
        ("Mouse Logitech", "Informática", "Mouse", "150.00", "90.00", 100),
        ("Mouse Gamer", "Informática", "Mouse", "280.00", "170.00", 70),
        ("Headset Gamer", "Informática", "Áudio", "450.00", "280.00", 60),
        ("Webcam Full HD", "Informática", "Webcam", "300.00", "190.00", 45),
        ("SSD 480GB", "Informática", "Armazenamento", "320.00", "230.00", 55),
        ("SSD 1TB", "Informática", "Armazenamento", "590.00", "420.00", 40),
        ("HD Externo 1TB", "Informática", "Armazenamento", "450.00", "320.00", 35),
        ("Memória RAM 8GB", "Informática", "Memória", "180.00", "120.00", 90),
        ("Memória RAM 16GB", "Informática", "Memória", "320.00", "220.00", 75),
        ("Placa de Vídeo RTX", "Informática", "Vídeo", "2800.00", "2200.00", 20),
        ("Fonte 650W", "Informática", "Fonte", "450.00", "300.00", 40),
        ("Gabinete Gamer", "Informática", "Gabinete", "500.00", "340.00", 30),
        ("Impressora Multifuncional", "Impressão", "Impressora", "850.00", "600.00", 25),
        ("Nobreak 1200VA", "Energia", "Nobreak", "750.00", "520.00", 30),
    ]

    produtos = [
        Produto(
            nome_produto=nome,
            categoria=categoria,
            subcategoria=subcategoria,
            preco_venda=Decimal(preco_venda),
            preco_custo=Decimal(preco_custo),
            quantidade_estoque=estoque,
        )
        for (
            nome,
            categoria,
            subcategoria,
            preco_venda,
            preco_custo,
            estoque,
        ) in produtos_data
    ]

    db.add_all(produtos)
    db.flush()

    return produtos

def criar_pedidos(db, clientes, produtos):
    random.seed(42)

    data_inicio = date(2024, 9, 1)
    data_fim = date(2026, 8, 31)

    status = [
        "FINALIZADO",
        "FINALIZADO",
        "FINALIZADO",
        "ENVIADO",
        "PENDENTE",
        "CANCELADO",
    ]

    formas_pagamento = [
        "PIX",
        "CARTAO",
        "BOLETO",
    ]

    pedidos = []
    itens = []

    data_atual = data_inicio

    while data_atual <= data_fim:

        ano = data_atual.year
        mes = data_atual.month

        # ----------------------------------------------------
        # SAZONALIDADE
        # ----------------------------------------------------

        fator_sazonalidade = {
            1: 0.80,
            2: 0.85,
            3: 0.95,
            4: 0.90,
            5: 1.00,
            6: 1.05,
            7: 1.10,
            8: 1.00,
            9: 1.05,
            10: 1.15,
            11: 1.70,
            12: 2.40,
        }[mes]

        pedidos_base = 35

        quantidade_pedidos = int(
            pedidos_base * fator_sazonalidade
        )

        # Pequena variação natural
        quantidade_pedidos += random.randint(-4, 4)

        for _ in range(quantidade_pedidos):

            dia = random.randint(
                1,
                28,
            )

            data_pedido = datetime(
                ano,
                mes,
                dia,
                random.randint(8, 20),
                random.randint(0, 59),
            )

            cliente = random.choice(clientes)

            pedido = Pedido(
                id_cliente=cliente.id_cliente,
                data_pedido=data_pedido,
                status_pedido=random.choices(
                    status,
                    weights=[
                        65,
                        15,
                        8,
                        6,
                        4,
                        2,
                    ],
                    k=1,
                )[0],
                valor_total=Decimal("0.00"),
                valor_frete=Decimal(
                    random.choice(
                        [
                            "0.00",
                            "15.00",
                            "20.00",
                            "25.00",
                            "30.00",
                        ]
                    )
                ),
                forma_pagamento=random.choice(
                    formas_pagamento
                ),
            )

            db.add(pedido)
            db.flush()

            quantidade_itens = random.randint(1, 5)

            produtos_pedido = random.sample(
                produtos,
                k=quantidade_itens,
            )

            valor_itens = Decimal("0.00")

            for produto in produtos_pedido:

                quantidade = random.randint(1, 4)

                # ------------------------------------------------
                # DEZEMBRO / BLACK FRIDAY
                # ------------------------------------------------

                if mes == 11:
                    quantidade += random.choice(
                        [0, 1, 1, 2]
                    )

                elif mes == 12:
                    quantidade += random.choice(
                        [0, 1, 2, 2, 3]
                    )

                preco_unitario = produto.preco_venda

                subtotal = (
                    preco_unitario
                    * quantidade
                )

                item = ItemPedido(
                    id_pedido=pedido.id_pedido,
                    id_produto=produto.id_produto,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario,
                    subtotal=subtotal,
                )

                db.add(item)

                valor_itens += subtotal

                # produto.quantidade_estoque -= quantidade

                itens.append(item)

            pedido.valor_total = (
                valor_itens
                + pedido.valor_frete
            )

            pedidos.append(pedido)

        # Próximo mês
        if mes == 12:
            data_atual = date(
                ano + 1,
                1,
                1,
            )
        else:
            data_atual = date(
                ano,
                mes + 1,
                1,
            )

    db.flush()

    return pedidos, itens

def main():
    db = SessionLocal()

    try:
        print("Iniciando carga de dados...")

        limpar_banco(db)

        clientes = criar_clientes(db)
        print(f"Clientes criados: {len(clientes)}")

        produtos = criar_produtos(db)
        print(f"Produtos criados: {len(produtos)}")

        pedidos, itens = criar_pedidos(
            db,
            clientes,
            produtos,
        )

        print(f"Pedidos criados: {len(pedidos)}")
        print(f"Itens criados: {len(itens)}")

        db.commit()

        print()
        print("Carga concluída com sucesso.")

    except Exception:
        db.rollback()
        print("Erro durante a carga. Rollback executado.")
        raise

    finally:
        db.close()

if __name__ == "__main__":
    main()