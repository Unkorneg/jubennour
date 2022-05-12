# from flask import current_app
import enum
from flask import current_app, url_for
from app import db


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(28), nullable=False)
    code = db.Column(db.String(3), nullable=False)
    lexicons = db.relationship("Lexicon", backref="language", lazy=True)

    def __repr__(self):
        return "<Language {}>".format(self.name)


class Lexicon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(28), nullable=False)
    language_id = db.Column(
        db.Integer, db.ForeignKey("language.id"), nullable=False
    )
    lexical_entries = db.relationship(
        "LexicalEntry", backref="lexicon", lazy=True
    )

    def __repr__(self):
        return "<Lexicon {}>".format(self.name)

    def get_language(self):
        return self.language.name


components = db.Table(
    "components",
    db.Column("component_id", db.Integer, db.ForeignKey("lexical_entry.id")),
    db.Column("composite_id", db.Integer, db.ForeignKey("lexical_entry.id")),
)


class LexicalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    lexicon_id = db.Column(
        db.Integer, db.ForeignKey("lexicon.id"), nullable=False
    )
    canonical_form = db.relationship(
        "CanonicalForm", back_populates="lexical_entry", uselist=False
    )
    inflected_forms = db.relationship(
        "InflectedForm",
        back_populates="lexical_entry",
        lazy=True,
    )
    senses = db.relationship(
        "LexicalSense", back_populates="lexical_entry", lazy=True
    )
    composed_of = db.relationship(
        "LexicalEntry",
        secondary=components,
        primaryjoin=(components.c.composite_id == id),
        secondaryjoin=(components.c.component_id == id),
        lazy="dynamic",
        backref=db.backref("components", lazy="dynamic"),
    )

    __mapper_args__ = {
        "polymorphic_identity": "lexical_senses",
        "with_polymorphic": "*",
        "polymorphic_on": type,
    }

    def __repr__(self):
        if self.canonical_form:
            return "<LexicalEntry {}>".format(self.canonical_form.written_form)
        else:
            return "<LexicalEntry {}>".format(self.id)

    def get_language(self):
        return self.lexicon.get_language()


class Phrase(LexicalEntry):
    origin = db.Column(db.String(256))

    __mapper_args__ = {
        "polymorphic_identity": "phrase",
        "with_polymorphic": "*",
    }


class PartOfSpeechEnum(enum.Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJ = "adjective"
    ADV = "adverb"
    PRO = "pronoun"
    PRE = "preposition"
    CON = "conjunction"
    INT = "interjection"
    ART = "article"
    NONE = ""


class PartAffixEnum(enum.Enum):
    PREF = "prefix"
    SUF = "suffix"
    NONE = ""


class Word(LexicalEntry):
    part_of_speech = db.Column(db.Enum(PartOfSpeechEnum))

    __mapper_args__ = {"polymorphic_identity": "word", "with_polymorphic": "*"}


class Part(LexicalEntry):
    affix = db.Column(db.Enum(PartAffixEnum))

    __mapper_args__ = {"polymorphic_identity": "part", "with_polymorphic": "*"}


class FormGendersEnum(enum.Enum):
    feminine = "feminine"
    masculine = "masculine"
    neutral = "neutral"
    NONE = ""


class FormNumbersEnum(enum.Enum):
    singular = "singular"
    plural = "plural"
    collective = "collective"
    dual = "dual"
    NONE = ""


class FormMoodsEnum(enum.Enum):
    indicative = "indicative"
    imperative = "imperative"
    conditional = "conditional"
    subjonctive = "subjonctive"
    infinitive = "infinitive"
    participle = "participle"
    gerund = "gerund"
    NONE = ""


class FormTensesEnum(enum.Enum):
    present = "present"
    past = "past"
    future = "future"
    imperfect = "imperfect"
    NONE = ""


class FormPersonsEnum(enum.Enum):
    first = "first"
    second = "second"
    third = "third"
    unpersonal = "unpersonal"
    NONE = ""


class LexicalForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    written_form = db.Column(db.String(28), nullable=False)
    alternative_form = db.Column(db.String(28), nullable=True)
    phonetic_form = db.Column(db.String(28), nullable=True)
    lexical_entry_id = db.Column(
        db.Integer, db.ForeignKey("lexical_entry.id"), nullable=False
    )

    number = db.Column(db.Enum(FormNumbersEnum), nullable=True)
    gender = db.Column(db.Enum(FormGendersEnum), nullable=True)
    mood = db.Column(db.Enum(FormMoodsEnum), nullable=True)
    tense = db.Column(db.Enum(FormTensesEnum), nullable=True)
    person = db.Column(db.Enum(FormPersonsEnum), nullable=True)

    def __repr__(self):
        return "<LexicalForm {}>".format(self.written_form)


class InflectionTypeEnum(enum.Enum):
    conjugation = "conjugation"
    mutation = "mutation"
    NONE = ""


class InflectedForm(LexicalForm):
    lexical_entry = db.relationship(
        "LexicalEntry", back_populates="inflected_forms"
    )
    inflection_type = db.Column(db.Enum(InflectionTypeEnum), nullable=True)


class CanonicalForm(LexicalForm):
    lexical_entry = db.relationship(
        "LexicalEntry", back_populates="canonical_form"
    )


translations = db.Table(
    "translations",
    db.Column("source_id", db.Integer, db.ForeignKey("lexical_sense.id")),
    db.Column("target_id", db.Integer, db.ForeignKey("lexical_sense.id")),
)


class LexicalSense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lexical_entry_id = db.Column(
        db.Integer, db.ForeignKey("lexical_entry.id"), nullable=False
    )
    lexical_entry = db.relationship("LexicalEntry", back_populates="senses")
    definition = db.Column(db.Text, nullable=True)
    disambiguator = db.Column(db.Text, nullable=True)
    targets = db.relationship(
        "LexicalSense",
        secondary=translations,
        primaryjoin=(translations.c.source_id == id),
        secondaryjoin=(translations.c.target_id == id),
        back_populates="sources",
        lazy="dynamic",
    )
    sources = db.relationship(
        "LexicalSense",
        secondary=translations,
        primaryjoin=(translations.c.target_id == id),
        secondaryjoin=(translations.c.source_id == id),
        back_populates="targets",
        lazy="dynamic",
    )

    def get_language(self):
        return self.lexical_entry.get_language()
