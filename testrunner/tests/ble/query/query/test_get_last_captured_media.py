import camera
import proto

def test_get_last_captured_media(cfg):
    req = camera.GetLastCapturedMedia()
    msg = camera.proceed_agw_test(req, cfg)
    
    print(f'last captured media = \n{msg} {type(msg)}')
    assert type(msg) == proto.ResponseLastCapturedMedia
    assert msg.result == proto.EnumResultGeneric.RESULT_SUCCESS
    assert type(msg.media.folder) == str
    assert type(msg.media.file) == str
    assert len(msg.media.folder) > 0
    assert len(msg.media.file) > 0

