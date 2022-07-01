# JTT808 API接口文档

## 1. 枚举参数

### 1.1 LicensePlateColor

> 该类枚举了 JT/T 697.7--2014 文档中车牌颜色对应编码, **该编码用于终端注册中车牌颜色参数**

| Color      | Code     |
| :----------| ---------|
| blue       | 1        |
| yellow     | 2        |
| black      | 3        |
| white      | 4        |
| green      | 5        |
| other      | 9        |

示例:

```python
from jt_message import LicensePlateColor

LicensePlateColor.blue
# 1
LicensePlateColor.yellow
# 2
LicensePlateColor.black
# 3
LicensePlateColor.white
# 4
LicensePlateColor.green
# 5
LicensePlateColor.other
# 9
```

### 1.2 ResultCode

> 终端通用应答结果对应编码

| Result         | Code     |
| :--------------| ---------|
| success        | 0        |
| failure        | 1        |
| message_error  | 2        |
| not_support    | 3        |

示例:

```python
from jt_message import ResultCode

ResultCode.success
# 0
ResultCode.failure
# 1
ResultCode.message_error
# 2
ResultCode.not_support
# 3
```

## 2. 配置参数管理

### 2.1 TerminalParams

> 终端配置参数类, 用于记录终端配置参数, 并将参数值转换成协议规定的字节流数据.

#### 导入初始化

```python
from jt_message import TerminalParams

TerminalParamsObj = TerminalParams()
```

#### set_params

> 设置配置参数与参数值

参数:

|参数|类型|说明|
|:---|---|---|
|param_id|INT|参数ID|
|param_value|tuple|参数值, 不同的参数ID, 传入的参数值数量不一致, 具体参数id对应参数值见下表|

参数ID对应参数值

|参数ID|参数值|参数值类型|描述及要求|
|---|---|---|---|
|0x0001|(value,)|(int,)|终端心疼发送时间间隔, 单位秒(s)|
|0x0002|(value,)|(int,)|TCP消息应答超时时间, 单位秒(s)|
|0x0003|(value,)|(int,)|TCP消息重传次数|
|0x0004|(value,)|(int,)|UDP消息应答超时时间, 单位秒(s)|
|0x0005|(value,)|(int,)|UDP消息重传次数|
|0x0006|(value,)|(int,)|SMS消息应答超时时间, 单位秒(s)|
|0x0007|(value,)|(int,)|SMS消息重传次数|
|0x0010|(value,)|(str,)|主服务器APN, 无线通信拨号访问点, 若网络制式为CDMA, 则该处为PPP拨号号码|
|0x0011|(value,)|(str,)|主服务器无线通信拨号用户名|
|0x0012|(value,)|(str,)|主服务器无线通信拨号密码|
|0x0013|(value,)|(str,)|JT/T808--2019:<br>主服务器地址, IP或域名, 以冒号分隔主机和端口, 多个服务器使用半角分号分隔<br>JT/T808--2013:<br>主服务器地址, IP或域名|
|0x0014|(value,)|(str,)|备份服务器APN|
|0x0015|(value,)|(str,)|备份服务器无线通信拨号用户名|
|0x0016|(value,)|(str,)|备份服务器无线通信拨号密码|
|0x0017|(value,)|(str,)|JT/T808--2019:<br>备份服务器地址, IP或域名, 以冒号分隔主机和端口, 多个服务器使用半角分号分隔<br>JT/T808--2013:<br>备份服务器地址, IP或域名|
|0x0018|(value,)|(int,)|JT/T808--2013:服务器TCP端口<br>JT/T808--2019:合并至0x0013|
|0x0019|(value,)|(int,)|JT/T808--2013:服务器UDP端口<br>JT/T808--2019:合并至0x0013|
|0x001A|(value,)|(str,)|道路运输证IC卡认证主服务器IP地址或域名|
|0x001B|(value,)|(int,)|道路运输证IC卡认证主服务器TCP端口|
|0x001C|(value,)|(int,)|道路运输证IC卡认证主服务器UDP端口|
|0x001D|(value,)|(str,)|道路运输证IC卡认证备份服务器IP地址或域名, 端口同主服务器端口|
|0x0020|(value,)|(int,)|位置汇报策略, 0: 定时汇报; 1: 定距汇报; 2: 定时和定距汇报|
|0x0021|(value,)|(int,)|位置汇报方案, 0: 根据ACC状态; 1: 根据登录状态和ACC状态, 先判断登录状态, 若登录再根据ACC状态|
|0x0022|(value,)|(int,)|驾驶员未登录汇报时间间隔, 单位为秒(s)>0|
|0x0023|(value,)|(str,)|从服务器APN。该值为空时, 终端应使用主服务器相同配置|
|0x0024|(value,)|(str,)|从服务器无线通信拨号用户名。该值为空时, 终端应使用主服务器相同配置|
|0x0025|(value,)|(str,)|从服务器无线通信拨号密码。该值为空时, 终端应使用主服务器相同配置|
|0x0026|(value,)|(str,)|从服务器备份地址、IP或域名, 主机和端口用冒号分割, 多个服务器使用分号分割|
|0x0027|(value,)|(int,)|休眠时汇报时间间隔, 单位为秒(s)>0|
|0x0028|(value,)|(int,)|紧急报警时汇报时间间隔, 单位为秒(s)>0|
|0x0029|(value,)|(int,)|缺省时间汇报间隔, 单位为秒(s)>0|
|0x002C|(value,)|(int,)|缺省距离汇报间隔, 单位为米(m)>0|
|0x002D|(value,)|(int,)|驾驶员未登录汇报距离间隔, 单位为米(m)>0|
|0x002E|(value,)|(int,)|休眠时汇报距离间隔, 单位为米(m)>0|
|0x002F|(value,)|(int,)|紧急报警时汇报距离间隔, 单位为米(m)>0|
|0x0030|(value,)|(int,)|拐点补传角度, <180°|
|0x0031|(value,)|(int,)|电子围栏半径(非法位移阈值), 单位为米(v)|
|0x0032|(start_hour, start_minute, end_hour, end_minute)|(int, int, int, int)|违规行驶时段范围, 精确到分。<br>start_hour: 违规行驶开始时间的小时部分; <br>start_minute: 违规行驶开始时间的分钟部分; <br>end_hour: 违规行驶结束时间的小时部分; <br>end_minute: 违规行驶结束时间的分钟部分; <br>示例: (22, 50, 10, 30), 表示当天晚上10点50分到第二天早上10点30分属于违规行驶时段|
|0x0040|(value,)|(str,)|监控平台电话号码|
|0x0041|(value,)|(str,)|复位电话号码, 可采用此电话号码拨打终端电话让终端复位|
|0x0042|(value,)|(str,)|恢复出厂设置电话号码, 可采用此电话号码拨打终端电话让终端恢复出厂设置|
|0x0043|(value,)|(str,)|监控平台 SMS 电话号码|
|0x0044|(value,)|(str,)|接收终端 SMS 文本报警号码|
|0x0045|(value,)|(int,)|终端电话接听策略, 0: 自动接听; 1: ACC ON 时自动接听, OFF 时手动接听|
|0x0046|(value,)|(int,)|每次最长通话时间, 单位为秒(s), 0 为不允许通话, 0xFFFFFFFF 为不限制|
|0x0047|(value,)|(int,)|当月最长通话时间, 单位为秒(s), 0 为不允许通话, 0xFFFFFFFF 为不限制|
|0x0048|(value,)|(str,)|监听电话号码|
|0x0049|(value,)|(str,)|监管平台特权短信号码|
|0x0050|(value,)|(int,)|报警屏蔽字。与位置信息汇报消息中的报警标志相对应, 相应位为 1 则相应报警被屏蔽|
|0x0051|(value,)|(int,)|报警发送文本 SMS 开关, 与位置信息汇报消息中的报警标志相对应, 相应位为 1 则相应报警时发送文本 SMS|
|0x0052|(value,)|(int,)|报警拍摄开关, 与位置信息汇报消息中的报警标志相对应, 相应位为 1 则相应报警时摄像头拍摄|
|0x0053|(value,)|(int,)|报警拍摄存储标志, 与位置信息汇报消息中的报警标志相对应, 相应位为 1 则对相应报警时牌的照片进行存储, 否则实时长传|
|0x0054|(value,)|(int,)|关键标志, 与位置信息汇报消息中的报警标志相对应, 相应位为 1 则对相应报警为关键报警|
|0x0055|(value,)|(int,)|最高速度, 单位为公里每小时(km/h)|
|0x0056|(value,)|(int,)|超速持续时间, 单位为秒(s)|
|0x0057|(value,)|(int,)|连续驾驶时间门限, 单位为秒(s)|
|0x0058|(value,)|(int,)|当天累计驾驶时间门限, 单位为秒(s)|
|0x0059|(value,)|(int,)|最小休息时间, 单位为秒(s)|
|0x005A|(value,)|(int,)|最长停车时间, 单位为秒(s)|
|0x005B|(value,)|(int,)|超速预警差值, 单位为1/10千米每小时(1/10km/h)|
|0x005C|(value,)|(int,)|疲劳驾驶预警差值, 单位为秒(s), 值大于零|
|0x005D|(millisecond, acceleration)|(int, int)|碰撞报警参数设置: <br>millisecond: 为碰撞时间, 单位为毫秒(ms); <br>acceleration: 为碰撞加速度, 单位为0.1g; 设置范围为0~79, 默认为10.|
|0x005E|(value,)|(int,)|侧翻报警参数设置: 侧翻角度, 单位为度(°), 默认为30°|
|0x0064|(camera_1_onoff, camera_2_onoff, camera_3_onoff, camera_4_onoff, camera_5_onoff, camera_1_storage, camera_2_storage, camera_3_storage, camera_4_storage, camera_5_storage, unit, interval)|(int, int, int, int, int, int, int, int, int, int, int, int)|定时拍照控制: <br>camera_1_onoff: 摄像通道1定时开关标志, 0 - 关, 1 - 开;<br>camera_2_onoff: 摄像通道2定时开关标志, 0 - 关, 1 - 开;<br>camera_3_onoff: 摄像通道3定时开关标志, 0 - 关, 1 - 开;<br>camera_4_onoff: 摄像通道4定时开关标志, 0 - 关, 1 - 开;<br>camera_5_onoff: 摄像通道5定时开关标志, 0 - 关, 1 - 开;<br>camera_1_storage: 摄像通道1定时存储标志, 0 - 存储, 1 - 上传;<br>camera_2_storage: 摄像通道2定时存储标志, 0 - 存储, 1 - 上传;<br>camera_3_storage: 摄像通道3定时存储标志, 0 - 存储, 1 - 上传;<br>camera_4_storage: 摄像通道4定时存储标志, 0 - 存储, 1 - 上传;<br>camera_5_storage: 摄像通道5定时存储标志, 0 - 存储, 1 - 上传;<br>unit: 定时时间单位: 0 - 秒(s), 当数值小于5s时, 终端按5秒处理; 1 - 分(m);<br>interval: 定时时间间隔, 收到参数设置或重新启动后执行;|
|0x0065|(camera_1_onoff, camera_2_onoff, camera_3_onoff, camera_4_onoff, camera_5_onoff, camera_1_storage, camera_2_storage, camera_3_storage, camera_4_storage, camera_5_storage, unit, interval)|(int, int, int, int, int, int, int, int, int, int, int, int)|定距拍照控制: <br>camera_1_onoff: 摄像通道1定时开关标志, 0 - 关, 1 - 开;<br>camera_2_onoff: 摄像通道2定时开关标志, 0 - 关, 1 - 开;<br>camera_3_onoff: 摄像通道3定时开关标志, 0 - 关, 1 - 开;<br>camera_4_onoff: 摄像通道4定时开关标志, 0 - 关, 1 - 开;<br>camera_5_onoff: 摄像通道5定时开关标志, 0 - 关, 1 - 开;<br>camera_1_storage: 摄像通道1定时存储标志, 0 - 存储, 1 - 上传;<br>camera_2_storage: 摄像通道2定时存储标志, 0 - 存储, 1 - 上传;<br>camera_3_storage: 摄像通道3定时存储标志, 0 - 存储, 1 - 上传;<br>camera_4_storage: 摄像通道4定时存储标志, 0 - 存储, 1 - 上传;<br>camera_5_storage: 摄像通道5定时存储标志, 0 - 存储, 1 - 上传;<br>unit: 定距距离单位: 0 - 米(m), 当数值小于100m时, 终端按100m处理; 1 - 千米(km);<br>interval: 定距距离间隔, 收到参数设置或重新启动后执行;|
|0x0070|(value,)|(int,)|图像/视频质量, 1-10, 1 最优质量|
|0x0071|(value,)|(int,)|亮度, 设置范围 0-255|
|0x0072|(value,)|(int,)|对比度, 设置范围 0-127|
|0x0073|(value,)|(int,)|饱和度, 设置范围 0-127|
|0x0074|(value,)|(int,)|色度, 设置范围 0-255|
|0x0080|(value,)|(int,)|车辆里程表读数, 1/10km|
|0x0081|(value,)|(int,)|车辆所在的省域 ID|
|0x0082|(value,)|(int,)|车辆所在的市域 ID|
|0x0083|(value,)|(str,)|公安交通管理部门颁发的机动车号牌|
|0x0084|(value,)|(int,)|车牌颜色, 按照 JT/T697.7--2014 中的规定, 未上车牌车辆填0|
|0x0090|(gps_onoff, bds_onoff, glonass_onoff, galileo_onoff)|(int, int, int, int)|GNSS定位模式, 定义如下: <br>gps_onoff: 0 - 禁用GPS定位, 1 - 启用GPS定位, <br>bds_onoff: 0 - 禁用北斗定位, 1 - 启用北斗定位; <br>glonass_onoff: 0 - 禁用GLONASS定位, 1 - 启用GLONASS定位; <br>galileo_onoff: 0 - 禁用Galileo定位, 1 - 启用Galileo定位; |
|0x0091|(value,)|(int,)|GNSS波特率, 定义如下: <br>0x00 - 4800; <br>0x01 - 9600; <br>0x02 - 19200; <br>0x03 - 38400; <br>0x04 - 57600; <br>0x05 - 115200;|
|0x0092|(value,)|(int,)|GNSS模块详细定位数据输出频率, 定义如下: <br>0x00 - 500ms; <br>0x01 - 1000ms(默认值); <br>0x02 - 2000ms; <br>0x03 - 3000ms; <br>0x04 - 4000ms;|
|0x0093|(value,)|(int,)|GNSS模块详细定位数据采集频率, 单位为秒(s), 默认为1|
|0x0094|(value,)|(int,)|GNSS模块详细定位数据上传方式: <br>0x00 - 本地存储, 不上传(默认值); <br>0x01 - 按时间间隔上传; <br>0x02 - 按距离间隔上传; <br>0x0B - 按累计时间上传, 达到传输时间后自动停止上传; <br>0x0C - 按累计距离上传, 达到距离后自动停止上传; <br>0x0D - 按累计条数上传, 达到上传条数后自动停止上传; |
|0x0095|(value,)|(int,)|GNSS模块详细定位数据上传设置: <br>上传方式为0x01时, 单位为秒(s); <br>上传方式为0x02时, 单位为米(m); <br>上传方式为0x0B时, 单位为秒(s); <br>上传方式为0x0C时, 单位为米(m); <br>上传方式为0x0D时, 单位为条;|
|0x0100|(value,)|(int,)|CAN总线通道1采集时间间隔, 单位为毫秒(ms), 0表示不采集|
|0x0101|(value,)|(int,)|CAN总线通道1上传时间间隔, 单位为秒(s), 0表示不上传|
|0x0102|(value,)|(int,)|CAN总线通道2采集时间间隔, 单位为毫秒(ms), 0表示不采集|
|0x0103|(value,)|(int,)|CAN总线通道2上传时间间隔, 单位为秒(s), 0表示不上传|
|0x0110|(can_bus_id, collection_method, frame_type, can_channel_no, collection_time_interval)|(int, int, int, int, int)|CAN总线ID单独采集设置: <br>collection_time_interval表示此ID采集时间间隔(ms), 0表示不采集; <br>can_channel_no表示CAN通道号, 0: CAN1, 1: CAN2; <br>frame_type表示帧类型, 0: 标准帧, 1: 扩展帧; <br>collection_method表示数据采集方式, 0: 原始数据, 1: 采集区间计算值; <br>can_bus_id表示CAN总线ID|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
TerminalParamsObj.set_params(0x0001, *(60,))
TerminalParamsObj.set_params(0x0013, *("127.0.0.1:8001;127.0.0.1:8002",))
TerminalParamsObj.set_params(0x0032, *(22, 50, 10, 30))
```

#### get_params

> 获取设置好的终端配置参数

返回值:

|数据类型|说明|
|:---|---|
|DICT|key: 参数ID, <br>value: 参数值字典<br> - key: `value`, value: int/str数值, <br> - key: `hex`, value: 字符串十六进制数据, 用于消息发送|

示例:

```python
params_data = TerminalParamsObj.get_params()
print(params_data):
# {1: {'value': 60, 'hex': '0000003C'}, 50: {'value': (22, 50, 10, 30), 'hex': '1632A1E'}, 19: {'value': '127.0.0.1:8001;127.0.0.1:8002', 'hex': '3132372E302E302E313A383030313B3132372E302E302E313A38303032'}}
```

#### del_params

> 删除配置参数

参数:

|参数|类型|说明|
|:---|---|---|
|param_id|INT|参数ID|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
TerminalParamsObj.del_params(0x0001)
```

### 2.2 LocStatusConfig

> 定位状态信息配置

定位状态信息表

|编码|数据类型|说明|
|---|---|---|
|acc_onoff|int|ACC开关状态: 0 - 关, 1 - 开|
|loc_status|int|是否定位: 0 - 未定位, 1 - 定位|
|NS_latitude|int|纬度方向: 0 - 北纬, 1 - 南纬|
|EW_longitude|int|经度方向: 0 - 东经, 1 - 西经|
|operational_status|int|运营状态: 0 - 运营, 1 - 停运|
|long_lat_encryption|int|经纬度是否保密插件加密: 0 - 未加密, 1 - 加密|
|forward_collision_warning|int|0 - 无, 1 - 紧急刹车系统采集的前撞预警|
|lane_departure_warning|int|0 - 无, 1 - 车道偏移预警|
|load_status|int|车辆装载状态: 0x00 - 空车, 0x01 - 半载, 0x10 - 保留, 0x11 - 满载. 可标识客车的空载状态, 重车及货车的空载, 满载状态, 该状态可由人工输入或传感器获取.|
|vehicle_oil_status|int|车辆油路状态: 0 - 正常, 1 - 断开|
|vehicle_circuit_status|int|车辆电路状态: 0 - 正常, 1 - 断开|
|door_lock|int|车门锁定状态: 0 - 解锁, 1 - 加锁|
|door_1_status|int|门1状态: 0 - 关, 1 - 开|
|door_2_status|int|门2状态: 0 - 关, 1 - 开|
|door_3_status|int|门3状态: 0 - 关, 1 - 开|
|door_4_status|int|门4状态: 0 - 关, 1 - 开|
|door_5_status|int|门5状态: 0 - 关, 1 - 开|
|gps_onoff|int|是否使用GPS卫星进行定位: 0 - 否, 1 - 是|
|bds_onoff|int|是否使用北斗卫星进行定位: 0 - 否, 1 - 是|
|glonass_onoff|int|是否使用GLONASS卫星进行定位: 0 - 否, 1 - 是|
|galileo_onoff|int|是否使用Galileo卫星进行定位: 0 - 否, 1 - 是|
|running_status|int|车辆状态: 0 - 停止状态, 1 - 行驶状态|

#### 导入初始化

```python
from usr.jt_message import LocStatusConfig

LocStatusConfigObj = LocStatusConfig()
```

#### set_config

> 设置指定定位状态配置信息

参数:

|参数|类型|说明|
|:---|---|---|
|name|STR| 编码, 详见`定位状态信息表` |
|value|INT| 参数值, 详见`定位状态信息表`, 所有数据全部默认0 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
LocStatusConfigObj.set_config("acc_onoff", 1)
# True
LocStatusConfigObj.set_config("loc_status", 1)
# True
```

#### get_config

> 获取指定定位状态配置信息值

参数:

|参数|类型|说明|
|:---|---|---|
|name|STR| 编码, 详见`定位状态信息表` |

返回值:

|数据类型|说明|
|:---|---|
|INT|具体含义见`定位状态信息表`|

示例:

```python
acc_onoff = LocStatusConfigObj.get_config("acc_onoff")
print(acc_onoff)
# 1
loc_status = LocStatusConfigObj.get_config("loc_status")
print(loc_status)
# 1
```

#### value

> 获取所有定位状态配置信息, 已根据协议转换成整数, 用于定位信息上报接口

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|INT|整数数值|

示例:

```python
loc_status_cfg = LocStatusConfigObj.value()
print(loc_status_cfg)
# 3
```

### 2.3 LocAlarmWarningConfig

> 定位告警参数配置

定位告警参数项列表

|告警编码|定义|处理说明|
|---|---|---|
|emergency_alarm|1:紧急报警, 触动报警开关后触发|收到应答后清零|
|over_speed_alarm|1:超速报警|标志维持至报警条件接触|
|fatigue_driving_alarm|1:疲劳驾驶报警|标志维持至报警条件接触|
|dangerous_driving_behaviour_alarm|1:危险驾驶行为报警|标志维持至报警条件接触|
|gnss_module_failure_alarm|1:GNSS模块发送故障报警|标志维持至报警条件接触|
|gnss_antenna_disconnection_alarm|1:GNSS天线未接或被剪短报警|标志维持至报警条件接触|
|gnss_antenna_short_circuit_alarm|1:GNSS天线短路报警|标志维持至报警条件接触|
|terminal_main_power_supply_undervoltage_alarm|1:终端主电源欠压报警|标志维持至报警条件接触|
|terminal_main_power_failure_alarm|1:终端主电源掉电报警|标志维持至报警条件接触|
|terminal_lcd_or_display_failure_alarm|1:终端LCD或显示器报警|标志维持至报警条件接触|
|tts_module_fault_alarm|1:TTS模块故障报警|标志维持至报警条件接触|
|camera_failure_alarm|1:摄像头故障报警|标志维持至报警条件接触|
|road_transport_license_ic_card_module_fault_alarm|1:道路运输证IC卡模块故障报警|标志维持至报警条件接触|
|over_speed_warning|1:超速预警|标志维持至报警条件接触|
|fatigue_driving_warning|1:疲劳驾驶预警|标志维持至报警条件接触|
|illegal_driving_alarm|1:违规形式报警|标志维持至报警条件接触|
|tire_pressure_warning|1:胎压预警|标志维持至报警条件接触|
|right_turn_blind_spot_abnormal_alarm|1:右转盲区异常报警|标志维持至报警条件接触|
|cumulative_driving_overtime_alarm_for_the_day|1:当天累计驾驶超时报警|标志维持至报警条件接触|
|overtime_parking_alarm|1:超时停车报警|标志维持至报警条件接触|
|in_and_out_of_the_area_alarm|1:进出区域报警|收到应答后清零|
|entry_and_exit_route_alarm|1:进出路线报警|收到应答后清零|
|insufficient_or_too_long_driving_time_on_the_road_section_alarm|1:路段行驶时间不足/过长报警|收到应答后清零|
|route_departure_alarm|1:路线偏离报警|标志维持至报警条件接触|
|vehicle_vss_failure_alarm|1:车辆VSS故障报警|标志维持至报警条件接触|
|vehicle_fuel_abnormality_alarm|1:车辆油量异常报警|标志维持至报警条件接触|
|vehicle_theft_alarm|1:车辆被盗报警(通过车辆防盗器)|标志维持至报警条件接触|
|vehicle_illegal_ignition_alarm|1:车辆非法点火报警|收到应答后清零|
|vehicle_illegal_displacement_alarm|1:车辆非法位移报警|收到应答后清零|
|collision_rollover_alarm|1:碰撞侧翻报警|标志维持至报警条件接触|
|rollover_alarm|1:侧翻报警|标志维持至报警条件接触|
|illegal_door_opening_alarm|1:非法开门报警(终端未设置区域时, 不判断非法开门)(JT/T808--2013)|收到应答后清零|

#### 导入初始化

```python
from jt_message import LocAlarmWarningConfig

LocAlarmWarningConfigObj = LocAlarmWarningConfig()
```

#### set_alarm

> 设置指定报警参数配置

参数:

|参数|类型|说明|
|:---|---|---|
|name|STR| 告警编码 |
|onoff|INT| 告警触发: 0 - off, 1 - on, 默认0|
|shield_switch|INT| 终端参数报警屏蔽字: 0 - off, 1 - on, 默认0|
|sms_switch|INT| 终端参数报警发送文本SMS开关: 0 - off, 1 - on, 默认0|
|shoot_switch|INT| 终端参数报警拍摄开关: 0 - off, 1 - on, 默认0|
|shoot_store|INT| 终端参数报警拍摄存储标志: 0 - live upload, 1 - local store, 默认1|
|key_sign|INT| 终端参数关键标志: 0 - not key alarm, 1 - key alarm, 默认0|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
name = "over_speed_alarm"
onoff = 1
shield_switch = 1
sms_switch = 1
shoot_switch = 1
shoot_store = 1
key_sign = 1
LocAlarmWarningConfigObj.set_alarm(name, onoff, shield_switch, sms_switch, shoot_switch, shoot_store, key_sign)
```

#### get_alarm

> 获取指定报警参数配置

参数:

|参数|类型|说明|
|:---|---|---|
|name|STR| 告警编码 |

返回值:

|数据类型|说明|
|:---|---|
|TUPLE|(onoff, shield_switch, sms_switch, shoot_switch, shoot_store, key_sign)<br>onoff - 告警触发<br>shield_switch - 报警屏蔽字<br>sms_switch报警发送文本SMS开关<br>shoot_switch - 报警拍摄开关<br>shoot_store - 报警拍摄存储标志<br>key_sign - 关键标志|

示例:

```python
name = "over_speed_alarm"
alarm_cfg = LocAlarmWarningConfigObj.get_alarm(name)
print(alarm_cfg)
# (1, 1, 1, 1, 1, 1)
```

#### value

> 获取终端完整告警配置数据

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|TUPLE|(onoff, shield_switch, sms_switch, shoot_switch, shoot_store, key_sign)<br>onoff - 告警触发<br>shield_switch - 报警屏蔽字<br>sms_switch报警发送文本SMS开关<br>shoot_switch - 报警拍摄开关<br>shoot_store - 报警拍摄存储标志<br>key_sign - 关键标志|

示例:

```python
alarms_cfg = LocAlarmWarningConfigObj.value()
print(alarms_cfg)
# (2, 2, 2, 2, 65535, 2)
```

### 2.4 LocAdditionalInfoConfig

> 定位附加信息配置

#### 导入初始化

```python
from jt_message import LocAdditionalInfoConfig

LocAdditionalInfoConfigObj = LocAdditionalInfoConfig()
```

#### set_mileage

> 设置车辆里程数, 单位km, 对应车辆里程表读数

参数:

|参数|类型|说明|
|:---|---|---|
|value|int| 车辆里程表读数, 单位km |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
LocAdditionalInfoConfigObj.set_mileage(101)
```

#### get_mileage

> 获取设置的车辆里程数

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|int| 车辆里程表数, 单位km, 参数未设置返回-1|

示例:

```python
mileage = LocAdditionalInfoConfigObj.get_mileage()
print(mileage)
# 101
```

#### set_oil_quantity

> 设置油量, 单位L, 对应车辆油量表读数

参数:

|参数|类型|说明|
|:---|---|---|
|value|int| 车辆油量表读数, 单位L |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
LocAdditionalInfoConfigObj.set_oil_quantity(50)
```

#### get_oil_quantity

> 获取设置的车辆油量数

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|int| 车辆油量表数, 单位L, 参数未设置返回-1 |

示例:

```python
oil_quantity = LocAdditionalInfoConfigObj.get_oil_quantity()
print(oil_quantity)
# 50
```

#### set_speed

> 设置车速, 单位km/h, 形式记录功能获取的速度。

参数:

|参数|类型|说明|
|:---|---|---|
|value|int| 车辆车速, 单位km/h |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
LocAdditionalInfoConfigObj.set_speed(60)
```

#### get_speed

> 获取设置的车辆车速

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|int| 车辆车速, 单位km/h, 参数未设置返回-1 |

示例:

```python
speed = LocAdditionalInfoConfigObj.get_speed()
print(speed)
# 60
```

#### set_manually_confirm_the_alarm_event_id

> 设置需要人工确认的报警事件的ID

参数:

|参数|类型|说明|
|:---|---|---|
|value|int| 报警事件ID |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
LocAdditionalInfoConfigObj.set_manually_confirm_the_alarm_event_id(10)
```

#### get_manually_confirm_the_alarm_event_id

> 获取设置的需要人工确认的报警事件的ID

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|int| 报警事件ID, 参数未设置返回-1 |

示例:

```python
alarm_event_id = LocAdditionalInfoConfigObj.get_manually_confirm_the_alarm_event_id()
print(alarm_event_id)
# 10
```

#### set_tire_pressure

> 设置车辆胎压, 单位Pa, 标定轮子的顺序为从车头开始从左到右顺序排列, 例如: 前左1, 前左2, 前右1, 前右2, 中左1, 中左2, 中左3, 中右1, 中右2, 中右3, 后左1, 后左2, 后左3..., 以此类推。

参数:

|参数|类型|说明|
|:---|---|---|
|values|list| 元素为车辆胎压, 单位Pa, 最大254, 超过254以254存储 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
values = [240, 240, 235, 230]
LocAdditionalInfoConfigObj.set_tire_pressure(values)
```

#### get_tire_pressure

> 获取设置的车辆胎压

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|list| 元素为车辆胎压, 单位Pa, 参数未设置返回-1 |

示例:

```python
tire_pressure = LocAdditionalInfoConfigObj.get_tire_pressure()
print(tire_pressure)
# [240, 240, 235, 230]
```

#### set_temperature

> 设置车厢温度, 单位摄氏度, 取值范围-32767~32767

参数:

|参数|类型|说明|
|:---|---|---|
|value|int| 车厢温度, 单位摄氏度 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
LocAdditionalInfoConfigObj.set_temperature(25)
```

#### get_temperature

> 获取设置的车厢温度

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|int| 车厢温度, 单位摄氏度, 参数未设置返回-1 |

示例:

```python
temperature = LocAdditionalInfoConfigObj.get_temperature()
print(temperature)
# 25
```

#### set_over_speed_alarm

> 设置超速报警附加信息

参数:

|参数|类型|说明|
|:---|---|---|
|loc_type|int| 位置类型:<br>0 - 无特定位置;<br>1 - 圆形区域;<br>2 - 矩形区域;<br>3 - 多边形区域;<br>4 - 路段; |
|area_segment_id|int| 区域或路段ID, 若位置类型为0, 该字段不传, 不为0, 则该字段必传 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
loc_type = 2
area_segment_id = 5
LocAdditionalInfoConfigObj.set_over_speed_alarm(loc_type, area_segment_id)
```

#### get_over_speed_alarm

> 获取设置的超速报警附加信息

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|dict| `loc_type` - 位置类型, `area_segment_id` - 区域或路段ID, 位置类型为0, 该key对应的value值为None; 参数未设置返回空字典 |

示例:

```python
over_speed_alarm = LocAdditionalInfoConfigObj.get_over_speed_alarm()
print(over_speed_alarm)
# {"loc_type": 2, "area_segment_id": 5}
```

#### set_in_out_area_segment_alarm

> 设置进出区域/路线报警附加信息

参数:

|参数|类型|说明|
|:---|---|---|
|loc_type|int| 位置类型:<br>1 - 圆形区域;<br>2 - 矩形区域;<br>3 - 多边形区域;<br>4 - 路段; |
|area_segment_id|int| 区域或路段ID |
|direction|int| 方向, 0 - 进; 1 - 出 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
loc_type = 2
area_segment_id = 5
direction = 1
LocAdditionalInfoConfigObj.set_in_out_area_segment_alarm(loc_type, area_segment_id, direction)
```

#### get_in_out_area_segment_alarm

> 获取设置的进出区域/路线报警附加信息

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|dict| `loc_type` - 位置类型, `area_segment_id` - 区域或路段ID, `direction` - 方向; 参数未设置返回空字典 |

示例:

```python
in_out_area_segment_alarm = LocAdditionalInfoConfigObj.get_in_out_area_segment_alarm()
print(in_out_area_segment_alarm)
# {"loc_type": 2, "area_segment_id": 5, "direction": 1}
```

#### set_insufficient_or_too_long_driving_time

> 设置路段行驶时间不足或过长报警附加信息

参数:

|参数|类型|说明|
|:---|---|---|
|road_id|int| 路段ID; |
|travel_time|int| 路段行驶时间, 单位s |
|result|int| 结果, 0 - 不足; 1 - 过长 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
road_id = 2
travel_time = 5
result = 1
LocAdditionalInfoConfigObj.set_insufficient_or_too_long_driving_time(road_id, travel_time, result)
```

#### get_insufficient_or_too_long_driving_time

> 获取设置的路段行驶时间不足或过长报警附加信息

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|dict| `road_id` - 路段ID, `travel_time` - 路段行驶时间, `result` - 结果; 参数未设置返回空字典 |

示例:

```python
insufficient_or_too_long_driving_time = LocAdditionalInfoConfigObj.get_insufficient_or_too_long_driving_time()
print(insufficient_or_too_long_driving_time)
# {"road_id": 2, "travel_time": 5, "result": 1}
```

#### set_vehicle_signal_status

> 设置扩展车辆信号状态位

参数:

|参数|类型|说明|
|:---|---|---|
|low_beam_lights|int|近光灯信号 0 - off, 1 - on|
|high_beam|int|远光灯信号 0 - off, 1 - on|
|right_turn|int|右转向灯信号 0 - off, 1 - on|
|left_turn|int|左转向灯信号 0 - off, 1 - on|
|brake|int|制动信号 0 - off, 1 - on|
|reverse|int|倒挡信号 0 - off, 1 - on|
|fog_light|int|雾灯信号 0 - off, 1 - on|
|position|int|示廓灯 0 - off, 1 - on|
|horn|int|喇叭信号 0 - off, 1 - on|
|air_conditioning|int|空调状态 0 - off, 1 - on|
|neutral|int|空挡信号 0 - off, 1 - on|
|retarder|int|缓速器工作 0 - off, 1 - on|
|abs_work|int|ABS工作 0 - off, 1 - on|
|heating|int|加热器工作 0 - off, 1 - on|
|clutch|int|离合器工作 0 - off, 1 - on|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
low_beam_lights = 1
high_beam = 1
right_turn = 1
left_turn = 1
brake = 1
reverse = 1
fog_light = 1
position = 1
horn = 1
air_conditioning = 1
neutral = 1
retarder = 1
abs_work = 1
heating = 1
clutch = 1
LocAdditionalInfoConfigObj.set_vehicle_signal_status(
    low_beam_lights, high_beam, right_turn, left_turn, brake,
    reverse, fog_light, position, horn, air_conditioning,
    neutral, retarder, abs_work, heating, clutch
)
```

#### get_vehicle_signal_status

> 获取设置的扩展车辆信号状态位

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|dict| low_beam_lights - 近光灯信号<br>high_beam - 远光灯信号<br>right_turn - 右转向灯信号<br>left_turn - 左转向灯信号<br>brake - 制动信号<br>reverse - 倒挡信号<br>fog_light - 雾灯信号<br>position - 示廓灯<br>horn - 喇叭信号<br>air_conditioning - 空调状态<br>neutral - 空挡信号<br>retarder - 缓速器工作<br>abs_work - ABS工作<br>heating - 加热器工作<br>clutch - 离合器工作; 参数未设置返回空字典 |

示例:

```python
vehicle_signal_status = LocAdditionalInfoConfigObj.get_vehicle_signal_status()
print(vehicle_signal_status)
# {"low_beam_lights": 1, "high_beam": 1, "right_turn": 1, "left_turn": 1, "brake": 1, "reverse": 1, "fog_light": 1, "position": 1, "horn": 1, "air_conditioning": 1, "neutral": 1, "retarder": 1, "abs_work": 1, "heating": 1, "clutch": 1}
```

#### set_io_status

> 设置IO状态位

参数:

|参数|类型|说明|
|:---|---|---|
|deep_sleep|int| 深度休眠状态, 0 - off, 1 - on |
|sleep|int| 休眠状态, 0 - off, 1 - on |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
deep_sleep = 1
sleep = 1
LocAdditionalInfoConfigObj.set_io_status(deep_sleep, sleep)
```

#### get_io_status

> 获取设置的IO状态位

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|dict| `deep_sleep` - 深度休眠状态, `sleep` - 休眠状态; 参数未设置返回空字典 |

示例:

```python
io_status = LocAdditionalInfoConfigObj.get_io_status()
print(io_status)
# {"deep_sleep": 1, "sleep": 1}
```

#### set_analog

> 设置模拟量

参数:

|参数|类型|说明|
|:---|---|---|
|ad0|int| AD0 |
|ad1|int| AD1 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
ad0 = 1
ad1 = 1
LocAdditionalInfoConfigObj.set_analog(ad0, ad1)
```

#### get_analog

> 获取设置的模拟量

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|dict| `ad0` - AD0, `ad1` - AD1; 参数未设置返回空字典 |

示例:

```python
analog = LocAdditionalInfoConfigObj.get_analog()
print(analog)
# {"ad0": 1, "ad1": 1}
```

#### set_wireless_communication_network_signal_strength

> 设置无线通信网络信号强度

参数:

|参数|类型|说明|
|:---|---|---|
|value|int| 无线通信网络信号强度 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
LocAdditionalInfoConfigObj.set_wireless_communication_network_signal_strength(31)
```

#### get_wireless_communication_network_signal_strength

> 获取设置的无线通信网络信号强度

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|int| 无线通信网络信号强度; 参数未设置返回-1 |

示例:

```python
wireless_communication_network_signal_strength = LocAdditionalInfoConfigObj.get_wireless_communication_network_signal_strength()
print(wireless_communication_network_signal_strength)
# 31
```

#### set_number_of_satellites

> 设置GNSS定位卫星数

参数:

|参数|类型|说明|
|:---|---|---|
|value|int| GNSS定位卫星数 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
LocAdditionalInfoConfigObj.set_number_of_satellites(12)
```

#### get_number_of_satellites

> 获取设置的GNSS定位卫星数

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|int| GNSS定位卫星数; 参数未设置返回-1 |

示例:

```python
number_of_satellites = LocAdditionalInfoConfigObj.get_number_of_satellites()
print(number_of_satellites)
# 12
```

#### value

> 定位附加信息转换协议格式数据, 用于定位信息上报接口

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|str| 定位附加信息转换协议格式数据 |

示例:

```python
loc_additional_info = LocAdditionalInfoConfigObj.value()
print(loc_additional_info)
# 0104000003e80202014503020000
```

## 3. JT/T808终端功能接口

### JTT808

> - 该模块实现了JT/T808设备端连接服务端进行数据交互的功能
> - 支持JT/T808--2011, JT/T808--2013, JT/T808--20119
> - 支持TCP, UDP两种通信方式

#### 导入初始化

```python
from jtt808 import JTT808

ip = "127.0.0.1"
port = 7611
domain = None
method = "TCP"
encryption = False
timeout = 30
retry_count = 3
life_time = 60
version = "2019"
client_id = "18888888888"

jtt808_obj = JTT808(
    ip=ip, port=port, domain=domain, method=method,timeout=timeout, retry_count=retry_count,
    life_time=life_time, version=version, client_id=client_id
)
```

参数:

|参数|类型|说明|
|:---|---|---|
|ip|str|服务端IP地址, 默认None, ip与domain二选一|
|port|int|服务端端口号, 默认None|
|domain|str|服务端域名地址, 默认None, domain与ip二选一|
|method|str|通信方式: TCP 或 UDP, 默认TCP|
|timeout|int|消息数据读取超时时间, 默认30秒|
|retry_count|int|消息数据发送失败重试次数, 默认3次|
|life_time|int|心跳发送周期, 默认60s|
|version|str|JTT808版本, 目前有2011, 2013, 2019三个版本, 默认2019|
|client_id|str|终端手机号, 默认空, **必填参数**|

#### set_callback

> 设置回到函数, 用于接收终端消息发送后的服务端的应答与服务端下发的消息数据

参数:

|参数|类型|说明|
|:---|---|---|
|callback|function|回调函数, 回到函数有一个形参args, args为一个字典, 有两个key值, `header`, `data`, 两个key对应的value值也为字典具体, 具体参数见下表。|、

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
def test_callback(args):
    header = args["header"]
    data = args["data"]
    print(header)
    print(data)

jtt808_obj.set_callback(test_callback)
# True
```

##### 回调函数参数`args`中`header`参数说明

|参数|类型|说明|
|:---|---|---|
|message_id|int|消息ID|
|properties|int|消息体属性|
|protocol_version|int|协议版本号|
|client_id|str|终端手机号|
|serial_no|int|消息流水号|
|package_total|int|消息包总数|
|package_no|int|包序号|

##### 回调函数参数`args`中`data`参数说明

> `data`中的参数根据`header`中的消息ID不同会有所变化, 具体详见 **4. 服务端下发消息数据**

#### set_encryption

> 设置与服务端通信加密, 需服务端下发加密公钥。
> 
> 可加密消息接口:
> 
> - `params_report`
> - `properties_report`
> - `upgrade_result_report`
> - `loction_report`
> - `event_report`
> - `issue_question_response`
> - `information_demand_cancellation`
> - `query_area_route_data_response`
> - `driving_record_data_upload`
> - `electronic_waybill_report`
> - `driver_identity_information_report`
> - `location_bulk_report`
> - `can_bus_data_upload`
> - `media_event_upload`
> - `camera_shoots_immediately_response`
> - `stored_media_data_retrieval_response`
> - `data_uplink_transparent_transmission`
> - `data_compression_report`

参数:

|参数|类型|说明|
|:---|---|---|
|encryption|bool|是否加密|
|rsa_e|int| 服务端公钥中的e, 由服务端下发, 消息ID: 0x8A00|
|rsa_n|str|服务端公钥中的n, 由服务端下发, 消息ID: 0x8A00|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
encryption = True
rsa_n = 0x010001
rsa_e = "E5A55035C17123BFAB98733E9A619152CEAA13214261BA971EE3563CCF9790FA221FDD9D582B4E14ED200173B2D9822E561E99EE54B3A812ACCDDDEAD97DF6DA682583080F7733035BF22C956F6F96ED8F3E2E8DA1DE80C38B1A18956D719DCA407EC13E0C86E40502553C418180D520E6B9A18E04E3817F9CD185769233C9CB"
set_encryption_res = jtt808_obj.set_encryption(encryption, rsa_e, rsa_n)
print(set_encryption_res)
# True
```

#### connect

> 连接服务器

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
jtt808_obj.connect()
# True
```

#### disconnect

> 断开服务器连接

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

示例:

```python
jtt808_obj.disconnect()
# True
```

#### status

> 获取设备与服务器连接状态

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|INT|-1 - 连接异常<br>0 - 已连接<br>1 - 正在连接<br>2 - 已断开连接|

示例:

```python
status = jtt808_obj.status()
# 0
```

#### register

> 终端注册

参数:

|参数|类型|说明|
|:---|---|---|
|province_id|str|省域ID, 标示终端安装车辆所在省域的ID, 0 保留, 由平台取默认值. 省域ID采用GB/T 2260中规定的行政区划代码六位中的前两位|
|city_id|str|市县域ID, 标示终端安装车辆所在市县域的ID, 0 保留, 由平台取默认值. 市县域ID采用GB/T 2260中规定的行政区划代码六位中的后四位|
|manufacturer_id|str|制造商ID, 由车载终端厂商所在地行政区划代码和制造商ID组成, 长度不超过11个字节|
|terminal_model|str|终端型号, 由制造商自行定义, 长度不超过30个字节|
|terminal_id|str|终端ID, 由大写字母和数字组成, 此终端ID由制造商自行定义|
|license_plate_color|int|车牌颜色, 按照JT/T 697.7--2014 中的规定, 未上车牌车辆填0, 可使用`LicensePlateColor`类中的枚举值|
|license_plate|str|公安交通管理部门颁发的机动车号牌, 如果车辆未上牌则填写车架号|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|终端注册消息流水号|
|registration_result|int|注册结果:<br>0 - 成功<br>1 - 车辆已被注册<br>2 - 数据库中无该车辆<br>3 - 终端已被注册<br>4 - 数据库中无该终端|
|auth_code|str|鉴权码, 注册结果为成功时, 该字段才有效|

示例:

```python
import modem

province_id = "34"
city_id = "0100"
manufacturer_id = "quectel"
terminal_model = "EC200U-CNAA"
terminal_id = modem.getDevImei()
license_plate_color = LicensePlateColor.blue
license_plate = "皖A88888"

register_res = jtt808_obj.register(province_id, city_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, license_plate)
print(register_res)
# {"serial_no": 1, "registration_result": 0, "auth_code": "869523052033462"}
```

#### authentication

> 终端鉴权

参数:

|参数|类型|说明|
|:---|---|---|
|auth_code|str|鉴权码|
|imei|str|终端IMEI|
|app_version|str|软件版本号|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|终端鉴权消息流水号|
|message_id|int|终端鉴权消息ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
import modem

auth_code = "869523052033462"
imei = modem.getDevImei()
app_version = "v1.0.0"

auth_res = tt808_obj.authentication(auth_code, imei, app_version)
print(auth_res)
# {"serial_no": 1, "message_id": 258, "result_code": 0}
```

#### logout

> 终端注销

参数:

无

返回值(BOOL): True - 成功, False - 失败

示例:

```python
logout_res = tt808_obj.logout()
print(logout_res)
# True
```

#### general_answer

> 终端通用应答

参数:

|参数|类型|说明|
|:---|---|---|
|response_serial_no|int|平台消息流水号|
|response_msg_id|int|平台消息ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持, 默认0, 可使用`ResultCode`类中的枚举值|

返回值(BOOL): True - 成功, False - 失败

示例:

```python
response_serial_no = 2
response_msg_id = 0x8103
result_code = 0

general_answer_res = tt808_obj.general_answer(response_serial_no, response_msg_id, result_code)
print(general_answer_res)
# True
```

#### query_server_time

> 终端查询服务器时间

参数:

无

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|utc_time|str|UTC时间, 时间格式: YYYY-MM-DD HH:mm:ss|

示例:

```python
server_time = tt808_obj.query_server_time(response_serial_no, response_msg_id, result_code)
print(server_time)
# {"utc_time": "2022-06-24 08:12:34"}
```

#### params_report

> 查询终端参数应答

参数:

|参数|类型|说明|
|:---|---|---|
|response_serial_no|int|对应终端参数查询消息流水号|
|terminal_params|dict|终端参数键值对, key为参数id, value为参数值(转换后hex模式的参数值), 通过`TerminalParams`功能获取|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|查询终端参数应答流水号|
|message_id|int|查询终端参数应答ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
TerminalParamsObj = TerminalParams()
TerminalParamsObj.set_params(0x0013, "127.0.0.1:7611")
TerminalParamsObj.set_params(0x0001, 60)
TerminalParamsObj.set_params(0x0002, 30)
TerminalParamsObj.set_params(0x0032, 8, 12, 17, 30)
param_data = TerminalParamsObj.get_params()
terminal_params = {key: val["hex"] for key, val in param_data.items()}
response_serial_no = 3

params_report_res = jtt808_obj.params_report(response_serial_no, terminal_params)
print(params_report_res)
# {"serial_no": 4, "message_id": 260, "result_code": 0}
```

#### properties_report

> 查询终端属性上报

参数:

|参数|类型|说明|
|:---|---|---|
|applicable_passenger_vehicles|int|是否适用客运车辆. 0 - 否, 1 - 是|
|applicable_to_dangerous_goods_vehicles|int|是否适用危险品车辆. 0 - 否, 1 - 是|
|applicable_to_ordinary_freight_vehicles|int|是否适用普通货运车辆. 0 - 否, 1 - 是|
|applicable_to_taxi|int|是否适用出租车辆. 0 - 否, 1 - 是|
|support_hard_disk_video|int|是否支持硬盘录像. 0 - 否, 1 - 是|
|machine_type|int|机器类型. 0 - 一体机, 1 - 分体机|
|applicable_to_trailer|int|是否适用挂车. 0 - 否, 1 - 是|
|manufacturer_id|str|制造商ID, 终端制造商编码, 长度不超过5个字节|
|terminal_model|str|终端型号, 由制造商自行定义, 长度不超过30个字节|
|terminal_id|str|终端ID, 由大写字母和数字组成, 此终端ID由制造商自行定义, 长度不超过30个字节|
|iccid|str|终端SIM卡ICCID|
|hardware_version|str|终端硬件版本号|
|firmware_version|str|终端固件版本号|
|support_gps|int|是否支持 GPS. 0 - 否, 1 - 是|
|support_bds|int|是否支持 BDS. 0 - 否, 1 - 是|
|support_glonass|int|是否支持 GLONASS. 0 - 否, 1 - 是|
|support_galileo|int|是否支持 GALILEO. 0 - 否, 1 - 是|
|support_gprs|int|是否支持 GPRS. 0 - 否, 1 - 是|
|support_cdma|int|是否支持 CDMA. 0 - 否, 1 - 是|
|support_td_scdma|int|是否支持 TD-SCDMA. 0 - 否, 1 - 是|
|support_wcdma|int|是否支持 WCDMA. 0 - 否, 1 - 是|
|support_cdma2000|int|是否支持 CDMA2000. 0 - 否, 1 - 是|
|support_td_lte|int|是否支持 TD-LTE. 0 - 否, 1 - 是|
|support_other_communication|int|是否支持其他通信方式. 0 - 否, 1 - 是|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|查询终端属性上报流水号|
|message_id|int|查询终端属性上报ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
import modem

applicable_passenger_vehicles = 1
applicable_to_dangerous_goods_vehicles = 1
applicable_to_ordinary_freight_vehicles = 1
applicable_to_taxi = 1
support_hard_disk_video = 1
machine_type = 0
applicable_to_trailer = 1
manufacturer_id = "quec"
terminal_model = "EC200U-CNAA"
terminal_id = "EC200UCNAA"
iccid = sim.getIccid()
hardware_version = modem.getDevImei()
firmware_version = modem.getDevFwVersion()
support_gps = 1
support_bds = 1
support_glonass = 1
support_galileo = 1
support_gprs = 1
support_cdma = 1
support_td_scdma = 1
support_wcdma = 1
support_cdma2000 = 1
support_td_lte = 1
support_other_communication = 0

properties_report_res = jtt808_obj.properties_report(
    applicable_passenger_vehicles, applicable_to_dangerous_goods_vehicles,
    applicable_to_ordinary_freight_vehicles, applicable_to_taxi, support_hard_disk_video,
    machine_type, applicable_to_trailer, manufacturer_id, terminal_model, terminal_id,
    iccid, hardware_version, firmware_version, support_gps, support_bds, support_glonass,
    support_galileo, support_gprs, support_cdma, support_td_scdma, support_wcdma,
    support_cdma2000, support_td_lte, support_other_communication
)
print(properties_report_res)
# {"serial_no": 5, "message_id": 263, "result_code": 0}
```

#### upgrade_result_report

> 终端升级结果上报

参数:

|参数|类型|说明|
|:---|---|---|
|upgrade_type|int|升级类型:<br>0 - 终端<br>12 - 道路运输证IC卡读卡器<br>52 - 卫星定位模块|
|result_code|int|升级结果:<br>0 - 成功<br>1 - 失败<br>2 - 取消|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|终端升级结果上报流水号|
|message_id|int|终端升级结果上报ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
upgrade_type = 0
result_code = 0
upgrade_result_report_res = jtt808_obj.upgrade_result_report(upgrade_type, result_code)
print(upgrade_result_report_res)
# {"serial_no": 6, "message_id": 264, "result_code": 0}
```

#### loction_report

> 该接口用于定位信息的上报, 以下三个消息上报功能
> 
> - 0x0200 - 定位信息上报
> - 0x0201 - 定位信息查询消息(0x8201)应答
> - 0x0500 - 车辆控制消息(0x8500)应答

参数:

|参数|类型|说明|
|:---|---|---|
|response_msg_id|int|对应服务端请求消息ID, 0x8201 - 车辆定位信息查询, 0x8500 - 车辆控制消息, 当用于定位信息上报时, 该参数传参None|
|response_serial_no|int|对应服务端请求消息流水号, 当用于定位信息上报时, 该参数传参None|
|alarm_flag|str| 定位告警信息, 数据来源定位告警配置: `LocAlarmWarningConfig().value()`|
|loc_status|str| 定位状态信息, 数据来源定位状态信息配置: `LocStatusConfig().value()`|
|latitude|float| 纬度|
|longitude|float| 经度 |
|altitude|int| 海拔, 单位为米(m)|
|speed|float| 速度: 单位为公里每小时(km/h), 精确到0.1|
|direction|int|方向, 0~359, 正北为0, 顺时针|
|time|str| GMT+8时间, 格式: YYMMDDhhmmss, 如: `220627101130`|
|loc_additional_info|str| 位置附加信息, 数据来源位置附加信息配置: `LocAdditonalInfoConfig().value()`|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|定位信息上报/定位信息查询消息应答/车辆控制消息应答流水号|
|message_id|int|定位信息上报/定位信息查询消息应答/车辆控制消息应答ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
def test_init_loction_data():
    # 位置信息项测试数据生成
    LocStatusConfigObj = LocStatusConfig()
    LocAlarmWarningConfigObj = LocAlarmWarningConfig()
    LocAdditionalInfoConfigObj = LocAdditionalInfoConfig()
    for key in LocStatusConfigObj._loc_cfg_offset.__dict__.keys():
        LocStatusConfigObj.set_config(key, 1)
    LocAdditionalInfoConfigObj.set_mileage(100)
    LocAdditionalInfoConfigObj.set_oil_quantity(32.5)
    LocAdditionalInfoConfigObj.set_speed(0)

    alarm_config = LocAlarmWarningConfigObj.value()
    loc_status = LocStatusConfigObj.value()
    latitude = 31.824845156501
    longitude = 117.24091089413
    altitude = 120
    speed = 0
    direction = 0
    time = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(*(utime.localtime()[:6]))[2:]
    loc_additional_info = LocAdditionalInfoConfigObj.value()
    logger.debug("loc_additional_info: %s" % loc_additional_info)

    return (alarm_config[0], loc_status, latitude, longitude, altitude, speed, direction, time, loc_additional_info)

# 0x0200 - 定位信息上报
loc_data = test_init_loction_data()
args = [None, None]
args.extend(list(loc_data))
loction_report_res = jtt808_obj.loction_report(*args)
print(loction_report)
# {"serial_no": 7, "message_id": 512, "result_code": 0}

# 0x0201 - 定位信息查询消息(0x8201)应答
response_msg_id = 0x8201
response_serial_no = 9
args = [response_msg_id, response_serial_no]
args.extend(list(loc_data))
loction_report_res = jtt808_obj.loction_report(*args)
print(loction_report)
# {"serial_no": 10, "message_id": 513, "result_code": 0}

# 0x0500 - 车辆控制消息(0x8500)应答
response_msg_id = 0x8500
response_serial_no = 11
args = [response_msg_id, response_serial_no]
args.extend(list(loc_data))
loction_report_res = jtt808_obj.loction_report(*args)
print(loction_report)
# {"serial_no": 12, "message_id": 1280, "result_code": 0}
```

#### event_report

> 事件上报

参数:

|参数|类型|说明|
|:---|---|---|
|event_id|int|事件ID, 事件ID来源于0x8301事件设置消息|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|事件上报流水号|
|message_id|int|事件上报ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
event_id = 10
event_report_res = jtt808_obj.event_report(event_id)
print(event_report_res)
# {"serial_no": 13, "message_id": 769, "result_code": 0}
```

#### issue_question_response

> 该接口用于下发问题消息(0x8302)应答

参数:

|参数|类型|说明|
|:---|---|---|
|response_serial_no|int|对应服务端下发问题消息流水号|
|answer_id|int|提问下发中附带的答案ID|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|下发问题消息应答流水号|
|message_id|int|下发问题消息应答ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
response_serial_no = 14
answer_id = 1
issue_question_response_res = jtt808_obj.issue_question_response(response_serial_no, answer_id)
print(issue_question_response_res)
# {"serial_no": 15, "message_id": 770, "result_code": 0}
```

#### information_demand_cancellation

> 信息点播/取消

参数:

|参数|类型|说明|
|:---|---|---|
|info_type|int|消息类型, 数据来源0x8303信息点播菜单设置.|
|onoff|int|0 - 取消, 1 - 点播|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|信息点播/取消流水号|
|message_id|int|信息点播/取消ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
info_type = 5
onoff = 1
information_demand_cancellation_res = jtt808_obj.information_demand_cancellation(info_type, onoff)
print(information_demand_cancellation_res)
# {"serial_no": 16, "message_id": 770, "result_code": 0}
```

#### query_area_route_data_response

> 查询区域或路线数据(0x8608)应答

参数:

|参数|类型|说明|
|:---|---|---|
|query_type|int|查询类型:<br>1 - 查询圆形区域数据<br>2 - 查询矩形区域数据<br>3 - 查询多边形区域数据<br>4 - 查询路线数据|
|data|list|区域或线路数据消息体列表, 元素为线路或区域源消息体数据, 数据来源:消息0x8600, 0x8602, 0x8604, 0x8606消息体中的`source_body`|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|查询区域或路线数据应答流水号|
|message_id|int|查询区域或路线数据应答ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
info_type = 5
onoff = 1
query_area_route_data_response_res = jtt808_obj.query_area_route_data_response(info_type, onoff)
print(query_area_route_data_response_res)
# {"serial_no": 16, "message_id": 770, "result_code": 0}
```

#### driving_record_data_upload

> 行驶记录数据采集命令(0x8700)应答, 行驶记录数据上传

参数:

|参数|类型|说明|
|:---|---|---|
|response_serial_no|int|对应服务端请求消息流水号|
|cmd_word|int|命令字:<br>33 - 行驶状态记录, <br>34 - 事故疑点记录, <br>35 - 超时驾驶记录, <br>35 - 驾驶人信息记录, <br>37 - 日志记录|
|cmd_data|bytes|数据块|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|行驶记录数据上传流水号|
|message_id|int|行驶记录数据上传ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
with open("/usr/xxx.xxx", "rb") as f:
    cmd_data = f.read()
    response_serial_no = 17
    cmd_word = 33
    driving_record_data_upload_res = jtt808_obj.driving_record_data_upload(response_serial_no, cmd_word, cmd_data)
    print(driving_record_data_upload_res)
# {"serial_no": 18, "message_id": 1792, "result_code": 0}
```

#### electronic_waybill_report

> 电子运单上报

参数:

|参数|类型|说明|
|:---|---|---|
|data|bytes|电子运单文件数据|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|电子运单上报流水号|
|message_id|int|电子运单上报ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
with open("/usr/xxx.xxx", "rb") as f:
    data = f.read()
    electronic_waybill_report_res = jtt808_obj.electronic_waybill_report(data)
    print(electronic_waybill_report_res)
# {"serial_no": 19, "message_id": 1793, "result_code": 0}
```

#### driver_identity_information_report

> 驾驶员身份信息采集上报

参数:

|参数|类型|说明|
|:---|---|---|
|status|int|状态: <br>0x01 - 从业资格证IC卡插入(驾驶员上班)<br>0x02 - 从业资格证IC卡拔出(驾驶员下班)|
|time|str|插/拔卡时间, 时间格式: YYMMDDhhmmss|
|ic_read_result|int|IC卡读取结果:<br>0x00 - IC卡读卡成功<br>0x01 - 读卡失败, 原因卡密钥认证未通过<br>0x02 - 读卡失败, 原因卡已被锁定<br>0x03 - 读卡失败, 卡已被拔出<br>0x04 - 读卡失败, 原因为数据校验错误<br>当状态为0x02时, 该字段传空字符串|
|driver_name|str|驾驶员姓名, 当状态为0x02时, 该字段传空字符串|
|qualification_certificate_code|str|从业资格证编码, 当状态为0x02时, 该字段传空字符串|
|issuing_agency_name|str|从业资格证发证机构名称, 当状态为0x02时, 该字段传空字符串|
|certificate_validity|str|证件有效期, 时间格式: YYYYMMDD, 当状态为0x02时, 该字段传空字符串|
|driver_id_number|str|驾驶员身份证号, 当状态为0x02时, 该字段传空字符串|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|驾驶员身份信息采集上报流水号|
|message_id|int|驾驶员身份信息采集上报ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
status = 1
time = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(*(utime.localtime()[:6]))[2:]
ic_read_result = 0
driver_name = "jack"
qualification_certificate_code = "88888"
issuing_agency_name = "市级道路运输管理机构"
certificate_validity = "20220701"
driver_id_number = "342426194910010001"
driver_identity_information_report_res = jtt808_obj.driver_identity_information_report(
    status, time, ic_read_result, driver_name, qualification_certificate_code,
    issuing_agency_name, certificate_validity, driver_id_number
)
print(driver_identity_information_report_res)
# {"serial_no": 20, "message_id": 1794, "result_code": 0}
```

#### location_bulk_report

> 定位数据批量上传

参数:

|参数|类型|说明|
|:---|---|---|
|data_type|int|位置数据类型: <br>0 - 正常位置批量汇报<br>1 - 盲区补报|
|loc_datas|list|位置信息列表, 元素为位置信息元组, 具体见下表(定位信息表)|

定位信息表

元素序号|参数|类型|说明|
|:---|---|---|---|
|0|alarm_flag|str| 定位告警信息, 数据来源定位告警配置: `LocAlarmWarningConfig().value()` |
|1|loc_status|str| 定位状态信息, 数据来源定位状态信息配置: `LocStatusConfig().value()` |
|2|latitude|float| 纬度 |
|3|longitude|float| 经度 |
|4|altitude|int| 海拔, 单位为米(m) |
|5|speed|float| 速度: 单位为公里每小时(km/h), 精确到0.1 |
|6|direction|int|方向, 0~359, 正北为0, 顺时针 |
|7|time|str| GMT+8时间, 格式: YYMMDDhhmmss, 如: `220627101130` |
|8|loc_additional_info|str| 位置附加信息, 数据来源位置附加信息配置: `LocAdditonalInfoConfig().value()` |

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|定位数据批量上传流水号|
|message_id|int|定位数据批量上传ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
loc_data = test_init_loction_data()
loc_datas = [loc_data] * 10
logger.debug("loc_datas: %s" % str(loc_datas))
data_type = 0
location_bulk_report_res = jtt808_obj.location_bulk_report(data_type, loc_datas)
print(location_bulk_report)
# {"serial_no": 21, "message_id": 1796, "result_code": 0}
```

#### can_bus_data_upload

> CAN总线数据上传

参数:

|参数|类型|说明|
|:---|---|---|
|recive_time|str|第一条CAN总线数据接收时间, 数据格式: hhmmssmsms|
|can_datas|list|CAN总线数据列表, 元素为CAN总线数据, 具体见下CAN总线数据信息表|

CAN总线数据信息表

|参数|类型|说明|
|:---|---|---|
|can_channel_no|int|CAN通道号: 0 - CAN1, 1 - CAN2|
|frame_type|int|帧类型: 0 - 标准帧, 1 - 扩展帧|
|collection_method|int|数据采集方式: 0 - 原始数据, 1 - 采集区间的平均值|
|can_id|int|CAN总线ID|
|can_data|str|CAN总线数据|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|CAN总线数据上传流水号|
|message_id|int|CAN总线数据上传ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
recive_time = ("{:2d}" * 3 + "0000").format(*(utime.localtime()[3:6]))
can_channel_no = 0
frame_type = 0
collection_method = 0
can_id = 0
can_data = "123"
can_datas = [(can_channel_no, frame_type, collection_method, can_id, can_data)] * 3
can_bus_data_upload_res = jtt808_obj.can_bus_data_upload(recive_time, can_datas)
print(can_bus_data_upload_res)
# {"serial_no": 22, "message_id": 1797, "result_code": 0}
```

#### media_event_upload

> 多媒体事件信息上报

参数:

|参数|类型|说明|
|:---|---|---|
|media_id|int|多媒体数据ID|
|media_type|int|多媒体数据类型:<br>0 - 图像<br>1 - 音频<br>2 - 视频|
|media_encoding|int|多媒体格式编码:<br>0 - JPEG<br>1 - TIF<br>2 - MP3<br>3 - WAV<br>4 - WMV|
|event_code|int|事件项编码:<br>0 - 平台下发指令<br>1 - 定时动作<br>2 - 抢劫报警触发<br>3 - 碰撞侧翻报警触发<br>4 - 门开拍照<br>5 - 门关拍照<br>6 - 车门由开变关, 车速从小于20km到超过20km<br>7 - 定距拍照|
|channel_id|int|通道ID|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|多媒体事件信息上报流水号|
|message_id|int|多媒体事件信息上报ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
media_id = 12
media_type = 0
media_encoding = 0
event_id = 4
channel_id = 1
media_event_upload_res = jtt808_obj.media_event_upload(media_id, media_type, media_encoding, event_id, channel_id)
print(media_event_upload_res)
# {"serial_no": 23, "message_id": 2048, "result_code": 0}
```

#### media_data_upload

> 多媒体数据信息上报

参数:

|参数|类型|说明|
|:---|---|---|
|media_id|int|多媒体数据ID|
|media_type|int|多媒体数据类型:<br>0 - 图像<br>1 - 音频<br>2 - 视频|
|media_encoding|int|多媒体格式编码:<br>0 - JPEG<br>1 - TIF<br>2 - MP3<br>3 - WAV<br>4 - WMV|
|event_code|int|事件项编码:<br>0 - 平台下发指令<br>1 - 定时动作<br>2 - 抢劫报警触发<br>3 - 碰撞侧翻报警触发<br>4 - 门开拍照<br>5 - 门关拍照<br>6 - 车门由开变关, 车速从小于20km到超过20km<br>7 - 定距拍照|
|channel_id|int|通道ID|
|media_data|bytes|多媒体数据包|
|loc_data|tuple|多媒体数据位置信息, 详见`定位信息表`, 无位置附加信息|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|多媒体数据信息上报流水号|
|message_id|int|多媒体数据信息上报ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
media_id = 14
media_type = 0
media_encoding = 0
event_id = 4
channel_id = 1
with open("/usr/system_config.json", "rb") as f:
    media_data = f.read()
loc_data = test_init_loction_data()[:-1]
media_data_upload_res = jtt808_obj.media_data_upload(media_id, media_type, media_encoding, event_id, channel_id, media_data, loc_data)
print(media_data_upload_res)
# {"serial_no": 24, "message_id": 2049, "result_code": 0}
```

#### camera_shoots_immediately_response

> 摄像头立即拍摄命令应答

参数:

|参数|类型|说明|
|:---|---|---|
|response_serial_no|(int)|服务端摄像头立即拍摄命令请求消息流水号|
|result|(int)|结果:<br>0 - 成功<br>1 - 失败<br>2 - 通道不支持|
|ids|(list)|多媒体ID列表|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|摄像头立即拍摄命令应答流水号|
|message_id|int|摄像头立即拍摄命令应答ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
response_serial_no = 25
result = 0
ids = list(range(10))
camera_shoots_immediately_response_res = jtt808_obj.camera_shoots_immediately_response(response_serial_no, result, ids)
print(camera_shoots_immediately_response_res)
# {"serial_no": 26, "message_id": 2053, "result_code": 0}
```

#### stored_media_data_retrieval_response

> 存储多媒体数据检索应答

参数:

|参数|类型|说明|
|:---|---|---|
|response_serial_no|(int)|服务端存储多媒体数据检索请求消息流水号|
|medias|(list)|多媒体数据项列表, 元素为元组, 具体数据见`多媒体数据项信息表`|

多媒体数据项信息表

元素序号|参数|类型|说明|
|:---|---|---|---|
|0|media_id|int|多媒体ID|
|1|media_type|int|多媒体类型: 0 - 图像1 - 音频2 - 视频|
|2|channel_id|int|通道ID|
|3|event_code|int|事件项编码:<br>0 - 平台下发指令<br>1 - 定时动作<br>2 - 抢劫报警触发<br>3 - 碰撞侧翻报警触发<br>其他保留|
|4|loc_data|tuple|多媒体数据位置信息, 详见`定位信息表`, 无位置附加信息)|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|存储多媒体数据检索应答流水号|
|message_id|int|存储多媒体数据检索应答ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
media_id = 1
media_type = 0
channel_id = 2
event_code = 5
loc_data = test_init_loction_data()[:-1]
medias = [(media_id, media_type, channel_id, event_code, loc_data)] * 10
stored_media_data_retrieval_response_res = jtt808_obj.stored_media_data_retrieval_response(response_serial_no, medias)
print(stored_media_data_retrieval_response_res)
# {"serial_no": 27, "message_id": 2050, "result_code": 0}
```

#### data_uplink_transparent_transmission

> 数据上行透传

参数:

|参数|类型|说明|
|:---|---|---|
|data_type|int|透传消息类型:<br>0x00 - GNSS模块详细定位数据<br>0x0B - 道路运输证IC卡信息<br>0x41 - 串口1透传<br>0x42 - 串口2透传<br>0xF0~0xFF - 用户自定义消息|
|data|str|透传消息内容|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|数据上行透传流水号|
|message_id|int|数据上行透传ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
data_type = 0
data = "123456"
data_uplink_transparent_transmission_res = jtt808_obj.data_uplink_transparent_transmission(data_type, data)
print(stored_media_data_retrieval_response_res)
# {"serial_no": 28, "message_id": 2304, "result_code": 0}
```

#### data_compression_report

> 数据压缩上报

参数:

|参数|类型|说明|
|:---|---|---|
|data|str|压缩数据|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|数据压缩上报流水号|
|message_id|int|数据压缩上报ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
    with open("/usr/xxx.tar.gz", "rb") as f:
        data = f.read()
        data_compression_report_res = jtt808_obj.data_compression_report(data)
        print(data_compression_report_res)
print(data_compression_report_res)
# {"serial_no": 29, "message_id": 2305, "result_code": 0}
```

#### terminal_rsa_public_key

> 终端RSA公钥上报

参数:

|参数|类型|说明|
|:---|---|---|
|e|int|终端RSA公钥{e, n}中的e|
|n|str|终端RSA公钥{e, n}中的n|

返回值(DICT):

|字段|字段类型|说明|
|---|---|---|
|serial_no|int|终端RSA公钥上报流水号|
|message_id|int|终端RSA公钥上报ID|
|result_code|int|结果: <br>0 - 成功/确认<br>1 - 失败<br>2 - 消息有误<br>3 - 不支持<br>4 - 报警处理确认|

示例:

```python
e = 0x010001  # 65537
n = "E5A55035C17123BFAB98733E9A619152CEAA13214261BA971EE3563CCF9790FA221FDD9D582B4E14ED200173B2D9822E561E99EE54B3A812ACCDDDEAD97DF6DA682583080F7733035BF22C956F6F96ED8F3E2E8DA1DE80C38B1A18956D719DCA407EC13E0C86E40502553C418180D520E6B9A18E04E3817F9CD185769233C9CB"
terminal_rsa_public_key_res = jtt808_obj.terminal_rsa_public_key(e, n)
print(terminal_rsa_public_key_res)
# {"serial_no": 30, "message_id": 2560, "result_code": 0}
```

## 4. 服务端下发消息数据

### **消息ID: 0x8103 -- 设置终端参数**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|params|list|列表元素元组, 元组中元素1为参数ID, 元素2为参数值|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8104 -- 查询终端参数**

**消息体`data`:** 无

**应答消息:** 该消息需使用`jtt808.params_report`接口进行应答

### **消息ID: 0x8105 -- 终端控制**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|cmd_word|int|命令参数:<br>1 - 无线升级<br>2 - 控制终端连接指定服务器<br>3 - 终端关机<br>4 - 终端复位<br>5 - 终端恢复出厂设置<br>6 - 关闭数据通信<br>6 - 关闭所有无线通信|
|cmd_params|dict|命令参数为1,2时, 命令参数见下表, 否则为空字典|

无线升级参数值

|编码|数据类型|说明|
|:---|---|---|
|url|str|URL地址|
|dial_point_name|str|拨号点名称|
|dial_user_name|str|拨号用户名|
|dial_password|str|拨号密码|
|addr|str|地址|
|tcp_port|str|TCP端口|
|udp_port|str|UDP端口|
|manufacturer_id|str|制造商ID|
|hardware_version|str|硬件版本|
|firmware_version|str|固件版本|
|conn_timeout|str|连接到指定服务器时限|

控制终端连接指定服务器参数值

|编码|数据类型|说明|
|:---|---|---|
|conn_ctrl|int|连接控制:<br>0 - 切换到指定监管平台服务器, 连接到该服务器后即进入应急状态, 此状态下仅有下发控制指令的监督平台可发送包括短信在内的控制指令<br>1 - 切换回原缺省监控平台服务器, 并恢复正常状态|
|auth_code|str|监管平台鉴权码|
|dial_point_name|str|拨号点名称|
|dial_user_name|str|拨号用户名|
|dial_password|str|拨号密码|
|addr|str|地址|
|tcp_port|str|TCP端口|
|udp_port|str|UDP端口|
|conn_timeout|str|连接到指定服务器时限|

> 连接控制为1时, 无其他参数

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8106 -- 查询指定终端参数**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|param_ids|list|列表元素为终端参数ID|

**应答消息:** 该消息需使用`jtt808.params_report`接口进行应答

### **消息ID: 0x8107 -- 查询终端属性**

**消息体`data`:** 无

**应答消息:** 该消息需使用`jtt808.properties_report`接口进行应答

### **消息ID: 0x8108 -- 下发终端升级包**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|upgrade_type|str|升级类型:<br>0 - 终端<br>12 - 道路运输证IC卡读卡器<br>52 - 卫星定位模块|
|manufacturer_id|str|制造商ID|
|terminal_firmware_verion|str|终端固件版本号|
|upgrade_package|bytes|升级数据包|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8201 -- 位置信息查询**

**消息体`data`:** 无

**应答消息:** 该消息需使用`jtt808.loction_report`接口进行应答

### **消息ID: 0x8202 -- 临时位置跟踪控制**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|time_interval|int|时间间隔, 单位秒(s), 时间间隔为0时停止跟踪, 停止跟踪无需带后继参数.|
|location_tracking_validity_period|int|位置跟踪有效期, 单位秒(s), 终端在接收到位置跟踪控制消息后, 在有效期截至时间之前, 依据消息中的时间间隔发送位置汇报.|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8203 -- 人工确认报警消息**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|alarm_msg_serial_no|int|需人工确认的报警消息流水号, 0 表示该报警类型所有消息|
|emergency_alarm|int|1 - 确认紧急报警|
|hazard_alarm|int|1 - 确认危险预警|
|in_out_area_alarm|int|1 - 确认进出区域报警|
|in_out_road_alarm|int|1 - 确认进出路线报警|
|insufficient_or_too_long_travel_time_on_the_road_alarm|int|1 - 确认路段行驶时间不足/过长报警|
|vehicle_illegal_ignition_alarm|int|1 - 确认车辆非法点火报警|
|vehicle_illegal_displacement_alarm|int|1 - 确认车辆非法位移报警|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8204 -- 链路检测**

**消息体`data`:** 无

**应答消息:** 该消息需使用`jtt808.loction_report`接口进行应答

### **消息ID: 0x8300 -- 文本信息下发**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|flag_type|int|文本标志类型: <br>1 - 服务<br>2 - 紧急<br>3 - 通知|
|terminal_display|int|1 - 终端显示器显示|
|terminal_tts_broadcast_and_read|int|1 - 终端TTS播报|
|flag_msg_type|int|0 - 中心导航信息, 1 - CAN故障码信息|
|msg_type|int|文本类型: 1 - 通知, 2 - 服务|
|message|int|文本信息|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8301 -- 事件设置**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|set_type|int|设置类型: <br>0 - 删除终端现有所有事件, 事件项为空<br>1 - 更新事件<br>2 - 追加事件<br>3 - 修改事件<br>4 - 删除特定几项事件|
|events|list|事件项列表, 元素为字典, 包含两个key值, `id`为事件id, `data`为事件内容|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8302 -- 提问下发**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|flag|dict|提问下发标志: <br>`emergency`: 是否紧急, 0 - 否, 1 - 是; <br>`terminal_tts_broadcast_and_read`: 终端TTS播读, 0 - 否, 1 - 是; <br>`advertising_screen_display`: 广告屏显示, 0 - 否, 1 - 是|
|question_info|str|问题内容|
|answers|list|候选答案列表, 元素为答案字典信息, 包含`id`答案id, `data`答案内容, 两个key值|

**应答消息:** 该消息需使用`jtt808.issue_question_response`接口进行应答

### **消息ID: 0x8303 -- 信息点播菜单设置**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|set_type|int|设置类型: <br>0 - 删除终端现有所有信息项<br>1 - 更新菜单<br>2 - 追加菜单<br>3 - 修改菜单|
|infos|list|信息项列表, 元素为字典, 包含两个key值, `type`为信息类型, `name`信息名称, 终端已有同类型的信息项, 则被覆盖.|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8304 -- 信息服务**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|info_type|int|信息类型|
|info_data|str|信息内容|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8400 -- 电话回拨**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|flag|int|标志: 0 - 普通通话; 1 - 监听;|
|phone_number|str|电话号码|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8401 -- 设置电话本**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|set_type|int|设置类型: <br>0 - 删除终端上所有存储的联系人; <br>1 - 更新电话本(删除终端已有全部联系人并追加消息中的联系人); <br>2 - 追加电话本; <br>3 - 修改电话本(以联系人为索引)|
|phonebook|list|联系人列表: 元素为字典, 包含三个key值, <br>`call_type` - 标志: 1 - 呼入, 2 - 呼出, 3 - 呼入/呼出<br>`phone` - 电话号码<br>`concat_user` - 联系人|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8500 -- 车辆控制**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|data|list|列表元素为控制信息, 包含`id`, `param`两个key值, 具体说明见车辆控制指令表|

车辆控制指令表

|控制ID|说明|控制参数|
|---|---|---|
|0x0001|车门控制|0 - 车门锁闭, 1 - 车门开启|
|0x0002~0x8000|标准修订预留||
|0xF001~0xFFFF|厂家自定义控制类型||

**应答消息:** 该消息需使用`jtt808.loction_report`接口进行应答

### **消息ID: 0x8600 -- 设置圆形区域**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|set_attr|int|设置属性: 0 - 更新; 1 - 追加; 2 - 修改;|
|area_data|list|圆形区域属性, 具体信息见`圆形区域属性表`|
|source_body|str|用于`jtt808.query_area_route_data_response`区域或路段查询上报接口|

圆形区域属性表

|属性|类型|说明|
|:---|---|---|
|area_id|int|区域ID|
|attributes|dict|区域属性, 具体信息见`区域属性表`|
|center_latitude|float|中心点纬度|
|center_longitude|float|中心点经度|
|radius|int|半径, 单位:米(m)|
|start_time|str|开始时间, 时间格式: YYMMDDhhmmss, 当区域属性`time_limit_enable`为0时, 该字段则为空|
|end_time|str|结束时间, 时间格式: YYMMDDhhmmss, 当区域属性`time_limit_enable`为0时, 该字段则为空|
|speed_limit|int|最高速度, 单位千米每小时(km/h), 当区域属性`speed_limit_enable`为0时, 该字段为0|
|over_speed_time|int|超速持续时间, 单位秒(s), 当区域属性`speed_limit_enable`为0时, 该字段为0|
|night_speed_limit|int|夜间最高速度, 单位千米每小时(km/h), 当区域属性`speed_limit_enable`为0时, 该字段为0|
|area_name|str|区域名称|

区域属性表

|属性|类型|说明|
|:---|---|---|
|time_limit_enable|int|是否启用起始与结束时间的判断规则: 0 - 否, 1 - 是|
|speed_limit_enable|int|是否启用最高速度, 超速持续时间和夜间最高速度的判断规则 0 - 否, 1 - 是|
|alert_driver_when_entering_area|int|进区域是否报警给驾驶员 0 - 否, 1 - 是|
|alert_platform_when_entering_area|int|进区域是否报警给平台 0 - 否, 1 - 是|
|alert_driver_when_leaving_area|int|出区域是否报警给驾驶员 0 - 否, 1 - 是|
|alert_platform_when_leaving_area|int|出区域是否报警给平台 0 - 否, 1 - 是|
|latitude_direction|int|纬度方向: 0 - 北纬, 1 - 南纬|
|longitude_direction|int|经度方向: 0 - 东经, 1 - 西经|
|open_the_door_enable|int|车门开关控制: 0 - 允许开车门, 1 - 不允许开车门|
|communication_module_enable_when_entering_area|int|进区域通信模块开关: 0 - 开, 1 - 关|
|gnss_enable_when_entering_area|int|进区域GNSS详细定位数据采集开关: 0 - 关, 1 - 开|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8601 -- 删除圆形区域**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|all|int|是否删除设备全部圆形区域: 0 - 否, 1 - 是, 当为0时, 删除指定ID的区域数据|
|area_ids|list|待删除的指定圆形区域ID列表|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8602 -- 设置矩形区域**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|set_attr|int|设置属性: 0 - 更新; 1 - 追加; 2 - 修改;|
|area_data|list|矩形区域属性, 具体信息见`矩形区域属性表`|
|source_body|str|用于`jtt808.query_area_route_data_response`区域或路段查询上报接口|

矩形区域属性表

|属性|类型|说明|
|:---|---|---|
|area_id|int|区域ID|
|attributes|dict|区域属性, 具体信息见`区域属性表`|
|upper_left_latitude|float|左上点纬度|
|upper_left_longitude|float|左上点经度|
|lower_right_latitude|float|右上点纬度|
|lower_right_longitude|float|右上点经度|
|start_time|str|开始时间, 时间格式: YYMMDDhhmmss, 当区域属性`time_limit_enable`为0时, 该字段则为空|
|end_time|str|结束时间, 时间格式: YYMMDDhhmmss, 当区域属性`time_limit_enable`为0时, 该字段则为空|
|speed_limit|int|最高速度, 单位千米每小时(km/h), 当区域属性`speed_limit_enable`为0时, 该字段为0|
|over_speed_time|int|超速持续时间, 单位秒(s), 当区域属性`speed_limit_enable`为0时, 该字段为0|
|night_speed_limit|int|夜间最高速度, 单位千米每小时(km/h), 当区域属性`speed_limit_enable`为0时, 该字段为0|
|area_name|str|区域名称|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8603 -- 删除矩形区域**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|all|int|是否删除设备全部矩形区域: 0 - 否, 1 - 是, 当为0时, 删除指定ID的区域数据|
|area_ids|list|待删除的指定矩形区域ID列表|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8604 -- 设置多边形区域**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|area_data|dict|多边形区域属性, 具体信息见`多边形区域属性表`|
|source_body|str|用于`jtt808.query_area_route_data_response`区域或路段查询上报接口|

多边形区域属性表

|属性|类型|说明|
|:---|---|---|
|area_id|int|区域ID|
|attributes|dict|区域属性, 具体信息见`区域属性表`|
|start_time|str|开始时间, 时间格式: YYMMDDhhmmss, 当区域属性`time_limit_enable`为0时, 该字段则为空|
|end_time|str|结束时间, 时间格式: YYMMDDhhmmss, 当区域属性`time_limit_enable`为0时, 该字段则为空|
|speed_limit|int|最高速度, 单位千米每小时(km/h), 当区域属性`speed_limit_enable`为0时, 该字段为0|
|over_speed_time|int|超速持续时间, 单位秒(s), 当区域属性`speed_limit_enable`为0时, 该字段为0|
|point_loction|list|顶点项列表, 元素为字典, 包含两个key值, `latitude` - 纬度, `longitude` - 经度|
|night_speed_limit|int|夜间最高速度, 单位千米每小时(km/h), 当区域属性`speed_limit_enable`为0时, 该字段为0|
|area_name|str|区域名称|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8605 -- 删除多边形区域**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|all|int|是否删除设备全部多边形区域: 0 - 否, 1 - 是, 当为0时, 删除指定ID的区域数据|
|area_ids|list|待删除的指定多边形区域ID列表|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8606 -- 设置路线**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|area_data|dict|路线信息, 具体信息见`路线信息属性表`|
|source_body|str|用于`jtt808.query_area_route_data_response`区域或路段查询上报接口|

路线信息属性表

|属性|类型|说明|
|:---|---|---|
|route_id|int|路线ID|
|attributes|dict|路线属性, 具体信息见`路线属性表`, |
|start_time|str|开始时间, 时间格式: YYMMDDhhmmss, 当区域属性`time_limit_enable`为0时, 该字段则为空|
|end_time|str|结束时间, 时间格式: YYMMDDhhmmss, 当区域属性`time_limit_enable`为0时, 该字段则为空|
|turning_points|list|线路拐点项列表, 元素为字典, 线路拐点项项信息见`线路拐点项信息表`|
|route_name|str|路线名称|

路线属性表

|属性|类型|说明|
|:---|---|---|
|time_limit_enable|int|是否启用起始与结束时间的判断规则: 0 - 否, 1 - 是|
|alert_driver_when_entering_area|int|进区域是否报警给驾驶员 0 - 否, 1 - 是|
|alert_platform_when_entering_area|int|进区域是否报警给平台 0 - 否, 1 - 是|
|alert_driver_when_leaving_area|int|出区域是否报警给驾驶员 0 - 否, 1 - 是|
|alert_platform_when_leaving_area|int|出区域是否报警给平台 0 - 否, 1 - 是|

线路拐点项信息表

|属性|类型|说明|
|:---|---|---|
|turning_point_id|int|拐点ID|
|road_section_id|int|路段ID|
|turning_point_latitude|float|拐点维度|
|turning_point_longitude|float|拐点进度|
|road_section_width|int|路段宽度, 单位:米(m)|
|attributes|dict|路段属性, 具体信息见`线路路段属性表`|
|driving_too_long_time_limit|int|路段行驶时间过长阈值, 单位:秒(s), 若线路路段属性`driving_time_limit_enable`为0, 则为-1|
|insufficient_travel_time_limit|int|路段行驶时间不足阈值, 单位:秒(s), 若线路路段属性`driving_time_limit_enable`为0, 则为-1|
|speed_limit|int|路段最高速度, 单位:公里每小时(km/h), 若线路路段属性`speed_limit_enable`为0, 则为0|
|over_speed_time|int|路段超速持续时间, 单位:秒(s), 若线路路段属性`speed_limit_enable`为0, 则为0|
|night_speed_limit|int|路段夜间最高速度, 单位:公里每小时(km/h), 若线路路段属性`speed_limit_enable`为0, 则为0|

线路路段属性表

|属性|类型|说明|
|:---|---|---|
|driving_time_limit_enable|int|行驶时间限制启用:0 - 禁用, 1 - 启用|
|speed_limit_enable|int|限速启用: 0 - 禁用, 1 - 启用|
|latitude_direction|int|纬度方向: 0 - 北纬, 1 - 南纬|
|longitude_direction|int|经度方向: 0 - 东经, 1 - 西经|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8607 -- 删除线路**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|all|int|是否删除设备全部线路: 0 - 否, 1 - 是, 当为0时, 删除指定ID的线路数据|
|route_ids|list|待删除的指定线路ID列表|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8608 -- 查询区域或路线数据**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|query_type|int|查询类型:<br>1 - 查询圆形区域数据, <br>2 - 查询矩形区域数据, <br>3 - 查询多边形区域数据, <br>4 - 查询线路数据|
|ids|list|如果为空则标识查询所有指定类型的区域数据, 不为空则查询指定id的区域或线路数据|

**应答消息:** 该消息需使用`jtt808.query_area_route_data_response`接口进行应答

### **消息ID: 0x8700 -- 形式记录数据采集命令**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|cmd_word|int|命令字:<br>33 - 行驶状态记录, <br>34 - 事故疑点记录, <br>35 - 超时驾驶记录, <br>35 - 驾驶人信息记录, <br>37 - 日志记录|
|cmd_data|bytes|数据块|

**应答消息:** 该消息需使用`jtt808.driving_record_data_upload`接口进行应答

### **消息ID: 0x8701 -- 行驶记录参数下传**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|cmd_word|int|命令字:<br>33 - 行驶状态记录, <br>34 - 事故疑点记录, <br>35 - 超时驾驶记录, <br>35 - 驾驶人信息记录, <br>37 - 日志记录|
|cmd_data|bytes|数据块|

**应答消息:** 该消息需使用`jtt808.query_area_route_data_response`接口进行应答

### **消息ID: 0x8702 -- 上报驾驶员身份信息请求**

**消息体`data`:** 无

**应答消息:** 该消息需使用`jtt808.driver_identity_information_report`接口进行应答

### **消息ID: 0x8801 -- 摄像头立即拍摄命令**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|channel_id|int|通道ID, 值大于零|
|shooting_order|int|拍摄命令: 0 - 停止拍摄, 0xFFFF - 录像, 0x0001~0xFFFE - 拍照张数|
|working_time|int|拍摄间隔/录像时间, 单位秒(s), 0表示按最小间隔拍照或一直录像|
|save_flag|int|保存标志: 1 - 保存, 0 - 实时上传|
|resolution|int|分辨率:<br>0x00 - 最低分辨率<br>0x01 - 320 × 240<br>0x02 - 640 × 480<br>0x03 - 800 × 600<br>0x04 - 1024 × 768<br>0x05 - 176 × 144;[Qcif];<br>0x06 - 352 × 288;[Cif];<br>0x07 - 704 × 288;[HALF D1];<br>0x08 - 704 × 576;[D1]<br>0xFF - 最高分辨率|
|quality|int|图像/视频质量, 取值范围1~10, 1代表质量损失最小, 10代表压缩比最大|
|brightness|int|亮度, 0~255|
|contrast|int|对比度, 0~127|
|saturation|int|饱和度, 0~127|
|chroma|int|色度, 0~255|

> 若终端不支持系统要求的分辨率, 则取最接近的分辨率拍摄上传

**应答消息:** 该消息需使用`jtt808.driving_record_data_upload`接口进行应答

### **消息ID: 0x8802 -- 存储多媒体数据检索**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|media_type|int|多媒体类型:<br>0 - 图像, <br>1 - 音频, <br>2 - 视频|
|channel_id|int|通道ID, 0表示检索该媒体类型的所有通道|
|event_code|int|事件项编码:<br>0 - 平台下发指令<br>1 - 定时动作<br>2 - 抢劫报警触发<br>3 - 碰撞侧翻报警触发<br>其他保留|
|start_time|str|起始时间: YYMMDDhhmmss|
|end_time|str|结束时间: YYMMDDhhmmss|

**应答消息:** 该消息需使用`jtt808.stored_media_data_retrieval_response`接口进行应答

### **消息ID: 0x8803 -- 存储多媒体数据上传命令**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|media_type|int|多媒体类型:<br>0 - 图像, <br>1 - 音频, <br>2 - 视频|
|channel_id|int|通道ID|
|event_code|int|事件项编码:<br>0 - 平台下发指令<br>1 - 定时动作<br>2 - 抢劫报警触发<br>3 - 碰撞侧翻报警触发<br>其他保留|
|start_time|str|起始时间: YYMMDDhhmmss|
|end_time|str|结束时间: YYMMDDhhmmss|
|delete_flag|int|删除标志: 0 - 保留, 1 - 删除|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8804 -- 录音开始命令**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|recording_cmd|int|录音命令: 0 - 停止录音, 1 - 开始录音|
|recording_time|int|录音时间: 单位为秒(s), 0 标识一直录音|
|save_flag|int|保存标志: 0 - 实时上传, 1 - 本地存储|
|audio_sample_rate|int|音频采样率: 0 - 8K, 1 - 11K, 2 - 23K, 3 - 32K|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8805 -- 单挑存储多媒体数据检索上传命令**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|media_id|int|多媒体ID|
|delete_flag|int|删除标志: 0 - 保留, 1 - 删除|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8900 -- 数据下行透传**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|data_type|int|透传消息类型:<br>0x00 - GNSS模块详细定位数据<br>0x0B - 道路运输证IC卡信息<br>0x41 - 串口1透传<br>0x42 - 串口2透传<br>0xF0~0xFF - 用户自定义消息|
|data|str|透传消息内容|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答

### **消息ID: 0x8A00 -- 平台RSA公钥**

**消息体`data`:**

|KEY|VALUE值类型|说明|
|:---|---|---|
|e|int|平台RSA公钥{e, n}中的e|
|n|str|平台RSA公钥{e, n}中的n|

**应答消息:** 该消息需使用`jtt808.general_answer`接口进行应答
