from unittest.mock import patch, MagicMock
from mysql.connector import Error
from database import connect_db

@patch("mysql.connector.connect")
def test_connect_db_sucesso(mock_connect):
    """Testa se connect_db retorna a conexão quando o MySQL conecta com sucesso."""
    mock_conn = MagicMock()
    mock_conn.is_connected.return_value = True
    mock_connect.return_value = mock_conn

    conn = connect_db()

    assert conn is not None
    assert conn.is_connected() is True
    mock_connect.assert_called_once()

@patch("mysql.connector.connect")
def test_connect_db_falha(mock_connect):
    """Testa se connect_db retorna None em caso de erro de conexão."""
    mock_connect.side_effect = Error("Falha de conexão simulada")

    conn = connect_db()

    assert conn is None
