# Instruction Manual

[中文](../zh/使用说明手册.md) | English

**Note:**

- The project only provides JT/T808 protocol client-side functionality , the server needs to dock the server provided by the three parties , or build their own open-source server to use .
- The project only provides a functional interface, the specific use of business needs to be developed separately.
- JT/T808 protocol requires the sending of failed data storage and retransmission, the project does not fail to store data, need to realize the failure of the business layer data storage and retransmission.
- Heartbeat will start automatically after the success of the authentication interface, no need to manually start the heartbeat.
- The downstream data and interrupt request response on the server side are processed through the `set_callback` function to register the callback function.

## Instructions For Use

### 1. Parameter Configuration

#### 1.1 Terminal Parameter Configuration Settings

```python
from usr.jt_message import TerminalParams

# Terminal Parameter Initialization
TerminalParamsObj = TerminalParams()
# Primary Server Address
TerminalParamsObj.set_params(0x0013, "220.180.239.212:7611")
# Terminal heartache sending interval
TerminalParamsObj.set_params(0x0001, 60)
# TCP message response timeout
TerminalParamsObj.set_params(0x0002, 30)
# Range of illegal driving hours
TerminalParamsObj.set_params(0x0032, 8, 12, 17, 30)
# Terminal parameter information,
# value value is used for service processing,
# hex value is used for reporting to server side
param_data = TerminalParamsObj.get_params()
print(param_data)
# {50: {'value': (8, 12, 17, 30), 'hex': '8C111E'}, 1: {'value': 60, 'hex': '0000003C'}, 2: {'value': 30, 'hex': '0000001E'}, 19: {'value': '220.180.239.212:7611', 'hex': '3232302E3138302E3233392E3231323A37363131'}}
```

#### 1.2 Positioning Status Configuration Settings

```python
from usr.jt_message import LocStatusConfig

LocStatusConfigObj = LocStatusConfig()
# Set ACC Enabled
LocStatusConfigObj.set_config("acc_onoff", 1)
# Set Positioning Enabled
LocStatusConfigObj.set_config("loc_status", 1)
# Set the direction of latitude to north
LocStatusConfigObj.set_config("NS_latitude", 0)
# Set the direction of longitude to East
LocStatusConfigObj.set_config("EW_longitude", 0)
```

#### 1.3 Positioning Alarm Configuration Settings

```python
from jt_message import LocAlarmWarningConfig

LocAlarmWarningConfigObj = LocAlarmWarningConfig()

# Speeding Alarm
name = "over_speed_alarm"
onoff = 1
shield_switch = 1
sms_switch = 1
shoot_switch = 1
shoot_store = 1
key_sign = 1
LocAlarmWarningConfigObj.set_alarm(name, onoff, shield_switch, sms_switch, shoot_switch, shoot_store, key_sign)

# Fatigue Driving Alarm
name = "fatigue_driving_alarm"
onoff = 1
shield_switch = 1
sms_switch = 1
shoot_switch = 1
shoot_store = 1
key_sign = 1
LocAlarmWarningConfigObj.set_alarm(name, onoff, shield_switch, sms_switch, shoot_switch, shoot_store, key_sign)
```

#### 1.4 Additional Positioning Configuration Settings

```python
from jt_message import LocAdditionalInfoConfig

LocAdditionalInfoConfigObj = LocAdditionalInfoConfig()
# Set vehicle mileage
LocAdditionalInfoConfigObj.set_mileage(101)
# Set number of vehicle fuel
LocAdditionalInfoConfigObj.set_oil_quantity(50)
# Set the speed
LocAdditionalInfoConfigObj.set_speed(60)
# Set Vehicle Tire Pressure
values = [240, 240, 235, 230]
LocAdditionalInfoConfigObj.set_tire_pressure(values)
```

### 2. Connection Initialization

#### 2.1. Function Initialization

```python
from usr.jtt808 import JTT808

ip = "220.180.239.212"
port = 7611
method = "TCP"
version = "2019"
client_id = "18888888888"

jtt808_obj = JTT808(ip=ip, port=port, method=method, version=version, client_id=client_id)
```

#### 2.2. Registering Callback Function

```python
def test_callback(args):
    header = args["header"]
    data = args["data"]
    # TODO: Different answer processing according to different messages.
    pass

res = jtt808_obj.set_callback(test_callback)
print(res)
# True
```

#### 2.3. Connecting To The Server

```python
conn_res = jtt808_obj.connect()
print(conn_res)
# True
```

#### 2.4. Setting Up Message Encryption

- This function requires the server to send the server public key information before the setting can take effect.

```python
from usr.jtt808 import GENERAL_ANSWER_MSG_ID

def test_callback(args):
    header = args["header"]
    data = args["data"]
    # GENERAL_ANSWER_MSG_ID contains the IDs of all server-side messages that use the generic response.
    if header["message_id"] in GENERAL_ANSWER_MSG_ID:
        # TODO: Answer after business processing based on different messages.
        jtt808_obj.general_answer(header["serial_no"], header["message_id"])
    # TODO: If the message ID is not in GENERAL_ANSWER_MSG_ID,
    # you need to answer the message according to the corresponding answer interface,
    # see API documentation for details.

res = jtt808_obj.set_callback(test_callback)
print(res)
# True
```

### 3. Terminal Registration & Authentication

#### 3.1. Terminal Registration

```python
import uos
import modem
from usr.jt_message import LicensePlateColor

province_id = "34"
city_id = "0100"
manufacturer_id = "quectel"
terminal_model = uos.uname()[0].split("=")[1]
terminal_id = modem.getDevImei()
license_plate_color = LicensePlateColor.blue
license_plate = "A88888"

register_res = jtt808_obj.register(province_id, city_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, license_plate)
print(register_res)
# {'registration_result': 0, 'serial_no': 0, 'auth_code': '865306057798238'}
```

#### 3.2. Terminal Authentication

```python
import modem

auth_code = "865306057798238"
imei = modem.getDevImei()
app_version = "v1.0.0"
res = jtt808_obj.authentication(auth_code, imei, app_version)
print(res)
# {'message_id': 258, 'serial_no': 1, 'result_code': 0}
```

### 4. Terminal-Server Information Interaction

#### 4.1. Send Heartbeat

- Periodically timed sends.

```python
heart_beat_res = tt808_obj.heart_beat()
print(heart_beat_res)
# True
```

#### 4.2. Query Server Time

```python
res = jtt808_obj.query_server_time()
print(res)
# {'utc_time': '2022-06-17 08:25:44'}
```

#### 4.3. Generate and Report Location Information

```python
import utime
from usr.jt_message import LocAlarmWarningConfig, LocStatusConfig, LocAdditionalInfoConfig

def test_init_loction_data():
    LocStatusConfigObj = LocStatusConfig()
    for key in LocStatusConfigObj._loc_cfg_offset.__dict__.keys():
        LocStatusConfigObj.set_config(key, 1)

    LocAlarmWarningConfigObj = LocAlarmWarningConfig()

    LocAdditionalInfoConfigObj = LocAdditionalInfoConfig()
    LocAdditionalInfoConfigObj.set_mileage(100)
    LocAdditionalInfoConfigObj.set_oil_quantity(32.5)
    LocAdditionalInfoConfigObj.set_speed(0)

    alarm_flag = LocAlarmWarningConfigObj.value()
    loc_status = LocStatusConfigObj.value()
    latitude = 31.824845156501
    longitude = 117.24091089413
    altitude = 120
    speed = 0
    direction = 0
    time = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(*(utime.localtime()[:6]))[2:]
    loc_additional_info = LocAdditionalInfoConfigObj.value()

    return (alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time, loc_additional_info)

loc_data = test_init_loction_data()
response_msg_id = None
response_serial_no = None
args = [response_msg_id, response_serial_no]
args.extend(list(loc_data))
res = jtt808_obj.loction_report(*args)
print(res)
# {'message_id': 512, 'serial_no': 3, 'result_code': 0}
```

#### 4.4. Bulk Reporting of Location Information

```python
loc_data = test_init_loction_data()
loc_datas = [loc_data] * 10
data_type = 0
res = jtt808_obj.location_bulk_report(data_type, loc_datas)
print(res)
# {'message_id': 1796, 'serial_no': 4, 'result_code': 0}
```

#### 4.5. Incident Reporting

```python
# event id from server message 0x8301 set event.
event_id = 12
res = jtt808_obj.event_report(event_id)
print(res)
# {'message_id': 769, 'serial_no': 5, 'result_code': 0}
```

#### 4.6. Reporting of Escalation Results

```python
upgrade_type = 0
result_code = 0
res = jtt808_obj.upgrade_result_report(upgrade_type, result_code)
print(res)
# {'message_id': 264, 'serial_no': 6, 'result_code': 0}
```

#### 4.7. Electronic Waybill Reporting

```python
with open("/path/xxx.xxx", "rb") as f:
    data = f.read()
    res = jtt808_obj.electronic_waybill_report(data)
    print(res)
# {'message_id': 1793, 'serial_no': 7, 'result_code': 0}
```

#### 4.8. Information on Demand / Cancel

```python
# info type from server message 0x8303, information on demand menu settings.
info_type = 12
# 1 - demand, 0 - cancel
onoff = 1
res = jtt808_obj.information_demand_cancellation(info_type, onoff)
print(res)
# {'message_id': 771, 'serial_no': 8, 'result_code': 0}
```

#### 4.9. CAN Bus Data Upload

```python
recive_time = ("{:2d}" * 3 + "0000").format(*(utime.localtime()[3:6]))
can_channel_no = 0
frame_type = 0
collection_method = 0
can_id = 0
can_data = "123"
can_datas = [(can_channel_no, frame_type, collection_method, can_id, can_data)] * 3
res = jtt808_obj.can_bus_data_upload(recive_time, can_datas)
print(res)
# {'message_id': 1797, 'serial_no': 9, 'result_code': 0}
```

#### 4.10. Multimedia Event Upload

```python
media_id = 12
media_type = 0
media_encoding = 0
event_id = 4
channel_id = 1
res = jtt808_obj.media_event_upload(media_id, media_type, media_encoding, event_id, channel_id)
print(res)
# {'message_id': 2048, 'serial_no': 10, 'result_code': 0}
```

#### 4.11. Multimedia Data Upload

```python
media_id = 14
media_type = 0
media_encoding = 0
event_id = 4
channel_id = 1
with open("/xxx/xxx.xxx", "rb") as f:
    media_data = f.read()
    loc_data = test_init_loction_data()[:-1]
    res = jtt808_obj.media_data_upload(media_id, media_type, media_encoding, event_id, channel_id, media_data, loc_data)
    print(res)
# {'message_id': 2049, 'serial_no': 11, 'result_code': 0}
```

#### 4.12. Data Uplink Passthrough

```python
data_type = 0
data = "123456"
res = jtt808_obj.data_uplink_transparent_transmission(data_type, data)
print(res)
# {'message_id': 2304, 'serial_no': 12, 'result_code': 0}
```

#### 4.13. Data Compression Reporting

```python
with open("/xxx/xxx.xxx", "rb") as f:
    data = f.read()
    res = jtt808_obj.data_compression_report(data)
    print(res)
# {'message_id': 2305, 'serial_no': 13, 'result_code': 0}
```

#### 4.14. Endpoint RSA Public Key Reporting

```python
e = 65537
n = "10923252007875538132171701535639644200191641194610072563985760225688326844567094363074" \
    "389543489252121216915728771174747297043916958910473388186667405361889"
res = jtt808_obj.terminal_rsa_public_key(e, n)
print(res)
# {'message_id': 2560, 'serial_no': 14, 'result_code': 0}
```
