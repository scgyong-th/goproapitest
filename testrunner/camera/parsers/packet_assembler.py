def assemble_packets(data):
    byte_arrays = [bytes.fromhex(packet) for packet in data["packets"]]
    assert len(byte_arrays) > 0, 'No response packet'
    first_packet = byte_arrays[0]
    assert len(first_packet) >= 3, f'First Packet Length is {len(first_packet)} < 3'
    first_byte = first_packet[0]
    payload_type = first_byte & 0xE0
    if payload_type == 0:
        assert len(byte_arrays) == 1
        assert len(first_packet) == first_byte + 1
        return first_packet[1:]
    elif payload_type == 0x20:
        assert len(byte_arrays) >= 2
        msb = first_packet[0] & 0x1F
        lsb = first_packet[1] & 0xFF
        msg_size = msb << 8 | lsb
        assembled = first_packet[2:]
    elif payload_type == 0x40:
        assert len(byte_arrays) >= 2
        msb = first_packet[1] & 0xFF
        lsb = first_packet[2] & 0xFF
        msg_size = msb << 8 | lsb
        assembled = first_packet[3:]

    print(f'Payload type=0x{payload_type:X}. Expected message size={msg_size}')
    counter = 0
    for i in range(1, len(byte_arrays)):
        packet = byte_arrays[i]
        header = packet[0]
        assert (header & 0xF0) == 0x80
        assert (header & 0x0F) == counter, f'Continuation Packet Counter Mismatch: {header & 0x0F} should be {counter}'
        counter = (counter + 1) % 16
        assembled += packet[1:]

    assert msg_size == len(assembled)

    return assembled

if __name__ == '__main__':
    data_samples = [
        {
            "packets": [
                "205B3C0004000000410C4845524F313320426C61",
                "80636B04307830350F4832342E30312E30322E30",
                "81322E30300E4333353331333235313531383935",
                "820A475032353135313839350C30363537343735",
                "836637613761010001010100025B5D0101"
            ],
            "error": ""
        }, {
            "packets": ["0432000200"], "error": ""
        }, {
            "packets": ["0432000300"], "error": ""
        }, {
            "packets": [
            "232C320002000300050006000D00130018001E00",
            "801F002000250029010929010C2A01082B01002B",
            "8101022B01032B01042C01092D01082F01072F01",
            "820C3601003601013B01003B01013B01043B0106",
            "833B01073E040003D0903E0400061A803E040009",
            "8427C03E04000AAE603E04000C35003E04000F42",
            "85403E0400124F803E0400186A003E04001E8480",
            "863E0400249F003E04002625A03E04003D090040",
            "8701004001014001024001034001044001054001",
            "880640010740010840010940010A40010B40010C",
            "894B004C00530100530101540100540101540102",
            "8A54010354010454010554010654010754010854",
            "8B010954010A54010B56010056010158010A5801",
            "8C1458011E58012858013258013C580146580150",
            "8D58015A5801645B01035B016466006701036701",
            "8E6469006C006F00700164700165700166700167",
            "8F70016872007300740075007600790100790103",
            "8079010479010979010A7A007B007D007E008000",
            "81810082008300840086010086010187008B0090",
            "82010C90010D90010F9001109001129001139001",
            "831490011590011890011A90011D90011E90011F",
            "8490012091009200930099009A01009A01019A01",
            "85029A01039C009D009F01019F01029F01039F01",
            "8604A10164A10165A10166A101C8A400A500A600",
            "87A700A800AB00AC00AF0100AF0101B00164B001",
            "8865B00174B0017EB20100B20101B300B40100B4",
            "89016FB40170B600B700B800BA0103BA0104BB00",
            "8ABD0102BD0103BD0104BD0105BD0106BD0107BD",
            "8B0108BD0109BD010ABD0164BF00C000C10165C1",
            "8C0167C10168C30100C30101C600C700C800C901",
            "8D00C90101C90102CA00CB00CD0100CD0101CE00",
            "8ECF00D000D100D200D300D400D500D600D700D8",
            "8F0146D80155D80164D90102D90103D90104D901",
            "8005D90106D90107D90108D90109D9010AD90164",
            "81DA00DB0101DB0102DB0103DB0104DC0100DC01",
            "8201DD0100DD0101DE0100DE0101DF0100DF0101",
            "83DF0102DF0103DF0104DF0105DF0106DF0107DF",
            "840108DF0109DF010ADF010BDF010CDF010DDF01",
            "850EE0010AE00114E0011EE00128E00132E0013C",
            "86E00146E00150E0015AE00164E10100E10101E1",
            "870104E10106E10107E20100E20101E300E40100",
            "88E40101E40102E40103E50100E50103E50104E5",
            "890109E5010AE600E700E800E900EA00"
            ], 
            "error": ""
        }
    ]
    for data in data_samples:
        msg = assemble_packets(data)
        print(hex(len(msg)), msg.hex())

