import os
import openai
import time
openai.api_key = "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"

def get_resp(phrase, message):
    if phrase == 1:
        promt = "Ответь только да или нет. Является ли событие ({paste}) подозрительным?"
    elif phrase == 2:
        promt = "Опиши событие ({paste}) в операционной системе Linux. Почему данное событие является подозрительным или аномальным? Чем может быть вызвано данное событие?"
    reqest_text = promt.replace("{paste}", message)
    time.sleep(30)
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": reqest_text}]
    )
    return response['choices'][0]['message']['content']