from app import create_app, db
from app.models import (
    Language,
    Lexicon,
    Orthography,
    FormRepresentation,
    WordForm,
    Lemma,
    LexicalEntry,
    Sense,
    SenseAxis,
)

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Language": Language,
        "Lexicon": Lexicon,
        "Orthography": Orthography,
        "FormRepresentation": FormRepresentation,
        "WordForm": WordForm,
        "Lemma": Lemma,
        "LexicalEntry": LexicalEntry,
        "Sense": Sense,
        "SenseAxis": SenseAxis,
    }

if __name__ == "__main__":
    create_app().run()