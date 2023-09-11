import json
import subprocess
        
# вызываем в консоль команду journalctl и собираем всё в файл result
# start и end передаются в формате str - поэтому передается без кавычек
def journalctl(start, end):
    try:
        result = subprocess.run(["journalctl", "--since", start, "--until", end, "-o", "json-pretty"], stdout=subprocess.PIPE) 
        text = result.stdout.decode('UTF-8').lstrip()
        text = correct_format(text)
        return text
    except Exception as ex:
        return exit(0)

# функция для корректировки формата до json
def correct_format(text):
    if text[0] != '[':
        text = '[' + text.replace('}', '},')[:-2] + ']'
    return text

# Передаем файл с логами, корректируем до формата json, используя функцию correct_format(text)
# Счтываем новый файл json, возвращаем список словарей data
def json_format(file_name):  
    with open(file_name) as file:
        text = file.read()

        # проверяем корректный ли формат
        text = correct_format(text)
    
    # переводим в json формат
    data = json.loads(text)
  
    return data

# Готовый датасет
# dataset = pandas.DataFrame(fomating('test.txt'))
# print(dataset)