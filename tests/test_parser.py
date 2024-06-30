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
        assert len(note.resources) == 1
        assert note.resources[0].data == "/9j/4AAQSkZJRgABAQAAAQABAAD/4gxYSUNDX1BST0ZJTEUAAQEAAAxITGlubwIQAABtbnRyUkd" + \
            "CIFhZWiAHzgACAAkABgAxAABhY3NwTVNGVAAAAABJRUMgc1JHQgAAAAAAAAAAAAAAAAAA9tYAAQAAAADTLUhQkfeIGT/+uufk8DpM0gy" + \
            "VjGfmzkgetesnUoTHJ+5Cxn86zmv4/wB75EW+QHAPUH/P9Ky+s1rtrr/wfvOmdBSamnq/xPKp/hpLKmS7x4OBjgn6elee6v4OuLJirRS" + \
            "Hb/FtyG9s9u1fR0+oTiIRvGq7W4bpisfUGk1CGVWtkIyM57n1rfDY+uqigtU76ffZkUsA6iajHZ6v/P8A4B//2Q=="
        assert note.resources[0].mime == "image/jpeg"
        assert note.resources[0].filename == "snapshot-DAE9FC15-88E3-46CF-B744-DA9B1B56EB57.jpg"
