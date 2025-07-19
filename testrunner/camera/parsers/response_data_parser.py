from . import register
import camera

def parse_get_hardware_info(data):
    print(f'parse_get_hardware_info(len={len(data)})')
    offset = 2  # 첫 2바이트는 responseId, status

    def next_bytes() -> bytes:
        nonlocal offset
        length = data[offset]
        offset += 1
        b = data[offset:offset + length]
        offset += length
        return b

    def next_string() -> str:
        return next_bytes().decode("utf-8")        

    ext_header = next_bytes()

    result = {
        "modelNumber": next_string(),
        "modelName": next_string(),
        # "deprecated": next_bytes()  # 생략됨
        "firmwareVersion": next_string(),
        "serialNumber": next_string(),
        "apSsid": next_string(),
        "apMacAddress": next_string(),
    }

    # 나머지는 reserved
    reserved = data[offset:]
    result["reserved"] = ' '.join(f"{b:02X}" for b in reserved)

    return result

register(camera.ID2.CHAR_Command_Response, 
    camera.CommandId.GET_HARDWARE_INFO, 
    parse_get_hardware_info
    )
