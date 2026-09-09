from unittest.mock import patch, MagicMock

def test_listar_imoveis_sucesso(client):
    """Testa se GET /imoveis consulta o banco e retorna a lista de imóveis formatada."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Simulando 1 registro retornado do MySQL com os 9 campos da tabela
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
    assert dados[0]["cidade"] == "São Paulo"
    assert dados[0]["valor"] == 750000.0
