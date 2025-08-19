import requests

DEEPSEEK_API_KEY = "sk-3758e7b8c30345959bc25004f3da6f04"  # 替换为你的API密钥
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"  # 可用模型: deepseek-chat / deepseek-reason

def extract_nested(s: str):
    stack, result = [], []
    for i, char in enumerate(s):
        if char == '(': 
            stack.append(i)
        elif char == ')' and stack:
            start = stack.pop()
            result.append(s[start+1:i])  # 提取括号内文本
        if char == '（': 
            stack.append(i)
        elif char == '）' and stack:
            start = stack.pop()
            result.append(s[start+1:i]) 
    for x in sorted(result):
        s =s.replace(x,'')
    if "(" in s:
        s =s.replace(')','')
        s = s.replace('(','')
    if  '（' in s:
        s =s.replace('（','')
        s =s.replace('）','')
    if '/' in s:
        s = s.split('/')[1]
    return [s,result]

def perior_process(base_config_json,config_json):
    """
        预处理返回的信息
    """
    uie = [x['流程名称'] for x in config_json]
    print(uie)
    po,ds = [],[]
    for x in range(0,len(uie)):
        dfer = extract_nested(uie[x])
        po.append(dfer[0])
        ds.append(dfer[1])
    for y in range(0,len(po)):
        config_json[y]['流程名称'] =po[y]
        config_json[y]['备注'] =ds[y]
        if '冲污水' in po[y] :
            # config_json[y]['流程名称'] = '冲污水+'+f"{po[y+1]}"
            print("d")
        # sda.append(config_json[y])
        config_json[y]["水洗段配置要求"] =  deepseek_procerssas(base_config_json,config_json[y])
    return config_json

def deepseek_procerssas(sda,names):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        with open(r"D:\\UserBackup\\tan-j1\\桌面\\除胶渣连水平沉铜机\\提示词\\"+names['流程名称']+r".txt",'r',encoding="utf-8") as file:
            sort = file.read()
        print(f"D:\\UserBackup\\tan-j1\\桌面\\除胶渣连水平沉铜机\\提示词\\"+names['流程名称']+".txt")
        print(sda)
        # 3. 准备对话内容
        messages = [
            {"role": "system", "content": "药水段后的水洗段的配置助手"},
            {"role": "user", "content": 
            f"""
            段落名是:{str(names)}
            通用配置:{str(sda['工作速度'])}
            具体段落要求为:{str(sort)}。
            根据以上数据返回,段落的水洗的速度的配置规则。
            不要多余的字符文字解释。
            例如：返回 默认冲污水+*级水刀洗，有长度限制可以按冲污水+*级水刀洗
            例如：返回 按***级水刀洗，可以默认*级水刀洗，有长度限制可以按*级水刀洗

            """}
        ]
        # 4. 请求参数
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.1,
            "top_p": 0.9,
            "max_tokens": 4096,
            "stream": False  # 设置为 True 可使用流式传输
        }
        # 5. 发送请求
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # print(result)
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # 6. 处理响应
            if "choices" in result:
                ai_response = result["choices"][0]["message"]["content"]
                print("AI回复:",ai_response)
                return ai_response
            else:
                return ""
        except requests.exceptions.RequestException as e:
            return ""
        except Exception as e:
            return ""
    except Exception as e:
        print(e)


def sdaw():
    configsd = {
    'baseconfig': {'入板方向': '左入右出', '滚轮直径': 32, '输送面宽': 860, '工作速度': 1.5, '孔径比': '20:1', '最小孔径': '通孔：0.2mm，盲孔:0.075mm', '轴距': 35}, 
                'config': [
                    {'流程名称': '入板', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '膨松', '反应时间': 125, '工作温度': 75, '水洗级数': None}, 
                    {'流程名称': '止水洗', '反应时间': None, '工作温度': None, '水洗级数': None},
                    {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '除胶渣', '反应时间': 249, '工作温度': 87, '水洗级数': None}, 
                    {'流程名称': '回收水洗+DI水洗', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 2}, 
                    {'流程名称': '预中和', '反应时间': 21, '工作温度': 25, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 1}, 
                    {'流程名称': '中和', '反应时间': 47, '工作温度': 37, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '检查', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '除油', '反应时间': 61, '工作温度': 60, '水洗级数': None}, 
                    {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3},
                    {'流程名称': '调整', '反应时间': 61, '工作温度': 60, '水洗级数': None}, 
                    {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None},
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '微蚀', '反应时间': 79, '工作温度': 34, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '预浸', '反应时间': 24, '工作温度': 25, '水洗级数': None}, 
                    {'流程名称': '水刀冲洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '预浸', '反应时间': 24, '工作温度': 27, '水洗级数': None}, 
                    {'流程名称': '活化', '反应时间': 67, '工作温度': 45, '水洗级数': None}, 
                    {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '还原', '反应时间': 53, '工作温度': 35, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '沉铜', '反应时间': 419, '工作温度': 37, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 4}, 
                    {'流程名称': '干板组合', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '冷却', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '出板', '反应时间': None, '工作温度': None, '水洗级数': None}
                    ]
    }
    configsd['config'] = perior_process(configsd['baseconfig'],configsd['config'])
    configsd['config'] = chongwushui(configsd['baseconfig'],configsd['config'])
    return {"baseconfig": configsd['baseconfig'] ,"config": configsd['config'] }

def chongwushui(base_config_json,config_json):
    sd = []
    d = 0
    for x in range(0,len(config_json)):
        if d == x and x !=0:
            config_json[x]['流程名称'] = f"{config_json[x-1]['流程名称']}+"+f"{config_json[x]['流程名称']}"
            sd.append(config_json[x])
            continue
        if config_json[x]['流程名称'] == "冲污水" or config_json[x]['流程名称'] == "回收水洗":
            d = x+1
            continue
        sd.append(config_json[x])
    return sd

    # print(base_config_json,config_json)


def chongwushui(base_config_json,config_json):
    repeat = []
    for x in range(0,len(config_json)):
        if config_json[x]['流程名称'] == "冲污水" and config_json[x+1]['流程名称'] == "冲污水":
            print(config_json[x])
            repeat.append(config_json[x]['流程名称']+"+"+config_json[x+1]['流程名称'])
        if config_json[x]['流程名称'] == "预中和":
            pass
        
    print(repeat)

if __name__ == "__main__":
    # print(sdaw())
    configsd = {'baseconfig': {'入板方向': '左入右出', '滚轮直径': 32, '输送面宽': 860, '工作速度': 1.5, '孔径比': '20:1', '最小孔径': '通孔：0.2mm，盲孔:0.075mm', '轴距': 35}, 
                'config': [
                    {'流程名称': '入板', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '膨松', '反应时间': 125, '工作温度': 75, '水洗级数': None}, 
                    {'流程名称': '止水洗', '反应时间': None, '工作温度': None, '水洗级数': None},
                    {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '除胶渣', '反应时间': 249, '工作温度': 87, '水洗级数': None}, 
                    {'流程名称': '回收水洗+DI水洗', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 2}, 
                    {'流程名称': '预中和', '反应时间': 21, '工作温度': 25, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 1}, 
                    {'流程名称': '中和', '反应时间': 47, '工作温度': 37, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '检查', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '除油', '反应时间': 61, '工作温度': 60, '水洗级数': None}, 
                    {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3},
                    {'流程名称': '调整', '反应时间': 61, '工作温度': 60, '水洗级数': None}, 
                    {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None},
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '微蚀', '反应时间': 79, '工作温度': 34, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '预浸', '反应时间': 24, '工作温度': 25, '水洗级数': None}, 
                    {'流程名称': '水刀冲洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '预浸', '反应时间': 24, '工作温度': 27, '水洗级数': None}, 
                    {'流程名称': '活化', '反应时间': 67, '工作温度': 45, '水洗级数': None}, 
                    {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '还原', '反应时间': 53, '工作温度': 35, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                    {'流程名称': '沉铜', '反应时间': 419, '工作温度': 37, '水洗级数': None}, 
                    {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 4}, 
                    {'流程名称': '干板组合', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '冷却', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                    {'流程名称': '出板', '反应时间': None, '工作温度': None, '水洗级数': None}
                    ]
                    }
    chongwushui(configsd['baseconfig'],configsd['config'])

    # configsd['config'] = perior_process(configsd['baseconfig'],configsd['config'])
    # chongwushui(configsd['baseconfig'],configsd['config'])


    # 'config': [ 
    #             {'流程名称': '入板', '反应时间': None, '工作温度': None, '水洗级数': None},
    #             {'流程名称': '膨松', '反应时间': 125, '工作温度': 75, '水洗级数': None}, 
    #             {'流程名称': '止水洗（水刀结构）', '反应时间': None, '工作温度': None, '水洗级数': None},
    #             {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
    #             {'流程名称': '加压水洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
    #             {'流程名称': '除胶渣', '反应时间': 249, '工作温度': 87, '水洗级数': None}, 
    #             {'流程名称': '超声波浸洗', '反应时间': None, '工作温度': None, '水洗级数': None}, 
    #             {'流程名称': '加压水洗', '反应时间': None, '工作温度': None, '水洗级数': 2},
    #             {'流程名称': 'Water Blast', '反应时间': 21, '工作温度': 20, '水洗级数': None}, 
    #             {'流程名称': '加压水洗', '反应时间': None, '工作温度': None, '水洗级数': 1}, 
    #             {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 1}, 
    #             {'流程名称': '回收水洗', '反应时间': None, '工作温度': None, '水洗级数': 1},
    #             {'流程名称': '冲污水', '反应时间': 47, '工作温度': 35, '水洗级数': None}, 
    #             {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
    #             {'流程名称': '预中和', '反应时间': None, '工作温度': None, '水洗级数': None},
    #             {'流程名称': '水刀洗', '反应时间': 61, '工作温度': 60, '水洗级数': None},
    #             {'流程名称': '中和', '反应时间': None, '工作温度': None, '水洗级数': None},
    #             {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
    #             {'流程名称': '检查', '反应时间': 61, '工作温度': 60, '水洗级数': None}, 
    #             {'流程名称': '整孔/调整', '反应时间': None, '工作温度': None, '水洗级数': None},
    #             {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3},
    #             {'流程名称': '(预微蚀+)微蚀（(喷淋)+水刀结构）', '反应时间': 79, '工作温度': 33, '水洗级数': None},
    #             {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
    #             {'流程名称': '预浸(沉铜)', '反应时间': 24, '工作温度': 28, '水洗级数': None}, 
    #             {'流程名称': '活化', '反应时间': 67, '工作温度': 40, '水洗级数': None},
    #             {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
    #             {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
    #             {'流程名称': '还原', '反应时间': 53, '工作温度': 30, '水洗级数': None}, 
    #             {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3},
    #             {'流程名称': '沉铜', '反应时间': 419, '工作温度': 30, '水洗级数': None}, 
    #             {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 4},
    #             {'流程名称': '干板组合', '反应时间': None, '工作温度': None, '水洗级数': None}, 
    #             {'流程名称': '冷却', '反应时间': None, '工作温度': None, '水洗级数': None},
    #             {'流程名称': '出板', '反应时间': None, '工作温度': None, '水洗级数': None}
    #             ]