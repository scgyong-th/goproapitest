import re
from pathlib import Path

# 입력 파일 경로
input_path = Path("status_api.txt")

# 상태 블록 파싱
with input_path.open("r", encoding="utf-8") as f:
    lines = f.readlines()

status_dict = {}
current_name = None
current_id = None
options = []
collecting = False

# 정규식 정의
header_pattern = re.compile(r"^(.*?)\s+\((\d+)\)")
option_pattern = re.compile(r"^(-?\d+)\s+(.+)$")

for line in lines:
    line = line.strip()

    header_match = header_pattern.match(line)
    if header_match:
        if current_name and options:
            status_dict[current_id] = {
                "name": current_name,
                "options": options
            }
        current_name = header_match.group(1).strip()
        current_id = int(header_match.group(2))
        options = []
        collecting = False
        continue

    if "ID" in line and "Option Name" in line:
        collecting = True
        continue

    if collecting:
        opt_match = option_pattern.match(line)
        if opt_match:
            value = int(opt_match.group(1))
            label = opt_match.group(2).strip()
            options.append((value, label))

# 마지막 항목 저장
if current_name and options:
    status_dict[current_id] = {
        "name": current_name,
        "options": options
    }

# 출력
print("possible_values = {")
for sid in sorted(status_dict):
    info = status_dict[sid]
    print(f"    0x{sid:02X}: {{  # {info['name']} ({sid})")
    for val, label in info["options"]:
        print(f"        {val},  # {label}")
    print("    },")
print("}")

