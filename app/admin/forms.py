from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    IntegerField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class NewEntryForm(FlaskForm):
    written_form = StringField(
        "Written form", validators=[DataRequired(), Length(min=1, max=64)]
    )
    phonetic_form = StringField(
        "Phonetic form", validators=[DataRequired(), Length(min=1, max=64)]
    )
    language = StringField(
        "Language", validators=[DataRequired(), Length(min=1, max=64)]
    )
    lexicon = StringField(
        "Lexicon", validators=[DataRequired(), Length(min=1, max=64)]
    )
    orthography = StringField(
        "Orthography", validators=[DataRequired(), Length(min=1, max=64)]
    )
    submit = SubmitField("Submit")
