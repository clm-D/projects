
import re

nums = '	赵姓名字大全共有赵姓名字162998个'

num = re.findall(r'\d+', nums)
print(num)