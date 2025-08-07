from . import register
import camera
import proto

class Parser:
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def next_bytes(self) -> bytes:
        length = self.next_byte()
        b = self.data[self.offset:self.offset + length]
        self.offset += length
        return b
    def next_byte(self) -> int:
        length = self.data[self.offset]
        self.offset += 1
        return length
    def next_i16(self):
        val = int.from_bytes(self.data[self.offset:self.offset+2], 'big', signed=True)
        self.offset += 2
        return val
    def next_u16(self):
        val = int.from_bytes(self.data[self.offset:self.offset+2], 'big')
        self.offset += 2
        return val
    def next_u32(self):
        val = int.from_bytes(self.data[self.offset:self.offset+4], 'big')
        self.offset += 4
        return val
    def next_string(self) -> str:
        o = self.offset
        s = self.next_bytes().decode("utf-8")
        # print(f'offset={o} str={s}')
        return s

    def next_tlv(self):
        t = self.next_byte()
        v = self.next_bytes_or_int()
        return t, v

    def next_bytes_or_int(self):
        v = self.next_bytes()
        l = len(v)
        if l == 1:
            v = v[0]
        elif l == 2 or l == 4 or l == 8:
            v = int.from_bytes(v, 'big')
        else:
            # assert False, 'Unknown size TLV value. Should be pre-processed, not here.'
            print(f'Unknown size. {len(v)=} {v=}')
            # v = bytes
        return v

    def parse(self):
        assert false, 'Not Implmemented'

    def parseHeader(self):
        assert len(self.data) >= 2, 'Data too short'

        self.responseId = self.data[0]
        self.status = self.data[1]
        self.offset = 2  # 첫 2바이트는 responseId, status

    def parseTlvArray(self):
        self.tlvArray = dict()
        while self.offset + 2 <= len(self.data):
            t, v = self.next_tlv()
            self.tlvArray[t] = v

    def parseCommonResponse(self):
        self.parseHeader()
        self.parseTlvArray()
        self.result = {
            "responseId": self.responseId,
            "status": self.status,
            "tlv": self.tlvArray,
        }
        return self.result

class CommandParser(Parser):
    id2 = camera.ID2.CHAR_Command_Response
    first_byte = 0x00 # wild card

    def parse(self):
        print(f'CommandParser.parse(len={len(self.data)}) id=0x{self.data[0]:02x}')
        return self.parseCommonResponse()

register(CommandParser)

class QueryParser(Parser):
    id2 = camera.ID2.CHAR_Query_Response
    first_byte = 0x00 # wild card

    def parse(self):
        print(f'QueryParser.parse(len={len(self.data)}) id=0x{self.data[0]:02x}')
        return self.parseCommonResponse()

    def next_tlv(self):
        t = self.next_byte()
        v = None
        if self.responseId == camera.QueryId.GET_SETTING_VALUES:
            if t == camera.SettingId.NIGHTLAPSE_RATE:
                l = self.next_byte()
                assert l == 4
                v = self.next_u32()
        if self.responseId == camera.QueryId.GET_STATUS_VALUES:
            if t == camera.StatusId.AP_WIFI_NAME:
                v = self.next_string()
            elif t == camera.StatusId.CLIENT_WIFI_NAME:
                v = self.next_string()

        if v == None:
            v = self.next_bytes_or_int()

        print(f'next_tlv(), r={self.responseId}/{t=} {v=}')
        if self.responseId == camera.QueryId.GET_STATUS_VALUES:
            if t in camera.StatusId_possible_values:
                print(f' possible_values: {camera.StatusId_possible_values[t]}')
                assert v in camera.StatusId_possible_values[t]

        return t, v

register(QueryParser)

class SettingParser(QueryParser):
    id2 = camera.ID2.CHAR_Settings_Response
    first_byte = 0x00 # wild card

register(SettingParser)

from datetime import datetime

class GetDateTimeParser(CommandParser):
    id2 = camera.ID2.CHAR_Command_Response
    first_byte = camera.CommandId.GET_DATE_TIME
    def parse(self):
        self.parseHeader()

        self.result = {
            "responseId": self.responseId,
            "status": self.status,

            "payload_length": self.next_byte(),
            "year": self.next_u16(),
            "month": self.next_byte(),
            "day": self.next_byte(),
            "hour": self.next_byte(),
            "minute": self.next_byte(),
            "second": self.next_byte(),
            "weekday": self.next_byte(),
        } 

        return self.result
    def to_datetime(self):
        return datetime(
            self.result["year"], self.result["month"], 
            self.result["day"], self.result["hour"],
            self.result["minute"], self.result["second"]
        )

register(GetDateTimeParser)

class GetLocalDateTimeParser(GetDateTimeParser):
    first_byte = camera.CommandId.GET_LOCAL_DATE_TIME
    def parse(self):
        super().parse()
        self.offset -= 1 # no weekday in local_date_time
        self.result["offset"] = self.next_i16()
        self.result["is_dst"] = self.next_byte()
        return self.result

register(GetLocalDateTimeParser)

class GetOpenGoproVersionParser(CommandParser):
    id2 = camera.ID2.CHAR_Command_Response
    first_byte = camera.CommandId.GET_OPEN_GOPRO_VERSION
    def parse(self):
        self.parseHeader()
        self.major = self.next_bytes()
        self.minor = self.next_bytes()

        self.result = {
            "responseId": self.responseId,
            "status": self.status,
            "major": self.major,
            "minor": self.minor,
        } 

        return self.result

register(GetOpenGoproVersionParser)

class GetHardwareInfoParser(CommandParser):
    id2 = camera.ID2.CHAR_Command_Response
    first_byte = camera.CommandId.GET_HARDWARE_INFO
    def parse(self):
        print(f'GetHardwareInfoParser.parse(len={len(self.data)})')
        self.parseHeader()

        self.ext_header = self.next_bytes()

        result = {
            "responseId": self.responseId,
            "status": self.status,

            "modelNumber": self.next_string(),
            "modelName": self.next_string(),
            # "deprecated": next_bytes()  # 생략됨
            "firmwareVersion": self.next_string(),
            "serialNumber": self.next_string(),
            "apSsid": self.next_string(),
            "apMacAddress": self.next_string(),
        }

        # 나머지는 reserved
        reserved = self.data[self.offset:]
        result["reserved"] = ' '.join(f"{b:02X}" for b in reserved)

        return result

register(GetHardwareInfoParser)

class ProtobufResponseParser(Parser):
    def __init__(self, data, featureId, actionId, resp_class = proto.ResponseGeneric):
        super().__init__(data)
        self.featureId = featureId
        self.actionId = actionId
        self.resp_class = resp_class

    def parse(self):
        msg = self.resp_class()
        featureId = self.data[0]
        actionId = self.data[1]
        assert featureId == self.featureId
        assert actionId == self.actionId
        msg.ParseFromString(self.data[2:])

        self.result = msg
        return msg
 
