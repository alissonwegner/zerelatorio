from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import tabula
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdfFile' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'})

        file = request.files['pdfFile']

        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Nome de arquivo inválido ou formato não permitido'})

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        resultado_relatorio = processar_pdf(file_path)

        return jsonify(resultado_relatorio)

    return render_template('index.html')

def processar_pdf(file_path):
    try:
        tabelas = tabula.read_pdf(file_path, pages='all', multiple_tables=True)

        valores_quarta_coluna = []

        for i, tabela_atual in enumerate(tabelas, start=1):
            quarta_coluna = tabela_atual.iloc[:, 3].tolist()
            valores_quarta_coluna.extend(quarta_coluna)

        if valores_quarta_coluna:
            df_resultado = pd.DataFrame({"Quarta Coluna": valores_quarta_coluna})
            nome_arquivo_excel = "planilha_quarta_coluna.xlsx"
            caminho_arquivo_excel = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo_excel)
            df_resultado.to_excel(caminho_arquivo_excel, index=False)

            numero_de_linhas = len(valores_quarta_coluna)
            print(f"\nValores da quarta coluna de todas as tabelas foram salvos em {caminho_arquivo_excel}")
            print(f"Ja fez:{numero_de_linhas} teles.")
            print(f"Ja fez: R${numero_de_linhas*7} Reais.")

            return {'success': True, 'numero_linhas': numero_de_linhas, 'caminho_arquivo_excel': caminho_arquivo_excel}

        return {'error': 'Não foram encontradas tabelas no PDF.'}

    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
