# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020-11-29 22:26
# software: PyCharm
import frida, sys
import requests

rpc = '''
Interceptor.attach(Module.findExportByName("libyuanrenxue_native.so","sleep"), {
    onEnter: function(args) {
        args[0]=ptr(0);
    },
    onLeave:function(retval){

    }
});
rpc.exports = {
    getsign:function(a){
        var ret = "";
        Java.perform(
            function(){
            var l = Java.use('com.yuanrenxue.onlinejudge2020.OnlineJudgeApp');           
            send("rpc:"+a)
            ret = l.getSign1(a)            
            }
        )
        return ret;
    }
}

'''


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


def get_sig_hook(script, str):
    sig = script.exports.getsign(str)
    print('sig:', sig)
    return sig


def prepare_hook():
    process = frida.get_usb_device().attach('com.yuanrenxue.onlinejudge2020')
    script = process.create_script(rpc)
    script.on('message', on_message)
    script.load()
    return script


def req(i, sign):
    headers = {
        'Host': 'sekiro.virjar.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.7.0',
    }
    params = (
        ('id', f'{i}'),
        ('sign', sign)
    )
    response = requests.get('https://sekiro.virjar.com/yuanrenxue/query', headers=headers, params=params)
    print(response.json())
    return response.json()['data']


script = prepare_hook()
for i in range(10000):
    sign = get_sig_hook(script, i)
    print(sign)
    num = req(i, sign)
print(sum(list(dict.values())))
