# -*-coding:utf-8-*-
"""
调用GPT接口进行信息批量处理
"""
import time
import csv
import openai
import random

#官方API调用
openai.api_key ="这里填写你的key"
openai.api_base = "https://api.openai.com/v1"

#chatanywhere API调用
#openai.api_key = "key"
#openai.api_base = "https://api.chatanywhere.com.cn/v1"

"""向GPT发送prompt获取响应"""

# 角色卡或者提示信息
prompt ="例如：对下面的文本进行重写，随机一百字到500字左右，不要超过200字，并且只输出一段，你只需要重写转述部分，而不需要输出多余的东西,必须使用中文输出"

use_modle='gpt-3.5-turbo'#本次询问使用的模型


INPUT_FILE_PATH = "./output1.csv"#读入文本路径
OUTPUT_JSON_FILE = "./out.csv"#输出文本路径

def rand(min_value, max_value):
    """生成指定范围内的随机整数"""
    return random.randint(min_value, max_value)
def read_csv(csv_file_path: str):
    """读取本地csv文件"""

    with open(csv_file_path, "r", newline="") as csv_file:
        csv_reader = csv.reader(csv_file)

        processed_lines = []

        for row in csv_reader:
            line = "".join(row).strip()
            if line:
                processed_lines.append(line)
    return processed_lines


def gpt_35_api_stream(messages: list):
    """流式传输"""
    print("成功进入gpt_35_api_stream函数")
    try:
        response = openai.ChatCompletion.create(
           model=use_modle,
           messages=messages,
           stream=True,
        )
        completion = {'role': '', 'content': ''}
        for event in response:
            if event['choices'][0]['finish_reason'] == 'stop':
                break
            for delta_k, delta_v in event['choices'][0]['delta'].items():
                completion[delta_k] += delta_v
        messages.append(completion)  # 直接在传入参数 messages 中追加消息
        return (True, '')
    except Exception as err:
        print('出现异常，等待十秒再次尝试')
        time.sleep(10)# 如果异常 等十秒再次发出请求
        gpt_35_api_stream(messages)

def extract_by_gpt(source_text: str):
    target_text = "这次的文本：" + source_text + ""#拼接完整的请求信息

    messages = [
        {
            "role": "user",
            "content": prompt  + target_text,
        },
    ]
    print(gpt_35_api_stream(messages))
    reply = messages[len(messages) - 1]["content"]
    return reply

def req(messages):
    print(gpt_35_api_stream(messages))
    reply = messages[len(messages) - 1]["content"]
    return reply
if __name__ == "__main__":

    text_list = read_csv(INPUT_FILE_PATH)
    for i, text in enumerate(text_list):
        with open(OUTPUT_JSON_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            print("--user:\n" + text)
            REPLY_TEXT = extract_by_gpt(text)
            print("##########--GPT:\n" + REPLY_TEXT)
            csv_writer.writerow([REPLY_TEXT])
    
        print(f"已完成chatGPT识别次数：{i}")

        if i%55==0 and i!=0:
            time.sleep(3600)
        else :
            time.sleep(10)