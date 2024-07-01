import pytest
from note import Note, NoteResource, NoteWriter
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

def test_output_content_utf8():
    # Windows open() uses cp1252 by default but some characters can't be printed
    # in that encoding. UTF-8 can handle anything
    expected_output_path = Path('pytest_output', '2010', '20100101T000000Z.md')
    expected_output_path.unlink(missing_ok=True)

    note_writer = NoteWriter('pytest_output')
    note = Note()
    note.created = datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    note.title = "Unprintable with cp1252: 😀"
    note_writer.add_note(note)

    # If the file exists, then we didn't get an exception and crash
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

def test_output_content(note_writer, result_string_io):
    note = Note()
    note.content = '<en-note>Test content</en-note>'
    note_writer.add_note(note)
    assert "Test content" in result_string_io.getvalue()

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

def test_output_resources(note_writer, result_string_io):
    note = Note()
    note.created = datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    resource = NoteResource()
    resource.filename = "Test-page-color-Final.pdf"
    resource.mime = "application/pdf"
    with open(Path('pytest_input_files', 'b64-test-page-color-final-pdf.txt'), "r") as f:
        resource.data = f.read()
    note.resources.append(resource)
    note_writer.add_note(note)
    expected_resource_name = "Test-page-color-Final.pdf"
    expected_url = expected_resource_name
    assert f"[20100101T000000Z-{expected_resource_name}](20100101T000000Z-{expected_url})" in result_string_io.getvalue()

def test_output_image_resources(note_writer, result_string_io):
    note = Note()
    note.created = datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    resource = NoteResource()
    resource.filename = "Color Splash PNG Free Download.png"
    resource.mime = "image/png"
    with open(Path('pytest_input_files', 'b64-color-splash-png-free-download-png.txt'), "r") as f:
        resource.data = f.read()
    note.resources.append(resource)
    note_writer.add_note(note)
    expected_resource_name = "Color Splash PNG Free Download.png"
    expected_url = expected_resource_name
    expected_url = expected_url.replace(" ", "%20") # url-encoded spaces
    assert f"![20100101T000000Z-{expected_resource_name}](20100101T000000Z-{expected_url})" in result_string_io.getvalue()

def test_output_image_resources_blank_filename(note_writer, result_string_io):
    note = Note()
    note.created = datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    resource = NoteResource()
    resource.filename = ""
    resource.mime = "image/png"
    with open(Path('pytest_input_files', 'b64-color-splash-png-free-download-png.txt'), "r") as f:
        resource.data = f.read()
    note.resources.append(resource)
    note_writer.add_note(note)
    expected_resource_name = "file-0.png" # Filename created using an index and mime-type
    expected_url = expected_resource_name
    assert f"![20100101T000000Z-{expected_resource_name}](20100101T000000Z-{expected_url})" in result_string_io.getvalue()

def test_output_image_resources_weird_filename(note_writer, result_string_io):
    note = Note()
    note.created = datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    resource = NoteResource()
    resource.filename = "weird-characters:é😀.png"
    resource.mime = "image/png"
    with open(Path('pytest_input_files', 'b64-color-splash-png-free-download-png.txt'), "r") as f:
        resource.data = f.read()
    note.resources.append(resource)
    note_writer.add_note(note)
    # Filename translations
    # : -> -
    # é -> -
    # 😀 dropped
    expected_resource_name = "weird-characters-e.png"
    expected_url = expected_resource_name
    assert f"![20100101T000000Z-{expected_resource_name}](20100101T000000Z-{expected_url})" in result_string_io.getvalue()

def test_output_multiple_resources(note_writer, result_string_io):
    test_resources = [
        ("Test-page-color-Final.pdf", "application/pdf", 'b64-test-page-color-final-pdf.txt', ""),
        ("Color-Splash-PNG-Free-Download.png", "image/png", 'b64-color-splash-png-free-download-png.txt', "!"),
    ]
    note = Note()
    note.created = datetime(2010, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    for test_resource in test_resources:
        resource = NoteResource()
        resource.filename = test_resource[0]
        resource.mime = test_resource[1]
        with open(Path('pytest_input_files', test_resource[2]), "r") as f:
            resource.data = f.read()
        note.resources.append(resource)
    note_writer.add_note(note)
    for test_resource in test_resources:
        assert f"{test_resource[3]}[20100101T000000Z-{test_resource[0]}](20100101T000000Z-{test_resource[0]})" in result_string_io.getvalue()

@pytest.mark.parametrize("resource_name, resource_datafile", [
    ("Test-page-color-Final.pdf", 'b64-test-page-color-final-pdf.txt'),
    ("Color-Splash-PNG-Free-Download.png", 'b64-color-splash-png-free-download-png.txt'),
])
def test_output_resource_files(resource_name, resource_datafile):
    expected_output_path = Path('pytest_output', '2001', F"20010203T040506Z-{resource_name}")
    expected_output_path.unlink(missing_ok=True)

    note_writer = NoteWriter('pytest_output')
    note = Note()
    note.created = datetime(2001, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    resource = NoteResource()
    resource.filename = resource_name
    resource.mime = "asdf"
    with open(Path('pytest_input_files', resource_datafile), "r") as f:
        resource.data = f.read()
    note.resources.append(resource)
    note_writer.add_note(note)

    assert expected_output_path.exists()

def test_output_multiple_resource_files():
    test_resources = [
        ("Test-page-color-Final.pdf", 'b64-test-page-color-final-pdf.txt'),
        ("Color-Splash-PNG-Free-Download.png", 'b64-color-splash-png-free-download-png.txt'),
    ]
    for test_resource in test_resources:
        expected_output_path = Path('pytest_output', '2001', F"20010203T040506Z-{test_resource[0]}")
        expected_output_path.unlink(missing_ok=True)

    note_writer = NoteWriter('pytest_output')
    note = Note()
    note.created = datetime(2001, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    for test_resource in test_resources:
        resource = NoteResource()
        resource.filename = test_resource[0]
        resource.mime = "asdf"
        with open(Path('pytest_input_files', test_resource[1]), "r") as f:
            resource.data = f.read()
        note.resources.append(resource)
    note_writer.add_note(note)

    for test_resource in test_resources:
        expected_output_path = Path('pytest_output', '2001', F"20010203T040506Z-{test_resource[0]}")
        assert expected_output_path.exists()
