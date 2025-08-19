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

# 1. 准备工作
app = Flask(__name__)
CORS(app)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

DEEPSEEK_API_KEY = "sk-3758e7b8c30345959bc25004f3da6f04"  # 替换为你的API密钥
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"  # 可用模型: deepseek-chat / deepseek-reason

@app.route('/query', methods=['POST'])
def handler_search():
    try:
        # 解析请求数据（保持原始data不变）
        request_data = request.get_json(force=True)
        print(request_data)
        sdaf=link_table.yuchuli(request_data.get('config', []))
        # request_data.get('config', [])
        perior_process(sdaf)
        # 直接传递参数给process_2
        def generate():
            # 直接遍历process_2返回的生成器
            for result in process_3(
                request_data["baseconfig"], 
                sdaf
            ):
                yield json.dumps(result) + "\n"
        
        return app.response_class(generate(), mimetype='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def handl_search():
    try:
        # 解析请求数据（保持原始data不变）
        request_data = request.get_json(force=True)
        print(request_data)
        sdaf=link_table.yuchuli(request_data.get('config', []))
        # request_data.get('config', [])
        perior_process(sdaf)
        # 直接传递参数给process_2
        def generate():
            # 直接遍历process_2返回的生成器
            for result in process_2(
                request_data["baseconfig"], 
                sdaf
            ):
                yield json.dumps(result) + "\n"
        
        return app.response_class(generate(), mimetype='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['POST'])
def handle_search():
    """物料查询API（增加Content-Type校验）"""
    # 检查Content-Type
    if request.content_type != 'application/json':
        return jsonify({
            "error": "Unsupported Media Type",
            "message": "Content-Type must be application/json",
            "status": "error"
        }), 415 
    try:
        # sue = []
        data = request.get_json(force=True)  # 强制解析
        if not data or 'baseconfig' not in data:
            return jsonify({
                "error": "Missing required parameter: question",
                "status": "error"
            }), 400
        # for x in range(0,len(data['config'])):
        #     print({x+1:data['config'][x]['流程名称']})
        #     sue.append({x+1:data['config'][x]['流程名称']})
        # print(sue)   
        data = process_1(data["baseconfig"],data['config'])
        # result = {"response":data}
        response = jsonify({"response": data})
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    except Exception as e:
        # logger.error(f"处理异常: {str(e)}", exc_info=True)
        return jsonify({
            "error": "服务器内部错误",
            "details": str(e),
            "status": "error"
        }), 500


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
    return result 

def perior_process(config_json):
    [x['流程名称'] for x in config_json]
    for x in config_json:
        print(extract_nested(x["流程名称"]))

def traverse_with_neighbors(process_list):
    for i in range(len(process_list)):
        prev = process_list[i-1] if i > 0 else None
        current = process_list[i]
        next = process_list[i+1] if i < len(process_list)-1 else None
        
        print(f"\n索引 {i}: {current['流程名称']}")
        print(f"前一个元素: {prev['流程名称'] if prev else None}")
        print(f"当前元素:  {current['流程名称']}")
        print(f"后一个元素: {next['流程名称'] if next else None}")

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

def process_3(baseconfig_json, config_json):
    """
        流式输出的主函数
    """
    excel_file = r"D:\\UserBackup\\tan-j1\\桌面\\规格书\\UCE图纸编码规则说明21.7.16.xlsx"
    try:
        asd = ""
        for x in range(0,len(config_json)):
            speed_sort = {}
            try:
                if x == 0:
                    speed_sort["当前流程"] = config_json[x]['流程名称']
                    speed_sort["下一个流程"] = config_json[x+1]['流程名称']
                if config_json[x]['流程名称'] == config_json[-1]['流程名称']:
                    speed_sort["当前流程"] = config_json[x]['流程名称']
                    speed_sort["上一个流程"] = config_json[x-1]['流程名称'] 
                if  x != 0 and config_json[x]['流程名称'] != config_json[-1]['流程名称']:
                    speed_sort["当前流程"] = config_json[x]['流程名称']
                    speed_sort["上一个流程"] = config_json[x-1]['流程名称']
                    speed_sort["下一个流程"] = config_json[x+1]['流程名称']
                asd =config_json[x]['流程名称']
                grapargh = {**baseconfig_json, **config_json[x]}
                aiw = exact_geshi(grapargh)  
                data = son.sd(aiw)
                if data.get("反应时间"):   # 反应时间
                    length = 1000 * float(data["工作速度"]) * int(data['反应时间']) / 60
                    data["有效长度"] = length
                
                # 获取Excel数据
                df = process_excel_data(excel_file,data)
                context = deepseek_means_test_1(speed_sort,config_json[x]['流程名称'], df, data)
              
                yield {
                    "Msg":context["备注"],
                    "Data":{"process": asd,"result":  context["draw"]},
                    "Success": True
                }
            except Exception as e:
                yield 
                {
                    "Msg":None,
                    "Data":{"process": asd,"result":  f"{e}"},
                    "Success": True
                }
                continue
    except Exception as e:
        yield {
                    "Msg":None,
                    "Data":{"process": asd,"result":  f"{e}"},
                    "Success": True
            }
        
def process_2(baseconfig_json, config_json):
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
              
                yield {
                    "process": asd,
                    "result":  context
                }
            except Exception as e:
                yield {
                    "process": asd,
                    "result": f"{e}"
                }
                continue
    except Exception as e:
        yield {
            "process": asd,
            "result": f"{e}"
        }
        
# 格式提取
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

def process_1(baseconfig_json,config_json):
    try:
        uw = []
        excel_file = r"D:\\UserBackup\\tan-j1\\桌面\\规格书\\UCE图纸编码规则说明21.7.16.xlsx"
        for x in config_json:
            grapargh = {**baseconfig_json, **x}
            if x["反应时间"] != "":
                length = 1000*grapargh["工作速度"]*int(grapargh['反应时间'][:-1])/60
                b = {"有效长度":length} 
                grapargh["有效长度"]=length

            df = process_excel_data(excel_file, grapargh)
            uw.append({f"""{x['流程名称']}""":deepseek_means_test(x['流程名称'],df,grapargh)})
                # return {f"""{x['流程名称']}""":deepseek_means_test(x['流程名称'],process_excel_data(excel_file,grapargh),grapargh)}
    except Exception as e:
            return [{"error": str(e),"process": x['流程名称'], "config": x}]
    return uw

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
        {"role": "system", "content": """你图块号智能选取助手,根据规则选取图块号,回答按照json格式返回,输出的 JSON 需遵守以下的格式：

{
  "draw": {图块号数据库中选中的图块号（一连串字母，数字以及-符号的编号）},
  "备注": 告诉用是否要接检查段和吸水辘，都不需要就输出无
}"""},
        {"role": "user", "content": 
         f"""
         {sort}
         具体要求为:{stercha}。
         图块号数据库为:{str(csv_string)}
         仔细检查获得的有效长度是否符合要求,获得的图块号与要求的有效长度差距不大都能接受不需要多个图块号，导致浪费。例如：要求3000mm，找到3100mm的是可以接受的，要求3000mm，找到2900mm的也是是可以接受的
         需要返回多个图块号的情况下,就算返回的编号相同也要返回两个，编号之间用逗号隔开，而且所有图块总长加起来超过6000mm要提醒增加马达隔离位。
         所有编号输出一定要完整。沉铜后四级水刀洗要加吸水辘。

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
            return son.sd(ai_response)
        else:
            return ""
    except requests.exceptions.RequestException as e:
        return ""
    except Exception as e:
        return ""
    
def deepseek_means_test_1(seepp,names,df,stercha):
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
        {"role": "system", "content": """你图块号智能选取助手,根据规则选取图块号,回答按照json格式返回,输出的 JSON 需遵守以下的格式：

{
  "draw": {图块号数据库中选中的图块号（一连串字母，数字以及-符号的编号）},
  "备注": 告诉用是否要接检查段和吸水辘，都不需要就输出无
}"""},
        {"role": "user", "content": 
         f"""
          相邻段落为:{seepp}
         {sort}
         具体要求为:{stercha}。
         图块号数据库为:{str(csv_string)}
         仔细检查获得的有效长度是否符合要求,获得的图块号与要求的有效长度差距不大都能接受不需要多个图块号，导致浪费。例如：要求3000mm，找到3100mm的是可以接受的，要求3000mm，找到2900mm的也是是可以接受的
         需要返回多个图块号的情况下,就算返回的编号相同也要返回两个，编号之间用逗号隔开，而且所有图块总长加起来超过6000mm要提醒增加马达隔离位。
         所有编号输出一定要完整。沉铜后水刀洗要考虑加吸水辘。

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
            return son.sd(ai_response)
        else:
            return ""
    except requests.exceptions.RequestException as e:
        return ""
    except Exception as e:
        return ""

if __name__ == "__main__":
    run_simple(
        '0.0.0.0', 
        5102, 
        app,
        threaded=True,
        processes=1
    )
    
    