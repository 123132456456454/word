import requests
import pandas as pd

DEEPSEEK_API_KEY = "sk-3758e7b8c30345959bc25004f3da6f04"  # 替换为你的API密钥
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"  # 可用模型: deepseek-chat / deepseek-reason

def deepseek_grapargh_check_1(str_0,file,df,str_1): # 使用段落规则检查啊
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    # 3. 准备对话内容
    messages = [
        {"role": "system", "content": "你是有帮助的AI助手"},
        {"role": "user", "content": f"""
        整个的段落流程:{df}
        当前段落名称:{str_0}
        ai选择的机身材质为:{str_1[2:]}
        对应的段落流程如下：{file}

        根据段落的规则，检查该ai选择的配置是否合适。
        严格按照格式输出:
            例如:
                "当前段落名称": "回收水洗+DI水洗",
                "ai选择的机身材质": "PVC",
                "检查结果": "不合适",
                "建议配置": "SST机身"
         """}
    ]

    # 4. 请求参数 
    payload = {
        "messages": messages,
        "temperature": 0.1,
        "top_p": 0.9,
        "max_tokens": 2000,
        "stream": False  # 设置为 True 可使用流式传输
    }
    # 5. 发送请求
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        print(result)

        # 6. 处理响应
        if "choices" in result:
            ai_response = result["choices"][0]["message"]["content"]
            # print("AI回复:")
            return ai_response
        else:
            return ""

    except requests.exceptions.RequestException as e:
        return ""
    except Exception as e:
        return ""

def deepseek_grapargh_check(str_0,file,df,str_1): # 使用段落规则检查啊
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    # 3. 准备对话内容
    messages = [
        {"role": "system", "content": "你是有帮助的AI助手"},
        {"role": "user", "content": f"""
        整个段落名称{df}
        当前段落名称:{str_0}
        ai选择的机身材质为:{str_1[2:]}
        对应的段落流程如下：{file}

        根据段落的规则，检查该ai选择的配置是否合适。
        严格按照格式输出:
            例如:
                "当前段落名称": "回收水洗+DI水洗",
                "ai选择的机身材质": "PVC",
                "检查结果": "不合适",
                "建议配置": "SST机身"
         """}
    ]

    # 4. 请求参数 
    payload = {
        "messages": messages,
        "temperature": 0.1,
        "top_p": 0.9,
        "max_tokens": 2000,
        "stream": False  # 设置为 True 可使用流式传输
    }
    # 5. 发送请求
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        print(result)

        # 6. 处理响应
        if "choices" in result:
            ai_response = result["choices"][0]["message"]["content"]
            # print("AI回复:")
            return ai_response
        else:
            return ""

    except requests.exceptions.RequestException as e:
        return ""
    except Exception as e:
        return ""

if __name__ == "__main__":
    grapargh_message =  [
                        {'入板': 'COINPL-MSSST-2386-3235-511-001'}, 
                        {'膨松': 'CDSWEL-FSSST-3186-3235-3450-C3115-001-E'}, 
                        {'止水洗': 'WDCONL-FSSST-1186-3235-610-001-EH'},
                        {'冲污水+水刀洗': 'WDMFRL-FSSST-1386-3235-1230-001-EH'}, 
                        {'除胶渣': 'CDPERL-FSSST-3186-3235-3753-C3115-001-E,CDPERL-FSSST-3186-3235-3450-C3115-001-E'}, 
                        {'回收水洗+DI水洗': 'WDRECL-MSPVC-1186-3235-1123-001-E'},
                        {'水刀洗+预中和+水刀洗': 'WDWACL-FSPVC-0386-3235-1829-001-DH'}, 
                        {'Water Blast': 'HPBLAL-FSSST-1186-3235-1053-001-E'}, 
                        {'水刀洗': 'WDMFRL-FSPVC-1186-3235-499-001-EH'}, 
                        {'中和': 'CDNEUL-FSPVC-1186-3235-1489-C1165-001-DH'}, 
                        {'水刀洗': 'WDMFRL-FSPVC-1386-3235-1059-001-EH'},
                        {'检查': 'WDWACL-FSPVC-0386-3235-2249-001-DH'}, 
                        {'除油': 'CDCONL-FSPP-1586-3235-1839-C1515-001-D'},
                        {'冲污水+水刀洗': 'WDMFRL-FSSST-1386-3235-1230-001-EH'},
                        {'调整': 'CDCONL-FSPP-1586-3235-1839-C1515-001-D'}, 
                        {'冲污水+水刀洗': 'WDMFRL-FSSST-1386-3235-1230-001-EH'}
                        ]
    
    source_file = r"D:\\UserBackup\\tan-j1\\桌面\\规格书\\流程总表.xlsx" 
    df_1 = pd.read_excel(source_file,usecols=['流程名称'])
    
    for x in grapargh_message:
        try:
            with open(r"D:\\UserBackup\\tan-j1\\桌面\\规格书\\规则提示词\\"+list(x.keys())[0]+"提示词.txt",'r',encoding="utf-8") as f:
                file = f.read()
                print(file)
            print(deepseek_grapargh_check(list(x.keys())[0],file,df_1,x[list(x.keys())[0]].split("-")[1]))
        except:
            continue
        finally:
            print("----------------------".center(50))
    # print(deepseek_grapargh_check(df_1))

    # for index,row in df_1.iterrows():
    #     print(row)
    # deepseek_grapargh_check()