"""
MySensors Constants - Protocol Version 1.6
"""

from enum import IntEnum


class MessageType(IntEnum):
    """ MySensors message types """
    C_PRESENTATION = 0
    C_SET = 1
    C_REQ = 2
    C_INTERNAL = 3
    C_STREAM = 4


class Presentation(IntEnum):
    """ MySensors presentation sub-types """
    S_DOOR = 0                      # Door and window sensors
    S_MOTION = 1                    # Motion sensors
    S_SMOKE = 2                     # Smoke sensor
    S_LIGHT = 3                     # Light Actuator (on/off)
    S_BINARY = 3                    # Binary device (on/off), Alias for S_LIGHT
    S_DIMMER = 4                    # Dimmable device of some kind
    S_COVER = 5                     # Window covers or shades
    S_TEMP = 6                      # Temperature sensor
    S_HUM = 7                       # Humidity sensor
    S_BARO = 8                      # Barometer sensor (Pressure)
    S_WIND = 9                      # Wind sensor
    S_RAIN = 10                     # Rain sensor
    S_UV = 11                       # UV sensor
    S_WEIGHT = 12                   # Weight sensor for scales etc.
    S_POWER = 13                    # Power measuring device, like power meters
    S_HEATER = 14                   # Heater device
    S_DISTANCE = 15                 # Distance sensor
    S_LIGHT_LEVEL = 16              # Light sensor
    S_ARDUINO_NODE = 17             # Arduino node device
    S_ARDUINO_REPEATER_NODE = 18    # Arduino repeating node device
    S_LOCK = 19                     # Lock device
    S_IR = 20                       # Ir sender/receiver device
    S_WATER = 21                    # Water meter
    S_AIR_QUALITY = 22              # Air quality sensor e.g. MQ-2
    S_CUSTOM = 23                   # Use this for custom sensors
    S_DUST = 24                     # Dust level sensor
    S_SCENE_CONTROLLER = 25         # Scene controller device
    S_RGB_LIGHT = 26                # RGB light
    S_RGBW_LIGHT = 27               # RGBW light (with separate white component)
    S_COLOR_SENSOR = 28             # Color sensor
    S_HVAC = 29                     # Thermostat/HVAC device
    S_MULTIMETER = 30               # Multimeter device
    S_SPRINKLER = 31                # Sprinkler device
    S_WATER_LEAK = 32               # Water leak sensor
    S_SOUND = 33                    # Sound sensor
    S_VIBRATION = 34                # Vibration sensor
    S_MOISTURE = 35                 # Moisture sensor
    S_INFO = 36
    S_GAS = 37
    S_GPS = 38


class SetReq(IntEnum):
    """ MySensors set/req sub-types """
    V_TEMP = 0              # Temperature
    V_HUM = 1               # Humidity
    V_STATUS = 2            # Binary status, 0=off, 1=on
    V_LIGHT = 2             # Deprecated. Alias for V_STATUS. Light Status.0=off 1=on
    V_PERCENTAGE = 3        # Percentage value. 0-100 (%)
    V_DIMMER = 3            # Deprecated. Alias for V_PERCENTAGE. Dimmer value. 0-100 (%)
    V_PRESSURE = 4          # Atmospheric Pressure
    V_FORECAST = 5
    V_RAIN = 6              # Amount of rain
    V_RAINRATE = 7          # Rate of rain
    V_WIND = 8              # Windspeed
    V_GUST = 9              # Gust
    V_DIRECTION = 10        # Wind direction
    V_UV = 11               # UV light level
    V_WEIGHT = 12           # Weight (for scales etc)
    V_DISTANCE = 13         # Distance
    V_IMPEDANCE = 14        # Impedance value
    V_ARMED = 15
    V_TRIPPED = 16
    V_WATT = 17                 # Watt value for power meters
    V_KWH = 18                  # Accumulated number of KWH for a power meter
    V_SCENE_ON = 19             # Turn on a scene
    V_SCENE_OFF = 20            # Turn of a scene
    V_HVAC_FLOW_STATE = 21
    V_HVAC_SPEED = 22           # HVAC/Heater fan speed ("Min", "Normal", "Max", "Auto")
    V_LIGHT_LEVEL = 23          # Uncalibrated light level. 0-100%. Use V_LEVEL for light level in lux.
    V_VAR1 = 24                 # Custom value
    V_VAR2 = 25                 # Custom value
    V_VAR3 = 26                 # Custom value
    V_VAR4 = 27                 # Custom value
    V_VAR5 = 28                 # Custom value
    V_UP = 29                   # Window covering. Up.
    V_DOWN = 30                 # Window covering. Down.
    V_STOP = 31                 # Window covering. Stop.
    V_IR_SEND = 32              # Send out an IR-command
    V_IR_RECEIVE = 33           # This message contains a received IR-command
    V_FLOW = 34                 # Flow of water (in meter)
    V_VOLUME = 35               # Water volume
    V_LOCK_STATUS = 36          # Set or get lock status. 1=Locked, 0=Unlocked
    V_LEVEL = 37                # Used for sending level-value
    V_VOLTAGE = 38              # Voltage level
    V_CURRENT = 39              # Current level
    V_RGB = 40                  # RGB value transmitted as ASCII hex string (I.e "ff0000" for red)
    V_RGBW = 41                 # RGBW value transmitted as ASCII hex string (I.e "ff0000ff" for red + full white)
    V_ID = 42                   # Optional unique sensor id (e.g. OneWire DS1820b ids)
    V_UNIT_PREFIX = 43
    V_HVAC_SETPOINT_COOL = 44   # HVAC cold setpoint (Integer between 0-100)
    V_HVAC_SETPOINT_HEAT = 45   # HVAC/Heater setpoint (Integer between 0-100)
    V_HVAC_FLOW_MODE = 46       # Flow mode for HVAC ("Auto", "ContinuousOn", "PeriodicOn")
    V_TEXT = 47
    V_CUSTOM = 48
    V_POSITION = 49



class Internal(IntEnum):
    """ MySensors internal sub-types """
    I_BATTERY_LEVEL = 0
    I_TIME = 1
    I_VERSION = 2
    I_ID_REQUEST = 3
    I_ID_RESPONSE = 4
    I_INCLUSION_MODE = 5
    I_CONFIG = 6
    I_FIND_PARENT = 7
    I_FIND_PARENT_RESPONSE = 8
    I_LOG_MESSAGE = 9
    I_CHILDREN = 10
    I_SKETCH_NAME = 11
    I_SKETCH_VERSION = 12
    I_REBOOT = 13
    I_GATEWAY_READY = 14
    I_REQUEST_SIGNING = 15
    I_GET_NONCE = 16
    I_GET_NONCE_RESPONSE = 17
    I_HEARTBEAT = 18
    I_PRESENTATION = 19
    I_DISCOVER = 20
    I_DISCOVER_RESPONSE = 21


class Stream(IntEnum):
    ST_FIRMWARE_CONFIG_REQUEST = 0	 
    ST_FIRMWARE_CONFIG_RESPONSE = 1	 
    ST_FIRMWARE_REQUEST = 2
    ST_FIRMWARE_RESPONSE = 3	 
    ST_SOUND = 4
    ST_IMAGE = 5

subtypes = {MessageType.C_PRESENTATION: Presentation,
            MessageType.C_SET: SetReq,
            MessageType.C_REQ: SetReq,
            MessageType.C_INTERNAL: Internal,
            MessageType.C_STREAM: Stream}