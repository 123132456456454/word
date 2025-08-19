# 链表结构
class ListNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None

def list_to_linked_list(lst):
    if not lst:
        return None
        
    head = ListNode(lst[0])
    current = head
    
    for item in lst[1:]:
        current.next = ListNode(item)
        current = current.next
        
    return head

class DoublyListNode:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

def list_to_doubly_linked_list(lst):
    if not lst:
        return None, None
        
    head = DoublyListNode(lst[0])
    tail = head
    current = head
    
    for item in lst[1:]:
        new_node = DoublyListNode(item)
        current.next = new_node
        new_node.prev = current
        current = new_node
        tail = new_node
        
    return head, tail

# 全局变量
global head
global tail

# 查找节点函数（增加键存在检查）
def find_node_by_process(head, process_name):
    current = head
    while current:
        if isinstance(current.data, dict) and '流程名称' in current.data:
            if current.data['流程名称'] == process_name:
                return current
        current = current.next
    return None

# 合并三个节点（增加键存在检查）
def merge_three_nodes(node):
    """合并当前节点及其前后节点为一个节点"""
    if not node or not node.prev or not node.next:
        return node
    
    # 确保所有节点都有流程名称数据
    if not (isinstance(node.data, dict) and '流程名称' in node.data):
        return node
    if not (isinstance(node.prev.data, dict) and '流程名称' in node.prev.data):
        return node
    if not (isinstance(node.next.data, dict) and '流程名称' in node.next.data):
        return node
    
    # 定义水洗节点类型
    water_washes = ["水刀洗", "水刀冲洗", "热水刀洗", "加压水洗"]
    
    prev_node = node.prev
    next_node = node.next
    
    # 检查前后节点是否都是水洗节点
    is_prev_water = any(wash in prev_node.data['流程名称'] for wash in water_washes)
    is_next_water = any(wash in next_node.data['流程名称'] for wash in water_washes)
    
    if not (is_prev_water and is_next_water):
        return node
    
    # 获取水洗级数（使用安全获取）
    prev_level = prev_node.data.get('水洗级数', '?')
    next_level = next_node.data.get('水洗级数', '?')
    
    # 创建新节点数据
    new_name = f"{prev_level}级水刀洗+{node.data['流程名称']}+{next_level}级水刀洗"
    new_data = {
        '流程名称': new_name,
        '反应时间': node.data.get('反应时间', None),
        '工作温度': node.data.get('工作温度', None),
        '水洗级数': None
    }
    
    # 创建新节点
    new_node = DoublyListNode(new_data)
    
    # 连接新节点到链表
    if prev_node.prev:
        prev_node.prev.next = new_node
        new_node.prev = prev_node.prev
    else:
        global head
        head = new_node
        new_node.prev = None
    
    if next_node.next:
        next_node.next.prev = new_node
        new_node.next = next_node.next
    else:
        global tail
        tail = new_node
        new_node.next = None
    
    print(f"!! 合并节点: {prev_node.data['流程名称']} + {node.data['流程名称']} + {next_node.data['流程名称']}")
    print(f"   新节点: {new_name}")
    
    return new_node

# 从指定节点开始顺序遍历（完全重写，增加安全检查）
def traverse_forward_from(start_node, processed_nodes):
    # 安全检查：确保节点有数据
    if not start_node or not start_node.data or not isinstance(start_node.data, dict):
        print("!! 节点数据无效，跳过")
        return None
        
    # 如果此节点已经处理过，直接返回下一个节点
    if id(start_node) in processed_nodes:
        if start_node.next:
            print(f"跳过已处理节点")
            return start_node.next
        else:
            return None
    else:
        # 标记为已处理
        processed_nodes.add(id(start_node))
        print(f"\n开始处理节点")
    
    # 确保有流程名称
    if '流程名称' not in start_node.data:
        print("!! 节点缺少'流程名称'，跳过")
        return start_node.next if start_node.next else None
    
    print(f"节点名称: {start_node.data['流程名称']}")
    
    # 特殊规则 - 冲污水节点
    if start_node.data['流程名称'] == '冲污水' and start_node.next:
        # 确保下一个节点有数据
        if (not start_node.next.data or 
            not isinstance(start_node.next.data, dict) or 
            '流程名称' not in start_node.next.data):
            print("!! 冲污水的下一个节点无效，跳过")
            return start_node.next if start_node.next else None
            
        next_name = start_node.next.data['流程名称']
        
        # 定义水洗节点类型
        water_washes = ["水刀洗", "水刀冲洗", "热水刀洗", "加压水洗"]
        is_water_wash = any(wash in next_name for wash in water_washes)
        
        if is_water_wash:
            # 修改下一个节点名称
            new_name = "冲污水+" + next_name
            start_node.next.data['流程名称'] = new_name
            
            # 删除当前节点
            if start_node.prev:
                start_node.prev.next = start_node.next
                start_node.next.prev = start_node.prev
            else:
                global head
                head = start_node.next
                head.prev = None
            
            print(f"!! 合并冲污水节点: 冲污水 + '{next_name}' -> '{new_name}'")
            
            # 返回新处理的下一个节点
            return start_node.next
        else:
            # 无法合并
            print(f"!! 无法合并冲污水节点")
            return start_node.next if start_node.next else None
    
    # 特殊规则 - 回收水洗节点
    if start_node.data['流程名称'] == '回收水洗' and start_node.next:
        # 确保下一个节点有数据
        if (not start_node.next.data or 
            not isinstance(start_node.next.data, dict) or 
            '流程名称' not in start_node.next.data):
            print("!! 回收水洗的下一个节点无效，跳过")
            return start_node.next if start_node.next else None
            
        next_name = start_node.next.data['流程名称']
        
        if 'DI水洗' in next_name:
            # 修改下一个节点名称
            new_name = "回收水洗+DI水洗"
            start_node.next.data['流程名称'] = new_name
            
            # 删除当前节点
            if start_node.prev:
                start_node.prev.next = start_node.next
                start_node.next.prev = start_node.prev
            else:
                head = start_node.next
                head.prev = None
            
            print(f"!! 合并回收水洗节点: 回收水洗 + 'DI水洗' -> '{new_name}'")
            return start_node.next
        else:
            print(f"!! 无法合并回收水洗节点")
            return start_node.next if start_node.next else None
    
    # 特殊规则 - 预中和节点
    if start_node.data['流程名称'] == '预中和':
        merged_node = merge_three_nodes(start_node)
        if merged_node != start_node:
            print(f"!! 成功合并预中和节点")
            return merged_node
        else:
            print(f"!! 无法合并预中和节点")
            return start_node.next if start_node.next else None
    
    # 普通节点直接返回下一个
    return start_node.next if start_node.next else None

# 水洗级数预处理
def hengzhe(tables):
    for x in tables:
        if x.get('水洗级数') in ['', None]:
            x['水洗级数'] = None
        elif isinstance(x['水洗级数'], str) and x['水洗级数'].isdigit():
            x['水洗级数'] = int(x['水洗级数'])
    return tables

# 主处理函数（完全重写遍历逻辑，增加安全性）
def yuchuli(table):
    global head, tail
    table = hengzhe(table)
    head, tail = list_to_doubly_linked_list(table)
    
    # 跟踪已处理的节点
    processed_nodes = set()
    
    # 需要检测的节点类型
    target_processes = ['冲污水', '回收水洗', '预中和']
    
    # 改进的逻辑：只处理目标节点
    current = head
    while current:
        # 安全检查
        if not current.data or not isinstance(current.data, dict):
            current = current.next
            continue
            
        # 检查是否有"流程名称"键
        process_name = current.data.get('流程名称') if '流程名称' in current.data else ''
        
        # 如果是目标节点类型才处理
        if process_name in target_processes:
            print(f"处理目标节点: {process_name}")
            next_node = traverse_forward_from(current, processed_nodes)
            
            # 如果函数返回下一个节点，则继续处理
            if next_node:
                current = next_node
                continue
            
        # 普通节点前进
        current = current.next
    
    # 导出最终链表
    return export_linked_list_to_array(head)

# 将链表导出为数组（增加安全性）
def export_linked_list_to_array(head):
    array = []
    current = head
    while current:
        if current.data:
            if isinstance(current.data, dict):
                array.append(current.data.copy())
            else:
                array.append(current.data)
        current = current.next
    return array

# 测试代码
if __name__ == "__main__":
    data = [
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
        {'流程名称': '检查', '反应时间': None, '工作温度': None, '水洗极': None},
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
    
    print("原始数据长度:", len(data))
    
    processed_data = yuchuli(data)
    print(processed_data)
    print("\n处理后的数据:")
    for i, item in enumerate(processed_data):
        print(f"{i+1}. {item.get('流程名称', '未知节点')}")
    
    print("\n处理后的数据长度:", len(processed_data))