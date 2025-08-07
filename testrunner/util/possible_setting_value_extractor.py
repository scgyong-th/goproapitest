import re

# ✅ 파일 읽기 및 배지 URL → 모델명 치환
with open("setting_api.txt", encoding="utf-8") as f:
    raw_text = f.read()

# 🔁 https://img.shields.io/badge/HERO13Black-4cbee0 → HERO13Black
text = re.sub(r"https?://\S+/badge/(\w+)-\S+", r"\1", raw_text)
lines = text.splitlines()

# ✅ 파싱 처리
possible_values = {}
current_sid = None
current_name = None
pattern_sid = re.compile(r"^(.*)\((\d+)\)")
names = {}

for line in lines:
    line = line.strip()
    if not line:
        continue

    match_sid = pattern_sid.match(line)
    if match_sid:
        current_name = match_sid.group(1).strip()
        current_sid = int(match_sid.group(2))
        names[current_sid] = current_name
        possible_values[current_sid] = []
        continue

    if current_sid is not None:
        match_value = re.match(r"(-?\d+)\s+(.+)", line)
        if match_value:
            val = int(match_value.group(1))
            desc = match_value.group(2).strip()
            possible_values[current_sid].append((val, desc))

# ✅ 출력
print("possible_values = {")
for sid, values in possible_values.items():
    print(f"    0x{sid:02X}: {{  # {names[sid]} ({sid})")
    for val, desc in values:
        print(f"        {val},  # {desc}")
    print("    },")
print("}")