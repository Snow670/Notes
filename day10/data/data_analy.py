'''
    数据分析基本流程：
    1. 数据收集：
    2. 数据处理：数据清洗，数据规整
    3. 数据分析：数据统计，探索性数据分析（EDA）、数据建模
    4. 结果展示：数据可视化，报表生成，结果保存

    Numpy：高性能科学计算和数据分析的基础包，提供多维数组对象(ndarray)
    具有矢量/向量化运算能力 、快速、节省空间
    import numpy as np
    Pandas：数据清洗（去重，去除空值）
    Matplotlib：目的是为Python创建一个matlab式的绘图接口
'''
'''
    共享单车每季度的平均骑行时间（换算成小时）
'''
import os
import numpy as np
import matplotlib.pyplot as plt

data_path = './data'
data_filenames = ['2017-q1_trip_history_data.csv','2017-q2_trip_history_data.csv',
'2017-q3_trip_history_data.csv','2017-q4_trip_history_data.csv'] 

# 数据收集
def collect_data():
    data_arr_list = []
    for data_filename in data_filenames:
        data_file_path = os.path.join(data_path,data_filename)
        data_arr = np.loadtxt(data_file_path,delimiter=',',dtype='str',skiprows=1)
        data_arr_list.append(data_arr)

    return data_arr_list

# 数据处理
def process_data(data_arr_list):
    duration_in_min_list = []
    for data_arr in data_arr_list:
        duration_str_col = data_arr[:,0]
        # 去掉引号
        duration_in_ms = np.core.defchararray.replace(duration_str_col,"",'')
        # ms到分钟，类型转换
        duration_in_min = duration_in_ms.astype('float')/1000/60
        duration_in_min_list.append(duration_in_min)
    return duration_in_min_list

# 数据分析
def analyze_data(duration_in_min_list):
    duration_mean_list = []
    for i,duration in enumerate(duration_in_min_list):
        duration_mean = np.mean(duration)
        print('第{}季度的平均骑行时长：{:.2f}分钟'.format(i+1,duration_mean))
        duration_mean_list.append(duration_mean)
    return duration_mean_list

# 结果展示
def show_result(duration_mean_list):
    plt.figure()
    # bar 绘制柱状图
    plt.bar(range(len(duration_mean_list)),duration_mean_list)
    plt.show()

if __name__ == "__main__":
    data_arr_list = collect_data()
    duration_in_min_list = process_data(data_arr_list)
    duration_mean_list = analyze_data(duration_in_min_list)
    show_result(duration_mean_list)