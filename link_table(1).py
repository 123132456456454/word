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

# 给定的数据
# data = [
#     {'流程名称': '入板', '反应时间': None, '工作温度': None, '水洗级数': None}, 
#     {'流程名称': '膨松', '反应时间': 125, '工作温度': 75, '水洗级数': None}, 
#     {'流程名称': '止水洗', '反应时间': None, '工作温度': None, '水洗级数': None},
#     {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
#     {'流程名称': '热水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 2}, 
#     {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
#     {'流程名称': '除胶渣', '反应时间': 249, '工作温度': 87, '水洗级数': None}, 
#     {'流程名称': '回收水洗+DI水洗', '反应时间': None, '工作温度': None, '水洗级数': None}, 
#     {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 2}, 
#     {'流程名称': '预中和', '反应时间': 21, '工作温度': 25, '水洗级数': None}, 
#     {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 1}, 
#     {'流程名称': '中和', '反应时间': 47, '工作温度': 37, '水洗级数': None}, 
#     {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
#     {'流程名称': '检查', '反应时间': None, '工作温度': None, '水洗级数': None}, 
#     {'流程名称': '除油', '反应时间': 61, '工作温度': 60, '水洗级数': None}, 
#     {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
#     {'流程名称': '水刀洗', '反应时间': None, '工作极': None, '水洗级数': 3},
#     {'流程名称': '调整', '反应时间': 61, '工作温度': 60, '水洗级数': None}, 
#     {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None},
#     {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
#     {'流程名称': '微蚀', '反应时间': 79, '工作温度': 34, '水洗级数': None}, 
#     {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
#     {'流程名称': '预浸', '反应时间': 24, '工作温度': 25, '水洗级数': None}, 
#     {'流程名称': '水刀冲洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
#     {'流程名称': '预浸', '反应时间': 24, '工作温度': 27, '水洗级数': None}, 
#     {'流程名称': '活化', '反应时间': 67, '工作温度': 45, '水洗级数': None}, 
#     {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
#     {'流程名称': '热水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 1},
#     {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 2}, 
#     {'流程名称': '还原', '反应时间': 53, '工作温度': 35, '水洗级数': None}, 
#     {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
#     {'流程名称': '沉铜', '反应时间': 419, '工作温度': 37, '水洗级数': None}, 
#     {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 4}, 
#     {'流程名称': '干板组合', '反应时间': None, '工作温度': None, '水洗级数': None}, 
#     {'流程名称': '冷却', '反应时间': None, '工作温度': None, '水洗级数': None}, 
#     {'流程名称': '出板', '反应时间': None, '工作温度': None, '水洗级数': None}
# ]
global head
global tail 
# 创建双向链表
# head, tail = list_to_doubly_linked_list(data)

# 查找特定流程名称的节点
def find_node_by_process(head, process_name):
    current = head
    while current:
        # 确保节点数据是字典类型
        if isinstance(current.data, dict) and '流程名称' in current.data:
            if current.data['流程名称'] == process_name :
                return current
        current = current.next
    return None


# 合并三个节点为一个节点
def merge_three_nodes(node):
    """合并当前节点及其前后节点为一个节点"""
    if not node or not node.prev or not node.next:
        return node
    
    # 检查前一个节点是否是水刀洗
    prev_node = node.prev
    if not (isinstance(prev_node.data, dict) and '流程名称' in prev_node.data and 
            ('水刀洗' in prev_node.data['流程名称'] or '水刀冲洗' in prev_node.data['流程名称'])):
        return node
    
    # 检查后一个节点是否是水刀洗
    next_node = node.next
    if not (isinstance(next_node.data, dict) and '流程名称' in next_node.data and 
            ('水刀洗' in next_node.data['流程名称'] or '水刀冲洗' in next_node.data['流程名称'])):
        return node
    
    # 获取水洗级数
    prev_level = prev_node.data.get('水洗级数', '?')
    next_level = next_node.data.get('水洗级数', '?')
    
    # 创建新节点数据
    new_name = f"{prev_level}级水刀洗+{node.data['流程名称']}+{next_level}级水刀洗"
    new_data = {
        '流程名称': new_name,
        '反应时间': node.data.get('反应时间', None),
        '工作温度': node.data.get('工作温度', None),
        '水洗级数': None  # 合并后不再有独立的水洗级数
    }
    
    # 创建新节点
    new_node = DoublyListNode(new_data)
    
    # 连接新节点到链表
    if prev_node.prev:
        prev_node.prev.next = new_node
        new_node.prev = prev_node.prev
    else:
        # 如果前一个节点是头节点
        global head
        head = new_node
        new_node.prev = None
    
    if next_node.next:
        next_node.next.prev = new_node
        new_node.next = next_node.next
    else:
        # 如果后一个节点是尾节点
        global tail
        tail = new_node
        new_node.next = None
    
    print(f"!! 合并节点: {prev_node.data['流程名称']} + {node.data['流程名称']} + {next_node.data['流程名称']}")
    print(f"   新节点: {new_name}")
    
    return new_node

# 从指定节点开始顺序遍历，并应用特殊规则
def traverse_forward_from(start_node):
    current = start_node
    print(f"\n从 '{start_node.data['流程名称']}' 开始顺序遍历:")
    
    # 处理特殊规则 - 冲污水节点
    if start_node.data['流程名称'] == '冲污水' and start_node.next:
        # 获取下一个节点名称（安全访问）
        next_name = ""
        if isinstance(start_node.next.data, dict) and '流程名称' in start_node.next.data:
            next_name = start_node.next.data['流程名称']
        
        # 检查下一个节点是否是水刀洗相关流程
        water_washes = ["水刀洗", "水刀冲洗", "热水刀洗","加压水洗"]
        if next_name in water_washes:
            # 修改下一个节点的名称
            start_node.next.data['流程名称'] = "冲污水+" + next_name
            
            # 删除当前冲污水节点
            if start_node.prev:
                start_node.prev.next = start_node.next
                start_node.next.prev = start_node.prev
            else:  # 如果冲污水是头节点
                global head
                head = start_node.next
                head.prev = None
            
            print(f"!! 应用特殊规则：删除 '{start_node.data['流程名称']}' 节点，"
                  f"并将下一个节点名称改为 '{start_node.next.data['流程名称']}'")
            
            # 从下一个节点开始遍历
            current = start_node.next
    
    # 处理特殊规则 - 预中和节点
    if start_node.data['流程名称'] == '预中和':
        # 尝试合并三个节点
        merged_node = merge_three_nodes(start_node)
        if merged_node != start_node:
            print(f"!! 应用特殊规则：合并三个节点为一个")
            current = merged_node
    
    # 开始遍历并打印节点
    count = 0
    while current and count < 20:  # 限制最多打印20个节点，避免无限循环
        # 安全获取相邻节点名称
        prev_name = ""
        next_name = ""
        
        if current.prev and isinstance(current.prev.data, dict) and '流程名称' in current.prev.data:
            prev_name = current.prev.data['流程名称']
        else:
            prev_name = "None" if current.prev is None else "Unknown"
        
        if current.next and isinstance(current.next.data, dict) and '流程名称' in current.next.data:
            next_name = current.next.data['流程名称']
        else:
            next_name = "None" if current.next is None else "Unknown"
        
        # 打印当前节点信息
        current_name = ""
        if isinstance(current.data, dict) and '流程名称' in current.data:
            current_name = current.data['流程名称']
        else:
            current_name = "Unknown"
        
        print(f"流程: {current_name} | 前一个: {prev_name} | 下一个: {next_name}")
        
        # 移动到下一个节点
        current = current.next
        count += 1
    if start_node.data['流程名称'] == '回收水洗' and start_node.next:
        # 获取下一个节点名称（安全访问）
        next_name = ""
        if isinstance(start_node.next.data, dict) and '流程名称' in start_node.next.data:
            next_name = start_node.next.data['流程名称']
        
        # 检查下一个节点是否是水刀洗相关流程
        water_washes = ["DI水洗"]
        if next_name in water_washes:
            # 修改下一个节点的名称
            start_node.next.data['流程名称'] = "回收水洗+" + next_name
            
            # 删除当前冲污水节点
            if start_node.prev:
                start_node.prev.next = start_node.next
                start_node.next.prev = start_node.prev
            else:  # 如果冲污水是头节点
               
                head = start_node.next
                head.prev = None
            
            print(f"!! 应用特殊规则：删除 '{start_node.data['流程名称']}' 节点，"
                  f"并将下一个节点名称改为 '{start_node.next.data['流程名称']}'")
            
            # 从下一个节点开始遍历
            current = start_node.next

# 从指定节点开始反向遍历
def traverse_backward_from(node):
    current = node
    print(f"\n从 '{node.data['流程名称']}' 开始反向遍历:")
    
    count = 0
    while current and count < 20:  # 限制最多打印20个节点
        # 安全获取相邻节点名称
        prev_name = ""
        next_name = ""
        
        if current.prev and isinstance(current.prev.data, dict) and '流程名称' in current.prev.data:
            prev_name = current.prev.data['流程名称']
        else:
            prev_name = "None" if current.prev is None else "Unknown"
        
        if current.next and isinstance(current.next.data, dict) and '流程名称' in current.next.data:
            next_name = current.next.data['流程名称']
        else:
            next_name = "None" if current.next is None else "Unknown"
        
        # 打印当前节点信息
        current_name = ""
        if isinstance(current.data, dict) and '流程名称' in current.data:
            current_name = current.data['流程名称']
        else:
            current_name = "Unknown"
        
        print(f"流程: {current_name} | 前一个: {prev_name} | 下一个: {next_name}")
        
        # 移动到前一个节点
        current = current.prev
        count += 1

# 将链表导出为数组
def export_linked_list_to_array(head):
    """将双向链表转换为数组"""
    array = []
    current = head
    while current:
        # 复制节点数据（避免修改原始数据）
        if isinstance(current.data, dict):
            array.append(current.data.copy())
        else:
            array.append(current.data)
        current = current.next
    return array

# 打印数组完整信息
def print_array_info(array):
    """打印数组的完整信息"""
    print("\n链表导出为数组的完整信息:")
    print("[" + ",\n ".join(str(item) for item in array) + "]")

def hengzhe(tables):
    for x in tables:
        if x['水洗级数'] == '' or x['水洗级数'] == None:
            x['水洗级数'] == None
        if type(x['水洗级数']) == str and x['水洗级数'] != '':
            x['水洗级数'] == int(x['水洗级数'])
    return tables

def yuchuli(table):
    # 初始链表导出为数组
    table = hengzhe(table)
    head, tail = list_to_doubly_linked_list(table)
    print("初始链表状态:")
    initial_array = export_linked_list_to_array(head)
    print_array_info(initial_array)
    
    while True:
        # 测试1：从预中和开始遍历（应用合并规则）
        process_to_find = "预中和"
        found_node = find_node_by_process(head, process_to_find)
        
        if found_node:
            print(f"\n成功找到节点: {found_node.data['流程名称']}")
            traverse_forward_from(found_node)
            traverse_backward_from(found_node)
        else:
            print(f"未找到名称为 '{process_to_find}' 的节点")
        
        # 测试2：从冲污水开始遍历（应用特殊规则）
        process_to_find = "冲污水"
        found_node = find_node_by_process(head, process_to_find)
        
        if found_node:
            print(f"\n成功找到节点: {found_node.data['流程名称']}")
            traverse_forward_from(found_node)
        else:
            print(f"未找到名称为 '{process_to_find}' 的节点")
        
        process_to_find = "回收水洗"
        found_node = find_node_by_process(head, process_to_find)
        
        if found_node:
            print(f"\n成功找到节点: {found_node.data['流程名称']}")
            traverse_forward_from(found_node)
        else:
            print(f"未找到名称为 '{process_to_find}' 的节点")
        
        # 测试3：从冲污水开始遍历另一个位置
        process_to_find = "冲污水"  # 如果有多个，会找到第一个
        found_node = find_node_by_process(head, process_to_find)
        
        if found_node:
            # 尝试找到不同的冲污水节点
            while found_node and found_node.data['流程名称'] == process_to_find:
                # 检查位置是否与之前相同（简单示例，实际应用需要更复杂的位置判断）
                next_name = found_node.next.data['流程名称'] if found_node.next else "None"
                if "水刀洗" in next_name:
                    print(f"\n找到另一个冲污水节点（下一站是: {next_name}）")
                    traverse_forward_from(found_node)
                    break
                found_node = find_node_by_process(found_node.next, process_to_find)
        else:
            print(f"未找到名称为 '{process_to_find}' 的节点")
            break
    
    # 最终链表导出为数组
    print("\n最终链表状态:")
    final_array = export_linked_list_to_array(head)
    print(final_array)
    return final_array

if __name__ == "__main__":
    # 初始链表导出为数组
    # print("初始链表状态:")
    # initial_array = export_linked_list_to_array(head)
    # print_array_info(initial_array)
    
    # while True:
    #     # 测试1：从预中和开始遍历（应用合并规则）
    #     process_to_find = "预中和"
    #     found_node = find_node_by_process(head, process_to_find)
        
    #     if found_node:
    #         print(f"\n成功找到节点: {found_node.data['流程名称']}")
    #         traverse_forward_from(found_node)
    #         traverse_backward_from(found_node)
    #     else:
    #         print(f"未找到名称为 '{process_to_find}' 的节点")
        
    #     # 测试2：从冲污水开始遍历（应用特殊规则）
    #     process_to_find = "冲污水"
    #     found_node = find_node_by_process(head, process_to_find)
        
    #     if found_node:
    #         print(f"\n成功找到节点: {found_node.data['流程名称']}")
    #         traverse_forward_from(found_node)
    #     else:
    #         print(f"未找到名称为 '{process_to_find}' 的节点")
        
    #     # 测试3：从冲污水开始遍历另一个位置
    #     process_to_find = "冲污水"  # 如果有多个，会找到第一个
    #     found_node = find_node_by_process(head, process_to_find)
        
    #     if found_node:
    #         # 尝试找到不同的冲污水节点
    #         while found_node and found_node.data['流程名称'] == process_to_find:
    #             # 检查位置是否与之前相同（简单示例，实际应用需要更复杂的位置判断）
    #             next_name = found_node.next.data['流程名称'] if found_node.next else "None"
    #             if "水刀洗" in next_name:
    #                 print(f"\n找到另一个冲污水节点（下一站是: {next_name}）")
    #                 traverse_forward_from(found_node)
    #                 break
    #             found_node = find_node_by_process(found_node.next, process_to_find)
    #     else:
    #         print(f"未找到名称为 '{process_to_find}' 的节点")
    #         break
    
    # # 最终链表导出为数组
    # print("\n最终链表状态:")
    # final_array = export_linked_list_to_array(head)
    # print(type(final_array))
    # print_array_info(final_array)

    # 
    data = [ 
            {'流程名称': '入板', '反应时间': None, '工作温度': None, '水洗级数': None},
            {'流程名称': '膨松', '反应时间': 125, '工作温度': 75, '水洗级数': None}, 
            {'流程名称': '止水洗', '反应时间': None, '工作温度': None, '水洗级数': None}, 
            {'流程名称': '冲污水', '反应时间': None, '工作温度': None, '水洗级数': None}, 
            {'流程名称': '水刀洗', '反应时间': None, '工作温度': None, '水洗级数': 3}, 
            {'流程名称': '除胶渣', '反应时间': 249, '工作温度': 87, '水洗级数': None}, 
            {'流程名`称': '回收水洗+DI水洗', '反应时间': None, '工作温度': None, '水洗级数': None}, 
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
            {'流程名称': '出板', '反应时间': None, '工作温度': None, '水洗级数': None}]
    print(yuchuli(data))