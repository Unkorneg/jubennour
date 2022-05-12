from app import create_app, db
from app.models import (
    Language,
    Lexicon,
    LexicalEntry,
    LexicalForm,
    LexicalSense,
    Word,
    Phrase,
    Part,
)

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Language": Language,
        "Lexicon": Lexicon,
        "LexicalEntry": LexicalEntry,
        "LexicalForm": LexicalForm,
        "LexicalSense": LexicalSense,
        "Word": Word,
        "Phrase": Phrase,
        "Part": Part,
    }
