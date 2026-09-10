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

if __name__ == '__main__':
    app.run(debug=True)
