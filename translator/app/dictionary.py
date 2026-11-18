"""Завантаження, пошук і редагування україно-англійського словника."""

import json
import re
from pathlib import Path


class BilingualDictionary:
    """Невеликий словник-підказка, який зберігається між запусками."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.entries = self._load()

    def _load(self) -> list[dict[str, str]]:
        """Читає словник з диска або створює порожній файл для першого запуску."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.file_path.write_text("[]\n", encoding="utf-8")

        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            # Не приховуємо пошкодження даних: користувач має знати, що виправити.
            raise ValueError(
                f"Файл словника має некоректний JSON: {self.file_path}"
            ) from error

        if not isinstance(data, list):
            raise ValueError("У файлі словника очікується JSON-список.")

        # Перевіряємо структуру, щоб неправильні записи не зламали пошук і prompt.
        for item in data:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("uk"), str)
                or not isinstance(item.get("en"), str)
                or not item["uk"].strip()
                or not item["en"].strip()
            ):
                raise ValueError(
                    "Кожен запис словника повинен містити непорожні поля "
                    "'uk' та 'en'."
                )

        return data

    def add(self, ukrainian: str, english: str) -> None:
        """Додає нову пару або оновлює англійський переклад українського терміна."""
        ukrainian = ukrainian.strip()
        english = english.strip()
        if not ukrainian or not english:
            raise ValueError("Обидва слова або вислови мають бути непорожніми.")

        # У межах словника українська форма є ключем: повторне додавання її оновлює.
        for entry in self.entries:
            if entry["uk"].casefold() == ukrainian.casefold():
                entry["en"] = english
                self._save()
                return

        self.entries.append({"uk": ukrainian, "en": english})
        self._save()

    def search(self, query: str) -> list[dict[str, str]]:
        """Шукає фрагмент українського або англійського слова без урахування регістру."""
        normalized_query = query.strip().casefold()
        if not normalized_query:
            return []

        return [
            entry
            for entry in self.entries
            if normalized_query in entry["uk"].casefold()
            or normalized_query in entry["en"].casefold()
        ]

    def find_in_text(
        self, text: str, source_language: str
    ) -> list[dict[str, str]]:
        """Знаходить у тексті цілі терміни, щоб передати їх моделі як підказки."""
        if source_language == "українська":
            source_key = "uk"
        elif source_language == "англійська":
            source_key = "en"
        else:
            raise ValueError("Невідома мова оригіналу.")
        found_entries = []

        for entry in self.entries:
            term = entry[source_key].strip()

            # Межі слова не дають знайти, наприклад, "cat" усередині "education".
            # Для фрази з пробілами цей самий шаблон працює як пошук цілого вислову.
            pattern = rf"(?<!\w){re.escape(term)}(?!\w)"
            if re.search(pattern, text, flags=re.IGNORECASE | re.UNICODE):
                found_entries.append(entry)

        return found_entries

    def all_entries(self) -> list[dict[str, str]]:
        """Повертає копію записів, щоб зовнішній код не змінював сховище напряму."""
        return [entry.copy() for entry in self.entries]

    def _save(self) -> None:
        """Записує словник у зрозумілому для людини форматі."""
        self.file_path.write_text(
            json.dumps(self.entries, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
