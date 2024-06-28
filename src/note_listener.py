class NoteListener:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def iter_notes(self):
        for item in self.notes:
            yield item
