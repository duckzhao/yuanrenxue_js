# author: ZhaoKun
# contact: 1161678627@qq.com
# datetime: 2020-11-27 13:09
# software: PyCharm

import pywasm


def env_abort(_: pywasm.Ctx):
    return


vm = pywasm.load(r'C:\Users\Administrator\Desktop\main.wasm', {
    'env': {
        'abort': env_abort,
    }
})
r = vm.exec('encode', [803226584, 803226580])
print(r)