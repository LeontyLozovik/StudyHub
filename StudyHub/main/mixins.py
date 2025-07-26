class NotesMixin:
    def get_notes(self, lesson):
        filter_type = self.request.GET.get('filter', 'all')

        if filter_type == 'my':
            return lesson.notes_to_lesson.filter(user=self.request.user)
        elif filter_type == 'private':
            return lesson.notes_to_lesson.filter(user=self.request.user, availability='private')
        else:
            return lesson.notes_to_lesson.filter(availability='public')
