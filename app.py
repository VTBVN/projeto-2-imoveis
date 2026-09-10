from flask import Flask, jsonify, request
from database import connect_db

app = Flask(__name__)

@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    conn = connect_db()
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    try:
        tipo = request.args.get('tipo')
        cidade = request.args.get('cidade')

        query = """
            SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao
            FROM imoveis
        """
        condicoes = []
        params = []

        if tipo:
            condicoes.append("tipo = %s")
            params.append(tipo)
        if cidade:
            condicoes.append("cidade = %s")
            params.append(cidade)

        if condicoes:
            query += " WHERE " + " AND ".join(condicoes)

        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        linhas = cursor.fetchall()

        imoveis = []
        for lin in linhas:
            imoveis.append({
                "id": lin[0],
                "logradouro": lin[1],
                "tipo_logradouro": lin[2],
                "bairro": lin[3],
                "cidade": lin[4],
                "cep": lin[5],
                "tipo": lin[6],
                "valor": float(lin[7]) if lin[7] is not None else None,
                "data_aquisicao": str(lin[8]) if lin[8] is not None else None
            })

        return jsonify(imoveis), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/imoveis/<int:id>', methods=['GET'])
def buscar_imovel_por_id(id):
    conn = connect_db()
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        query = """
            SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao
            FROM imoveis
            WHERE id = %s
        """
        cursor.execute(query, (id,))
        lin = cursor.fetchone()

        if not lin:
            return jsonify({"erro": "Imóvel não encontrado"}), 404

        imovel = {
            "id": lin[0],
            "logradouro": lin[1],
            "tipo_logradouro": lin[2],
            "bairro": lin[3],
            "cidade": lin[4],
            "cep": lin[5],
            "tipo": lin[6],
            "valor": float(lin[7]) if lin[7] is not None else None,
            "data_aquisicao": str(lin[8]) if lin[8] is not None else None
        }

        return jsonify(imovel), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/imoveis', methods=['POST'])
def criar_imovel():
    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"erro": "JSON inválido ou corpo da requisição vazio"}), 400

    logradouro = dados.get('logradouro')
    cidade = dados.get('cidade')

    if not logradouro or not cidade:
        return jsonify({"erro": "Campos obrigatórios ausentes: 'logradouro' e 'cidade'"}), 400

    tipo_logradouro = dados.get('tipo_logradouro')
    bairro = dados.get('bairro')
    cep = dados.get('cep')
    tipo = dados.get('tipo')
    valor = dados.get('valor')
    data_aquisicao = dados.get('data_aquisicao')

    conn = connect_db()
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao
        ))
        conn.commit()

        novo_id = cursor.lastrowid

        imovel_criado = {
            "id": novo_id,
            "logradouro": logradouro,
            "tipo_logradouro": tipo_logradouro,
            "bairro": bairro,
            "cidade": cidade,
            "cep": cep,
            "tipo": tipo,
            "valor": float(valor) if valor is not None else None,
            "data_aquisicao": str(data_aquisicao) if data_aquisicao is not None else None
        }

        return jsonify(imovel_criado), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"erro": "JSON inválido ou corpo da requisição vazio"}), 400

    conn = connect_db()
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()

        query_busca = "SELECT id FROM imoveis WHERE id = %s"
        cursor.execute(query_busca, (id,))
        if not cursor.fetchone():
            return jsonify({"erro": "Imóvel não encontrado"}), 404

        logradouro = dados.get('logradouro')
        tipo_logradouro = dados.get('tipo_logradouro')
        bairro = dados.get('bairro')
        cidade = dados.get('cidade')
        cep = dados.get('cep')
        tipo = dados.get('tipo')
        valor = dados.get('valor')
        data_aquisicao = dados.get('data_aquisicao')

        query_update = """
            UPDATE imoveis
            SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s
            WHERE id = %s
        """
        cursor.execute(query_update, (
            logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao, id
        ))
        conn.commit()

        imovel_atualizado = {
            "id": id,
            "logradouro": logradouro,
            "tipo_logradouro": tipo_logradouro,
            "bairro": bairro,
            "cidade": cidade,
            "cep": cep,
            "tipo": tipo,
            "valor": float(valor) if valor is not None else None,
            "data_aquisicao": str(data_aquisicao) if data_aquisicao is not None else None
        }

        return jsonify(imovel_atualizado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
