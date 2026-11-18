"""Локальний переклад за допомогою моделей Helsinki-NLP OPUS-MT."""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class LocalLanguageModel:
    """Виконує переклад між українською та англійською."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

        print(f"\nЗавантажую модель {model_name}...")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name
        )

        self.model.eval()
        self.device = torch.device("cpu")
        self.model.to(self.device)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Перекладає текст за допомогою OPUS-MT."""

        inputs = self.tokenizer(
            user_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        )

        with torch.inference_mode():
            generated_tokens = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=512,
                num_beams=4,
            )

        result = self.tokenizer.decode(
            generated_tokens[0],
            skip_special_tokens=True,
        )

        return result.strip()