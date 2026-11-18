from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


def test_translation(model_name, text):
    print(f"\nЗавантаження {model_name}...")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    model.eval()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )

    with torch.inference_mode():
        output = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=128,
            num_beams=4,
        )

    translation = tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    )

    print("Оригінал:", text)
    print("Переклад:", translation)


test_translation(
    "Helsinki-NLP/opus-mt-uk-en",
    "Я їм їжу"
)

test_translation(
    "Helsinki-NLP/opus-mt-en-uk",
    "I eat food."
)