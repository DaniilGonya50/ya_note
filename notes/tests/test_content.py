from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestNoteList(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.list_url = reverse('notes:list')
        cls.author = User.objects.create(username='human')
        all_notes = [
            Note(
                title=f'Заметка {i}',
                text='Text',
                author=cls.author,
                slug=f'test{i}',
            )
            for i in range(3)
        ]
        Note.objects.bulk_create(all_notes)

    def test_notes_order(self):
        self.client.force_login(self.author)
        response = self.client.get(self.list_url)
        object_list = response.context['object_list']
        all_id = [note.id for note in object_list]
        sorted_id = sorted(all_id)
        self.assertEqual(all_id, sorted_id)
