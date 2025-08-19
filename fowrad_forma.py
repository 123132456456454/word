import requests
import requests
import pandas as pd
import logging
import sys
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask import make_response
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import json
import re 
import link_table
import son

DEEPSEEK_API_KEY = "sk-3758e7b8c30345959bc25004f3da6f04"  # 替换为你的API密钥
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"  # 可用模型: deepseek-chat / deepseek-reason

# def traverse_with_neighbors(process_list):
#     for i in range(len(process_list)):
#         prev = process_list[i-1] if i > 0 else None
#         current = process_list[i]
#         next = process_list[i+1] if i < len(process_list)-1 else None
        
#         print(f"\n索引 {i}: {current['流程名称']}")
#         print(f"前一个元素: {prev['流程名称'] if prev else None}")
#         print(f"当前元素:  {current['流程名称']}")
#         print(f"后一个元素: {next['流程名称'] if next else None}")

def process_excel_data(file_path,list_d):
    """
    读取Excel文件并逐行处理数据
    
    参数:
        file_path: Excel文件路径
    """
    try:
        # 读取Excel文件（支持.xlsx和.xls格式）skiprows=10,nrows=15
        df = pd.read_excel(file_path)
        print(list_d) 
        if '+' in list_d["流程名称"]:
            num_flow = list_d["流程名称"].split('+')
            for x in num_flow:
                df = df[df['图块名称'].str.contains(x, case=False, na=False)]
                # print(df)
            filtered_df = df 
        else:        
            filtered_df = df[df['图块名称'].str.contains(list_d["流程名称"], case=False, na=False)]
        # filtered_df["输送面"] = contain_df['输送面'].astype(str).fillna('')
        contain_df = filtered_df[filtered_df['输送面'].str.contains(list_d["输送面"][:-2], case=False, na=False)].copy()
        # print(contain_df)
        contain_df['滚轮直径'] = contain_df['滚轮直径'].astype(str).fillna('')
        contain_df['轴距'] = contain_df['轴距'].astype(str).fillna('')
        contain_df['级数'] = contain_df['级数'].astype(str).fillna('')
        des_df = contain_df[contain_df['滚轮直径'].str.contains(list_d['滚轮直径'], case=False, na=False)]
        des_df = des_df[des_df['轴距'].str.contains(list_d['轴距'], case=False, na=False)]
        s_df = des_df[des_df['入板方向'].str.contains(list_d['入板方向'],case=False,na=False)]
        print(s_df)
        if list_d["水洗级数"] != "":
            sfs_df = s_df[s_df['级数'].str.contains(str(list_d["水洗级数"]),case=False,na=False)]
            print(sfs_df)
            return sfs_df
        print(s_df)
        return s_df
        
    except FileNotFoundError:
        print(f"错误: 文件未找到 - {file_path}")
    except ValueError as ve:
        print(f"错误: 文件读取错误 - {str(ve)}")
    except Exception as e:
        print(f"发生未预期错误: {str(e)}")

def exact_geshi(sum_gra):
    """
        格式提取
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    # with open("exact\\"+names+r".txt",'r',encoding="utf-8") as file:
    #     sort = file.read()

    # 3. 准备对话内容
    messages = [
        {"role": "system", "content": """用户将提供给你一段问卷内容，请你分析问卷内容，并提取其中的关键信息，以JSON的形式输出，输出的JSON需严格遵守以下的格式：
                                        不需要带单位,严格按照以下格式输出。
                                        ** 规则如下**
                                            (1) 入板方向只输出;(左进右出|右进左出|左右都可)三个字符串
                                        '{
                                            "入板方向": "左进右出/右进左出/左右都可",
                                            "工作速度": "(具体速度数值字符)(不要带单位)",
                                            "滚轮直径": "滚路直径数值(不要带单位)",
                                            "轴距": "轴距的数值字符(不要带单位)",
                                            "输送面": "输送面数值字符(不要带单位)",
                                            "流程名称": "<当前段落名称>",
                                            "反应时间": "具体反应时间数值字符(不要带单位)",
                                            "工作温度": "",
                                            "客户选配": "",
                                            "水洗级数": ""
                                        }'
         """},
        {"role": "user", "content": 
         f"""
         {sum_gra}
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
            try:
                parsed_json = json.loads(ai_response)
                formatted_json = json.dumps(parsed_json, indent=4, sort_keys=True)
                return formatted_json
            except json.JSONDecodeError:
                # print("AI回复:",ai_response)
                return ai_response
        else:
            return ""
    except requests.exceptions.RequestException as e:
        return ""
    except Exception as e:
        return ""

def process_3(baseconfig_json, config_json):
    """
        流式输出的主函数
    """
    excel_file = r"D:\\UserBackup\\tan-j1\\桌面\\规格书\\UCE图纸编码规则说明21.7.16.xlsx"
    try:
        asd = ""
        for x in config_json:
            try:
                asd = x['流程名称']
                grapargh = {**baseconfig_json, **x}
                aiw = exact_geshi(grapargh)  
                data = son.sd(aiw)
                if data.get("反应时间"):   # 反应时间
                    length = 1000 * float(data["工作速度"]) * int(data['反应时间']) / 60
                    data["有效长度"] = length
                
                # 获取Excel数据
                df = process_excel_data(excel_file,data)
                context = deepseek_means_test(x['流程名称'], df, data)
                print(context)
                yield {
                    "Msg":None,
                    "Data":{"process": asd,"result":  context},
                    "Success": True
                }
            except Exception as e:
                yield 
                {
                    "Msg":None,
                    "Data":{"process": asd,"result":  f"{e}"},
                    "Success": False
                }
                continue
    except Exception as e:
        yield {
                    "Msg":None,
                    "Data":{"process": asd,"result":  f"{e}"},
                    "Success": False
            }

def deepseek_means_test(names,df,stercha):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    try:
        with open("exact\\"+names+r".txt",'r',encoding="utf-8") as file:
            sort = file.read()
    except:
         with open("exact\\other.txt",'r',encoding="utf-8") as file:
            sort = file.read()

    csv_string = df.to_csv(index=False, encoding='utf-8')
    # 3. 准备对话内容
    messages = [
        {"role": "system", "content": "你图块号智能选取助手"},
        {"role": "user", "content": 
         f"""
         {sort}
         具体要求为:{stercha}。
         图块号数据库为:{str(csv_string)}
         以json格式返回
         {"图块号":"",
          "检查段":""}
         是否需要增加检查段
         仔细检查获得的有效长度是否符合要求,获得的图块号与要求的有效长度差距不大都能接受不需要多个图块号，导致浪费。例如：要求3000mm，找到3100mm的是可以接受的，要求3000mm，找到2900mm的也是是可以接受的
         需要返回多个图块号的情况下,就算返回的编号相同也要返回两个，编号之间用逗号隔开，而且所有图块总长加起来超过6000mm要提醒增加马达隔离位。
         所有编号输出一定要完整。

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






sdfe = {"入板方向":"左进右出","滚轮直径":"32","轴距":"35","输送面宽":"860","工作速度":1.5,"孔径比":"20：1（通孔） 1:1 (盲孔)","最小孔径":"0.2mm(通孔)0.075mm（盲孔）"}
# 示例数据
process_data = [
                        {'流程名称': '入板', '反应时间': None, '工作温度': None, '水洗级数': None},
                        {'流程名称': '膨松', '反应时间': 125, '工作温度': 75, '水洗级数': None}, 
                        {'流程名称': '止水洗', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                        {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                        {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
                        {'流程名称': '除胶渣', '反应时间': 249, '工作温度': 87, '水洗级数': None}, 
                        {'流程名称': '回收水洗', '反应时间': None, '工作温度': None, '水洗级数': None}, 
                        {'流程名称': 'DI水洗', '反应时间': None, '工作温度': None, '水洗级数': None}, 
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

gen = process_3(sdfe,process_data)
for result in gen:
    print("===== 返回结果 =====")
    print(f"流程: {result}")
    print(f"流程: {result['Data']['process']}")
    print(f"结果: {result['Data']['result']}")
    print(f"成功状态: {result['Success']}")
    print("====================")

# 使用示例（读取第5个元素，索引从0开始）
# traverse_with_neighbors(process_data)
# print("前一个元素:", prev)
# print("当前元素: ", current)
# print("后一个元素:", next)