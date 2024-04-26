from bus import *
from train_api import *
from bike import *

# TODO: 兩交通工具規劃路徑 
if __name__ == '__main__':
    Bus_CYCU_0,Bus_CYCU_1 = Get_bus(156)
    # print("-----------"+Bus_CYCU_0.name[len(Bus_CYCU_0.name) - 1]+"-----------")
    # for i in range(len(Bus_CYCU_0.name)):
    #     print(Bus_CYCU_0.name[i]+'\n'+Bus_CYCU_0.time[i]+'\n')    

    # print("-----------"+Bus_CYCU_1.name[len(Bus_CYCU_1.name) - 1]+"-----------")
    # for i in range(len(Bus_CYCU_1.name)):
    #     print(Bus_CYCU_1.name[i]+'\n'+Bus_CYCU_1.time[i]+'\n')
    print(Bus_CYCU_0.name[7]+'\n'+Bus_CYCU_0.time[7] + '\n')
    U_bike = bike()
    
    for i in range(len(U_bike.Name)):
        print(U_bike.Name[i])
