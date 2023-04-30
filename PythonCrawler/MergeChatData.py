import pandas as pd
import os 

# 获取当前路径
current_path = os.getcwd()

# 列出当前路径下的所有文件和目录
files = os.listdir(current_path)

file_list = []
# 输出所有文件名
files.sort()
for file in files:
    if "ChatGPT" in file:
        file_list.append(current_path+'\\'+file)

# 按文件名排序
sorted_files = sorted(file_list, key=lambda x: x[-6:-4])
print(sorted_files)
# 读取所有Excel文件数据
df_list = []
for file in sorted_files:
    df = pd.read_csv(file)
    df_list.append(df)

# 合并所有数据
df_merged = pd.concat(df_list)

# 去除重复数据
df_unique = df_merged.drop_duplicates()

# 保存结果到新的Excel文件
df_unique.to_csv('ChatGPT_merged.csv', index=False,encoding='utf-8-sig')
