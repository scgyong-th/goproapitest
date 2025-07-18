import requests
import camera

def const_members(clazz):
    for name, value in vars(clazz).items():
        if name.startswith('__'): continue
        yield (name, value)

qName = "Status"
for name, value in const_members(camera.StatusId):
    req = camera.QueryRequest(camera.QueryId.GET_STATUS_VALUES, value, None)
    print(f"{qName}:{name}({value}) {req.toJson()}")

print("Done")
