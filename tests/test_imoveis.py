def test_listar_imoveis_deve_retornar_status_200_e_lista(client):
    resposta = client.get('/imoveis')
    assert resposta.status_code == 200
    assert isinstance(resposta.json, list)
