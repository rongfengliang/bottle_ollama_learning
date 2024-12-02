import sys
import os

from bottle import route, run, template,static_file

from ollama import chat

if hasattr(sys, '_MEIPASS'):
    # 获取打包后的临时路径
    resource_path = os.path.join(sys._MEIPASS, 'static')
else:
    resource_path = os.path.join(os.path.dirname(__file__), 'static')

def chat_demo(message):
    stream = chat(model='qwen2.5:0.5b',stream=True, messages=[
        {
          'role': 'system',
          'content': '你是指导助手,使用中文进行交流',
        },
        {
            'role': 'user',
            'content': message,
        },
    ])
    for chunk in stream:
        print(chunk['message']['content'])
        yield template("{{content}}",**{"content":chunk['message']['content']})


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=resource_path)
@route('/<name>')
def index(name):
    for item in  chat_demo(name):
        yield item

run(host='localhost', port=8080,reloader=True)