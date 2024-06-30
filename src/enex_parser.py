import logging
from lxml import etree
from datetime import datetime, timezone
from note import Note, NoteResource

logger = logging.getLogger("enex2markdown." + __name__)

# Thanks to http://www.hanxiaogang.com/writing/parsing-evernote-export-file-enex-using-python/
# for inspiration
class EnexParser:
    def __init__(self):
        self.note_store = NoteStore()
        self.init_taghandlers()

    def init_taghandlers(self):
        self.tag_handlers = {
            "note": NoteHandler(self.note_store),
            "created": CreatedHandler(self.note_store),
            "updated": UpdatedHandler(self.note_store),
            "title": TitleHandler(self.note_store),
            "tag": TagsHandler(self.note_store),
            "resource": ResourceHandler(self.note_store),
            "data": DataHandler(self.note_store),
            "mime": MimeHandler(self.note_store),
            "file-name": FileNameHandler(self.note_store),
        }

    def parseNoteXML(self, xmlFile: str) -> None:
        counter = 100
        context = etree.iterparse(xmlFile, events=["start", "end"], encoding='utf-8', strip_cdata=False)
        for ind, (action, elem) in enumerate(context):
            self.handleParserEvent(ind, action, elem)
            counter -= 1
            if counter < 1:
                break

    def handleParserEvent(self, ind: int, action: str, elem) -> None:
        logger.debug(f"Found elem with tag: {elem.tag}. ind: {ind}, action: {action}")
        if elem.tag in self.tag_handlers:
            self.tag_handlers[elem.tag].handle_event(action, elem)

    def register_note_listener(self, listener):
        self.note_store.note_listener = listener

class NoteStore:
    def __init__(self):
        self.note = None
        self.note_listener = None

    def new_note(self):
        self.note = Note()

    def end_note(self):
        if self.note_listener:
            self.note_listener.add_note(self.note)
        self.note = None

    def new_resource(self):
        self.resource = NoteResource()

    def end_resource(self):
        self.note.resources.append(self.resource)
        self.resource = None

class BaseHandler:
    def __init__(self, note_store):
        self.note_store = note_store

    def handle_event(self, action, elem):
        pass

class NoteHandler(BaseHandler):
    def handle_event(self, action, _elem):
        if action == "start":
            logger.debug(f"Found a note")
            self.note_store.new_note()
        elif action == "end":
            self.note_store.end_note()

class CreatedHandler(BaseHandler):
    def handle_event(self, action, elem):
        if action == "end":
            datestr = elem.text
            logger.info(f"Created: {datestr}")
            self.note_store.note.created = parseDateTime(datestr)

class UpdatedHandler(BaseHandler):
    def handle_event(self, action, elem):
        if action == "end":
            datestr = elem.text
            self.note_store.note.updated = parseDateTime(datestr)

class TitleHandler(BaseHandler):
    def handle_event(self, action, elem):
        if action == "end":
            logger.info(f"Title: {elem.text}")
            self.note_store.note.title = elem.text

class TagsHandler(BaseHandler):
    def handle_event(self, action, elem):
        if action == "end":
            self.note_store.note.tags.append(elem.text)

class ResourceHandler(BaseHandler):
    def handle_event(self, action, elem):
        if action == "start":
            self.note_store.new_resource()
        elif action == "end":
            self.note_store.end_resource()

class DataHandler(BaseHandler):
    def handle_event(self, action, elem):
        if action == "end":
            self.note_store.resource.data = remove_all_whitespace(get_all_elem_text(elem))

class MimeHandler(BaseHandler):
    def handle_event(self, action, elem):
        if action == "end":
            self.note_store.resource.mime = elem.text

class FileNameHandler(BaseHandler):
    def handle_event(self, action, elem):
        if action == "end":
            self.note_store.resource.filename = elem.text

def parseDateTime(datestr: str) -> datetime:
    # Only accepts format:
    # 20130730T205204Z
    year = int(datestr[0:4])
    month = int(datestr[4:6])
    day = int(datestr[6:8])
    hour = int(datestr[9:11])
    minute = int(datestr[11:13])
    second = int(datestr[13:15])
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)

def remove_all_whitespace(s):
    return ''.join(s.split())

def get_all_elem_text(elem):
    return ''.join(elem.itertext())
