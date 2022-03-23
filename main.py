from flask import Blueprint
from flask import flash, request, redirect, render_template
from flask_login import login_required, current_user
import back

backend = back.back()
main = Blueprint('main', __name__, template_folder='templates')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'csv'}


@main.errorhandler(404)
def page_not_found(e):
    return


@main.route('/')
def index():
    user = current_user
    if not user.is_authenticated:
        return render_template('index.html', len_minio=backend.minio.count_obj(), is_auth=False)
    else:
        return render_template('index.html', len_minio=backend.minio.count_obj(), is_auth=True, user=current_user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/upload', methods=['GET', 'POST'])
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
                backend.mongo.upload_json(file.filename, facts)
            elif file.filename.rsplit('.', 1)[1].lower() == 'pdf':
                res = backend.minio.upload_file(file)
                doc = backend.pdf.pdf_to_text_stream_2(backend.minio.get_stream_file(res.object_name))
                backend.natasha.doc_init(doc)
            return render_template('index.html', len_minio=backend.minio.count_obj())
    return


@main.route('/download')
def download():
    return render_template('download.html')


@main.route('/search')
def search():
    return render_template('search.html')


@main.route('/extend')
def extend():
    return render_template('extend.html')
