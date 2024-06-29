
import logging

from enex_parser import EnexParser
from note import NoteWriter

logger = logging.getLogger("enex2markdown")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    parser = EnexParser()
    parser.register_note_listener(NoteWriter('f:\\yocheckit\\Documents\\Temp'))
    parser.parseNoteXML('f:\\yocheckit\\dropbox\\2024\\matts24s-notebook.enex')
