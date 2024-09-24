# API Reference

[中文](../zh/API参考手册.md) | English

## 1. Eenumeration Parameter

### 1.1 LicensePlateColor

- This class enumerates the corresponding code of the license plate color in the JT/T 697.7--2014 document, **this code is used for the license plate color parameter in the terminal registration**.

| Color      | Code     |
| :----------| ---------|
| blue       | 1        |
| yellow     | 2        |
| black      | 3        |
| white      | 4        |
| green      | 5        |
| other      | 9        |

**Examples:**

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

- The code corresponding to the terminal's generic response result.

| Result         | Code     |
| :--------------| ---------|
| success        | 0        |
| failure        | 1        |
| message_error  | 2        |
| not_support    | 3        |

**Examples:**

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

## 2. Configuration Parameter Management

### 2.1 TerminalParams

- The Terminal Configuration Parameters class, which is used to record terminal configuration parameters and convert the parameter values into byte stream data as specified by the protocol.

```python
from jt_message import TerminalParams

TerminalParamsObj = TerminalParams()
```

#### TerminalParams.set_params

- Set configuration parameters and parameter values.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|param_id|int|Parameter ID|
|param_value|tuple|Parameter values, different parameter IDs, the number of parameter values passed in is not the same, the specific parameter ID corresponding to the parameter value see the following table|

**Parameter ID Corresponds to Parameter Value:**

|Parameter ID|Parameter Values|Parameter Value Type|Description and Requirements|
|---|---|---|---|
|0x0001|(value,)|(int,)|Terminal heartbeat sending interval, unit: second|
|0x0002|(value,)|(int,)|TCP message response timeout in seconds.|
|0x0003|(value,)|(int,)|TCP message retransmission count|
|0x0004|(value,)|(int,)|UDP message response timeout, in seconds.|
|0x0005|(value,)|(int,)|UDP message retransmission count|
|0x0006|(value,)|(int,)|SMS message response timeout, in seconds.|
|0x0007|(value,)|(int,)|SMS message retransmission count|
|0x0010|(value,)|(str,)|Primary server APN, dial-up access point for wireless communication, or PPP dialing number if the network format is CDMA|
|0x0011|(value,)|(str,)|Master server wireless communication dial-up user name|
|0x0012|(value,)|(str,)|Master server wireless communication dialing password|
|0x0013|(value,)|(str,)|JT/T808--2019:<br>The main server address, IP or domain name, separate the host and port with a colon, multiple servers are separated by semicolons<br>JT/T808--2013:<br>The main server address, IP or domain name|
|0x0014|(value,)|(str,)|Backup server APN|
|0x0015|(value,)|(str,)|Backup server wireless communication dial-up user name|
|0x0016|(value,)|(str,)|Backup server wireless communication dialing password|
|0x0017|(value,)|(str,)|JT/T808--2019:<br>Backup server address, IP or domain name, separate the host and port with a colon, multiple servers are separated by semicolons<br>JT/T808--2013:<br>Backup server address, IP or domain name|
|0x0018|(value,)|(int,)|JT/T808--2013: server TCP port<br>JT/T808--2019: merged to 0x0013|
|0x0019|(value,)|(int,)|JT/T808--2013: server UDP port<br>JT/T808--2019: merged to 0x0013|
|0x001A|(value,)|(str,)|Road Transportation Certificate IC Card Authentication Master Server IP Address or Domain Name|
|0x001B|(value,)|(int,)|Road Transportation Certificate IC Card Authentication Master Server TCP Port|
|0x001C|(value,)|(int,)|Road Transportation Certificate IC Card Authentication Master Server UDP Port|
|0x001D|(value,)|(str,)|Road Transportation License IC card authentication backup server IP address or domain name, port is the same as the main server port|
|0x0020|(value,)|(int,)|Location reporting strategy<br>0 - Scheduled reporting<br>1 - Regular interval reporting<br>2 - Scheduled and regular interval reporting|
|0x0021|(value,)|(int,)|Location reporting scheme<br>0 - Based on ACC status<br>1 - Based on login status and ACC status, first determine login status, if logged in then based on ACC status|
|0x0022|(value,)|(int,)|Driver not logged in reporting interval, in seconds, greater than 0|
|0x0023|(value,)|(str,)|APN of the slave server, if this value is null, the terminal should use the same configuration as the master server|
|0x0024|(value,)|(str,)|Dial-up user name for wireless communication from the server, if this value is empty, the terminal should use the same configuration as the master server|
|0x0025|(value,)|(str,)|Slave server wireless communication dialing password, if this value is empty, the terminal should use the same configuration of the master server|
|0x0026|(value,)|(str,)|Backup addresses, IPs, or domain names from servers, separated by colons for hosts and ports, and semicolons for multiple servers|
|0x0027|(value,)|(int,)|Reporting interval when sleeping, in seconds, greater than 0|
|0x0028|(value,)|(int,)|Reporting time interval for emergency alarm, unit: second, greater than 0|
|0x0029|(value,)|(int,)|Default time reporting interval, in seconds, greater than 0|
|0x002C|(value,)|(int,)|Default distance reporting interval in meters, greater than 0|
|0x002D|(value,)|(int,)|Driver not logged in reporting distance interval, in meters, greater than 0|
|0x002E|(value,)|(int,)|Reporting distance interval when dormant, in meters, greater than 0|
|0x002F|(value,)|(int,)|Reporting Distance Interval for Emergency Alarms, in meters, greater than 0|
|0x0030|(value,)|(int,)|Corner complementary transmission angle, less than 180°|
|0x0031|(value,)|(int,)|Electronic fence radius (illegal displacement threshold) in meters|
|0x0032|(start_hour, start_minute, end_hour, end_minute)|(int, int, int, int)|The range of illegal driving periods is accurate to the minute. <br>start_hour: The hour part of the illegal driving start time;<br>start_minute: The minute part of the illegal driving start time;<br>end_hour: The hour part of the illegal driving end time;<br>end_minute: The minute part of the illegal driving end time Part;<br>Example: (22, 50, 10, 30), indicating that the illegal driving period is from 10:50 pm that day to 10:30 am the next day.|
|0x0040|(value,)|(str,)|Monitoring platform phone number|
|0x0041|(value,)|(str,)|Reset phone number, which can be used to call the terminal to reset it.|
|0x0042|(value,)|(str,)|Factory reset phone number, which can be used to call the terminal to restore its factory settings|
|0x0043|(value,)|(str,)|Monitoring platform SMS phone number|
|0x0044|(value,)|(str,)|Receiving terminal SMS text alarm number|
|0x0045|(value,)|(int,)|Terminal phone answer policy<br>0: Automatic answer<br>1: Automatic answer when ACC ON, manual answer when OFF|
|0x0046|(value,)|(int,)|Maximum duration of each call in seconds, 0 for no calls allowed, 0xFFFFFFFF for no limitations|
|0x0047|(value,)|(int,)|Maximum talk time for the month in seconds, 0 is no talk allowed, 0xFFFFFFFF is unlimited|
|0x0048|(value,)|(str,)|listen in on telephone numbers|
|0x0049|(value,)|(str,)|Supervisory Platform Privileged SMS Number|
|0x0050|(value,)|(int,)|Alarm blocking word, corresponds to the alarm flag in the position information report message, if the corresponding bit is 1, the corresponding alarm is blocked.|
|0x0051|(value,)|(int,)|Alarm send text SMS switch, corresponds to the alarm flag in the position information report message, the corresponding bit is 1 to send text SMS for the corresponding alarm.|
|0x0052|(value,)|(int,)|Alarm shooting switch, corresponds to the alarm flag in the position information report message, the corresponding bit is 1, then the camera shoots at the corresponding alarm.|
|0x0053|(value,)|(int,)|Alarm shooting storage flag, corresponds to the alarm flag in the position information reporting message, if the corresponding bit is 1, then the photo of the corresponding alarm license plate will be stored, otherwise, real-time long-distance transmission.|
|0x0054|(value,)|(int,)|Key flag, corresponds to the alarm flag in the position information report message, the corresponding bit is 1, then the corresponding alarm is a key alarm.|
|0x0055|(value,)|(int,)|Maximum speed in km/h|
|0x0056|(value,)|(int,)|Overdrive duration in seconds|
|0x0057|(value,)|(int,)|Continuous driving time threshold in seconds|
|0x0058|(value,)|(int,)|Cumulative driving time threshold for the day, in seconds|
|0x0059|(value,)|(int,)|Minimum rest time in seconds|
|0x005A|(value,)|(int,)|Maximum stopping time in seconds|
|0x005B|(value,)|(int,)|Difference in speed warning, in 1/10 km/h|
|0x005C|(value,)|(int,)|Fatigue Driving Warning Difference in seconds, value greater than zero|
|0x005D|(millisecond, acceleration)|(int, int)|Collision alarm parameter settings:<br>millisecond: for the collision time, unit: milliseconds; <br>acceleration: for the collision acceleration, unit: 0.1g, set range 0 ~ 79, default: 10|
|0x005E|(value,)|(int,)|Rollover alarm parameter setting: rollover angle, unit: degree, default: 30°.|
|0x0064|(camera_1_onoff, camera_2_onoff, camera_3_onoff, camera_4_onoff, camera_5_onoff, camera_1_storage, camera_2_storage, camera_3_storage, camera_4_storage, camera_5_storage, unit, interval)|(int, int, int, int, int, int, int, int, int, int, int, int)|Timing photo control: <br>camera_1_onoff: camera channel 1 timing switch flag, 0 - off, 1 - on; <br>camera_2_onoff: camera channel 2 timing switch flag, 0 - off, 1 - on; <br>camera_3_onoff: camera Channel 3 timing switch flag, 0 - off, 1 - on;<br>camera_4_onoff: Camera channel 4 timing switch flag, 0 - off, 1 - on;<br>camera_5_onoff: Camera channel 5 timing switch flag, 0 - off, 1 - on; <br>camera_1_storage: camera channel 1 scheduled storage flag, 0 - storage, 1 - upload; <br>camera_2_storage: camera channel 2 scheduled storage flag, 0 - storage, 1 - upload; <br>camera_3_storage: camera Channel 3 scheduled storage flag, 0 - storage, 1 - upload; <br>camera_4_storage: camera channel 4 scheduled storage flag, 0 - storage, 1 - upload; <br>camera_5_storage: camera channel 5 scheduled storage flag, 0 - storage, 1 - upload; <br>unit: timing time unit: 0 - second, when the value is less than 5 seconds, the terminal processes it in 5 seconds; 1 - minute; <br>interval: timing interval, receive parameter settings or restart later execution;|
|0x0065|(camera_1_onoff, camera_2_onoff, camera_3_onoff, camera_4_onoff, camera_5_onoff, camera_1_storage, camera_2_storage, camera_3_storage, camera_4_storage, camera_5_storage, unit, interval)|(int, int, int, int, int, int, int, int, int, int, int, int)|Fixed distance photo control: <br>camera_1_onoff: camera channel 1 timing switch flag, 0 - off, 1 - on; <br>camera_2_onoff: camera channel 2 timing switch flag, 0 - off, 1 - on; <br>camera_3_onoff: Camera channel 3 timing switch flag, 0 - off, 1 - on;<br>camera_4_onoff: Camera channel 4 timing switch flag, 0 - off, 1 - on;<br>camera_5_onoff: Camera channel 5 timing switch flag, 0 - off , 1 - on; <br>camera_1_storage: camera channel 1 scheduled storage flag, 0 - storage, 1 - upload; <br>camera_2_storage: camera channel 2 scheduled storage flag, 0 - storage, 1 - upload; <br>camera_3_storage: Camera channel 3 scheduled storage flag, 0 - storage, 1 - upload; <br>camera_4_storage: camera channel 4 scheduled storage flag, 0 - storage, 1 - upload; <br>camera_5_storage: camera channel 5 scheduled storage flag, 0 - storage , 1 - upload; <br>unit: fixed distance unit: 0 - meter, when the value is less than 100m, the terminal treats it as 100m; 1 - kilometers; <br>interval: fixed distance interval, received parameter setting or Execute after restart;|
|0x0070|(value,)|(int,)|Image / video quality, 1 - 10, 1 maximum quality|
|0x0071|(value,)|(int,)|Brightness, setting range 0 - 255|
|0x0072|(value,)|(int,)|Contrast, setting range 0 - 127|
|0x0073|(value,)|(int,)|Saturation, setting range 0 - 127|
|0x0074|(value,)|(int,)|Chromaticity, setting range 0 - 255|
|0x0080|(value,)|(int,)|Vehicle odometer reading, 1/10 kilometer|
|0x0081|(value,)|(int,)|ID of the province where the vehicle is located|
|0x0082|(value,)|(int,)|Municipal ID where the vehicle is located|
|0x0083|(value,)|(str,)|Motor vehicle number plates issued by the Public Security Traffic Management Department|
|0x0084|(value,)|(int,)|License plate color, in accordance with the provisions of JT/T697.7-2014, unlicensed vehicles fill in 0|
|0x0090|(gps_onoff, bds_onoff, glonass_onoff, galileo_onoff)|(int, int, int, int)|GNSS positioning mode, defined as follows:<br>gps_onoff: 0 - disable GPS positioning, 1 - enable GPS positioning, <br>bds_onoff: 0 - disable Beidou positioning, 1 - enable Beidou positioning; <br>glonass_onoff: 0 - disable GLONASS Positioning, 1 - Enable GLONASS positioning;<br>galileo_onoff: 0 - Disable Galileo positioning, 1 - Enable Galileo positioning;|
|0x0091|(value,)|(int,)|GNSS baud rate, defined as follows:<br>0x00 - 4800;<br>0x01 - 9600;<br>0x02 - 19200;<br>0x03 - 38400;<br>0x04 - 57600;<br>0x05 - 115200;|
|0x0092|(value,)|(int,)|The detailed positioning data output frequency of the GNSS module is defined as follows:<br>0x00 - 500ms;<br>0x01 - 1000ms (default value);<br>0x02 - 2000ms;<br>0x03 - 3000ms;<br>0x04 - 4000ms;|
|0x0093|(value,)|(int,)|GNSS Module Detailed Positioning Data Acquisition Frequency in seconds, default: 1|
|0x0094|(value,)|(int,)|GNSS module detailed positioning data upload method:<br>0x00 - local storage, no upload (default value);<br>0x01 - upload by time interval;<br>0x02 - upload by distance interval;<br>0x0B - by accumulation Time upload, automatically stop uploading when the transmission time is reached;<br>0x0C - Upload based on cumulative distance, automatically stop uploading after reaching the distance;<br>0x0D - Upload based on cumulative number of items, automatically stop uploading when the number of uploaded items is reached;|
|0x0095|(value,)|(int,)|GNSS module detailed positioning data upload settings:<br>When the upload method is 0x01, the unit is: seconds;<br>When the upload method is 0x02, the unit is: meters;<br>When the upload method is 0x0B, the unit is: seconds;<br> When the upload method is 0x0C, the unit is: meters;<br>When the upload method is 0x0D, the unit is: strips;|
|0x0100|(value,)|(int,)|CAN bus channel 1 Acquisition interval in milliseconds, 0 means no acquisition|
|0x0101|(value,)|(int,)|CAN bus channel 1 upload interval, unit: second, 0 means no upload|
|0x0102|(value,)|(int,)|CAN bus channel 2 acquisition interval in milliseconds, 0 means no acquisition|
|0x0103|(value,)|(int,)|CAN bus channel 2 upload interval, unit: second, 0 means no upload|
|0x0110|(can_bus_id, collection_method, frame_type, can_channel_no, collection_time_interval)|(int, int, int, int, int)|CAN bus ID separate collection settings: <br>collection_time_interval represents the ID collection time interval in milliseconds, 0 represents no collection; <br>can_channel_no represents the CAN channel number, 0: CAN1, 1: CAN2; <br>frame_type represents the frame type, 0 : Standard frame, 1: Extended frame;<br>collection_method represents the data collection method, 0: original data, 1: calculated value of collection interval;<br>can_bus_id represents CAN bus ID|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
TerminalParamsObj.set_params(0x0001, *(60,))
TerminalParamsObj.set_params(0x0013, *("127.0.0.1:8001;127.0.0.1:8002",))
TerminalParamsObj.set_params(0x0032, *(22, 50, 10, 30))
```

#### TerminalParams.get_params

- Get the set terminal configuration parameters.

**Return Value:**

|Data type|Description|
|:---|---|
|dict|key: parameter ID<br>value: parameter value dictionary<br> - key: `value`, value: int / str numerical value, <br> - key: `hex`, value: string hexadecimal data, use Send in message|

**Examples:**

```python
params_data = TerminalParamsObj.get_params()
print(params_data):
# {1: {"value": 60, "hex": "0000003C"}, 50: {"value": (22, 50, 10, 30), "hex": "16320A1E"}, 19: {"value": "127.0.0.1:8001;127.0.0.1:8002", "hex": "3132372E302E302E313A383030313B3132372E302E302E313A38303032"}}
```

#### TerminalParams.del_params

- Delete configuration parameters.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|param_id|int|Parameter ID|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
TerminalParamsObj.del_params(0x0001)
```

### 2.2 LocStatusConfig

- Positioning status information configuration.

**Positioning Status Information Table:**

|Encoding|Data type|Description|
|---|---|---|
|acc_onoff|int|ACC switch status: 0 - off, 1 - on|
|loc_status|int|Whether to locate: 0 - not positioned, 1 - positioned|
|NS_latitude|int|Latitude direction: 0 - North, 1 - South|
|EW_longitude|int|Longitude direction: 0 - East, 1 - West|
|operational_status|int|Operational status: 0 - operational, 1 - out of service|
|long_lat_encryption|int|Whether the latitude and longitude is confidential and the plug-in is encrypted: 0 - unencrypted, 1 - encrypted|
|forward_collision_warning|int|0 - None, 1 - Forward collision warning collected by emergency braking system|
|lane_departure_warning|int|0 - None, 1 - Lane Departure Warning|
|load_status|int|Vehicle loading status: 0x00 - Empty, 0x01 - Half loaded, 0x10 - Reserved, 0x11 - Fully<br> It can identify the empty status of passenger cars, the empty and full status of heavy trucks and trucks, this status can be input manually or by sensors Obtain|
|vehicle_oil_status|int|Vehicle oil line status: 0 - normal, 1 - disconnected|
|vehicle_circuit_status|int|Vehicle circuit status: 0 - OK, 1 - Disconnected|
|door_lock|int|Door lock status: 0 - unlocked, 1 - locked|
|door_1_status|int|Door 1 status: 0 - closed, 1 - open|
|door_2_status|int|Door 2 status: 0 - closed, 1 - open|
|door_3_status|int|Door 3 status: 0 - closed, 1 - open|
|door_4_status|int|Door 4 status: 0 - closed, 1 - open|
|door_5_status|int|Door 5 status: 0 - closed, 1 - open|
|gps_onoff|int|Whether to use GPS satellites for positioning: 0 - No, 1 - Yes|
|bds_onoff|int|Whether to use Beidou satellites for positioning: 0 - No, 1 - Yes|
|glonass_onoff|int|Whether to use GLONASS satellites for positioning: 0 - no, 1 - yes|
|galileo_onoff|int|Whether to use Galileo satellites for positioning: 0 - no, 1 - yes|
|running_status|int|Vehicle status: 0 - stopped, 1 - driving|

```python
from usr.jt_message import LocStatusConfig

LocStatusConfigObj = LocStatusConfig()
```

#### LocStatusConfig.set_config

- Set the specified positioning status configuration information.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|name|str|Encoding, see `Positioning Status Information Table` for details|
|value|int|Parameter values, see `Positioning Status Information Table` for details, all data defaults to 0|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
LocStatusConfigObj.set_config("acc_onoff", 1)
# True
LocStatusConfigObj.set_config("loc_status", 1)
# True
```

#### LocStatusConfig.get_config

- Get the specified positioning status configuration information value.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|name|str|Encoding, see `Positioning Status Information Table` for details|

**Return Value:**

|Data type|Description|
|:---|---|
|int|For the specific meaning, see `Positioning Status Information Table`|

**Examples:**

```python
acc_onoff = LocStatusConfigObj.get_config("acc_onoff")
print(acc_onoff)
# 1
loc_status = LocStatusConfigObj.get_config("loc_status")
print(loc_status)
# 1
```

#### LocStatusConfig.value

- Obtain all positioning status configuration information, which has been converted into integers according to the protocol and is used for positioning information reporting interface.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|int|Integer value|

**Examples:**

```python
loc_status_cfg = LocStatusConfigObj.value()
print(loc_status_cfg)
# 3
```

### 2.3 LocAlarmWarningConfig

- Configure location alarm parameters.

**Positioning Alarm Parameter List:**

|Alarm code|Definition|Processing instructions|
|---|---|---|
|emergency_alarm|1: emergency alarm, triggered after touching the alarm switch|cleared after receiving the response|
|over_speed_alarm|1: Overspeed alarm|The flag remains until the alarm condition is contacted|
|fatigue_driving_alarm|1: Fatigue driving alarm|The flag remains until the alarm condition is contacted|
|dangerous_driving_behaviour_alarm|1: Dangerous driving behavior alarm|The sign remains until the alarm condition is contacted|
|gnss_module_failure_alarm|1: The GNSS module sends a fault alarm |The flag is maintained until the alarm condition is contacted|
|gnss_antenna_disconnection_alarm|1: The GNSS antenna is not connected or is cut short and the alarm|flag is maintained until the alarm condition is contacted|
|gnss_antenna_short_circuit_alarm|1: GNSS antenna short circuit alarm|The flag remains until the alarm condition is contacted|
|terminal_main_power_supply_undervoltage_alarm|1: Terminal main power undervoltage alarm|The flag remains until the alarm condition is contacted|
|terminal_main_power_failure_alarm|1: Terminal main power failure alarm |The flag remains until the alarm condition is contacted|
|terminal_lcd_or_display_failure_alarm|1: Terminal LCD or display alarm |The flag remains until the alarm condition is contacted|
|tts_module_fault_alarm|1: TTS module fault alarm|The flag remains until the alarm condition is contacted|
|camera_failure_alarm|1: Camera failure alarm|The flag remains until the alarm condition is contacted|
|road_transport_license_ic_card_module_fault_alarm|1: Road Transport License IC card module fault alarm|The flag is maintained until the alarm condition is contacted|
|over_speed_warning|1: Overspeed warning|The sign remains until the alarm condition is contacted|
|fatigue_driving_warning|1: Fatigue driving warning|The sign remains until the alarm condition is contacted|
|illegal_driving_alarm|1: Violation form alarm|The sign is maintained until the alarm condition is contacted|
|tire_pressure_warning|1: Tire pressure warning|The mark remains until the alarm condition is contacted|
|right_turn_blind_spot_abnormal_alarm|1: Right turn blind spot abnormal alarm|The sign is maintained until the alarm condition is contacted|
|cumulative_driving_overtime_alarm_for_the_day|1: Cumulative driving overtime alarm for the day|The flag is maintained until the alarm condition is contacted|
|overtime_parking_alarm|1: Overtime parking alarm|The flag remains until the alarm condition is contacted|
|in_and_out_of_the_area_alarm|1: Alarm in and out of the area|Cleared after receiving response|
|entry_and_exit_route_alarm|1: Entry and exit route alarm|cleared after receiving response|
|insufficient_or_too_long_driving_time_on_the_road_section_alarm|1: Alarm for insufficient/too long driving time on the road section|Cleared after receiving response|
|route_departure_alarm|1: Route deviation alarm|The flag is maintained until the alarm condition is contacted|
|vehicle_vss_failure_alarm|1: Vehicle VSS failure alarm|flag maintained until alarm condition contact|
|vehicle_fuel_abnormality_alarm|1: Abnormal vehicle fuel level alarm|The flag remains until the alarm condition is contacted|
|vehicle_theft_alarm|1: Vehicle theft alarm (via vehicle immobilizer) |The flag remains until the alarm condition is contacted|
|vehicle_illegal_ignition_alarm|1: Vehicle illegal ignition alarm|cleared after receiving response|
|vehicle_illegal_displacement_alarm|1: illegal vehicle displacement alarm|cleared after receiving response|
|collision_rollover_alarm|1: Collision rollover alarm|The flag remains until the alarm condition is contacted|
|rollover_alarm|1: Rollover alarm|The flag remains until the alarm condition is contacted|
|illegal_door_opening_alarm|1: Illegal door opening alarm (when the terminal does not set an area, illegal door opening will not be judged) (JT/T808--2013) |Reset after receiving a response|

```python
from jt_message import LocAlarmWarningConfig

LocAlarmWarningConfigObj = LocAlarmWarningConfig()
```

#### LocAlarmWarningConfig.set_alarm

- Set the specified alarm parameter configuration.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|name|str|Alarm code|
|onoff|int|Alarm trigger: 0 - off, 1 - on, default: 0|
|shield_switch|int|Terminal parameter alarm shield word: 0 - off, 1 - on, default: 0|
|sms_switch|int|Terminal parameter alarm sending text SMS switch: 0 - off, 1 - on, default: 0|
|shoot_switch|int|Terminal parameter alarm shooting switch: 0 - off, 1 - on, default: 0|
|shoot_store|int|Terminal parameter alarm shooting storage flag: 0 - live upload, 1 - local store, default: 1|
|key_sign|int|Terminal parameter key sign: 0 - not key alarm, 1 - key alarm, default: 0|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

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

#### LocAlarmWarningConfig.get_alarm

- Get the specified alarm parameter configuration.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|name|str|Alarm code|

**Return Value:**

|Data type|Description|
|:---|---|
|tuple|(onoff, shield_switch, sms_switch, shoot_switch, shoot_store, key_sign)<br>onoff - alarm trigger<br>shield_switch - alarm shield word<br>sms_switch - alarm sending text SMS switch<br>shoot_switch - alarm shooting switch< br>shoot_store - alarm shooting storage sign<br>key_sign - key sign|

**Examples:**

```python
name = "over_speed_alarm"
alarm_cfg = LocAlarmWarningConfigObj.get_alarm(name)
print(alarm_cfg)
# (1, 1, 1, 1, 1, 1)
```

#### LocAlarmWarningConfig.value

- Get the complete alarm configuration data of the terminal.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|tuple|(onoff, shield_switch, sms_switch, shoot_switch, shoot_store, key_sign)<br>onoff - alarm trigger<br>shield_switch - alarm shield word<br>sms_switch - alarm sending text SMS switch<br>shoot_switch - alarm shooting switch< br>shoot_store - alarm shooting storage sign<br>key_sign - key sign|

**Examples:**

```python
alarms_cfg = LocAlarmWarningConfigObj.value()
print(alarms_cfg)
# (2, 2, 2, 2, 65535, 2)
```

### 2.4 LocAdditionalInfoConfig

- Targeting extension configuration.

```python
from jt_message import LocAdditionalInfoConfig

LocAdditionalInfoConfigObj = LocAdditionalInfoConfig()
```

#### LocAdditionalInfoConfig.set_mileage

- Set the vehicle mileage, corresponding to the vehicle odometer reading, unit: kilometers.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|value|int|Vehicle odometer reading, unit: kilometers|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
LocAdditionalInfoConfigObj.set_mileage(101)
```

#### LocAdditionalInfoConfig.get_mileage

- Get the set vehicle mileage.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|int|Vehicle odometer number, if the number is not set, returns -1, unit: kilometers|

**Examples:**

```python
mileage = LocAdditionalInfoConfigObj.get_mileage()
print(mileage)
# 101
```

#### LocAdditionalInfoConfig.set_oil_quantity

- Set the fuel volume, corresponding to the vehicle fuel gauge reading, unit: liter.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|value|int|Vehicle fuel gauge reading, unit: liters|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
LocAdditionalInfoConfigObj.set_oil_quantity(50)
```

#### LocAdditionalInfoConfig.get_oil_quantity

- Get the set vehicle fuel quantity.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|int|Vehicle fuel gauge number, if the parameter is not set, it returns -1, unit: liter|

**Examples:**

```python
oil_quantity = LocAdditionalInfoConfigObj.get_oil_quantity()
print(oil_quantity)
# 50
```

#### LocAdditionalInfoConfig.set_speed

- Set the vehicle speed, the speed obtained by the form recording function, unit: kilometers/hour.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|value|int|Vehicle speed, unit: kilometers/hour|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
LocAdditionalInfoConfigObj.set_speed(60)
```

#### LocAdditionalInfoConfig.get_speed

- Get the set vehicle speed.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|int|Vehicle speed, if the parameter is not set, it returns -1, unit: kilometers/hour|

**Examples:**

```python
speed = LocAdditionalInfoConfigObj.get_speed()
print(speed)
# 60
```

#### LocAdditionalInfoConfig.set_manually_confirm_the_alarm_event_id

- Set the ID of the alarm event that requires manual confirmation.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|value|int|Alarm event ID|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
LocAdditionalInfoConfigObj.set_manually_confirm_the_alarm_event_id(10)
```

#### LocAdditionalInfoConfig.get_manually_confirm_the_alarm_event_id

- Get the ID of the set alarm event that requires manual confirmation.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|int|Alarm event ID, the parameter is not set and returns -1|

**Examples:**

```python
alarm_event_id = LocAdditionalInfoConfigObj.get_manually_confirm_the_alarm_event_id()
print(alarm_event_id)
# 10
```

#### LocAdditionalInfoConfig.set_tire_pressure

- Set the vehicle tire pressure, unit: Pa. The order of calibrating the wheels is from left to right starting from the front of the car, for example: front left 1, front left 2, front right 1, front right 2, center left 1, center left 2, Center left 3, center right 1, center right 2, center right 3, back left 1, back left 2, back left 3..., and so on.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|values|list|The element is the vehicle tire pressure, the maximum is 254, if it exceeds 254, it is stored as 254, unit: Pa|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
values = [240, 240, 235, 230]
LocAdditionalInfoConfigObj.set_tire_pressure(values)
```

#### LocAdditionalInfoConfig.get_tire_pressure

- Get the set vehicle tire pressure.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|list|The element is vehicle tire pressure. If the parameter is not set, -1 will be returned. Unit: Pa|

**Examples:**

```python
tire_pressure = LocAdditionalInfoConfigObj.get_tire_pressure()
print(tire_pressure)
# [240, 240, 235, 230]
```

#### LocAdditionalInfoConfig.set_temperature

- Set the cabin temperature in degrees Celsius, with a value range of -32767 ~ 32767.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|value|int|Cabin temperature, unit: degrees Celsius|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
LocAdditionalInfoConfigObj.set_temperature(25)
```

#### LocAdditionalInfoConfig.get_temperature

- Get the set cabin temperature.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|int|Carriage temperature, if the parameter is not set, it returns -1, unit: degrees Celsius|

**Examples:**

```python
temperature = LocAdditionalInfoConfigObj.get_temperature()
print(temperature)
# 25
```

#### LocAdditionalInfoConfig.set_over_speed_alarm

- Set additional information for speed alarm.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|loc_type|int|Location type:<br>0 - no specific location<br>1 - circular area<br>2 - rectangular area<br>3 - polygonal area<br>4 - road segment|
|area_segment_id|int|Area or segment ID. If the location type is 0, this field is not passed. If it is not 0, this field must be passed|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
loc_type = 2
area_segment_id = 5
LocAdditionalInfoConfigObj.set_over_speed_alarm(loc_type, area_segment_id)
```

#### LocAdditionalInfoConfig.get_over_speed_alarm

- Get additional information about the set speed alarm.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|dict|key value is as follows:<br>`loc_type` - location type<br>`area_segment_id` - area or segment ID<br>The location type is 0, the value corresponding to this key is None<br>The parameter is not set and returned empty dictionary |

**Examples:**

```python
over_speed_alarm = LocAdditionalInfoConfigObj.get_over_speed_alarm()
print(over_speed_alarm)
# {"loc_type": 2, "area_segment_id": 5}
```

#### LocAdditionalInfoConfig.set_in_out_area_segment_alarm

- Set additional information for entry and exit area / route alarms.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|loc_type|int|Location type:<br>1 - circular area<br>2 - rectangular area<br>3 - polygonal area<br>4 - road segment|
|area_segment_id|int|area or segment ID|
|direction|int|Direction: 0 - in, 1 - out|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
loc_type = 2
area_segment_id = 5
direction = 1
LocAdditionalInfoConfigObj.set_in_out_area_segment_alarm(loc_type, area_segment_id, direction)
```

#### LocAdditionalInfoConfig.get_in_out_area_segment_alarm

- Get additional information about the set entry and exit zone/route alarms.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|dict|key values ​​are as follows:<br>`loc_type` - location type<br>`area_segment_id` - area or segment ID<br>`direction` - direction<br>Parameter not set returns empty dictionary|

**Examples:**

```python
in_out_area_segment_alarm = LocAdditionalInfoConfigObj.get_in_out_area_segment_alarm()
print(in_out_area_segment_alarm)
# {"loc_type": 2, "area_segment_id": 5, "direction": 1}
```

#### LocAdditionalInfoConfig.set_insufficient_or_too_long_driving_time

- Set additional alarm information for insufficient or excessive road segment driving time.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|road_id|int|Road ID|
|travel_time|int|Route segment travel time, unit: seconds|
|result|int|Result: 0 - not enough, 1 - too long|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
road_id = 2
travel_time = 5
result = 1
LocAdditionalInfoConfigObj.set_insufficient_or_too_long_driving_time(road_id, travel_time, result)
```

#### LocAdditionalInfoConfig.get_insufficient_or_too_long_driving_time

- Obtain additional information about the insufficient or excessive driving time of the set road section.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|dict|key values ​​are as follows:<br>`road_id` - road segment ID<br>`travel_time` - road segment travel time<br>`result` - result<br>The parameter is not set and returns an empty dictionary|

**Examples:**

```python
insufficient_or_too_long_driving_time = LocAdditionalInfoConfigObj.get_insufficient_or_too_long_driving_time()
print(insufficient_or_too_long_driving_time)
# {"road_id": 2, "travel_time": 5, "result": 1}
```

#### LocAdditionalInfoConfig.set_vehicle_signal_status

- Set the extended vehicle signal status bit.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|low_beam_lights|int|Low beam signal: 0 - off, 1 - on|
|high_beam|int|High beam signal: 0 - off, 1 - on|
|right_turn|int|Right turn signal: 0 - off, 1 - on|
|left_turn|int|Left turn signal: 0 - off, 1 - on|
|brake|int|Brake signal: 0 - off, 1 - on|
|reverse|int|Reverse signal: 0 - off, 1 - on|
|fog_light|int|Fog light signal: 0 - off, 1 - on|
|position|int|position light: 0 - off, 1 - on|
|horn|int|Horn signal: 0 - off, 1 - on|
|air_conditioning|int|Air conditioning status: 0 - off, 1 - on|
|neutral|int|Neutral signal: 0 - off, 1 - on|
|retarder|int|Retarder operation: 0 - off, 1 - on|
|abs_work|int|ABS work: 0 - off, 1 - on|
|heating|int|Heater operation: 0 - off, 1 - on|
|clutch|int|Clutch operation: 0 - off, 1 - on|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

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

#### LocAdditionalInfoConfig.get_vehicle_signal_status

- Gets the set extended vehicle signal status bits.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|dict|low_beam_lights - low beam signal<br>high_beam - high beam signal<br>right_turn - right turn signal<br>left_turn - left turn signal<br>brake - brake signal<br>reverse - reverse block signal<br>fog_light - fog light signal<br>position - position light<br>horn - horn signal<br>air_conditioning - air conditioning status<br>neutral - neutral signal<br>retarder - retarder work<br >abs_work - ABS work<br>heating - heater work<br>clutch - clutch work<br>Parameter not set returns empty dictionary |

**Examples:**

```python
vehicle_signal_status = LocAdditionalInfoConfigObj.get_vehicle_signal_status()
print(vehicle_signal_status)
# {"low_beam_lights": 1, "high_beam": 1, "right_turn": 1, "left_turn": 1, "brake": 1, "reverse": 1, "fog_light": 1, "position": 1, "horn": 1, "air_conditioning": 1, "neutral": 1, "retarder": 1, "abs_work": 1, "heating": 1, "clutch": 1}
```

#### LocAdditionalInfoConfig.set_io_status

- Set IO status bits.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|deep_sleep|int|Deep sleep state: 0 - off, 1 - on|
|sleep|int|Sleep state: 0 - off, 1 - on|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
deep_sleep = 1
sleep = 1
LocAdditionalInfoConfigObj.set_io_status(deep_sleep, sleep)
```

#### LocAdditionalInfoConfig.get_io_status

- Get the set IO status bit.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|dict|key values ​​are as follows:<br>`deep_sleep` - deep sleep state<br>`sleep` - sleep state<br>The parameter is not set and returns an empty dictionary|

**Examples:**

```python
io_status = LocAdditionalInfoConfigObj.get_io_status()
print(io_status)
# {"deep_sleep": 1, "sleep": 1}
```

#### LocAdditionalInfoConfig.set_analog

- Set analog quantities.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|ad0|int|AD0|
|ad1|int|AD1|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
ad0 = 1
ad1 = 1
LocAdditionalInfoConfigObj.set_analog(ad0, ad1)
```

#### LocAdditionalInfoConfig.get_analog

- Get the set analog quantity.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|dict|key values ​​are as follows:<br>`ad0` - AD0<br>`ad1` - AD1<br>The parameter is not set and returns an empty dictionary|

**Examples:**

```python
analog = LocAdditionalInfoConfigObj.get_analog()
print(analog)
# {"ad0": 1, "ad1": 1}
```

#### LocAdditionalInfoConfig.set_wireless_communication_network_signal_strength

-Set wireless communication network signal strength.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|value|int|Wireless communication network signal strength|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
LocAdditionalInfoConfigObj.set_wireless_communication_network_signal_strength(31)
```

#### LocAdditionalInfoConfig.get_wireless_communication_network_signal_strength

- Get the set wireless communication network signal strength.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|int|Wireless communication network signal strength, the parameter is not set and returns -1|

**Examples:**

```python
wireless_communication_network_signal_strength = LocAdditionalInfoConfigObj.get_wireless_communication_network_signal_strength()
print(wireless_communication_network_signal_strength)
# 31
```

#### LocAdditionalInfoConfig.set_number_of_satellites

- Set the number of GNSS positioning satellites.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|value|int|Number of GNSS positioning satellites|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
LocAdditionalInfoConfigObj.set_number_of_satellites(12)
```

#### LocAdditionalInfoConfig.get_number_of_satellites

- Get the set number of GNSS positioning satellites.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|int|Number of GNSS positioning satellites. If the parameter is not set, -1 will be returned.|

**Examples:**

```python
number_of_satellites = LocAdditionalInfoConfigObj.get_number_of_satellites()
print(number_of_satellites)
# 12
```

#### LocAdditionalInfoConfig.value

- Positioning additional information conversion protocol format data, used for positioning information reporting interface.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|str|Positioning additional information conversion protocol format data|

**Examples:**

```python
loc_additional_info = LocAdditionalInfoConfigObj.value()
print(loc_additional_info)
# 0104000003e80202014503020000
```

## 3. JT/T808 Terminal Function Interface

### JTT808

- This module implements the function of JT/T808 device connecting to the server for data exchange
- Support JT/T808--2011, JT/T808--2013, JT/T808--2019
- Support TCP and UDP two communication methods

```python
from jtt808 import JTT808

ip = "127.0.0.1"
port = 7611
domain = None
method = "TCP"
encryption = False
timeout = 30
retry_count = 3
version = "2019"
client_id = "18888888888"

jtt808_obj = JTT808(
    ip=ip, port=port, domain=domain, method=method,timeout=timeout, retry_count=retry_count,
    version=version, client_id=client_id
)
```

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|ip|str|Server IP address, default: None, choose one of ip and domain|
|port|int|Server port number, default: None|
|domain|str|Server domain name address, default: None, choose one between domain and ip|
|method|str|Communication method: `TCP` or `UDP`, default: `TCP`|
|timeout|int|Message data reading timeout, unit: seconds, default: 30|
|retry_count|int|The number of retries after failure to send message data, default: 3|
|version|str|JTT808 version, currently there are three versions: `2011`, `2013`, `2019`, default: `2019`|
|client_id|str|The unique identifier of the terminal, usually the terminal mobile phone number, default: empty string, **required parameter**|

#### JTT808.set_callback

- Set back to the function, which is used to receive the response from the server after the terminal message is sent and the message data sent by the server.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|callback|function|Callback function. The return function has a formal parameter args. args is a dictionary with two key values, `header` and `data`. The value values ​​corresponding to the two keys are also dictionary-specific. The specific parameters are shown in the table below.|

**Description of the `header` parameter in the callback function parameter `args`:**

|Parameters|Types|Description|
|:---|---|---|
|message_id|int|消息 ID|
|properties|int|消息体属性|
|protocol_version|int|协议版本号|
|client_id|str|终端手机号|
|serial_no|int|消息流水号|
|package_total|int|消息包总数|
|package_no|int|包序号|

**Description of the `data` parameter in the callback function parameter `args`:**

- The parameters in `data` will change according to the message ID in `header`. For details, see **4. Server Sends Mmessage Data**

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
def test_callback(args):
    header = args["header"]
    data = args["data"]
    print(header)
    print(data)

jtt808_obj.set_callback(test_callback)
# True
```

#### JTT808.set_encryption

- To set up communication encryption with the server, the server needs to issue an encryption public key.

**Encryptable message interface:**

- `params_report`
- `properties_report`
- `upgrade_result_report`
- `loction_report`
- `event_report`
- `issue_question_response`
- `information_demand_cancellation`
- `query_area_route_data_response`
- `driving_record_data_upload`
- `electronic_waybill_report`
- `driver_identity_information_report`
- `location_bulk_report`
- `can_bus_data_upload`
- `media_event_upload`
- `camera_shoots_immediately_response`
- `stored_media_data_retrieval_response`
- `data_uplink_transparent_transmission`
- `data_compression_report`

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|encryption|bool|Whether to encrypt|
|rsa_e|int|The e in the server's public key is issued by the server. Message ID: 0x8A00|
|rsa_n|str|The n in the server's public key is issued by the server. message ID: 0x8A00|

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
encryption = True
rsa_n = 0x010001
rsa_e = "E5A55035C17123BFAB98733E9A619152CEAA13214261BA971EE3563CCF9790FA221FDD9D582B4E14ED200173B2D98" \
        "22E561E99EE54B3A812ACCDDDEAD97DF6DA682583080F7733035BF22C956F6F96ED8F3E2E8DA1DE80C38B1A18956D" \
        "719DCA407EC13E0C86E40502553C418180D520E6B9A18E04E3817F9CD185769233C9CB"
set_encryption_res = jtt808_obj.set_encryption(encryption, rsa_e, rsa_n)
print(set_encryption_res)
# True
```

#### JTT808.connect

- Connect to the server.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
jtt808_obj.connect()
# True
```

#### JTT808.disconnect

- Disconnect from the server.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
jtt808_obj.disconnect()
# True
```

#### JTT808.status

- Get the connection status between the device and the server.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|int|-1 - Connection exception<br>0 - Connected<br>1 - Connecting<br>2 - Disconnected|

**Examples:**

```python
status = jtt808_obj.status()
# 0
```

#### JTT808.register

- Terminal registration.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|province_id|str|Provincial ID, indicating the ID of the province where the vehicle where the terminal is installed, 0 is reserved, and the platform takes the default value. The provincial ID uses the first two digits of the six digits of the administrative division code specified in GB/T 2260|
|city_id|str|City and county ID, indicating the ID of the city and county where the terminal is installed, 0 is reserved, and the platform takes the default value. The city and county ID uses the last four digits of the six digits of the administrative division code specified in GB/T 2260|
|manufacturer_id|str|Manufacturer ID, consisting of the administrative division code of the location of the vehicle terminal manufacturer and the manufacturer ID, with a length not exceeding 11 bytes|
|terminal_model|str|Terminal model, defined by the manufacturer, not exceeding 30 bytes in length|
|terminal_id|str|Terminal ID, consisting of uppercase letters and numbers, this terminal ID is defined by the manufacturer|
|license_plate_color|int|License plate color, according to the provisions of JT/T 697.7--2014, fill in 0 for vehicles without license plates, you can use the enumeration value in the `LicensePlateColor` class|
|license_plate|str|Motor vehicle license plate issued by the public security and traffic management department. If the vehicle is not plated, fill in the frame number|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Terminal registration message serial number|
|registration_result|int|Registration result:<br>0 - Successful<br>1 - The vehicle has been registered<br>2 - The vehicle is not in the database<br>3 - The terminal has been registered<br>4 - Not in the database The terminal |
|auth_code|str|Authentication code, this field is only valid when the registration result is successful|

**Examples:**

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

#### JTT808.authentication

- Terminal authentication

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|auth_code|str|Authentication code|
|imei|str|IMEI|
|app_version|str|Software version number|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Terminal authentication message serial number|
|message_id|int|Terminal authentication message ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
import modem

auth_code = "869523052033462"
imei = modem.getDevImei()
app_version = "v1.0.0"

auth_res = tt808_obj.authentication(auth_code, imei, app_version)
print(auth_res)
# {"serial_no": 1, "message_id": 258, "result_code": 0}
```

#### JTT808.heart_beat

- Report heartbeat.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
heart_beat_res = tt808_obj.heart_beat()
print(heart_beat_res)
# True
```

#### JTT808.logout

- Terminal logout.

**Parameters:**

No Parameter.

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
logout_res = tt808_obj.logout()
print(logout_res)
# True
```

#### JTT808.general_answer

- Terminal universal response.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|response_serial_no|int|Platform message serial number|
|response_msg_id|int|Platform message ID|
|result_code|int|Result:<br>0 - Success/Confirm<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported, default: 0, you can use the enumeration in the `ResultCode` class Value |

**Return Value:**

|Data type|Description|
|:---|---|
|bool|`True` - success<br>`False` - failure|

**Examples:**

```python
response_serial_no = 2
response_msg_id = 0x8103
result_code = 0

general_answer_res = tt808_obj.general_answer(response_serial_no, response_msg_id, result_code)
print(general_answer_res)
# True
```

#### JTT808.query_server_time

- Terminal query server time.

**Parameters:**

No Parameter.

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|utc_time|str|UTC time, time format: `YYYY-MM-DD HH:mm:ss`|

**Examples:**

```python
server_time = tt808_obj.query_server_time()
print(server_time)
# {"utc_time": "2022-06-24 08:12:34"}
```

#### JTT808.params_report

- Query terminal parameter response.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|response_serial_no|int|Corresponding terminal parameter query message serial number|
|terminal_params|dict|Terminal parameter key-value pair, key is parameter ID, value is parameter value (parameter value in hex mode after conversion), obtained through `TerminalParams` function|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Query terminal parameter response serial number|
|message_id|int|Query terminal parameter response ID|
|result_code|int|Result: <br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

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

#### JTT808.properties_report

- Query terminal attribute reporting.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|applicable_passenger_vehicles|int|Whether passenger vehicles are applicable. 0 - no, 1 - yes |
|applicable_to_dangerous_goods_vehicles|int|Whether dangerous goods vehicles are applicable. 0 - no, 1 - yes |
|applicable_to_ordinary_freight_vehicles|int|Whether it is applicable to ordinary freight vehicles. 0 - no, 1 - yes |
|applicable_to_taxi|int|Whether the taxi is applicable. 0 - no, 1 - yes |
|support_hard_disk_video|int|Whether hard disk video is supported. 0 - no, 1 - yes |
|machine_type|int|Machine type. 0 - All-in-one machine, 1 - Split machine |
|applicable_to_trailer|int|Whether the trailer is applicable. 0 - no, 1 - yes |
|manufacturer_id|str|Manufacturer ID, terminal manufacturer code, length not exceeding 5 bytes|
|terminal_model|str|Terminal model, defined by the manufacturer, not exceeding 30 bytes in length|
|terminal_id|str|Terminal ID, consisting of uppercase letters and numbers. This terminal ID is defined by the manufacturer and must not exceed 30 bytes in length|
|iccid|str|Terminal SIM card ICCID|
|hardware_version|str|Terminal hardware version number|
|firmware_version|str|Terminal firmware version number|
|support_gps|int| Whether to support GPS. 0 - no, 1 - yes |
|support_bds|int| Whether to support BDS. 0 - no, 1 - yes |
|support_glonass|int|Whether GLONASS is supported. 0 - no, 1 - yes |
|support_galileo|int|Whether GALILEO is supported. 0 - no, 1 - yes |
|support_gprs|int| Whether to support GPRS. 0 - no, 1 - yes |
|support_cdma|int| Whether to support CDMA. 0 - no, 1 - yes |
|support_td_scdma|int| Whether to support TD-SCDMA. 0 - no, 1 - yes |
|support_wcdma|int| Whether to support WCDMA. 0 - no, 1 - yes |
|support_cdma2000|int|Whether CDMA2000 is supported. 0 - No, 1 - Yes|
|support_td_lte|int| Whether to support TD-LTE. 0 - no, 1 - yes |
|support_other_communication|int|Whether other communication methods are supported. 0 - no, 1 - yes |

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Query the terminal attributes and report the serial number|
|message_id|int|Query terminal attribute reporting ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

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

#### JTT808.upgrade_result_report

- Reporting of terminal upgrade results.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|upgrade_type|int|Upgrade type:<br>0 - Terminal<br>12 - Road Transport Certificate IC Card Reader<br>52 - Satellite Positioning Module|
|result_code|int|Upgrade result:<br>0 - Success<br>1 - Failure<br>2 - Cancel|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Terminal upgrade result reporting serial number|
|message_id|int|Terminal upgrade result reporting ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
upgrade_type = 0
result_code = 0
upgrade_result_report_res = jtt808_obj.upgrade_result_report(upgrade_type, result_code)
print(upgrade_result_report_res)
# {"serial_no": 6, "message_id": 264, "result_code": 0}
```

#### JTT808.loction_report

This interface is used to report positioning information. The following three message reporting functions are:

- 0x0200 - Reporting positioning information
- 0x0201 - Positioning information query message (0x8201) response
- 0x0500 - Vehicle control message (0x8500) response

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|response_msg_id|int|corresponds to the server request message ID, 0x8201 - vehicle positioning information query, 0x8500 - vehicle control message, when used for positioning information reporting, this parameter is passed None|
|response_serial_no|int|corresponds to the server request message serial number. When used to report positioning information, this parameter is passed as None|
|alarm_flag|str|Location alarm information, data source location alarm configuration: `LocAlarmWarningConfig().value()`|
|loc_status|str|Location status information, data source location status information configuration: `LocStatusConfig().value()`|
|latitude|float|Latitude|
|longitude|float|Longitude|
|altitude|int|Altitude, unit: meters|
|speed|float|Speed, unit: kilometers/hour, accurate to 0.1|
|direction|int|Direction, 0~359, true north is 0, clockwise|
|time|str|GMT + 8 time, format: `YYMMDDhhmmss`, such as: `220627101130`|
|loc_additional_info|str|Location additional information, data source location additional information configuration: `LocAdditonalInfoConfig().value()`|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Positioning information reporting/Positioning information query message response/Vehicle control message response serial number|
|message_id|int|Positioning information reporting/Positioning information query message response/Vehicle control message response ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
def test_init_loction_data():
    # Location information item test data generation
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

# 0x0200 - Report location information
loc_data = test_init_loction_data()
args = [None, None]
args.extend(list(loc_data))
loction_report_res = jtt808_obj.loction_report(*args)
print(loction_report)
# {"serial_no": 7, "message_id": 512, "result_code": 0}

# 0x0201 - Positioning information query message (0x8201) response
response_msg_id = 0x8201
response_serial_no = 9
args = [response_msg_id, response_serial_no]
args.extend(list(loc_data))
loction_report_res = jtt808_obj.loction_report(*args)
print(loction_report)
# {"serial_no": 10, "message_id": 513, "result_code": 0}

# 0x0500 - Vehicle control message (0x8500) response
response_msg_id = 0x8500
response_serial_no = 11
args = [response_msg_id, response_serial_no]
args.extend(list(loc_data))
loction_report_res = jtt808_obj.loction_report(*args)
print(loction_report)
# {"serial_no": 12, "message_id": 1280, "result_code": 0}
```

#### JTT808.event_report

- Incident reporting.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|event_id|int|Event ID, event ID comes from 0x8301 event setting message|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Event reporting serial number|
|message_id|int|Event reporting ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
event_id = 10
event_report_res = jtt808_obj.event_report(event_id)
print(event_report_res)
# {"serial_no": 13, "message_id": 769, "result_code": 0}
```

#### JTT808.issue_question_response

- This interface is used to deliver problem message 0x8302 response.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|response_serial_no|int|Corresponds to the serial number of the problem message issued by the server|
|answer_id|int|The answer ID attached to the question issuance|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Serial number for issuing question message response|
|message_id|int|Send problem message response ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
response_serial_no = 14
answer_id = 1
issue_question_response_res = jtt808_obj.issue_question_response(response_serial_no, answer_id)
print(issue_question_response_res)
# {"serial_no": 15, "message_id": 770, "result_code": 0}
```

#### JTT808.information_demand_cancellation

- Information on demand/cancellation.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|info_type|int|Message type, data source 0x8303 Information on demand menu setting.|
|onoff|int|0 - cancel, 1 - on-demand|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Information on demand/Cancel serial number|
|message_id|int|Message on demand/Cancel ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
info_type = 5
onoff = 1
information_demand_cancellation_res = jtt808_obj.information_demand_cancellation(info_type, onoff)
print(information_demand_cancellation_res)
# {"serial_no": 16, "message_id": 770, "result_code": 0}
```

#### JTT808.query_area_route_data_response

- Query area or route data 0x8608 response.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|query_type|int|Query type:<br>1 - Query circular area data<br>2 - Query rectangular area data<br>3 - Query polygonal area data<br>4 - Query route data|
|data|list|Region or line data message body list, the element is the line or region source message body data, data source: message 0x8600, 0x8602, 0x8604, 0x8606 `source_body` in the message body|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Query area or route data response serial number|
|message_id|int|Query area or route data response ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
info_type = 5
onoff = 1
query_area_route_data_response_res = jtt808_obj.query_area_route_data_response(info_type, onoff)
print(query_area_route_data_response_res)
# {"serial_no": 16, "message_id": 770, "result_code": 0}
```

#### JTT808.driving_record_data_upload

- Response to the driving record data collection command 0x8700, and the driving record data is uploaded.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|response_serial_no|int|corresponds to the server request message serial number|
|cmd_word|int|Command word:<br>33 - driving status record, <br>34 - accident suspicion record, <br>35 - overtime driving record, <br>35 - driver information record, <br>37 - Logging |
|cmd_data|bytes|data blocks|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Driving record data upload serial number|
|message_id|int|Driving record data upload ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
with open("/usr/xxx.xxx", "rb") as f:
    cmd_data = f.read()
    response_serial_no = 17
    cmd_word = 33
    driving_record_data_upload_res = jtt808_obj.driving_record_data_upload(response_serial_no, cmd_word, cmd_data)
    print(driving_record_data_upload_res)
# {"serial_no": 18, "message_id": 1792, "result_code": 0}
```

#### JTT808.electronic_waybill_report

- Submit electronic waybill.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|data|bytes|Electronic waybill document data|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Electronic waybill reporting serial number|
|message_id|int|Electronic waybill reporting ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
with open("/usr/xxx.xxx", "rb") as f:
    data = f.read()
    electronic_waybill_report_res = jtt808_obj.electronic_waybill_report(data)
    print(electronic_waybill_report_res)
# {"serial_no": 19, "message_id": 1793, "result_code": 0}
```

#### JTT808.driver_identity_information_report

- Collect and report driver identity information.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|status|int|Status:<br>0x01 - The IC card of the employment qualification certificate is inserted (the driver goes to work)<br>0x02 - The IC card of the employment qualification certificate is pulled out (the driver goes off duty)|
|time|str|Card insertion/removal time, time format: `YYMMDDhhmmss`|
|ic_read_result|int|IC card reading result:<br>0x00 - IC card reading was successful<br>0x01 - Card reading failed because the card key authentication failed<br>0x02 - Card reading failed because the card has been Locked<br>0x03 - Card reading failed, the card has been pulled out<br>0x04 - Card reading failed due to data verification error<br>When the status is 0x02, this field passes an empty string |
|driver_name|str|Driver name, when the status is 0x02, this field passes an empty string|
|qualification_certificate_code|str|Practice qualification certificate code, when the status is 0x02, this field passes an empty string|
|issuing_agency_name|str|The name of the professional qualification certificate issuing agency. When the status is 0x02, this field passes an empty string|
|certificate_validity|str|Certificate validity period, time format: `YYYYMMDD`, when the status is 0x02, this field passes an empty string|
|driver_id_number|str|Driver ID number, when the status is 0x02, this field passes an empty string|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Driver identity information collection and reporting serial number|
|message_id|int|Driver identity information collection and reporting ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
status = 1
time = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(*(utime.localtime()[:6]))[2:]
ic_read_result = 0
driver_name = "jack"
qualification_certificate_code = "88888"
issuing_agency_name = "Municipal road transport management agency"
certificate_validity = "20220701"
driver_id_number = "342426194910010001"
driver_identity_information_report_res = jtt808_obj.driver_identity_information_report(
    status, time, ic_read_result, driver_name, qualification_certificate_code,
    issuing_agency_name, certificate_validity, driver_id_number
)
print(driver_identity_information_report_res)
# {"serial_no": 20, "message_id": 1794, "result_code": 0}
```

#### JTT808.location_bulk_report

- Positioning data is uploaded in batches.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|data_type|int|Position data type:<br>0 - Normal position batch reporting<br>1 - Blind area supplementary reporting|
|loc_datas|list|Location information list, the elements are location information tuples, see the following table for details (Location information table)|

定位信息表

|元素序号|Parameters|Types|Description|
|:---|---|---|---|
|0|alarm_flag|str|Location alarm information, data source location alarm configuration: `LocAlarmWarningConfig().value()`|
|1|loc_status|str|Location status information, data source location status information configuration: `LocStatusConfig().value()`|
|2|latitude|float|Latitude|
|3|longitude|float|Longitude|
|4|altitude|int|Altitude, unit: meters|
|5|speed|float|Speed: unit: kilometers/hour, accurate to 0.1|
|6|direction|int|Direction, 0~359, true north is 0, clockwise|
|7|time|str|GMT + 8 time, format: `YYMMDDhhmmss`, such as: `220627101130`|
|8|loc_additional_info|str|Location additional information, data source location additional information configuration: `LocAdditonalInfoConfig().value()`|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Location data batch upload serial number|
|message_id|int|Location data batch upload ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
loc_data = test_init_loction_data()
loc_datas = [loc_data] * 10
logger.debug("loc_datas: %s" % str(loc_datas))
data_type = 0
location_bulk_report_res = jtt808_obj.location_bulk_report(data_type, loc_datas)
print(location_bulk_report)
# {"serial_no": 21, "message_id": 1796, "result_code": 0}
```

#### JTT808.can_bus_data_upload

- CAN bus data upload.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|recive_time|str|The first CAN bus data reception time, data format: `hhmmssmsms`|
|can_datas|list|CAN bus data list, the elements are CAN bus data, see the following CAN bus data information table for details|

**CAN Bus Data Information Table:**

|Parameters|Types|Description|
|:---|---|---|
|can_channel_no|int|CAN channel number: 0 - CAN1, 1 - CAN2|
|frame_type|int|Frame type: 0 - standard frame, 1 - extended frame|
|collection_method|int|Data collection method: 0 - original data, 1 - average value of collection interval|
|can_id|int|CAN bus ID|
|can_data|str|CAN bus data|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|CAN bus data upload serial number|
|message_id|int|CAN bus data upload ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

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

#### JTT808.media_event_upload

- Multimedia event information reporting.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|media_id|int|Multimedia data ID|
|media_type|int|Multimedia data type:<br>0 - Image<br>1 - Audio<br>2 - Video|
|media_encoding|int|Multimedia format encoding:<br>0 - JPEG<br>1 - TIF<br>2 - MP3<br>3 - WAV<br>4 - WMV|
|event_code|int|Event item code:<br>0 - Platform issues instructions<br>1 - Timing action<br>2 - Robbery alarm trigger<br>3 - Collision rollover alarm trigger<br>4 - Door open Taking pictures<br>5 - Taking pictures with the door closed<br>6 - The car door changes from open to closed, the vehicle speed changes from less than 20 kilometers to more than 20 kilometers<br>7 - Taking pictures at a fixed distance |
|channel_id|int|Channel ID|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Multimedia event information reporting serial number|
|message_id|int|Multimedia event information reporting ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

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

#### JTT808.media_data_upload

- Multimedia data information reporting.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|media_id|int|Multimedia data ID|
|media_type|int|Multimedia data type:<br>0 - Image<br>1 - Audio<br>2 - Video|
|media_encoding|int|Multimedia format encoding:<br>0 - JPEG<br>1 - TIF<br>2 - MP3<br>3 - WAV<br>4 - WMV|
|event_code|int|Event item code:<br>0 - Platform issues instructions<br>1 - Timing action<br>2 - Robbery alarm trigger<br>3 - Collision rollover alarm trigger<br>4 - Door open Taking pictures<br>5 - Taking pictures with the door closed<br>6 - The car door changes from open to closed, and the vehicle speed changes from less than 20 kilometers to more than 20 kilometers<br>7 - Taking pictures at a fixed distance |
|channel_id|int|Channel ID|
|media_data|bytes|Multimedia data packets|
|loc_data|tuple|Multimedia data location information, see `Location information table` for details, no additional location information|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Multimedia data reporting serial number|
|message_id|int|Multimedia data information reporting ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

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

#### JTT808.camera_shoots_immediately_response

- The camera responds to shooting commands immediately.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|response_serial_no|int|Server camera immediate shooting command request message serial number|
|result|int|Result:<br>0 - Success<br>1 - Failure<br>2 - Channel not supported|
|ids|list|Multimedia ID list|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Camera immediate shooting command response serial number|
|message_id|int|Camera shooting command response ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
response_serial_no = 25
result = 0
ids = list(range(10))
camera_shoots_immediately_response_res = jtt808_obj.camera_shoots_immediately_response(response_serial_no, result, ids)
print(camera_shoots_immediately_response_res)
# {"serial_no": 26, "message_id": 2053, "result_code": 0}
```

#### JTT808.stored_media_data_retrieval_response

- Store multimedia data retrieval responses.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|response_serial_no|int|Server-side storage multimedia data retrieval request message serial number|
|medias|list|List of multimedia data items, the elements are tuples, for specific data, see `Multimedia data item information table`|

多媒体数据项信息表

|元素序号|Parameters|Types|Description|
|:---|---|---|---|
|0|media_id|int|Multimedia ID|
|1|media_type|int|Multimedia type:<br>0 - Image<br>1 - Audio<br>2 - Video|
|2|channel_id|int|Channel ID|
|3|event_code|int|Event item code:<br>0 - Platform issues instructions<br>1 - Timed action<br>2 - Robbery alarm trigger<br>3 - Collision rollover alarm trigger<br>Others reserved |
|4|loc_data|tuple|Multimedia data location information, see `Location information table` for details, no additional location information|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Storage multimedia data retrieval response serial number|
|message_id|int|Stored multimedia data retrieval response ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

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

#### JTT808.data_uplink_transparent_transmission

- Data uplink transparent transmission.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|data_type|int|Transparent transmission message type:<br>0x00 - GNSS module detailed positioning data<br>0x0B - Road transport certificate IC card information<br>0x41 - Serial port 1 transparent transmission<br>0x42 - Serial port 2 transparent transmission< br>0xF0 ~ 0xFF - User-defined message|
|data|str|Transparent message content|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|data uplink transparent transmission serial number|
|message_id|int|Data uplink transparent transmission ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
data_type = 0
data = "123456"
data_uplink_transparent_transmission_res = jtt808_obj.data_uplink_transparent_transmission(data_type, data)
print(stored_media_data_retrieval_response_res)
# {"serial_no": 28, "message_id": 2304, "result_code": 0}
```

#### JTT808.data_compression_report

- Data compression reporting.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|data|str|Compressed data|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Data compression reporting serial number|
|message_id|int|Data compression reporting ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
with open("/usr/xxx.tar.gz", "rb") as f:
    data = f.read()
    data_compression_report_res = jtt808_obj.data_compression_report(data)
    print(data_compression_report_res)
# {"serial_no": 29, "message_id": 2305, "result_code": 0}
```

#### JTT808.terminal_rsa_public_key

- Terminal RSA public key reporting.

**Parameters:**

|Parameters|Types|Description|
|:---|---|---|
|e|int|e in terminal RSA public key {e, n}|
|n|str|n in terminal RSA public key {e, n}|

**Return Value (dict):**

|Field|Field type|Description|
|---|---|---|
|serial_no|int|Terminal RSA public key reporting serial number|
|message_id|int|Terminal RSA public key reporting ID|
|result_code|int|Result:<br>0 - Success/Confirmation<br>1 - Failure<br>2 - Wrong message<br>3 - Not supported<br>4 - Alarm processing confirmation|

**Examples:**

```python
e = 0x010001  # 65537
n = "E5A55035C17123BFAB98733E9A619152CEAA13214261BA971EE3563CCF9790FA221FDD9D582B4E14ED200173B2D9822E5" \
    "61E99EE54B3A812ACCDDDEAD97DF6DA682583080F7733035BF22C956F6F96ED8F3E2E8DA1DE80C38B1A18956D719DCA40" \
    "7EC13E0C86E40502553C418180D520E6B9A18E04E3817F9CD185769233C9CB"
terminal_rsa_public_key_res = jtt808_obj.terminal_rsa_public_key(e, n)
print(terminal_rsa_public_key_res)
# {"serial_no": 30, "message_id": 2560, "result_code": 0}
```

## 4. The Server Sends Message Data

### **Message ID: 0x8103 -- Set Terminal Parameters**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|params|list|A tuple of list elements. Element 1 in the tuple is the parameter ID, and element 2 is the parameter value.|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8104 -- Query Terminal Parameters**

**Message body `data`:**

No data.

**Answer message:**

This message needs to be answered using the `jtt808.params_report` interface.

### **Message ID: 0x8105 -- Terminal Control**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|cmd_word|int|Command parameters:<br>1 - Wireless upgrade<br>2 - Control the terminal to connect to the specified server<br>3 - Shut down the terminal<br>4 - Reset the terminal<br>5 - Restore the terminal to factory settings<br >6 - Turn off data communications<br>7 - Turn off all wireless communications |
|cmd_params|dict|When the command parameter is 1 or 2, the command parameters are shown in the table below, otherwise it is an empty dictionary|

**Wireless Upgrade Parameter Value:**

|Encoding|Data type|Description|
|:---|---|---|
|url|str|URL address|
|dial_point_name|str|Dial point name|
|dial_user_name|str|dial username|
|dial_password|str|Dial password|
|addr|str|address|
|tcp_port|str|TCP port|
|udp_port|str|UDP port|
|manufacturer_id|str|Manufacturer ID|
|hardware_version|str|hardware version|
|firmware_version|str|firmware version|
|conn_timeout|str|Time limit for connecting to the specified server|

**Control Terminal Connection To Specify Server Parameter Value:**

|Encoding|Data type|Description|
|:---|---|---|
|conn_ctrl|int|Connection control:<br>0 - Switch to the designated supervision platform server. After connecting to the server, it enters the emergency state. In this state, only the supervision platform that issues control instructions can send controls including text messages. Command<br>1 - Switch back to the original default monitoring platform server and restore to normal state|
|auth_code|str|Supervision platform authentication code|
|dial_point_name|str|Dial point name|
|dial_user_name|str|dial username|
|dial_password|str|Dial password|
|addr|str|address|
|tcp_port|str|TCP port|
|udp_port|str|UDP port|
|conn_timeout|str|Time limit for connecting to the specified server|

> When connection control is 1, there are no other parameters.

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8106 -- Query specified terminal parameters**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|param_ids|list|The list element is the terminal parameter ID|

**Answer message:**

This message needs to be answered using the `jtt808.params_report` interface.

### **Message ID: 0x8107 -- Query Terminal Properties**

**Message body `data`:**

No data.

**Answer message:**

This message needs to be answered using the `jtt808.properties_report` interface.

### **Message ID: 0x8108 -- Deliver Terminal Upgrade Package**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|upgrade_type|str|Upgrade type:<br>0 - Terminal<br>12 - Road Transport Certificate IC Card Reader<br>52 - Satellite Positioning Module|
|manufacturer_id|str|Manufacturer ID|
|terminal_firmware_verion|str|Terminal firmware version number|
|upgrade_package|bytes|Upgrade package|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8201 -- Location Information Query**

**Message body `data`:**

No data.

**Answer message:**

This message needs to be answered using the `jtt808.loction_report` interface.

### **Message ID: 0x8202 -- Temporary Location Tracking Control**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|time_interval|int|Time interval, unit: seconds, stop tracking when the time interval is 0, no subsequent parameters are required to stop tracking|
|location_tracking_validity_period|int|Location tracking validity period, unit: seconds. After receiving the location tracking control message, the terminal sends a location report according to the time interval in the message before the validity period expires|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8203 -- Manually Confirm Alarm Message**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|alarm_msg_serial_no|int|Alarm message serial number that requires manual confirmation, 0 means all messages of this alarm type|
|emergency_alarm|int|1 - Confirm emergency alarm|
|hazard_alarm|int|1 - Confirm hazard warning|
|in_out_area_alarm|int|1 - Confirm in and out area alarm|
|in_out_road_alarm|int|1 - Confirm in and out route alarm|
|insufficient_or_too_long_travel_time_on_the_road_alarm|int|1 - Confirm that the road segment travel time is insufficient/too long to alarm|
|vehicle_illegal_ignition_alarm|int|1 - Confirm vehicle illegal ignition alarm|
|vehicle_illegal_displacement_alarm|int|1 - Confirm vehicle illegal displacement alarm|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8204 -- Link Detection**

**Message body `data`:**

No data.

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8300 -- Text Message Delivery**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|flag_type|int|Text flag type:<br>1 - Service<br>2 - Urgent<br>3 - Notification|
|terminal_display|int|1 - terminal display display|
|terminal_tts_broadcast_and_read|int|1 - terminal TTS broadcast|
|flag_msg_type|int|0 - Center navigation information, 1 - CAN fault code information|
|msg_type|int|Text type: 1 - notification, 2 - service|
|message|int|Text message|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8301 -- Event Settings**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|set_type|int|Set type:<br>0 - Delete all existing events on the terminal, the event item is empty<br>1 - Update events<br>2 - Append events<br>3 - Modify events<br>4 - Delete specific events|
|events|list|Event item list, the element is a dictionary, containing two key values, `id` is the event id, `data` is the event content|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8302 -- Send Questions**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|flag|dict|Question issuing flag:<br>`emergency`: emergency or not, 0 - no, 1 - yes; <br>`terminal_tts_broadcast_and_read`: terminal TTS broadcast reading, 0 - no, 1 - yes; <br>`advertising_screen_display`: Advertising screen display, 0 - no, 1 - yes |
|question_info|str|Question content|
|answers|list|List of candidate answers, the element is answer dictionary information, including `id` answer id, `data` answer content, two key values|

**Answer message:**

This message needs to be answered using the `jtt808.issue_question_response` interface.

### **Message ID: 0x8303 -- Information on Demand Menu Settings**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|set_type|int|Set type:<br>0 - Delete all existing information items in the terminal<br>1 - Update menu<br>2 - Append menu<br>3 - Modify menu|
|infos|list|List of information items. The element is a dictionary and contains two key values. `type` is the information type and `name` is the information name. If the terminal already has an information item of the same type, it will be overwritten|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8304 -- Information Services**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|info_type|int|Information type|
|info_data|str|Information content|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8400 -- Call Back**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|flag|int|Flag: 0 - normal call, 1 - monitoring|
|phone_number|str|Phone number|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8401 -- Set Up Phone Book**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|set_type|int|Set type:<br>0 - Delete all contacts stored on the terminal<br>1 - Update the phone book (delete all existing contacts on the terminal and append contacts in messages)<br>2 - Add phone book<br>3 - Modify phone book (indexed by contacts) |
|phonebook|list|Contact list: The element is a dictionary, containing three key values,<br>`call_type` - Flag: 1 - incoming call, 2 - outgoing call, 3 - incoming/outgoing call<br>`phone` - Phone Number<br>`concat_user` - Contact |

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8500 -- Vehicle Control**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|data|list|The list element is control information, including two key values ​​of `id` and `param`. For details, see the vehicle control command table|

**Vehicle Control Instruction List:**

|Control ID|Description|Control Parameters|
|---|---|---|
|0x0001|Door control|0 - door locked, 1 - door open|
|0x0002~0x8000|Reserved for standard revision||
|0xF001~0xFFFF|Manufacturer-defined control type||

**Answer message:**

This message needs to be answered using the `jtt808.loction_report` interface.

### **Message ID: 0x8600 -- Set Circular Area**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|set_attr|int|Set attributes: 0 - update, 1 - append, 2 - modify|
|area_data|list|Circular area attributes, for detailed information, see `Circular area attribute table`|
|source_body|str|Used for `jtt808.query_area_route_data_response` area or road section query reporting interface|

**Circular Area Attribute Table:**

|Attributes|Type|Description|
|:---|---|---|
|area_id|int|area ID|
|attributes|dict|Regional attributes, for detailed information, see `Regional Attribute Table`|
|center_latitude|float|center point latitude|
|center_longitude|float|Center point longitude|
|radius|int|Radius, unit: meters|
|start_time|str|Start time, time format: `YYMMDDhhmmss`, when the area attribute `time_limit_enable` is 0, this field is empty|
|end_time|str|End time, time format: `YYMMDDhhmmss`, when the area attribute `time_limit_enable` is 0, this field is empty|
|speed_limit|int|Maximum speed, unit: kilometers/hour, when the area attribute `speed_limit_enable` is 0, this field is 0|
|over_speed_time|int|Overspeed duration, unit: seconds, when the zone attribute `speed_limit_enable` is 0, this field is 0|
|night_speed_limit|int|The maximum speed at night, unit: kilometers/hour, when the area attribute `speed_limit_enable` is 0, this field is 0|
|area_name|str|area name|

**Regional Attribute Table:**

|Attributes|Type|Description|
|:---|---|---|
|time_limit_enable|int|Whether to enable the start and end time judgment rules: 0 - no, 1 - yes|
|speed_limit_enable|int|Judgment rules for whether to enable maximum speed, overspeed duration and nighttime maximum speed: 0 - no, 1 - yes|
|alert_driver_when_entering_area|int|Whether to alert the driver when entering the area: 0 - no, 1 - yes|
|alert_platform_when_entering_area|int|Whether to alert the platform when entering the area: 0 - no, 1 - yes|
|alert_driver_when_leaving_area|int|Whether to alert the driver when leaving the area: 0 - no, 1 - yes|
|alert_platform_when_leaving_area|int|Whether to alert the platform when leaving the area: 0 - no, 1 - yes|
|latitude_direction|int|Latitude direction: 0 - North latitude, 1 - South latitude|
|longitude_direction|int|Longitude direction: 0 - east longitude, 1 - west longitude|
|open_the_door_enable|int|Door switch control: 0 - allow the door to be opened, 1 - do not allow the door to be opened|
|communication_module_enable_when_entering_area|int|Enter area communication module switch: 0 - on, 1 - off|
|gnss_enable_when_entering_area|int|Entering area GNSS detailed positioning data collection switch: 0 - off, 1 - on|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8601 -- Delete Circular Area**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|all|int|Whether to delete all circular areas of the device: 0 - no, 1 - yes, when it is 0, delete the area data of the specified ID|
|area_ids|list|List of specified circular area IDs to be deleted|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8602 -- Set Rectangular Area**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|set_attr|int|Set attributes: 0 - Update 1 - Append 2 - Modify|
|area_data|list|Rectangular area attributes, for detailed information, see `Rectangular area attribute table`|
|source_body|str|Used for `jtt808.query_area_route_data_response` area or road section query reporting interface|

**Rectangular Area Attribute Table:**

|Attributes|Type|Description|
|:---|---|---|
|area_id|int|area ID|
|attributes|dict|Regional attributes, for detailed information, see `Regional Attribute Table`|
|upper_left_latitude|float|upper left point latitude|
|upper_left_longitude|float|upper left point longitude|
|lower_right_latitude|float|Latitude of upper right point|
|lower_right_longitude|float|Longitude of upper right point|
|start_time|str|Start time, time format: `YYMMDDhhmmss`, when the area attribute `time_limit_enable` is 0, this field is empty|
|end_time|str|End time, time format: `YYMMDDhhmmss`, when the area attribute `time_limit_enable` is 0, this field is empty|
|speed_limit|int|Maximum speed, unit: kilometers/hour, when the area attribute `speed_limit_enable` is 0, this field is 0|
|over_speed_time|int|Overspeed duration, unit: seconds, when the zone attribute `speed_limit_enable` is 0, this field is 0|
|night_speed_limit|int|The maximum speed at night, unit: kilometers/hour, when the area attribute `speed_limit_enable` is 0, this field is 0|
|area_name|str|area name|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8603 -- Delete Rectangular Area**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|all|int|Whether to delete all rectangular areas of the device: 0 - no, 1 - yes, when it is 0, delete the area data of the specified ID|
|area_ids|list|List of specified rectangular area IDs to be deleted|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8604 -- Set Polygon Area**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|area_data|dict|Polygon area attributes, for detailed information, see `Polygon area attribute table`|
|source_body|str|Used for `jtt808.query_area_route_data_response` area or road section query reporting interface|

**Polygon Area Attribute Table:**

|Attributes|Type|Description|
|:---|---|---|
|area_id|int|area ID|
|attributes|dict|Regional attributes, for detailed information, see `Regional Attribute Table`|
|start_time|str|Start time, time format: `YYMMDDhhmmss`, when the area attribute `time_limit_enable` is 0, this field is empty|
|end_time|str|End time, time format: `YYMMDDhhmmss`, when the area attribute `time_limit_enable` is 0, this field is empty|
|speed_limit|int|Maximum speed, unit: kilometers/hour, when the area attribute `speed_limit_enable` is 0, this field is 0|
|over_speed_time|int|Overspeed duration, unit: seconds, when the zone attribute `speed_limit_enable` is 0, this field is 0|
|point_location|list|Vertex item list, the element is a dictionary, containing two key values, `latitude` - latitude, `longitude` - longitude|
|night_speed_limit|int|The maximum speed at night, unit: kilometers/hour, when the area attribute `speed_limit_enable` is 0, this field is 0|
|area_name|str|area name|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8605 -- Delete Polygon Area**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|all|int|Whether to delete all polygon areas of the device: 0 - no, 1 - yes, when it is 0, delete the area data of the specified ID|
|area_ids|list|List of specified polygon area IDs to be deleted|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8606 -- Set Route**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|area_data|dict|Route information, for specific information, see `Route Information Attribute Table`|
|source_body|str|Used for `jtt808.query_area_route_data_response` area or road section query reporting interface|

**Route Information Attribute Table:**

|Attributes|Type|Description|
|:---|---|---|
|route_id|int|route ID|
|attributes|dict|Route attributes, for detailed information, see `Route Attribute Table`|
|start_time|str|Start time, time format: `YYMMDDhhmmss`, when the area attribute `time_limit_enable` is 0, this field is empty|
|end_time|str|End time, time format: `YYMMDDhhmmss`, when the area attribute `time_limit_enable` is 0, this field is empty|
|turning_points|list|Line turning point item list, the element is a dictionary, for line turning point item information, see `Line turning point item information table`|
|route_name|str|route name|

**Route Attribute Table:**

|Attributes|Type|Description|
|:---|---|---|
|time_limit_enable|int| Whether to enable the judgment rules of start and end time: 0 - No, 1 - Yes|
|alert_driver_when_entering_area|int|Whether to alert the driver when entering the area: 0 - no, 1 - yes|
|alert_platform_when_entering_area|int|Whether to alert the platform when entering the area: 0 - No, 1 - Yes|
|alert_driver_when_leaving_area|int|Whether to alert the driver when leaving the area: 0 - No, 1 - Yes|
|alert_platform_when_leaving_area|int|Whether to alert the platform when leaving the area: 0 - No, 1 - Yes|

**Line Turning Point Item Information Table:**

|Attributes|Type|Description|
|:---|---|---|
|turning_point_id|int|turning point ID|
|road_section_id|int|Road section ID|
|turning_point_latitude|float|turning point dimension|
|turning_point_longitude|float|turning point progress|
|road_section_width|int|Road section width, unit: meters|
|attributes|dict|Road segment attributes, for detailed information, see `Line Segment Attribute Table`|
|driving_too_long_time_limit|int|The road segment driving time is too long threshold, unit: seconds, if the line segment attribute `driving_time_limit_enable` is 0, it is -1|
|insufficient_travel_time_limit|int|Insufficient driving time threshold of the road segment, unit: seconds, if the line segment attribute `driving_time_limit_enable` is 0, it is -1|
|speed_limit|int|The maximum speed of the road segment, unit: kilometers/hour, if the line segment attribute `speed_limit_enable` is 0, it will be 0|
|over_speed_time|int|The overspeeding duration of the road segment, unit: seconds, if the line segment attribute `speed_limit_enable` is 0, it is 0|
|night_speed_limit|int|The maximum speed of the road segment at night, unit: kilometers/hour, if the line segment attribute `speed_limit_enable` is 0, it will be 0|

**Line Segment Attribute Table:**

|Attributes|Type|Description|
|:---|---|---|
|driving_time_limit_enable|int|Driving time limit enable: 0 - disabled, 1 - enabled|
|speed_limit_enable|int|Speed ​​limit enable: 0 - disable, 1 - enable|
|latitude_direction|int|Latitude direction: 0 - North latitude, 1 - South latitude|
|longitude_direction|int|Longitude direction: 0 - east longitude, 1 - west longitude|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8607 -- Delete Line**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|all|int|Whether to delete all lines of the device: 0 - no, 1 - yes, when it is 0, delete the line data of the specified ID|
|route_ids|list|List of specified route IDs to be deleted|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8608 -- Query area or Route Data**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|query_type|int|Query type:<br>1 - Query circular area data<br>2 - Query rectangular area data<br>3 - Query polygonal area data<br>4 - Query line data|
|ids|list|If it is empty, it will query all the regional data of the specified type. If it is not empty, it will query the regional or line data of the specified ID|

**Answer message:**

This message needs to be answered using the `jtt808.query_area_route_data_response` interface.

### **Message ID: 0x8700 -- Form Record Data Acquisition Command**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|cmd_word|int|Command word:<br>33 - Driving status record<br>34 - Accident suspicion record<br>35 - Overtime driving record<br>35 - Driver information record<br>37 - Log record|
|cmd_data|bytes|data blocks|

**Answer message:**

This message needs to be answered using the `jtt808.driving_record_data_upload` interface.

### **Message ID: 0x8701 -- Download Driving Record Parameters**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|cmd_word|int|Command word:<br>33 - Driving status record<br>34 - Accident suspicion record<br>35 - Overtime driving record<br>35 - Driver information record<br>37 - Log record|
|cmd_data|bytes|data blocks|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8702 -- Report Driver Identification Information Request**

**Message body `data`:**

No data.

**Answer message:**

This message needs to be answered using the `jtt808.driver_identity_information_report` interface.

### **Message ID: 0x8801 -- Camera Shooting Command Immediately**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|channel_id|int|Channel ID, value greater than zero|
|shooting_order|int|shooting command: 0 - stop shooting, 0xFFFF - video, 0x0001~0xFFFE - number of photos taken|
|working_time|int|Shooting interval/recording time, unit: seconds, 0 means taking pictures at the minimum interval or recording all the time|
|save_flag|int|Save flag: 1 - save, 0 - live upload|
|resolution|int|Resolution:<br>0x00 - lowest resolution<br>0x01 - 320 × 240<br>0x02 - 640 × 480<br>0x03 - 800 × 600<br>0x04 - 1024 × 768<br >0x05 - 176 × 144;[Qcif];<br>0x06 - 352 × 288;[Cif];<br>0x07 - 704 × 288;[HALF D1];<br>0x08 - 704 × 576;[D1] <br>0xFF - highest resolution |
|quality|int|Image/video quality, value range 1 ~ 10, 1 represents the minimum quality loss, 10 represents the maximum compression ratio|
|brightness|int|Brightness, 0 ~ 255|
|contrast|int|Contrast, 0 ~ 127|
|saturation|int|Saturation, 0 ~ 127|
|chroma|int|Chroma, 0 ~ 255|

> If the terminal does not support the resolution required by the system, the closest resolution will be used to shoot and upload.

**Answer message:**

This message needs to be answered using the `jtt808.camera_shoots_immediately_response` interface.

### **Message ID: 0x8802 -- Stored Multimedia Data Retrieval**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|media_type|int|Multimedia type:<br>0 - Image<br>1 - Audio<br>2 - Video|
|channel_id|int|Channel ID, 0 means retrieving all channels of this media type|
|event_code|int|Event item code:<br>0 - Platform issues instructions<br>1 - Timing action<br>2 - Robbery alarm trigger<br>3 - Collision rollover alarm trigger<br>Other reserved|
|start_time|str|Start time: `YYMMDDhhmmss`|
|end_time|str|End time: `YYMMDDhhmmss`|

**Answer message:**

This message needs to be answered using the `jtt808.stored_media_data_retrieval_response` interface.

### **Message ID: 0x8803 -- Store Multimedia Data Upload Commands**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|media_type|int|Multimedia type:<br>0 - Image<br>1 - Audio<br>2 - Video|
|channel_id|int|Channel ID|
|event_code|int|Event item code:<br>0 - Platform issues instructions<br>1 - Timing action<br>2 - Robbery alarm trigger<br>3 - Collision rollover alarm trigger<br>Other reserved|
|start_time|str|Start time: `YYMMDDhhmmss`|
|end_time|str|End time: `YYMMDDhhmmss`|
|delete_flag|int|Delete flag: 0 - keep, 1 - delete|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8804 -- Recording Start Command**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|recording_cmd|int|Recording command: 0 - stop recording, 1 - start recording|
|recording_time|int|Recording time: unit: seconds, 0 indicates continuous recording|
|save_flag|int|Save flag: 0 - real-time upload, 1 - local storage|
|audio_sample_rate|int|Audio sample rate: 0 - 8K, 1 - 11K, 2 - 23K, 3 - 32K|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8805 -- Single Stored Multimedia Data Retrieval and Upload Command**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|media_id|int|Multimedia ID|
|delete_flag|int|Delete flag: 0 - keep, 1 - delete|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8900 -- Data Downlink Transparent Transmission**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|data_type|int|Transparent transmission message type:<br>0x00 - GNSS module detailed positioning data<br>0x0B - Road transport certificate IC card information<br>0x41 - Serial port 1 transparent transmission<br>0x42 - Serial port 2 transparent transmission< br>0xF0 ~ 0xFF - User-defined message|
|data|str|Transparent message content|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.

### **Message ID: 0x8A00 -- Platform RSA Public Key**

**Message body `data`:**

|KEY|VALUE Type|Description|
|:---|---|---|
|e|int|e in platform RSA public key {e, n}|
|n|str|n in platform RSA public key {e, n}|

**Answer message:**

This message needs to be answered using the `jtt808.general_answer` interface.
