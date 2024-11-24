# DARTS_Bluetooth.py
# The bluetooth process for the DARTS Application.

import asyncio
import math
import time

from bleak import BleakClient, BleakScanner

import DARTS_Messages as messages
import DARTS_API as api

DARTS_Database = None
DARTS_Environment = None

########################################################################
#
# CORALS BLE Device Class Definition
#
########################################################################

class CORALS_Device:
    
    def __init__(self):

        self.client = None
        
        Environment = lambda name: DARTS_Environment[name] if DARTS_Environment and name in DARTS_Environment else None
        
        self.device_name = Environment("BLE_DEVICE_NAME_CORALS")
        self.device_local_name = Environment("BLE_DEVICE_LOCAL_NAME_CORALS")
        
        self.uuid_advertisement = Environment("BLE_UUID_CORALS_ADVERTISEMENT")
        
        self.uuid_receive_service = Environment("BLE_UUID_CORALS_RECEIVE_SERVICE")

        self.uuid_1r_characteristic = Environment("BLE_UUID_CORALS_1R_CHARACTERISTIC")
        self.uuid_2r_characteristic = Environment("BLE_UUID_CORALS_2R_CHARACTERISTIC")
        self.uuid_3r_characteristic = Environment("BLE_UUID_CORALS_3R_CHARACTERISTIC")
        self.uuid_4r_characteristic = Environment("BLE_UUID_CORALS_4R_CHARACTERISTIC")
        self.uuid_5r_characteristic = Environment("BLE_UUID_CORALS_5R_CHARACTERISTIC")

        self.uuid_transmit_service = Environment("BLE_UUID_CORALS_TRANSMIT_SERVICE")

        self.uuid_1t_characteristic = Environment("BLE_UUID_CORALS_1T_CHARACTERISTIC")
        self.uuid_2t_characteristic = Environment("BLE_UUID_CORALS_2T_CHARACTERISTIC")
        self.uuid_3t_characteristic = Environment("BLE_UUID_CORALS_3T_CHARACTERISTIC")
        self.uuid_4t_characteristic = Environment("BLE_UUID_CORALS_4T_CHARACTERISTIC")
        self.uuid_5t_characteristic = Environment("BLE_UUID_CORALS_5T_CHARACTERISTIC")

    async def discover(self):

        devices = await BleakScanner.discover(5.0, return_adv=True)
        for device in devices:
            advertisement = devices[device][1]
            if advertisement.local_name == self.device_local_name:
                if advertisement.rssi > -90:
                    self.device = devices[device]
                    return device
        
        raise LookupError(f"Device \"{self.device_local_name}\" not found")
    
    async def connect(self):
        try:
            address = await self.discover()
        except LookupError as e:
            raise LookupError(f"Device not found: {e}")
            return

        if address is not None:
            try:
                print(f"Found device at address: {address}")
                print("Attempting to connect...")
                self.client = BleakClient(address)
                await self.client.connect()
                print("Connected to device")
            except Exception as e:
                raise Exception(f"Failed to connect to device: {e}")

        else:
            raise ValueError("Device address is None")
        
    async def disconnect(self):
        if self.client is not None:
            print("Disconnecting from device...")
            await self.client.disconnect()
            print("Disconnected from device")
        else:
            raise Exception("Warning: Failed to disconnect. Check for hanging connections.")
        
    async def _read_characteristic(self, uuid):
        try:
            return await self.client.read_gatt_char(uuid)
        except:
            raise Exception(f"Failed to read characteristic ({uuid})")
        
    async def _write_characteristic(self, uuid, value):
        try:
            await self.client.write_gatt_char(uuid, value)
        except:
            raise Exception(f"Failed to write characteristic ({uuid})")
        
    async def read_1t(self):
        message = messages.CORALS_1T()
        message.raw = await self._read_characteristic(self.uuid_1t_characteristic)
        return message
    
    async def read_2t(self):
        message = messages.CORALS_2T()
        message.raw = await self._read_characteristic(self.uuid_2t_characteristic)
        return message
    
    async def read_3t(self):
        message = messages.CORALS_3T()
        message.raw = await self._read_characteristic(self.uuid_3t_characteristic)
        return message
    
    async def read_4t(self):
        message = messages.CORALS_4T()
        message.raw = await self._read_characteristic(self.uuid_4t_characteristic)
        return message
    
    async def read_5t(self):
        message = messages.CORALS_5T()
        message.raw = await self._read_characteristic(self.uuid_5t_characteristic)
        return message
    
    async def write_1r(self, message):
        await self._write_characteristic(self.uuid_1r_characteristic, message.raw)

    async def write_2r(self, message):
        await self._write_characteristic(self.uuid_2r_characteristic, message.raw)

    async def write_3r(self, message):
        await self._write_characteristic(self.uuid_3r_characteristic, message.raw)

    async def write_4r(self, message):
        await self._write_characteristic(self.uuid_4r_characteristic, message.raw)

    async def write_5r(self, message):
        await self._write_characteristic(self.uuid_5r_characteristic, message.raw)

########################################################################
#
# CORALS BLE MESSAGE HANDLING
#
########################################################################

def Build_1R_Message() -> messages.CORALS_1R:
    def Fixed_Point_Convert(value: float) -> tuple[int]:
        negative = value < 0
        value = abs(value)

        value_10ths = value * 10 // 1
        value_100ths = value * 100 // 10
        value_1000ths = value * 1000 // 100
        value_10000ths = value * 10000 // 1000

        return negative, value_10ths, value_100ths, value_1000ths, value_10000ths
    
    message = messages.CORALS_1R()
    message.data.W1.data.command_active = True
    message.data.W1.data.target = {"Back": 1, "Front": 2, "Index": 3} \
                                    [api.Get_BLE_Target_Type()]
    message.data.W1.data.action = {"Get": 0, "Add": 1, "Remove": 2, "Replace": 3} \
                                    [api.Get_BLE_Target_Action()]
    message.data.W1.data.index = api.Get_BLE_Target_Index()

    message.data.W1.data.commanded_q0_negative, \
    message.data.W2.data.commanded_q0_10ths, \
    message.data.W2.data.commanded_q0_100ths, \
    message.data.W2.data.commanded_q0_1000ths, \
    message.data.W2.data.commanded_q0_10000ths = Fixed_Point_Convert(api.Get_BLE_Commanded_Q0())
    
    message.data.W1.data.commanded_q1_negative, \
    message.data.W3.data.commanded_q1_10ths, \
    message.data.W3.data.commanded_q1_100ths, \
    message.data.W3.data.commanded_q1_1000ths, \
    message.data.W3.data.commanded_q1_10000ths = Fixed_Point_Convert(api.Get_BLE_Commanded_Q1())

    message.data.W1.data.commanded_q2_negative, \
    message.data.W4.data.commanded_q2_10ths, \
    message.data.W4.data.commanded_q2_100ths, \
    message.data.W4.data.commanded_q2_1000ths, \
    message.data.W4.data.commanded_q2_10000ths = Fixed_Point_Convert(api.Get_BLE_Commanded_Q2())

    message.data.W1.data.commanded_q3_negative, \
    message.data.W5.data.commanded_q3_10ths, \
    message.data.W5.data.commanded_q3_100ths, \
    message.data.W5.data.commanded_q3_1000ths, \
    message.data.W5.data.commanded_q3_10000ths = Fixed_Point_Convert(api.Get_BLE_Commanded_Q3())

def Process_1T_Message(message: messages.CORALS_1T):
    pass
    
def Process_2T_Message(message: messages.CORALS_2T):
    def Fixed_Point_Convert(value_negative, value_10ths, value_100ths, value_1000ths, value10000ths) -> float:
        value = value_10ths * 0.1 + value_100ths * 0.01 + value_1000ths * 0.001 + value10000ths * 0.0001
        return value * (-1 if value_negative else 1)
    
    receipt_time = time.time() - api.Attitude_Plot_Get_StartTime()
    api.Attitude_Plot_Push_TimeData(receipt_time)

    q4_data = Fixed_Point_Convert(message.data.W1.data.attitude_q0_negative,
                                  message.data.W2.data.attitude_q0_10ths,
                                  message.data.W2.data.attitude_q0_100ths,
                                  message.data.W2.data.attitude_q0_1000ths,
                                  message.data.W2.data.attitude_q0_10000ths)
    
    q1_data = Fixed_Point_Convert(message.data.W1.data.attitude_q1_negative,
                                  message.data.W3.data.attitude_q1_10ths,
                                  message.data.W3.data.attitude_q1_100ths,
                                  message.data.W3.data.attitude_q1_1000ths,
                                  message.data.W3.data.attitude_q1_10000ths)
    
    q2_data = Fixed_Point_Convert(message.data.W1.data.attitude_q2_negative,
                                  message.data.W4.data.attitude_q2_10ths,
                                  message.data.W4.data.attitude_q2_100ths,
                                  message.data.W4.data.attitude_q2_1000ths,
                                  message.data.W4.data.attitude_q2_10000ths)
    
    q3_data = Fixed_Point_Convert(message.data.W1.data.attitude_q3_negative,
                                  message.data.W5.data.attitude_q3_10ths,
                                  message.data.W5.data.attitude_q3_100ths,
                                  message.data.W5.data.attitude_q3_1000ths,
                                  message.data.W5.data.attitude_q3_10000ths)
    
    quat_data = [q1_data, q2_data, q3_data, q4_data]
    api.Attitude_Plot_Push_AttitudeData(quat_data, type="Quaternion")
    api.Attitude_Set_Current_Type(quat_data, type="Quaternion")

    while receipt_time - api.Attitude_Plot_Get_TimeData()[0] > api.Attitude_Plot_Get_TimeLength():
        api.Attitude_Plot_Pop_TimeData()
        api.Attitude_Plot_Pop_AttitudeData()

def Build_4R_Message() -> messages.CORALS_4R:
    def Fixed_Point_Convert(value: float) -> tuple[int]:
        negative = value < 0
        value = abs(value)
        value_exponent = math.ceil(math.log10(value))
        value_mantissa = value * (10 ** -value_exponent)

        value_10ths = value_mantissa * 10 // 1
        value_100ths = value_mantissa * 100 // 10
        exp_negative = value_exponent < 0
        exponent = abs(value_exponent)
        
        return negative, value_10ths, value_100ths, exp_negative, exponent
    
    message = messages.CORALS_4R()

    gains_matrix = api.Gains_Get_Matrix()
    gains_exponent = api.Gains_Get_Exponent()

    message.data.W1.data.command_active = True

    message.data.W1.data.commanded_gain11_negative, \
    message.data.W2.data.commanded_gain11_10ths, \
    message.data.W2.data.commanded_gain11_100ths, \
    message.data.W2.data.commanded_gain11_exp_negative, \
    message.data.W2.data.commanded_gain11_exp = Fixed_Point_Convert(gains_matrix[0][0] * (10 ** gains_exponent))

    message.data.W1.data.commanded_gain12_negative, \
    message.data.W3.data.commanded_gain12_10ths, \
    message.data.W3.data.commanded_gain12_100ths, \
    message.data.W3.data.commanded_gain12_exp_negative, \
    message.data.W3.data.commanded_gain12_exp = Fixed_Point_Convert(gains_matrix[0][1] * (10 ** gains_exponent))

    message.data.W1.data.commanded_gain13_negative, \
    message.data.W4.data.commanded_gain13_10ths, \
    message.data.W4.data.commanded_gain13_100ths, \
    message.data.W4.data.commanded_gain13_exp_negative, \
    message.data.W4.data.commanded_gain13_exp = Fixed_Point_Convert(gains_matrix[0][2] * (10 ** gains_exponent))

    message.data.W1.data.commanded_gain21_negative, \
    message.data.W5.data.commanded_gain21_10ths, \
    message.data.W5.data.commanded_gain21_100ths, \
    message.data.W5.data.commanded_gain21_exp_negative, \
    message.data.W5.data.commanded_gain21_exp = Fixed_Point_Convert(gains_matrix[1][0] * (10 ** gains_exponent))

    message.data.W1.data.commanded_gain22_negative, \
    message.data.W6.data.commanded_gain22_10ths, \
    message.data.W6.data.commanded_gain22_100ths, \
    message.data.W6.data.commanded_gain22_exp_negative, \
    message.data.W6.data.commanded_gain22_exp = Fixed_Point_Convert(gains_matrix[1][1] * (10 ** gains_exponent))

    message.data.W1.data.commanded_gain23_negative, \
    message.data.W7.data.commanded_gain23_10ths, \
    message.data.W7.data.commanded_gain23_100ths, \
    message.data.W7.data.commanded_gain23_exp_negative, \
    message.data.W7.data.commanded_gain23_exp = Fixed_Point_Convert(gains_matrix[1][2] * (10 ** gains_exponent))

    message.data.W1.data.commanded_gain31_negative, \
    message.data.W8.data.commanded_gain31_10ths, \
    message.data.W8.data.commanded_gain31_100ths, \
    message.data.W8.data.commanded_gain31_exp_negative, \
    message.data.W8.data.commanded_gain31_exp = Fixed_Point_Convert(gains_matrix[2][0] * (10 ** gains_exponent))

    message.data.W1.data.commanded_gain32_negative, \
    message.data.W9.data.commanded_gain32_10ths, \
    message.data.W9.data.commanded_gain32_100ths, \
    message.data.W9.data.commanded_gain32_exp_negative, \
    message.data.W9.data.commanded_gain32_exp = Fixed_Point_Convert(gains_matrix[2][1] * (10 ** gains_exponent))

    message.data.W1.data.commanded_gain33_negative, \
    message.data.W10.data.commanded_gain33_10ths, \
    message.data.W10.data.commanded_gain33_100ths, \
    message.data.W10.data.commanded_gain33_exp_negative, \
    message.data.W10.data.commanded_gain33_exp = Fixed_Point_Convert(gains_matrix[2][2] * (10 ** gains_exponent))

    return message

def Process_4T_Message(message: messages.CORALS_4T):
    pass

########################################################################
#
# CORALS BLE PROCESS
#
########################################################################

CORALS_BLE = CORALS_Device()

async def run_bluetooth():
    
    global CORALS_BLE
    if CORALS_BLE.client is None or not CORALS_BLE.client.is_connected:
        await CORALS_BLE.connect()

    match api.Get_1RT_Status():
        case "Inactive":
            pass

        case "Pending":
            await CORALS_BLE.write_1r(Build_1R_Message())
            await CORALS_BLE.client.start_notify(CORALS_BLE.uuid_1t_characteristic, lambda: api.Set_1RT_Status("Confirm"))

        case "Confirm":
            CORALS_BLE.client.stop_notify(CORALS_BLE.uuid_1t_characteristic)

            message_1t = await CORALS_BLE.read_1t()

            if message_1t.data.W1.data.command_complete:

                Process_1T_Message(message_1t)

                api.Set_1RT_Status("Complete")

                message_1r = messages.CORALS_1R()
                message_1r.data.W1.data.command_active = False

                await CORALS_BLE.write_1r(message_1r)

        case "Complete":
            message_1t = await CORALS_BLE.read_1t()

            if not message_1t.data.W1.data.command_complete:
                api.Set_1RT_Status("Inactive")

    CORALS_BLE.client.start_notify(CORALS_BLE.uuid_2t_characteristic, Process_2T_Message)

    match api.Get_4RT_Status():
        case "Inactive":
            pass

        case "Pending":
            message_4r = messages.CORALS_4R()

            await CORALS_BLE.write_4r(Build_4R_Message())
            await CORALS_BLE.client.start_notify(CORALS_BLE.uuid_4t_characteristic, lambda: api.Set_4RT_Status("Confirm"))

        case "Confirm":
            CORALS_BLE.client.stop_notify(CORALS_BLE.uuid_4t_characteristic)

            message_4t = await CORALS_BLE.read_4t()

            if message_4t.data.W1.data.command_complete:

                Process_4T_Message(message_4t)

                api.Set_4RT_Status("Complete")

                message_4r = messages.CORALS_4R()
                message_4r.data.W1.data.command_active = False

                await CORALS_BLE.write_4r(message_4r)

        case "Complete":
            message_4t = await CORALS_BLE.read_4t()

            if not message_4t.data.W1.data.command_complete:
                api.Set_4RT_Status("Inactive")

def BluetoothProcess(**kwargs):
    global DARTS_Environment
    DARTS_Environment = kwargs["Environment"]

    print ("Bluetooth Process")

    if "DUMMY_DATA" in DARTS_Environment and DARTS_Environment["DUMMY_DATA"]:
        print("Dummy Data Generation - Bluetooth Override")
        from DARTS_Dummy import DummyAttitudeProcess as AttitudeProcess
        AttitudeProcess(**kwargs)

    else:
        asyncio.get_event_loop().run_until_complete(run_bluetooth())

