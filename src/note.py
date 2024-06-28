import logging

from pathlib import Path
from enum import Enum
from contextlib import contextmanager
from datetime import datetime
from note_listener import NoteListener

logger = logging.getLogger("enex2md." + __name__)

class Note:
    def __init__(self):
        self.created = None
        self.updated = None
        self.title = None
        self.tags = []

class NoteWriter(NoteListener):
    class OutputStyle(Enum):
        PATH = 1
        STREAM = 2

    def __init__(self, output_obj, output_style = OutputStyle.PATH):
        self.output_obj = output_obj
        self.output_style = output_style

    def add_note(self, note):
        with self.output_stream(note) as f:
            if note.title is not None:
                f.write(f"# {note.title}\n")
            if note.created is not None:
                f.write(f"Created: {note.created.strftime('%Y-%m-%d %H:%M:%S')}\n")
            if note.updated is not None:
                f.write(f"Updated: {note.updated.strftime('%Y-%m-%d %H:%M:%S')}\n")
            if len(note.tags) > 0:
                tagstr = ", ".join(note.tags)
                f.write(f"Tags: {tagstr}")


    def iter_notes(self):
        pass

    @contextmanager
    def output_stream(self, note):
        if self.output_style == NoteWriter.OutputStyle.PATH:
            filename = self.getOutputFilename(note)
            self.createOutputFiledir(filename)
            logger.debug(f"Writing file: {filename}")
            f = open(filename, "w")
            yield f
            f.close()
        else:
            yield self.output_obj

    def getOutputFilename(self, note):
        return Path(self.output_obj, str(note.created.year), f"{note.created.strftime('%Y%m%dT%H%M%SZ')}.md")

    def createOutputFiledir(self, filename):
        filename.parent.mkdir(parents=True, exist_ok=True)
