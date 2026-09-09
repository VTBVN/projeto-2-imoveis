from unittest.mock import patch, MagicMock

def test_listar_imoveis_sucesso(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Rua Quatá", "Rua", "Vila Olímpia", "São Paulo", "04546-042", "apartamento", 750000.0, "2023-05-10")
    ]

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.get('/imoveis')

    assert resposta.status_code == 200
    dados = resposta.json
    assert isinstance(dados, list)
    assert len(dados) == 1
    assert dados[0]["id"] == 1

def test_listar_imoveis_filtro_tipo(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Rua Quatá", "Rua", "Vila Olímpia", "São Paulo", "04546-042", "apartamento", 750000.0, "2023-05-10")
    ]

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.get('/imoveis?tipo=apartamento')

    assert resposta.status_code == 200
    args, _ = mock_cursor.execute.call_args
    assert "WHERE" in args[0]
    assert "tipo = %s" in args[0]
    assert args[1] == ["apartamento"]

def test_listar_imoveis_filtro_cidade(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Rua Quatá", "Rua", "Vila Olímpia", "São Paulo", "04546-042", "apartamento", 750000.0, "2023-05-10")
    ]

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.get('/imoveis?cidade=São Paulo')

    assert resposta.status_code == 200
    args, _ = mock_cursor.execute.call_args
    assert "WHERE" in args[0]
    assert "cidade = %s" in args[0]
    assert args[1] == ["São Paulo"]

def test_buscar_imovel_por_id_sucesso(client):
    """Testa se GET /imoveis/<id> retorna 200 e o JSON do imóvel quando encontrado."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (
        1, "Rua Quatá", "Rua", "Vila Olímpia", "São Paulo", "04546-042", "apartamento", 750000.0, "2023-05-10"
    )

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.get('/imoveis/1')

    assert resposta.status_code == 200
    assert resposta.json["id"] == 1
    assert resposta.json["logradouro"] == "Rua Quatá"

def test_buscar_imovel_por_id_nao_encontrado(client):
    """Testa se GET /imoveis/<id> retorna 404 quando o ID não existe no banco."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.get('/imoveis/999')

    assert resposta.status_code == 404
    assert "erro" in resposta.json
