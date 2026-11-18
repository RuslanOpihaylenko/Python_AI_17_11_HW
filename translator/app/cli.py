"""Текстове меню: точка взаємодії студента з перекладачем."""

from app.config import (
    DICTIONARY_PATH,
    UK_EN_MODEL,
    EN_UK_MODEL,
    TRANSLATION_STYLES,
)

from app.dictionary import BilingualDictionary
from app.llm import LocalLanguageModel
from app.translator import Translator


def choose_translation_direction() -> tuple[str, str]:
    """Питає напрям і повертає назви мов для сервісу перекладу."""

    print("\nНапрям перекладу:")
    print("1. Українська → англійська")
    print("2. Англійська → українська")

    while True:
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            return "українська", "англійська"

        if choice == "2":
            return "англійська", "українська"

        print("Введіть 1 або 2.")


def choose_style() -> str:
    """Показує підтримувані стилі та повертає вибір користувача."""

    print("\nСтиль перекладу:")

    for key, style in TRANSLATION_STYLES.items():
        print(f"{key}. {style.capitalize()}")

    while True:
        choice = input("Ваш вибір: ").strip()

        if choice in TRANSLATION_STYLES:
            return TRANSLATION_STYLES[choice]

        print("Введіть номер одного з перелічених стилів.")


def translate_text(dictionary: BilingualDictionary) -> None:
    """Збирає параметри та виконує переклад."""

    source_language, target_language = choose_translation_direction()

    text = input("\nВведіть текст для перекладу: ")

    style = choose_style()

    explain = (
        input("Пояснити складні слова? (т/н): ")
        .strip()
        .casefold() == "т"
    )

    if source_language == "українська":
        model_name = UK_EN_MODEL
    else:
        model_name = EN_UK_MODEL

    language_model = LocalLanguageModel(model_name)

    translator = Translator(language_model, dictionary)

    result = translator.translate(
        text=text,
        source_language=source_language,
        target_language=target_language,
        style=style,
        explain=explain,
    )

    print("\nРезультат:")
    print(result)


def add_dictionary_entry(dictionary: BilingualDictionary) -> None:
    """Додає пару слів українською та англійською."""

    ukrainian = input("Слово або фраза українською: ")
    english = input("Відповідник англійською: ")

    dictionary.add(ukrainian, english)

    print("Пару збережено.")


def show_dictionary(dictionary: BilingualDictionary) -> None:
    """Виводить усі пари словника."""

    entries = dictionary.all_entries()

    if not entries:
        print("\nСловник поки порожній.")
        return

    print("\nУкраїнсько-англійський словник:")

    for entry in entries:
        print(f"- {entry['uk']} — {entry['en']}")


def search_dictionary(dictionary: BilingualDictionary) -> None:
    """Шукає термін у словнику."""

    query = input("Введіть слово або його частину: ")

    matches = dictionary.search(query)

    if not matches:
        print("Збігів не знайдено.")
        return

    for entry in matches:
        print(f"- {entry['uk']} — {entry['en']}")


def run() -> None:
    """Створює залежності та запускає головний цикл меню."""

    dictionary = BilingualDictionary(DICTIONARY_PATH)

    while True:
        print(
            "\n=== Українсько-англійський AI-перекладач ===\n"
            "1. Перекласти текст\n"
            "2. Додати пару до словника\n"
            "3. Показати словник\n"
            "4. Знайти слово у словнику\n"
            "0. Вийти"
        )

        choice = input("Ваш вибір: ").strip()

        try:
            if choice == "1":
                translate_text(dictionary)

            elif choice == "2":
                add_dictionary_entry(dictionary)

            elif choice == "3":
                show_dictionary(dictionary)

            elif choice == "4":
                search_dictionary(dictionary)

            elif choice == "0":
                print("До побачення!")
                break

            else:
                print("Введіть номер одного з пунктів меню.")

        except (ValueError, OSError) as error:
            print(f"Помилка: {error}")


if __name__ == "__main__":
    run()