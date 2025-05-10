import json

# Чтение диалогов из файла
def parse_dialogues(file_path):
    dialogues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("Содержимое файла:")
        print(lines)  # Вывод содержимого файла для проверки
        for line in lines:
            # Игнорировать пустые строки
            if not line.strip():
                continue

            # Разделим строку на вопрос-ответ и тег
            parts = line.split("—")
            if len(parts) == 2:
                question = parts[0].strip()
                answer_and_tag = parts[1].strip()

                # Разделим ответ и тег по 'tag='
                if 'tag=' in answer_and_tag:
                    answer, tag_part = answer_and_tag.split('tag=', 1)
                    tag = tag_part.strip()
                    answer = answer.strip()
                    dialogues.append((question, answer, tag))
                else:
                    print(f"⚠️ В строке пропущен тег: {line.strip()}")
    
    return dialogues

# Преобразуем в структуру для intents.json
def generate_intents(dialogues):
    intents = {
        "intents": []
    }

    # Создаем intent для каждого диалога
    for question, answer, tag in dialogues:
        intent = {
            "tag": tag,
            "patterns": [question],
            "responses": [answer]
        }
        intents["intents"].append(intent)
    
    return intents

# Генерация intents и сохранение в файл
def save_intents_to_json(file_path, intents):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(intents, f, ensure_ascii=False, indent=4)

input_file = 'data/dialogues.txt'
output_file = 'data/intents.json'

dialogues = parse_dialogues(input_file)
print("Диалоги после парсинга:")
print(dialogues)  # Печать полученных диалогов для проверки

intents = generate_intents(dialogues)
save_intents_to_json(output_file, intents)

print(f"Диалоги успешно сохранены в {output_file}!")
