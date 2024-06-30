import logging

from pathlib import Path
from enum import Enum
from contextlib import contextmanager
from datetime import datetime
import base64

from note_listener import NoteListener

logger = logging.getLogger("enex2markdown." + __name__)

class Note:
    def __init__(self):
        self.created = None
        self.updated = None
        self.title = None
        self.content = None
        self.tags = []
        self.resources = []

class NoteResource:
    def __init__(self):
        self.data = None
        self.mime = None
        self.filename = None

class NoteWriter(NoteListener):
    class OutputStyle(Enum):
        PATH = 1
        STREAM = 2

    def __init__(self, output_obj, output_style = OutputStyle.PATH):
        self.output_obj = output_obj
        self.output_style = output_style

    def add_note(self, note):
        fix_resource_names(note)
        with self.output_stream(note) as f:
            write_title(f, note)
            write_created(f, note)
            write_updated(f, note)
            write_tags(f, note)
            write_resources(f, note)
        self.write_resource_files(note)

    def iter_notes(self):
        pass

    @contextmanager
    def output_stream(self, note):
        if self.output_style == NoteWriter.OutputStyle.PATH:
            filename = self.get_output_filename(note)
            self.create_outputfile_dir(filename)
            logger.debug(f"Writing file: {filename}")
            f = open(filename, "w")
            yield f
            f.close()
        else:
            yield self.output_obj

    def get_output_filename(self, note):
        return Path(self.output_obj, str(note.created.year), f"{note.created.strftime('%Y%m%dT%H%M%SZ')}.md")

    def create_outputfile_dir(self, filename):
        filename.parent.mkdir(parents=True, exist_ok=True)

    def write_resource_files(self, note):
        for resource in note.resources:
            with self.resource_output_stream(note, resource) as f:
                if f is not None:
                    f.write(base64.b64decode(resource.data))

    @contextmanager
    def resource_output_stream(self, note, resource):
        if self.output_style == NoteWriter.OutputStyle.PATH:
            filename = self.get_resource_output_filename(note, resource)
            self.create_outputfile_dir(filename)
            logger.debug(f"Writing file: {filename}")
            f = open(filename, "wb")
            yield f
            f.close()
        else:
            yield None

    def get_resource_output_filename(self, note, resource):
        return Path(self.output_obj, str(note.created.year), resource.filename)


def fix_resource_names(note):
    if len(note.resources) > 0:
        resource_prefix = note.created.strftime('%Y%m%dT%H%M%SZ') + "-"
        for resource in note.resources:
            resource.filename = resource_prefix + resource.filename

def write_title(f, note):
    if note.title is not None:
        f.write(f"# {note.title}\n")

def write_created(f, note):
    if note.created is not None:
        f.write(f"Created: {note.created.strftime('%Y-%m-%d %H:%M:%S')}\n")

def write_updated(f, note):
    if note.updated is not None:
        f.write(f"Updated: {note.updated.strftime('%Y-%m-%d %H:%M:%S')}\n")

def write_tags(f, note):
    if len(note.tags) > 0:
        tagstr = ", ".join(note.tags)
        f.write(f"Tags: {tagstr}")

def write_resources(f, note):
    for resource in note.resources:
        write_resource(f, resource)

def write_resource(f, resource):
    write_resource_link(f, resource)

def write_resource_link(f, resource):
    if resource.filename is not None:
        img_md = ""
        if "image" in resource.mime:
            img_md = "!"
        f.write(f"{img_md}[{resource.filename}]({resource.filename})\n")
