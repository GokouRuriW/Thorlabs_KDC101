import time
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.DCServoCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.DCServoCLI import *
from System import Decimal

class KDC101():

    def __int__(self):
        pass

    def init(self, sn):
        # Create new device
        serial_no = sn  # 输入KDC101上面的序列号
        DeviceManagerCLI.BuildDeviceList()
        device = KCubeDCServo.CreateKCubeDCServo(serial_no)
        print(DeviceManagerCLI.GetDeviceList())
        # Connect, begin polling, and enable
        device.Connect(serial_no)  # 连接控制器
        time.sleep(0.1)
        device.StartPolling(50)
        time.sleep(0.1)
        device.EnableDevice()
        time.sleep(0.1)  # 等待设备启动
        # Get Device information
        device_info = device.GetDeviceInfo()
        print(device_info.Description)
        self.device = device

        # Wait for Settings to Initialise
        if not device.IsSettingsInitialized():
            device.WaitForSettingsInitialized(3000)  # 等待初始化完成
            assert device.IsSettingsInitialized() is True

        m_config = device.LoadMotorConfiguration(serial_no, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        m_config.DeviceSettingsName = "Z825B"  # 填入设备名称
        m_config.UpdateCurrentConfiguration()
        device.SetSettings(device.MotorDeviceSettings, True, False)

    def kill(self):
        """
        orderly exit
        """
        self.device.StopImmediate()
        self.device.Disconnect()
        del self

    def home(self):
        self.device.Home(0)

    def move_to(self, position): # 单位mm
        self.device.MoveTo(Decimal(position), 0)

    def get_position(self):
        return Decimal.ToDouble(self.device.DevicePosition)

    def disconnect(self):
        self.device.Disconnect()

    def set_movespeed(self, Acceleration, MaxVelocity):
        Velocity_params = self.device.GetVelocityParams()
        Velocity_params.MaxVelocity = Decimal(MaxVelocity)
        Velocity_params.Acceleration = Decimal(Acceleration)
        self.device.SetVelocityParams(Velocity_params)

    def device_state(self):
        return self.device.IsDeviceBusy

