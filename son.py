import json

def sd(uiwe):
    # json_string = '''
    # {
    #     "入板方向": "左进右出",
    #     "工作速度": "1.5",
    #     "滚轮直径": "32",
    #     "轴距": "35",
    #     "输送面": "860",
    #     "流程名称": "入板",
    #     "反应时间": "",
    #     "工作温度": "",
    #     "客户选配": "",
    #     "水洗级数": ""
    # }
    # '''

    sad = uiwe.replace("```","").replace("json",'')
    print(sad)
    json_object = json.loads(sad)
    print(json_object)
    return json_object
    print(json_object)  # 输出: {'name': 'John', 'age': 30, 'city': 'New York'}
    print(type(json_object))  # 输出: <class 'dict'>

if __name__ == "__main__":
    uiwe = """```json
{
    "入板方向": "左进右出",
    "工作速度": "1.5",     
    "滚轮直径": "32",      
    "轴距": "35",
    "输送面": "860",       
    "流程名称": "入板",    
    "反应时间": "",        
    "工作温度": "",        
    "客户选配": "",        
    "水洗级数": ""
}
```"""
    sd(uiwe)