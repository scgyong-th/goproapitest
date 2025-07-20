from .cmd_resp_parser import *
from .packet_assembler import *

_factory = {}

def register(cls):
    name = f'{cls.id2}{cls.first_byte:02x}'
    _factory[name] = cls

def get(id2, first_byte):
    name = f'{id2}{first_byte:02x}'
    return _factory[name]

def parse(id2, byte_array):
    parser_class = get(id2, byte_array[0])
    parser = parser_class(byte_array)
    return parser.parse()

# 등록 대상 모듈을 명시적으로 import (자동 등록 유도)
from . import response_data_parser  # <-- 이 줄 매우 중요

# 공용으로 노출
factory = type('ParserFactory', (), {
    "get": get, "register": register
})

