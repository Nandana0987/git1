my_list = [10, 20, 30, 40, 50]
reversed_list = []
for i in range(len(my_list) - 1, -1, -1):
    reversed_list.append(my_list[i])
print(f'original list: {my_list}')
print(f'reversed list:{reversed_list}')
