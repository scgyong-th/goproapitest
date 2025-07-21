try:
    from .constants import CommandId, QueryId, SettingId, StatusId, ID2
except ImportError:
    from constants import CommandId, QueryId, SettingId, StatusId, ID2
import json

class BleRequest:
    def __init__(self, try_count=3):
        self.try_count = try_count
    def toJson(self):
        d = dict()
        d['char'] = self.characteristic
        d['msg'] = self.messageBytes()
        return json.dumps(d)

    def messageBytes(self):
        return ''.join(f'{b:02X}' for b in self.value)

    def toForwardPath(self):
        return f'fw/{self.characteristic}/{self.messageBytes()}'


class BleReadRequest(BleRequest):
    def __init__(self, characteristic, on_return=None):
        super().__init__()
        self.characteristic = characteristic
        self._value = None
        self.on_return = on_return

    @property
    def value_string(self):
        return (self._value or b'').decode('utf-8')

    def set_response(self, resp: bytes):
        self._value = resp
        if self.on_return:
            self.on_return(resp)


class BleWriteRequest(BleRequest):
    def __init__(self, characteristic, value: bytes, wait_for_response=True, on_return=None):
        super().__init__()
        self.characteristic = characteristic
        self.value = value
        self.wait_for_response = wait_for_response
        self.on_return = on_return
        self._response = None

    def set_response(self, resp):
        self._response = resp
        if self.on_return:
            self.on_return(resp)

class GetDateTime(BleWriteRequest):
    def __init__(self, on_return):
        super().__init__(
            characteristic=ID2.CHAR_Command,
            value=bytes([0x01, CommandId.GET_DATE_TIME]),
            on_return=lambda it: on_return(it)
        )

class GetHardwareInfo(BleWriteRequest):
    def __init__(self, on_return):
        super().__init__(
            characteristic=ID2.CHAR_Command,
            value=bytes([0x01, CommandId.GET_HARDWARE_INFO]),
            on_return=lambda it: on_return(it)  # 캐스팅은 생략
        )
        self.try_count = 10


class CommandRequest(BleWriteRequest):
    def __init__(self, command_id: int, on_return=None):
        super().__init__(
            characteristic=ID2.CHAR_Command,
            value=bytes([0x01, command_id]),
            on_return=on_return
        )


class GetWifiApSsid(BleReadRequest):
    def __init__(self, on_return):
        def decode_utf8(byte_data):
            return on_return((byte_data or b'').decode('utf-8'))
        super().__init__(
            characteristic=ID2.CHAR_WiFi_AP_SSID,
            on_return=decode_utf8
        )


class GetWifiApPassword(BleReadRequest):
    def __init__(self, on_return):
        def decode_utf8(byte_data):
            return on_return((byte_data or b'').decode('utf-8'))
        super().__init__(
            characteristic=ID2.CHAR_WiFi_AP_Password,
            on_return=decode_utf8
        )


class SetApControl(BleWriteRequest):
    def __init__(self, enables: bool, on_return):
        super().__init__(
            characteristic=ID2.CHAR_Command,
            value=bytes([0x03, CommandId.SET_AP_CONTROL, 0x01, 0x01 if enables else 0x00]),
            on_return=on_return
        )


class QueryRequest(BleWriteRequest):
    def __init__(self, query_id: int, ids, on_return):
        # ids: int or bytes
        if isinstance(ids, int):
            ids = bytes([ids])
        elif not isinstance(ids, (bytes, bytearray)):
            raise TypeError("ids must be int or bytes")

        payload = bytes([len(ids) + 1, query_id]) + ids

        super().__init__(
            characteristic=ID2.CHAR_Query,
            value=payload,
            on_return=on_return
        )

def const_members(clazz):
    for name, value in vars(clazz).items():
        if name.startswith('__'): continue
        yield (name, value)

if __name__ == "__main__":
    cases = [
        ("Setting", QueryId.GET_SETTING_VALUES, SettingId),
        ("Status", QueryId.GET_STATUS_VALUES, StatusId)
    ]
    for case in cases:
        qName, qId, subType = case
        for name, value in const_members(subType):
            req = QueryRequest(qId, value, None)
            print(f"{qName}:{name}({value}) {req.toJson()} {req.toForwardPath()}")
