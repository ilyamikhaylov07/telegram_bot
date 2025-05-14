import json
from collections import defaultdict

# Чтение и парсинг диалогов из файла
def parse_dialogues(file_path):
    dialogues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("Содержимое файла:")
        print(lines)
        for line in lines:
            if not line.strip():
                continue

            parts = line.split("—")
            if len(parts) == 2:
                question = parts[0].strip()
                answer_and_tag = parts[1].strip()

                if 'tag=' in answer_and_tag:
                    answer, tag_part = answer_and_tag.split('tag=', 1)
                    tag = tag_part.strip()
                    answer = answer.strip()
                    dialogues.append((question, answer, tag))
                else:
                    print(f"⚠️ В строке пропущен тег: {line.strip()}")
    return dialogues

# Генерация intents с группировкой по тегу
def generate_intents(dialogues):
    grouped = defaultdict(lambda: {"patterns": set(), "responses": set()})

    for question, answer, tag in dialogues:
        grouped[tag]["patterns"].add(question)
        grouped[tag]["responses"].add(answer)

    intents = {"intents": []}
    for tag, data in grouped.items():
        intents["intents"].append({
            "tag": tag,
            "patterns": list(data["patterns"]),
            "responses": list(data["responses"])
        })

    return intents

# Сохранение в JSON
def save_intents_to_json(file_path, intents):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(intents, f, ensure_ascii=False, indent=4)

# Основной код
input_file = 'data/dialogues.txt'
output_file = 'data/intents.json'

dialogues = parse_dialogues(input_file)
print("Диалоги после парсинга:")
print(dialogues)

intents = generate_intents(dialogues)
save_intents_to_json(output_file, intents)

print(f"✅ Intents успешно сохранены в {output_file}!")
