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
    assert dados["id"] == 1

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
    assert "WHERE" in args
    assert "tipo = %s" in args
    assert args == ["apartamento"]

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
    assert "WHERE" in args
    assert "cidade = %s" in args
    assert args == ["São Paulo"]

def test_buscar_imovel_por_id_sucesso(client):
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
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.get('/imoveis/999')

    assert resposta.status_code == 404
    assert "erro" in resposta.json

def test_criar_imovel_sucesso(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 10

    payload = {
        "logradouro": "Avenida Paulista",
        "tipo_logradouro": "Avenida",
        "bairro": "Bela Vista",
        "cidade": "São Paulo",
        "cep": "01310-100",
        "tipo": "comercial",
        "valor": 1200000.0,
        "data_aquisicao": "2024-01-15"
    }

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.post('/imoveis', json=payload)

    assert resposta.status_code == 201
    assert resposta.json["id"] == 10
    assert resposta.json["logradouro"] == "Avenida Paulista"
    mock_conn.commit.assert_called_once()

def test_criar_imovel_campos_obrigatorios_ausentes(client):
    payload_invalido = {
        "tipo_logradouro": "Rua",
        "cidade": "São Paulo"
    }

    resposta = client.post('/imoveis', json=payload_invalido)

    assert resposta.status_code == 400
    assert "erro" in resposta.json

def test_atualizar_imovel_sucesso(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (
        1, "Rua Quatá", "Rua", "Vila Olímpia", "São Paulo", "04546-042", "apartamento", 750000.0, "2023-05-10"
    )

    payload_atualizacao = {
        "logradouro": "Rua Quatá Atualizada",
        "tipo_logradouro": "Rua",
        "bairro": "Vila Olímpia",
        "cidade": "São Paulo",
        "cep": "04546-042",
        "tipo": "apartamento",
        "valor": 800000.0,
        "data_aquisicao": "2023-05-10"
    }

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.put('/imoveis/1', json=payload_atualizacao)

    assert resposta.status_code == 200
    assert resposta.json["valor"] == 800000.0
    mock_conn.commit.assert_called_once()

def test_atualizar_imovel_nao_encontrado(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    payload = {
        "logradouro": "Rua Inexistente",
        "cidade": "São Paulo"
    }

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.put('/imoveis/999', json=payload)

    assert resposta.status_code == 404
    assert "erro" in resposta.json

def test_deletar_imovel_sucesso(client):
    """Testa se DELETE /imoveis/<id> remove o imóvel e retorna status 204 No Content."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simula que o imóvel existe para remoção
    mock_cursor.fetchone.return_value = (1,)

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.delete('/imoveis/1')

    assert resposta.status_code == 204
    assert resposta.data == b''  # Corpo retornado deve ser vazio no 204
    mock_conn.commit.assert_called_once()

def test_deletar_imovel_nao_encontrado(client):
    """Testa se DELETE /imoveis/<id> retorna status 404 Not Found se o ID não existir."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simula que o imóvel não existe
    mock_cursor.fetchone.return_value = None

    with patch("app.connect_db", return_value=mock_conn):
        resposta = client.delete('/imoveis/999')

    assert resposta.status_code == 404
    assert "erro" in resposta.json
