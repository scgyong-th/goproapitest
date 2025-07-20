from . import register
import camera

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

    def next_string(self) -> str:
        o = self.offset
        s = self.next_bytes().decode("utf-8")
        print(f'offset={o} str={s}')
        return s

    def next_tlv(self):
        t = self.next_byte()
        v = self.next_bytes()
        return t, v

    def parse(self):
        assert false, 'Not Implmemented'

class CommandParser(Parser):
    id2 = camera.ID2.CHAR_Command_Response
    first_byte = None
    def parse(self):
        pass

class GetHardwareInfoParser(Parser):
    id2 = camera.ID2.CHAR_Command_Response
    first_byte = camera.CommandId.GET_HARDWARE_INFO
    def parse(self):

        print(f'parse_get_hardware_info(len={len(self.data)})')
        self.offset = 2  # 첫 2바이트는 responseId, status
        ext_header = self.next_bytes()

        result = {
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
