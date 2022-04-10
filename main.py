import json
from io import BytesIO
import time
from flask import Blueprint
from flask import flash, request, redirect, render_template, url_for, send_file
from flask_login import login_required, current_user
import back

backend = back.back()
main = Blueprint('main', __name__, template_folder='templates')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'csv'}


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.route('/')
def index():
    user = current_user
    if not user.is_authenticated:
        return render_template('index.html')
    else:
        return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No part file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected files')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if file.filename.rsplit('.', 1)[1].lower() == 'docx':
                res = backend.minio.upload_file(file)
                doc = backend.docx.load_txt(backend.minio.get_stream_file(res.object_name))
                backend.natasha.doc_init(doc)
                facts = backend.natasha.get_facts()
                backend.mongo.upload_json(file.filename, facts, '', 'docx')
            elif file.filename.rsplit('.', 1)[1].lower() == 'pdf':
                res = backend.minio.upload_file(file)
                doc = backend.pdf.pdf_to_text_stream_2(backend.minio.get_stream_file(res.object_name))
                backend.natasha.doc_init(doc)
            return render_template('index.html')
    return


@main.route('/download', methods=['GET', 'POST'])
@login_required
def download():
    if request.method == 'GET':
        result = backend.minio.get_object()
        return render_template('download.html', result=result)


@main.route('/download_file/<filename>', methods=['GET', 'POST'])
@login_required
def download_file(filename):
    file = backend.minio.get_stream_file(filename)
    return send_file(file, as_attachment=True, attachment_filename=filename)


@main.route('/search_files', methods=['GET', 'POST'])
@login_required
def search_files():
    if request.method == 'GET':
        result = backend.minio.get_object()
        return render_template('search_files.html', result=result)
    if request.method == 'POST':
        result = backend.minio.get_object()
        search_str = request.form.get('search_str')
        result_search = []
        for item in result:
            if search_str in item:
                result_search.append(item)
                continue
        return render_template('search_files.html', result=result_search)


@main.route('/search_tags', methods=['GET', 'POST'])
@login_required
def search_tags():
    if request.method == 'GET':
        result = backend.mongo.get_all_files()
        return render_template('search_tags.html', result=result)
    if request.method == 'POST':
        result = backend.mongo.get_all_files()
        search_str = request.form.get('search_str')
        result_search = []
        for item in result:
            if search_str in item['file']:
                result_search.append(item)
                continue
            for tag in item['tags']:
                if search_str in tag:
                    result_search.append(item)
                    continue
        return render_template('search_tags.html', result=result_search)


@main.route('/settings_telegram', methods=['GET', 'POST'])
@login_required
def settings_telegram():
    return render_template('settings_telegram.html')


@main.route('/put_messages', methods=['POST', 'PUT', 'GET'])
def put_message():
    res = request.json
    new_messages = json.loads(res)
    i = 1
    str_mes = ''
    for mes in new_messages:
        str_mes += str(i) + ' ' + mes+'\n'
        i += 1
    file = BytesIO(str_mes.encode('utf-8'))
    time_now = time.strftime("%Y-%m-%d %H", time.localtime())
    name_file = 'telegram_' + time_now + 'hour.txt'
    backend.minio.upload_custom_file(file, name_file)
    doc = backend.docx.load_txt(backend.minio.get_stream_file(name_file))
    backend.natasha.doc_init(doc)
    facts = backend.natasha.get_facts()
    backend.mongo.upload_json(name_file, facts, 'telegram', 'txt')
    return 'ok'
