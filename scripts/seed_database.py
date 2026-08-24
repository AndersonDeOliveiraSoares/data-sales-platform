from datetime import datetime, timedelta
from decimal import Decimal

from src.database.connection import SessionLocal
from src.database.models.cliente import Cliente
from src.database.models.item_pedido import ItemPedido
from src.database.models.pedido import Pedido
from src.database.models.produto import Produto


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
    produtos = [
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
        ) in produtos
    ]

    db.add_all(produtos)
    db.flush()

    return produtos


def criar_pedidos(db, clientes, produtos):
    combinacoes = [
        (0, [0, 6]),
        (1, [2, 4]),
        (2, [1, 7]),
        (3, [3, 5]),
        (4, [8, 9]),
        (5, [10, 13]),
        (6, [11, 14]),
        (7, [12, 16]),
        (8, [15, 17]),
        (9, [18, 19]),
        (0, [0, 2]),
        (1, [6, 8]),
        (2, [4, 10]),
        (3, [7, 11]),
        (4, [3, 14]),
    ]

    status = [
        "FINALIZADO",
        "FINALIZADO",
        "PENDENTE",
        "FINALIZADO",
        "ENVIADO",
        "FINALIZADO",
        "PENDENTE",
        "FINALIZADO",
        "CANCELADO",
        "FINALIZADO",
        "PENDENTE",
        "ENVIADO",
        "FINALIZADO",
        "PENDENTE",
        "FINALIZADO",
    ]

    formas_pagamento = [
        "PIX",
        "CARTAO",
        "PIX",
        "CARTAO",
        "BOLETO",
    ]

    pedidos = []
    itens = []

    for index, (cliente_index, produto_indices) in enumerate(combinacoes):
        pedido = Pedido(
            id_cliente=clientes[cliente_index].id_cliente,
            data_pedido=datetime.now() - timedelta(days=15 - index),
            status_pedido=status[index],
            valor_total=Decimal("0.00"),
            valor_frete=Decimal("20.00"),
            forma_pagamento=formas_pagamento[index % len(formas_pagamento)],
        )

        db.add(pedido)
        db.flush()

        valor_itens = Decimal("0.00")

        for produto_index in produto_indices:
            produto = produtos[produto_index]

            quantidade = 1 if index % 3 else 2

            preco_unitario = produto.preco_venda
            subtotal = preco_unitario * quantidade

            item = ItemPedido(
                id_pedido=pedido.id_pedido,
                id_produto=produto.id_produto,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal,
            )

            db.add(item)

            valor_itens += subtotal

            produto.quantidade_estoque -= quantidade

            itens.append(item)

        pedido.valor_total = valor_itens + pedido.valor_frete
        pedidos.append(pedido)

    db.flush()

    return pedidos, itens


def main():
    db = SessionLocal()

    try:
        print("Iniciando carga de dados...")

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