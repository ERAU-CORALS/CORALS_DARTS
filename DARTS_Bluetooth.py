# DARTS_Bluetooth.py
# The bluetooth process for the DARTS Application.

import asyncio
from bleak import BleakClient, BleakScanner
from math import floor

import DARTS_Messages as messages
import DARTS_API as api

DARTS_Database = None
DARTS_Environment = None

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

async def run_bluetooth():
    device = CORALS_Device()
    await device.connect()

    if api.Send_1R_Requested():
        message_1r = messages.CORALS_1R()

        message_1r.data.W1.data.command_active = True
        message_1r.data.W1.data.commanded_q0_negative = api.Get_BLE_Commanded_Q0() < 0
        message_1r.data.W1.data.commanded_q1_negative = api.Get_BLE_Commanded_Q1() < 0
        message_1r.data.W1.data.commanded_q2_negative = api.Get_BLE_Commanded_Q2() < 0
        message_1r.data.W1.data.commanded_q3_negative = api.Get_BLE_Commanded_Q3() < 0
        message_1r.data.W1.data.target = {"Back": 1, "Front": 2, "Index": 3} \
                                            [api.Get_BLE_Target_Type()]
        message_1r.data.W1.data.action = {"Get": 0, "Add": 1, "Remove": 2, "Replace": 3} \
                                            [api.Get_BLE_Target_Action()]
        message_1r.data.W1.data.index = api.Get_BLE_Target_Index()

        message_1r.data.W2.data.commanded_q0_10ths = api.Get_BLE_Commanded_Q0() * 10 // 1
        message_1r.data.W2.data.commanded_q0_100ths = api.Get_BLE_Commanded_Q0() * 100 // 10
        message_1r.data.W2.data.commanded_q0_1000ths = api.Get_BLE_Commanded_Q0() * 1000 // 100
        message_1r.data.W2.data.commanded_q0_10000ths = api.Get_BLE_Commanded_Q0() * 10000 // 1000

        message_1r.data.W3.data.commanded_q1_10ths = api.Get_BLE_Commanded_Q1() * 10 // 1
        message_1r.data.W3.data.commanded_q1_100ths = api.Get_BLE_Commanded_Q1() * 100 // 10
        message_1r.data.W3.data.commanded_q1_1000ths = api.Get_BLE_Commanded_Q1() * 1000 // 100
        message_1r.data.W3.data.commanded_q1_10000ths = api.Get_BLE_Commanded_Q1() * 10000 // 1000

        message_1r.data.W4.data.commanded_q2_10ths = api.Get_BLE_Commanded_Q2() * 10 // 1
        message_1r.data.W4.data.commanded_q2_100ths = api.Get_BLE_Commanded_Q2() * 100 // 10
        message_1r.data.W4.data.commanded_q2_1000ths = api.Get_BLE_Commanded_Q2() * 1000 // 100
        message_1r.data.W4.data.commanded_q2_10000ths = api.Get_BLE_Commanded_Q2() * 10000 // 1000

        message_1r.data.W5.data.commanded_q3_10ths = api.Get_BLE_Commanded_Q3() * 10 // 1
        message_1r.data.W5.data.commanded_q3_100ths = api.Get_BLE_Commanded_Q3() * 100 // 10
        message_1r.data.W5.data.commanded_q3_1000ths = api.Get_BLE_Commanded_Q3() * 1000 // 100
        message_1r.data.W5.data.commanded_q3_10000ths = api.Get_BLE_Commanded_Q3() * 10000 // 1000

        await device.write_1r(message_1r)

    if api.Send_2R_Requested():
        await device.write_2r(api.Send_2R())

    if api.Send_3R_Requested():

    
def BluetoothProcess(**kwargs):
    global DARTS_Environment
    DARTS_Environment = kwargs["Environment"]

    print ("Bluetooth Process")

    asyncio.get_event_loop().run_until_complete(run_bluetooth())

