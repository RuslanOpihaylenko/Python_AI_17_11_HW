"""Налаштування застосунку в одному місці."""

from pathlib import Path

# Папка проєкту — батьківська для пакета app.
# Так шляхи до даних не залежать від того, з якої папки запустили програму.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Невелика інструктивна модель Qwen з Hugging Face.
# Вона завантажується автоматично при першому запуску та зберігається в кеші.
UK_EN_MODEL = "Helsinki-NLP/opus-mt-uk-en"

EN_UK_MODEL = "Helsinki-NLP/opus-mt-en-uk"

# Словник зберігається у звичайному JSON-файлі, який легко відкрити й пояснити.
DICTIONARY_PATH = PROJECT_ROOT / "data" / "uk_en_dictionary.json"

# Варіанти стилю, доступні в меню та передані моделі в prompt.
TRANSLATION_STYLES = {
    "1": "нейтральний",
    "2": "розмовний",
    "3": "офіційний",
}
