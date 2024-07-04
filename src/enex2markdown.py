
import logging
import argparse

from enex_parser import EnexParser
from note import NoteWriter

logger = logging.getLogger("enex2markdown")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)

def get_cli_args():
    argparser = argparse.ArgumentParser(
        prog='enex2markdown.py',
        description='Converts an EXEX export file from Evernote to a directory of markdown files and attachments.',
        )
    argparser.add_argument('input_filename')
    argparser.add_argument('-o', '--output-dir', default='.')
    argparser.add_argument('-l', '--log-level', default="warning", choices=["debug", "info", "warning", "error", "critical"])
    return argparser.parse_args()

def set_logging_level(level_str):
    level_dict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    logger.setLevel(level_dict[level_str])

def main():
    args = get_cli_args()
    set_logging_level(args.log_level)
    parser = EnexParser()
    parser.register_note_listener(NoteWriter(args.output_dir))
    parser.parseNoteXML(args.input_filename)

if __name__ == '__main__':
    main()