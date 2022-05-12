from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import (
    Language,
    Lexicon,
    LexicalEntry,
    Phrase,
    Word,
    Part,
    FormMoodsEnum,
    FormTensesEnum,
    FormPersonsEnum,
    FormGendersEnum,
    FormNumbersEnum,
    PartOfSpeechEnum,
    LexicalForm,
    LexicalSense,
)


class NewWordForm(FlaskForm):
    canonical_form_written = StringField(
        "Entrée", validators=[DataRequired("Veuillez remplir ce champ")]
    )
    lexicon = SelectField(
        "Lexique",
        validators=[DataRequired()],
    )
    part_of_speech = SelectField(
        "Catégorie Morphosyntaxique",
        choices=[choice.value for choice in PartOfSpeechEnum],
    )

    canonical_form_alt = StringField("Forme alternative")
    canonical_form_phonetic = StringField("Forme phonétique")
    canonical_form_gender = SelectField(
        "Genre", choices=[""] + [gender.value for gender in FormGendersEnum]
    )
    canonical_form_number = SelectField(
        "Nombre", choices=[""] + [number.value for number in FormNumbersEnum]
    )
    canonical_form_mood = SelectField(
        "Mode", choices=[""] + [mood.value for mood in FormMoodsEnum]
    )
    canonical_form_tense = SelectField(
        "Temps", choices=[""] + [tense.value for tense in FormTensesEnum]
    )
    canonical_form_person = SelectField(
        "Personne", choices=[""] + [person.value for person in FormPersonsEnum]
    )
    submit = SubmitField()
