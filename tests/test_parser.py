import pytest
from enex_parser import EnexParser
from note_listener import NoteListener
from note import NoteWriter
from pathlib import Path
import textwrap
from datetime import datetime, timezone

@pytest.fixture
def single_note():
    xmlpath = Path('pytest_input_files', 'test_parse_note.xml')
    return xmlpath

def test_write_file(single_note):
    expected_output_path = Path('pytest_output', '2013', '20130730T205204Z.md')
    expected_output_path.unlink(missing_ok=True)

    parser = EnexParser()
    parser.register_note_listener(NoteWriter('pytest_output'))
    parser.parseNoteXML(single_note)

    assert expected_output_path.exists()
    with open(expected_output_path, "r") as f:
        text = f.read()
        assert "Test Note for Export" in text
        assert "Created: 2013-07-30 20:52:04" in text

@pytest.fixture
def note_listener():
    return NoteListener()

def test_parse_note(single_note, note_listener):
    parser = EnexParser()
    parser.register_note_listener(note_listener)
    parser.parseNoteXML(single_note)

    for note in note_listener.iter_notes():
        assert note.title == "Test Note for Export"
        assert note.created == datetime(2013, 7, 30, 20, 52, 4, tzinfo=timezone.utc)
        assert note.updated == datetime(2013, 7, 30, 20, 56, 24, tzinfo=timezone.utc)
        assert note.tags == ["fake-tag"]
