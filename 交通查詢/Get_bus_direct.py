from asyncore import write
import pandas as pd
import time
route = pd.read_csv(r"C:\python\交通查詢\公車站行駛路線.csv")
station = pd.read_csv(r"C:\python\交通查詢\公車路線經過的站.csv")
op = time.time()
with open(r'C:\python\交通查詢\公車能直達的站.csv',mode = 'w', encoding='utf-8') as file:
    file.write('站點\n')
for i in range(len(route['站名'])-1):
    temp = []
    start = time.time()
    with open(r'C:\python\交通查詢\公車能直達的站.csv',mode = 'a', encoding='utf-8') as file:
        file.write(route['站名'][i])
    for j in range(44):
        num = route['路線'+str(j+1)][i]
        for k in range(len(station['車次'])):
            if route['路線'+str(j+1)][i] == station['車次'][k]:
                for l in range(158):
                    if str(station['站點'+str(l+1)][k]) == 'nan':
                        break
                    if station['站點'+str(l+1)][k] not in temp:
                        with open(r'C:\python\交通查詢\公車能直達的站.csv',mode = 'a', encoding='utf-8') as file:
                            file.write(','+station['站點'+str(l+1)][k])
                        temp.append(station['站點'+str(l+1)][k])
    with open(r'C:\python\交通查詢\公車能直達的站.csv',mode = 'a', encoding='utf-8') as file:
        file.write('\n')
    end = time.time()
    print(format(end-start))

final = time.time()
print(format(final-op))
                    

















# for i in range(len(route['站名'])-1):
#     temp = []
#     start = time.time()
#     with open(r'C:\python\交通查詢\公車能直達的站.csv',mode = 'a', encoding='utf-8') as file:
#         file.write(route['站名'][i])
#     for j in range(44):
#         num = route['路線'+str(j+1)][i]
#         for l in range(len(route['站名'])-i-1):
#             for k in range(44):
#                 num2 = route['路線'+str(k+1)][l+i+1]
#                 if num == num2:
#                     if route['站名'][l+i+1] not in temp:
#                         temp.append(route['站名'][l+i+1])
#                         with open(r'C:\python\交通查詢\公車能直達的站.csv',mode = 'a', encoding='utf-8') as file:
#                             file.write(','+route['站名'][l+i+1])
#                 elif(str(num) == 'nan'):
#                     break
#     with open(r'C:\python\交通查詢\公車能直達的站.csv',mode = 'a', encoding='utf-8') as file:
#         file.write('\n')
#     end = time.time()
#     print(format(end-start))
