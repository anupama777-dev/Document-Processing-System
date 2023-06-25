from flask import Flask, render_template, request
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired
from flask import jsonify
from werkzeug.utils import secure_filename
import os
from flask_migrate import Migrate
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from wtforms_alchemy import ModelForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'files'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Base = declarative_base()

class CategoryI(db.Model):
    __tablename__ = 'category1'
    fac_types = [('engg', 'Engineering'), ('other', 'Language/Humanities/Social Sciences/Management')]
    doc_types = [('ref_journal', 'Refereed Journals'), ('non_ref', 'Non-refereed journals'), ('seminar', 'Seminar, Conference proceedings etc'), ('poster', 'Poster presentations')]
    doc_cat = [('inter', 'International'), ('national', 'National')]
    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    faculty_type = sa.Column(ChoiceType(fac_types), nullable=False)
    document_type = sa.Column(ChoiceType(doc_types), nullable=False)
    document_category = sa.Column(ChoiceType(doc_cat), nullable=False)
    document_file = sa.Column(sa.String(255), nullable=False)

class CategoryIForm(ModelForm):
    document_file = FileField('Document File', validators=[DataRequired()])
    class Meta:
        model = CategoryI
        include_primary_keys = False
    submit = SubmitField('Submit')

class CategoryII(db.Model):
    __tablename__ = 'category2'
    fac_types = [('engg', 'Engineering'), ('other', 'Language/Humanities/Social Sciences/Management')]
    doc_types = [('text', 'Text/Reference Books'), ('sub_national', 'Subject Books by National level publishers/State and Central Govt Publications'), ('sub_local', 'Subject Books by local publishers'), ('chap_inter', 'Chapters published by International Publishers'), ('chap_national', 'Chapters published by National Publishers'),('articles', 'Article publication in technical magazines')]
    doc_cat = [('ext', 'External'), ('int', 'Internal')]
    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    faculty_type = sa.Column(ChoiceType(fac_types))
    document_type = sa.Column(ChoiceType(doc_types))
    document_category = sa.Column(ChoiceType(doc_cat))
    document_file = sa.Column(sa.String(255))


class CategoryIIForm(ModelForm):
    document_file = FileField('Document File', validators=[DataRequired()])
    class Meta:
        model = CategoryII
        include_primary_keys = True
    submit = SubmitField('Submit')


class CategoryIII(db.Model):
    __tablename__ = 'category3'
    fac_types = [('engg', 'Engineering'), ('other', 'Language/Humanities/Social Sciences/Management')]
    doc_types = [('sponsor', 'Sponsored Projects'), ('consult', 'Consultancy Projects'), ('quality_eval', 'Completed Projects Quality Evaluation'), ('proj_outcome', 'Projects Outcome Outputs'), ('grants', 'Grants received for FDP/Conference')]
    doc_cat = [('demo', 'Category')]
    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    faculty_type = sa.Column(ChoiceType(fac_types))
    document_type = sa.Column(ChoiceType(doc_types))
    document_category = sa.Column(ChoiceType(doc_cat))
    document_file = sa.Column(sa.String(255))

class CategoryIIIForm(ModelForm):
    document_file = FileField('Document File', validators=[DataRequired()])
    class Meta:
        model = CategoryIII
        include_primary_keys = True
    submit = SubmitField('Submit')

class CategoryIV(db.Model):
    __tablename__ = 'category4'
    fac_types = [('engg', 'Engineering'), ('other', 'Language/Humanities/Social Sciences/Management')]
    doc_types = [('mphil', 'M.Phil./ME/M.Tech'), ('phd', 'Ph.D'), ('ug', 'UG')]
    doc_cat = [('demo', 'Category')]
    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    faculty_type = sa.Column(ChoiceType(fac_types))
    document_type = sa.Column(ChoiceType(doc_types))
    document_category = sa.Column(ChoiceType(doc_cat))
    document_file = sa.Column(sa.String(255))

class CategoryIVForm(ModelForm):
    document_file = FileField('Document File', validators=[DataRequired()])
    class Meta:
        model = CategoryIV
        include_primary_keys = True
    submit = SubmitField('Submit')

class CategoryV(db.Model):
    __tablename__ = 'category5'
    fac_types = [('engg', 'Engineering'), ('other', 'Language/Humanities/Social Sciences/Management')]
    doc_types = [('workshop','Attended Refresher courses, workshops, Training, FDPs'), ('paper', 'Papers in Conferences/Seminars/Workshops'), ('lecture', 'Invited lectures or presentations for conferences')]
    doc_cat = [('demo', 'Category')]
    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    faculty_type = sa.Column(ChoiceType(fac_types))
    document_type = sa.Column(ChoiceType(doc_types))
    document_category = sa.Column(ChoiceType(doc_cat))
    document_file = sa.Column(sa.String(255))

class CategoryVForm(ModelForm):
    document_file = FileField('Document File', validators=[DataRequired()])
    class Meta:
        model = CategoryV
        include_primary_keys = True
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        category = request.form['category']
        if category == 'Category I':
            form = CategoryIForm()   

        elif category == 'Category II':
            form = CategoryIIForm()
        
        elif category == 'Category III':
            form = CategoryIIIForm()
        
        elif category == 'Category IV':
            form = CategoryIVForm()
            
        elif category == 'Category V':
            form = CategoryVForm()
        
        else:
            form = None

        return render_template('category.html', category=category, form=form)
    return render_template('dashboard.html')

@app.route('/process', methods=['POST'])
def process_form():
    category = request.form['category']
    if category == 'Category I':
        form_data = CategoryIForm(request.form)
        if form_data.validate():
            faculty_type = form_data.faculty_type.data
            document_type = form_data.document_type.data
            document_category = form_data.document_category.data
            document_file = request.files['document_file']
            if document_file:
                filename = secure_filename(document_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                document_file.save(file_path)
            else:
                file_path = None
            document = CategoryI(
                faculty_type = faculty_type,
                document_type = document_type,
                document_category = document_category,
                document_file = file_path
            )
            db.session.add(document)
            db.session.commit()
        else:
            print(form_data.errors)

    elif category == 'Category II':
        form_data = CategoryIIForm(request.form)
        if form_data.validate():
            faculty_type = form_data.faculty_type.data
            document_type = form_data.document_type.data
            document_category = form_data.document_category.data
            document_file = form_data.document_file.data
            if document_file:
                filename = secure_filename(document_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                document_file.save(file_path)
            else:
                file_path = None
            document = CategoryII(
                faculty_type = faculty_type,
                document_type = document_type,
                document_category = document_category,
                document_filepath = file_path
            )
            db.session.add(document)
            db.session.commit()

    elif category == 'Category III':
        form_data = CategoryIIIForm(request.form)
        if form_data.validate():
            faculty_type = form_data.faculty_type.data
            document_type = form_data.document_type.data
            document_category = form_data.document_category.data
            document_file = form_data.document_file.data
            if document_file:
                filename = secure_filename(document_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                document_file.save(file_path)
            else:
                file_path = None
            document = CategoryIII(
                faculty_type = faculty_type,
                document_type = document_type,
                document_category = document_category,
                document_filepath = file_path
            )
            db.session.add(document)
            db.session.commit()

    elif category == 'Category IV':
        form_data = CategoryIVForm(request.form)
        if form_data.validate():
            faculty_type = form_data.faculty_type.data
            document_type = form_data.document_type.data
            document_category = form_data.document_category.data
            document_file = form_data.document_file.data
            if document_file:
                filename = secure_filename(document_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                document_file.save(file_path)
            else:
                file_path = None
            document = CategoryIV(
                faculty_type = faculty_type,
                document_type = document_type,
                document_category = document_category,
                document_filepath = file_path
            )
            db.session.add(document)
            db.session.commit()

    elif category == 'Category V':
        form_data = CategoryVForm(request.form)
        if form_data.validate():
            faculty_type = form_data.faculty_type.data
            document_type = form_data.document_type.data
            document_category = form_data.document_category.data
            document_file = form_data.document_file.data
            if document_file:
                filename = secure_filename(document_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                document_file.save(file_path)
            else:
                file_path = None
            document = CategoryV(
                faculty_type = faculty_type,
                document_type = document_type,
                document_category = document_category,
                document_filepath = file_path
            )
            db.session.add(document)
            db.session.commit()

    response = jsonify(message='Success!')
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'

    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()