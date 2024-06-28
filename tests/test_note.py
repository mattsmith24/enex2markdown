import pytest
from note import Note, NoteWriter
import io
from datetime import datetime, timezone
from pathlib import Path

def test_output_filename():
    expected_output_path = Path('pytest_output', '2010', '20100101T000000Z.md')
    expected_output_path.unlink(missing_ok=True)

    note_writer = NoteWriter('pytest_output')
    note = Note()
    note.created = datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    note_writer.add_note(note)

    assert expected_output_path.exists()

@pytest.fixture
def result_string_io():
    result = io.StringIO()
    yield result
    result.close()

@pytest.fixture
def note_writer(result_string_io):
    note_writer = NoteWriter(result_string_io, NoteWriter.OutputStyle.STREAM)
    yield note_writer


def test_output_title(note_writer, result_string_io):
    note = Note()
    note.title = "Test title"
    note_writer.add_note(note)
    assert "Test title" in result_string_io.getvalue()

def test_output_created(note_writer, result_string_io):
    note = Note()
    note.created = datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    note_writer.add_note(note)
    assert "Created: 2010-01-01 00:00:00" in result_string_io.getvalue()

def test_output_updated(note_writer, result_string_io):
    note = Note()
    note.updated = datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    note_writer.add_note(note)
    assert "Updated: 2010-01-01 00:00:00" in result_string_io.getvalue()

def test_output_tags(note_writer, result_string_io):
    note = Note()
    note.tags = ["hello", "world"]
    note_writer.add_note(note)
    assert "Tags: hello, world" in result_string_io.getvalue()
