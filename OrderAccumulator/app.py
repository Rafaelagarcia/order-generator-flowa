from flask import Flask, request, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

exposicao_atual = {
    "PETR4": 0.0,
    "VALE3": 0.0,
    "VIIA4": 0.0
}

LIMIT = 1000000.00

@app.route('/order', methods=['POST'])
def processar_ordem():
    data = request.json
    
    if not data:
        return jsonify({"sucesso": False, "msg_erro": "Dados não enviados."}), 400
  #Tratamento de exceções, caso o usuário use dados inválidos ou incorretos  
    try:
        ativo = data.get('ativo')
        lado = data.get('lado')
        quantidade = int(data.get('quantidade'))
        preco = float(data.get('preco'))
         
        if ativo not in exposicao_atual:
            return jsonify ({"sucesso": False, "msg_erro": "Exposição não valida, tente novamente."}), 400
        
        valor_ordem = quantidade * preco
        
        if lado == 'C':
            exposicao_futura = exposicao_atual[ativo] + valor_ordem
        else:
            exposicao_futura = exposicao_atual[ativo] - valor_ordem
            
        if abs(exposicao_futura) > LIMIT:
            return jsonify({
                "sucesso": False,
                "exposicao_atual": round(exposicao_atual[ativo], 2),
                "msg_erro": "Limite de exposição de R$ 1.000.000,00 excedido para este ativo."
            }), 400

        exposicao_atual[ativo] = exposicao_futura

        return jsonify({
            "sucesso": True,
            "exposicao_atual": round(exposicao_atual[ativo], 2),
            "msg_erro": ""
        }), 200

    except (ValueError, TypeError):
        return jsonify({"sucesso": False, "msg_erro": "Quantidade ou Preço inválidos."}), 400

if __name__ == '__main__':
    app.run(debug=True)


