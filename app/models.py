# from flask import current_app
import enum
from flask import current_app, url_for
from app import db

# models based on the Lexical Markup Framework (LMF)
# https://lirics.loria.fr/doc_pub/LMF_revision_14.pdf


class GlobalInformations(db.Model):
    __tablename__ = "global_informations"
    id = db.Column(db.Integer, primary_key=True)


class LexicalRessource(db.Model):
    __tablename__ = "lexical_ressources"
    id = db.Column(db.Integer, primary_key=True)
    lexicons = db.relationship("LexicalEntry", backref="lexical_ressource")


class Orthography(db.Model):
    __tablename__ = "orthographies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    language_id = db.Column(db.Integer, db.ForeignKey("languages.id"))

    def __repr__(self):
        return "<Orthography {}>".format(self.name)


class Language(db.Model):
    __tablename__ = "languages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    code_iso = db.Column(db.String(3), index=True, unique=True)
    orthographies = db.relationship("Orthography", backref="language")
    lexicons = db.relationship("Lexicon", backref="language")

    def __repr__(self):
        return "<Language {}>".format(self.name)


class Lexicon(db.Model):
    __tablename__ = "lexicons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    lexical_ressource_id = db.Column(db.Integer, db.ForeignKey("lexical_ressources.id"))
    language_id = db.Column(db.Integer, db.ForeignKey("languages.id"))

    def __repr__(self):
        return "<Lexicon {}>".format(self.name)


class FormRepresentation(db.Model):
    __tablename__ = "form_representations"
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey("languages.id"))
    written_form = db.Column(db.String(64), index=True, unique=True)
    orthography_id = db.Column(db.Integer, db.ForeignKey("orthographies.id"))

    def __repr__(self):
        return "<FormRepresentation {}>".format(self.written_form)


@db.declarative_mixin
class LexicalFormMixin:
    phonetic_form = db.Column(db.String(64), index=True)

    @db.declared_attr
    def form_representations(cls):
        return db.relationship("FormRepresentation", backref="lexical_form")


class Lemma(db.Model, LexicalFormMixin):
    __tablename__ = "lemmas"
    id = db.Column(db.Integer, primary_key=True)
    lexical_entry_id = db.Column(db.Integer, db.ForeignKey("lexical_entries.id"))

    def __repr__(self):
        return "<Lemma {}>".format(self.name)


class WordForm(db.Model, LexicalFormMixin):
    __tablename__ = "word_forms"
    id = db.Column(db.Integer, primary_key=True)
    lexical_entry_id = db.Column(db.Integer, db.ForeignKey("lexical_entries.id"))
    form_representation_id = db.Column(
        db.Integer, db.ForeignKey("form_representations.id")
    )

    def __repr__(self):
        return "<WordForm {}>".format(self.written_form)


class ExampleAxis(db.Model):
    __tablename__ = "example_axes"
    id = db.Column(db.Integer, primary_key=True)
    examples = db.relationship("SenseExample", backref="example_axis")


class SenseExample(db.Model):
    __tablename__ = "sense_examples"
    id = db.Column(db.Integer, primary_key=True)
    sense_id = db.Column(db.Integer, db.ForeignKey("senses.id"))
    example_axis_id = db.Column(db.Integer, db.ForeignKey("example_axes.id"))


class SenseAxis(db.Model):
    __tablename__ = "sense_axes"
    id = db.Column(db.Integer, primary_key=True)
    senses = db.relationship("Sense", backref="sense_axis")

    def __repr__(self):
        return "<SenseAxis {}>".format(self.id)


class Sense(db.Model):
    __tablename__ = "senses"
    id = db.Column(db.Integer, primary_key=True)
    lexical_entry_id = db.Column(db.Integer, db.ForeignKey("lexical_entries.id"))
    sense_number = db.Column(db.Integer, index=True)
    definition = db.Column(db.String(256), index=True)
    sense_axis_id = db.Column(db.Integer, db.ForeignKey("sense_axes.id"))

    def __repr__(self):
        return "<Sense {}>".format(
            self.lexical_entry.lemma.written_form + str(self.sense_number)
        )


class Component(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    lexical_entry_id = db.Column(db.Integer, db.ForeignKey("lexical_entries.id"))

    def __repr__(self):
        return "<Component {}>".format(self.lexical_entry.lemma.written_form)


class ListOfComponents(db.Model):
    __tablename__ = "list_of_components"
    id = db.Column(db.Integer, primary_key=True)
    lexical_entry_id = db.Column(db.Integer, db.ForeignKey("lexical_entries.id"))
    components = db.relationship(
        "Component", backref="list_of_components", uselist=True, lazy="dynamic"
    )

    def __repr__(self):
        return "<ListOfComponents {}>".format(self.component_type)


class PartOfSpeech(enum.Enum):
    noun = "noun"
    verb = "verb"
    adjective = "adjective"
    adverb = "adverb"
    auxiliary_verb = "auxiliary_verb"
    pronoun = "pronoun"
    proper_noun = "proper_noun"
    preposition = "preposition"
    conjunction = "conjunction"
    interjection = "interjection"
    numeral = "numeral"
    determiner = "determiner"
    particle = "particle"
    subordinating_conjunction = "subordinating_conjunction"
    symbol = "symbol"
    other = "other"


class LexicalEntry(db.Model):
    __tablename__ = "lexical_entries"
    id = db.Column(db.Integer, primary_key=True)
    lexicon_id = db.Column(db.Integer, db.ForeignKey("lexicons.id"))
    lexicon = db.relationship(
        "Lexicon", backref=db.backref("lexical_entries", lazy="dynamic")
    )
    lemma = db.relationship(
        "Lemma", backref="lexical_entry", uselist=False, lazy="dynamic"
    )
    word_forms = db.relationship("WordForm", backref="lexical_entry")
    part_of_speech = db.Column(db.Enum(PartOfSpeech), index=True)
    senses = db.relationship(
        "Sense", backref="lexical_entry", uselist=False, lazy="dynamic"
    )
    list_of_components = db.relationship(
        "ListOfComponents", backref="lexical_entry", uselist=True, lazy="dynamic"
    )
    component = db.relationship(
        "Component", backref="lexical_entry", uselist=False, lazy="dynamic"
    )

    def __repr__(self):
        return "<LexicalEntry {}>".format(self.lemma.written_form)
