from unittest.mock import patch, MagicMock

def test_listar_imoveis_sucesso(client):
    """Testa se GET /imoveis consulta o banco e retorna a lista de imóveis formatada."""
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
    assert dados[0]["logradouro"] == "Rua Quatá"

def test_listar_imoveis_filtro_tipo(client):
    """Testa a filtragem por tipo via query parameter ?tipo=apartamento."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Rua Quatá", "Rua", "Vila Olímpia", "São Paulo", "04546-042", "apartamento", 750000.0, "2023-05-10")
    ]

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.get('/imoveis?tipo=apartamento')

    assert resposta.status_code == 200
    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args
    sql_executada = args[0]
    params = args[1]
    assert "WHERE" in sql_executada
    assert "tipo = %s" in sql_executada
    assert params == ["apartamento"]

def test_listar_imoveis_filtro_cidade(client):
    """Testa a filtragem por cidade via query parameter ?cidade=São Paulo."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Rua Quatá", "Rua", "Vila Olímpia", "São Paulo", "04546-042", "apartamento", 750000.0, "2023-05-10")
    ]

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.get('/imoveis?cidade=São Paulo')

    assert resposta.status_code == 200
    mock_cursor.execute.assert_called_once()
    args, _ = mock_cursor.execute.call_args
    sql_executada = args[0]
    params = args[1]
    assert "WHERE" in sql_executada
    assert "cidade = %s" in sql_executada
    assert params == ["São Paulo"]
