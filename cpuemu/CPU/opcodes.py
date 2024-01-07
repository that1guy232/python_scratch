OPCODES = {
    'BRK': {'code': 0x00, 'method': '_BRK'},

    'LDA': {'code': 0x01, 'method': '_LDA'},
    'LDX': {'code': 0x02, 'method': '_LDX'},
    'LDY': {'code': 0x03, 'method': '_LDY'},


    'STA': {'code': 0x05, 'method': '_STA'},
    'STX': {'code': 0x06, 'method': '_STX'},
    'STY': {'code': 0x07, 'method': '_STY'},

    'TAX': {'code': 0x08, 'method': '_TAX'},
    'TAY': {'code': 0x09, 'method': '_TAY'},
    'TXA': {'code': 0x0A, 'method': '_TXA'},
    'TYA': {'code': 0x0B, 'method': '_TYA'},

    'ADC': {'code': 0x04, 'method': '_ADC'},
    'SBC': {'code': 0x0C, 'method': '_SBC'},
    'INC': {'code': 0x0D, 'method': '_INC'},
    'DEC': {'code': 0x0E, 'method': '_DEC'},

    'AND': {'code': 0x0F, 'method': '_AND'},
    'ORA': {'code': 0x10, 'method': '_ORA'},
    'EOR': {'code': 0x11, 'method': '_EOR'},

    'CMP': {'code': 0x12, 'method': '_CMP'},
    'CPX': {'code': 0x13, 'method': '_CPX'},
    'CPY': {'code': 0x14, 'method': '_CPY'},

    #'BNC': {'code': 0x15, 'method': '_BNC'},
    'BCS': {'code': 0x16, 'method': '_BCS'},
    'BEQ': {'code': 0x17, 'method': '_BEQ'},
    'BNE': {'code': 0x18, 'method': '_BNE'},
    'BVC': {'code': 0x19, 'method': '_BVC'},
    'BVS': {'code': 0x1A, 'method': '_BVS'},

    'JMP': {'code': 0x1B, 'method': '_JMP'},
    'JSR': {'code': 0x1C, 'method': '_JSR'},
    'RTS': {'code': 0x1D, 'method': '_RTS'},

    'CLC': {'code': 0x1E, 'method': '_CLC'},
    'SEC': {'code': 0x1F, 'method': '_SEC'},
    'CLZ': {'code': 0x1F, 'method': '_CLZ'},
    'SEZ': {'code': 0x20, 'method': '_SEZ'},
    'CLV': {'code': 0x21, 'method': '_CLV'},
    'SEV': {'code': 0x22, 'method': '_SEV'},
    'CLN': {'code': 0x23, 'method': '_CLN'},
    'SEN': {'code': 0x24, 'method': '_SEN'},
    'CLB': {'code': 0x25, 'method': '_CLB'},
    'SEB': {'code': 0x26, 'method': '_SEB'},
}
#   'XXX': {'code': 0x00, 'method': '_XXX'},
