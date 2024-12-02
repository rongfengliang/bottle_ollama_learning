from bottle import route, run, template,static_file

from ollama import chat

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
    return static_file(filepath, root='static')
@route('/<name>')
def index(name):
    for item in  chat_demo(name):
        yield item

run(host='localhost', port=8080,reloader=True)