import app.repository
from test.resolver import EmptyPropertyResolver
import unittest
from unittest.mock import patch

class TestRepository(unittest.TestCase):
    def test_test_changes__if_no_changes(self):
        repo = app.repository.PageRepository('sqlite:///:memory:')
        url = "https://example.com"
        title = "Title 1"
        assert repo.test_changes(url, title)
        assert not repo.test_changes(url, title)

    def test_test_changes__if_page_changed(self):
        repo = app.repository.PageRepository('sqlite:///:memory:')
        url = "https://example.com"
        title = "Title 1"
        changed_title = "Title 2"
        assert repo.test_changes(url, title)
        assert repo.test_changes(url, changed_title)

    