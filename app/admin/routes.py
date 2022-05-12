from flask import render_template, redirect, url_for
from app import db
from app.admin.forms import NewWordForm
from app.admin import bp
from app.models import (
    Language,
    Lexicon,
    Phrase,
    Word,
    Part,
    LexicalEntry,
    LexicalForm,
    CanonicalForm,
    InflectedForm,
    LexicalSense,
    FormMoodsEnum,
    FormTensesEnum,
    FormPersonsEnum,
    FormGendersEnum,
    FormNumbersEnum,
    PartOfSpeechEnum,
)


@bp.route("/admin")
def index():
    entry_list = LexicalEntry.query.all()
    return render_template("admin/index.html", entry_list=entry_list)


# aide pour avoir plusieurs fomulaires sur une même page :
# https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms

# page pour créer un nouveau mot
@bp.route("/admin/word/new", methods=["GET", "POST"])
def add_word():
    form = NewWordForm()
    form.lexicon.choices = [lexicon.name for lexicon in Lexicon.query.all()]

    if form.validate_on_submit():
        entry = Word(
            lexicon=Lexicon.query.filter_by(name=form.lexicon.data).first(),
            part_of_speech=PartOfSpeechEnum(form.part_of_speech.data).name,
        )
        canonical_form = CanonicalForm(
            written_form=form.canonical_form_written.data,
            alternative_form=form.canonical_form_alt.data,
            phonetic_form=form.canonical_form_phonetic.data,
            gender=FormGendersEnum(form.canonical_form_gender.data).name,
            number=FormNumbersEnum(form.canonical_form_number.data).name,
            mood=FormMoodsEnum(form.canonical_form_mood.data).name,
            tense=FormTensesEnum(form.canonical_form_tense.data).name,
            person=FormPersonsEnum(form.canonical_form_person.data).name,
            lexical_entry=entry,
        )
        db.session.add(entry)
        db.session.add(canonical_form)
        db.session.commit()
        return redirect(url_for("admin.index"))

    return render_template("admin/new_word.html", form=form)


# page d'admin d'un mot déjà créé
# -> form pour ajouter des formes
# -> form pour ajoter des sens
# -> form pour ajouter des traductions
@bp.route("/admin/word/<id>")
def word(id):
    word = Word.query.filter_by(id=id).first_or_404()
    forms = word.forms.order_by(LexicalForm.id)
