"""Перевірки двомовного словника без завантаження LLM."""

import json
import tempfile
import unittest
from pathlib import Path

from app.dictionary import BilingualDictionary


class BilingualDictionaryTests(unittest.TestCase):
    def setUp(self) -> None:
        # Тимчасовий файл не змінює словник, який використовує справжній застосунок.
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.path = Path(self.temporary_directory.name) / "dictionary.json"
        self.dictionary = BilingualDictionary(self.path)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_add_update_and_search_are_persisted(self) -> None:
        self.dictionary.add("Привіт", "hello")
        self.dictionary.add("привіт", "hi")

        self.assertEqual(self.dictionary.search("HI"), [{"uk": "Привіт", "en": "hi"}])
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8"))[0]["en"], "hi")

    def test_find_in_text_respects_language_and_word_boundaries(self) -> None:
        self.dictionary.add("кіт", "cat")

        self.assertEqual(
            self.dictionary.find_in_text("A cat is here.", "англійська"),
            [{"uk": "кіт", "en": "cat"}],
        )
        self.assertEqual(
            self.dictionary.find_in_text("education is useful", "англійська"),
            [],
        )

    def test_invalid_dictionary_file_is_reported(self) -> None:
        self.path.write_text("{broken", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "некоректний JSON"):
            BilingualDictionary(self.path)


if __name__ == "__main__":
    unittest.main()
