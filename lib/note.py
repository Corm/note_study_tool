import datetime

class Note():
    '''
        This is a note for the database. 
        It contains the note text, the review urgency, and which notes are its parent.
    '''
    def __init__(self, note=None, db_id=0, parent_notes_list=None):
        '''
            note = the note text, [textline1, ...]
            db_id = the unique database id for this
            parents = {id of parent:parent, ...}
            children = {id of child:child, ...}
            urgency = the normalized value for how important it is to review this now
            review date = the last date that we reviewed this
        '''
        self.note = note if note else []
        self.db_id = db_id
        self.parent_notes = parent_notes_list
        self.child_notes = {}
        self.review_urgency = 0
        self.review_date = datetime.datetime.now()

    def _add_text_to_children(self, child_notes, note, func):
        text = self._prep_note(self.db_id, note)
        for child in child_notes.itervalues():
            text += func(child)
        return text

    def make_all_text(self):
        def text_getter(kid):
            return ["\t" + kidtext for kidtext in kid.make_all_text()]
        all_text = self._add_text_to_children(self.child_notes, self.note, text_getter)
        return all_text

    def make_all_text_minus_one_indent(self):
        def text_getter(kid):
            return kid.make_all_text()
        all_text = self._add_text_to_children(self.child_notes, self.note, text_getter)
        return all_text

    def _get_attributes(self, note):
        return [
            note.note,
            note.parent_notes,
            note.child_notes, 
            note.review_urgency,
            note.review_date]
    def compare(self, orig_note):
        my_attributes = self._get_attributes(self)
        orig_attributes = self._get_attributes(orig_note)
        for mine, orig in zip(my_attributes, orig_attributes):
            if mine != orig:
                return False
        return True

    def copy_meta(note):
        self.review_urgency = note.review_urgency
        self.review_date = note.review_date
        self.child_notes = note.child_notes

    def add_child(self, note):
        self.child_notes[note.db_id] = note

    def set_reviewed(self):
        self.importance_to_review = 0
        self.review_date = datetime.datetime.now()

    @staticmethod
    def _prep_note(db_id, note):
        text = note[:]
        if text:
            text.insert(0, str(db_id))
            text.append("\n")
        return text
