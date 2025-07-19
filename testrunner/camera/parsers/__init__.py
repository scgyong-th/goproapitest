from .cmd_resp_parser import *
from .packet_assembler import *

_factory = {}

def register(id2, first_byte, cls):
    name = f'{id2}{first_byte:02x}'
    _factory[name] = cls

def get(id2, first_byte):
    name = f'{id2}{first_byte:02x}'
    return _factory[name]

def parse(id2, byte_array):
    parser = get(id2, byte_array[0])
    return parser(byte_array)

# 등록 대상 모듈을 명시적으로 import (자동 등록 유도)
from . import response_data_parser  # <-- 이 줄 매우 중요

# 공용으로 노출
factory = type('ParserFactory', (), {
    "get": get, "register": register
})

