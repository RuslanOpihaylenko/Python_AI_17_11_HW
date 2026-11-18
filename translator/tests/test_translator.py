"""Перевірки prompt-а та взаємодії перекладача без самої LLM."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.dictionary import BilingualDictionary
from app.translator import Translator


class FakeLanguageModel:
    """Заміна справжньої моделі, що запам'ятовує останній запит."""

    def __init__(self) -> None:
        self.system_prompt = ""
        self.user_prompt = ""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        return "fake translation"


class TranslatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        dictionary = BilingualDictionary(
            Path(self.temporary_directory.name) / "dictionary.json"
        )
        dictionary.add("мовна модель", "language model")
        self.model = FakeLanguageModel()
        self.translator = Translator(self.model, dictionary)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_translation_includes_matching_glossary_and_explanation_setting(self) -> None:
        result = self.translator.translate(
            text="Мовна модель допомагає.",
            source_language="українська",
            target_language="англійська",
            style="офіційний",
            explain=True,
        )

        self.assertEqual(result, "fake translation")
        self.assertEqual(self.model.user_prompt, "Мовна модель допомагає.")
        self.assertIn("мовна модель = language model", self.model.system_prompt)
        self.assertIn("офіційний", self.model.system_prompt)
        self.assertIn("коротко поясни", self.model.system_prompt)

    def test_empty_text_is_rejected_before_calling_model(self) -> None:
        with self.assertRaisesRegex(ValueError, "не може бути порожнім"):
            self.translator.translate(
                text=" ",
                source_language="українська",
                target_language="англійська",
                style="нейтральний",
                explain=False,
            )

        self.assertEqual(self.model.user_prompt, "")


if __name__ == "__main__":
    unittest.main()
