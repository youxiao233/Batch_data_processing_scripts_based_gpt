# 使用chatgpt的批量数据处理脚本
需要安装openai库
    
    pip install openai==0.28.0

下载并打开prompt.py

需要手动修改参数
```python
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
```
填完参数后，把输入的csv文件放在同一目录下，直接运行python脚本即可

# csv文件要求：
要求每行一条数据，并且每行没有其他多余信息，否则可能会有问题

# 输出格式
会得到和输入文件格式相同的，经过处理的输出信息

