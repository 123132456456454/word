import pyodbc
import pandas as pd
from datetime import datetime

def execute_fqc_report():
    # 数据库连接参数
    server = r"192.168.60.15\UCEOA"  # 使用原始字符串处理反斜杠
    database = "UCEOA_V2"
    username = "sa"
    password = "sa"
    driver = "SQL Server"  # 替换为实际使用的驱动程序名称
    
    # 构建连接字符串
    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    
    try:
        # 建立数据库连接
        print(f"正在连接到数据库: {server}\\{database}...")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        print("数据库连接成功!")
        
        # 定义SQL查询
        sql_query = """
        select   
            CreatedAt as 日期,
            OrderNo as 订单,
            CustomerName as 客户,
            DuanLeName as 机组名,
            ExcepDesc as 异常信息,
            CLcS as 处理措施,
            YuanYin as  原因分析,
	        repeatcheck as 终巡检,
            DuanLeStage as 段落  
        from 
            tbProductModify 
        where 
            CreatedAt>='2025-07-11' 
            and CreatedAt<'2025-07-18'      
        """
        
        # 执行查询
        print(f"正在执行查询 (时间范围: 2025-07-11 至 2025-07-18)...")
        cursor.execute(sql_query)
        
        # 获取列名
        columns = [column[0] for column in cursor.description]
        
        # 获取所有结果
        results = cursor.fetchall()
        
        if not results:
            print("未找到匹配的记录")
            return None
        
        print(f"找到 {len(results)} 条记录")
        
        # 1. 返回原始格式 (元组列表)
        raw_results = [tuple(row) for row in results]
        print("结果格式: 元组列表")
        
        # 2. 返回字典格式 (更易使用)
        dict_results = [dict(zip(columns, row)) for row in results]
        print("结果格式: 字典列表")
        
        # 3. 使用Pandas DataFrame (便于分析)
        df = pd.DataFrame.from_records(results, columns=columns)
        print("结果格式: Pandas DataFrame")
        
        # 添加日期格式化列
        df['格式化日期'] = df['日期'].apply(lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S'))
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"FQC报表_{timestamp}.xlsx"
        
        # 导出到Excel
        print(f"导出结果到: {excel_filename}")
        df.to_excel(excel_filename, index=False)
        
        print("查询处理完成!")
        
        return {
            "raw_results": raw_results,
            "dict_results": dict_results,
            "dataframe": df,
            "excel_file": excel_filename
        }
        
    except pyodbc.Error as ex:
        print(f"数据库错误: {ex}")
        # 提取更详细的错误信息
        if len(ex.args) > 1:
            print(f"SQL Server错误: {ex.args[1]}")
        return None
    except Exception as e:
        print(f"程序错误: {e}")
        return None
    finally:
        # 确保关闭连接
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
            print("数据库连接已关闭")

# 主程序
if __name__ == "__main__":
    print("="*50)
    print("FQC报表查询")
    print("="*50)
    
    report_data = execute_fqc_report()
    
    if report_data:
        print("\n结果演示:")
        # 展示前3条记录
        print(f"\n前3条记录示例 (字典格式):")
        for i, row in enumerate(report_data['dict_results'][:3]):
            print(f"\n记录 #{i+1}:")
            for key, value in row.items():
                print(f"  {key}: {value}")
        
        print("\n" + "="*50)
        print(f"已生成Excel报表: {report_data['excel_file']}")
        print("="*50)
    else:
        print("\n未能获取报表数据")