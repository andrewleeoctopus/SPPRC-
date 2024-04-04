# SPPRC-代码解释：
一、参数设置：

电量上限：10

时间消耗 = 电量消耗 = 路程

每个充电站有十种充电选择，可以充i单位电，消耗i时间(i=1,2,3,4,5,6,7,8,9,10)

最短路径评价：所有可行不被支配的最终标签中用时最短的路径

二、代码使用（详见test.py）

1、config文件夹中的.yaml文件包含targets和charge_stations的信息，其中targets每个包含position（坐标）以及time_window（最迟抵达时间），命名为1，2，3......charge_stations每个包含position（坐标）,命名为A，B，C......

2、create_map函数由config文件夹中的config文件建图，使用时需要在函数中修改文件路径，接受一个mode参数，mode == 1时建立无必经要求的图（即没有额外节点资源）， mode == 2时建立有必经要求的图

3、由图建立SP类，并用solve方法求解。其中solve方法接受一个可选参数"end"，不输入时为不指定终止节点，输入即指定终止节点

4、打印最短路径，使用get_best_solution方法，也接受一个可选参数"end"，不输入时为不指定终止节点，输入即指定终止节点

此外，代码会根据config文件画出网络的简图

总结一下，对于(1)给定终点，无必经要求，应选择mode = 1且指定终点"end",(2)给定终点，有必经要求, 应选择 mode = 2且指定终点"end"，(3)不给定终点，有必经要求，应选择 mode = 1且不指定终点"end"

三、实例验证，运行已包含的config文件和一些其他测试，结果都符合预期
