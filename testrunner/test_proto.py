from proto import ResponseLastCapturedMedia, EnumResultGeneric

# 전체 패킷 (예시)
hex_str = "1EF5ED080112180A08313030474F50524F120C47583031303030352E4D5034"
data = bytes.fromhex(hex_str)

# BLE 헤더 제거
payload = data[3:]  # 1E=length, F5=FeatureID, ED=ActionID

# protobuf 파싱
msg = ResponseLastCapturedMedia()
msg.ParseFromString(payload)

assert msg.result == EnumResultGeneric.RESULT_SUCCESS
print("✅ result:", msg.result)
print("📁 folder:", msg.media.folder)
print("📄 file:", msg.media.file)