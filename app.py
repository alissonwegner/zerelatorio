from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from subprocess import Popen, PIPE

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
        comando = ['python3', 'init.py', file_path]
        processo = Popen(comando, stdout=PIPE, stderr=PIPE)
        stdout, stderr = processo.communicate()

        if processo.returncode == 0:
            return {'success': stdout.decode()}
        else:
            return {'error': stderr.decode()}

    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
