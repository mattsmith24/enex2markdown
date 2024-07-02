class NoteListener:
    """
    This class decouples the parser from the conversion step which allows
    testing the parser without doing any conversion.
    """
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)
