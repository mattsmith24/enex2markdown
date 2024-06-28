import pytest
from enex_parser import EnexParser
from note_listener import NoteListener
from note import NoteWriter
from pathlib import Path
import textwrap
from datetime import datetime, timezone

@pytest.fixture
def single_note():
    xmlstr = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
        <en-export export-date="20130730T205637Z" application="Evernote" version="Evernote Mac">
            <note>
                <title>Test Note for Export</title>
                <content>
                    <![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                    <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
                    <en-note style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;">
                        Hello, World.
                        <div>
                            <br/>
                        </div>
                        <div>
                            <en-media alt="" type="image/jpeg" hash="dd7b6d285d09ec054e8cd6a3814ce093"/>
                        </div>
                        <div>
                            <br/>
                        </div>
                    </en-note>
                    ]]>
                </content>
                <created>20130730T205204Z</created>
                <updated>20130730T205624Z</updated>
                <tag>fake-tag</tag>
                <note-attributes>
                    <latitude>33.88394692352314</latitude>
                    <longitude>-117.9191355110099</longitude>
                    <altitude>96</altitude>
                    <author>Brett Kelly</author>
                </note-attributes>
                <resource>
                    <data encoding="base64">/9j/4AAQSkZJRgABAQAAAQABAAD/4gxYSUNDX1BST0ZJTEUAAQEAAAxITGlubwIQAABtbnRyUkdCIFhZ
                    WiAHzgACAAkABgAxAABhY3NwTVNGVAAAAABJRUMgc1JHQgAAAAAAAAAAAAAAAAAA9tYAAQAAAADTLUhQ
                    <!-- ... -->
                    kfeIGT/+uufk8DpM0gyVjGfmzkgetesnUoTHJ+5Cxn86zmv4/wB75EW+QHAPUH/P9Ky+s1rtrr/wfvOm
                    dBSamnq/xPKp/hpLKmS7x4OBjgn6elee6v4OuLJirRSHb/FtyG9s9u1fR0+oTiIRvGq7W4bpisfUGk1C
                    GVWtkIyM57n1rfDY+uqigtU76ffZkUsA6iajHZ6v/P8A4B//2Q==</data>
                    <mime>image/jpeg</mime>
                    <width>1280</width>
                    <height>720</height>
                    <resource-attributes>
                        <file-name>snapshot-DAE9FC15-88E3-46CF-B744-DA9B1B56EB57.jpg</file-name>
                    </resource-attributes>
                </resource>
            </note>
        </en-export>
        """)
    xmlpath = Path('pytest_input_files', 'test_parse_note.xml')
    xmlpath.parent.mkdir(parents=True, exist_ok=True)
    with open(xmlpath, "w") as f:
        f.write(xmlstr)
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
