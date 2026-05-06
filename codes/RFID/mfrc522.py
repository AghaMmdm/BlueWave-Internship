from machine import Pin, SPI

class MFRC522:
    def __init__(self, spi, cs, rst):
        self.spi = spi
        self.cs = Pin(cs, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.cs.value(1)
        self.rst.value(1)
        self.init()

    def _wreg(self, reg, val):
        self.cs.value(0)
        self.spi.write(bytearray([0x7E & (reg << 1), val]))
        self.cs.value(1)

    def _rreg(self, reg):
        self.cs.value(0)
        self.spi.write(bytearray([0x80 | (0x7E & (reg << 1))]))
        val = self.spi.read(1)[0]
        self.cs.value(1)
        return val

    def init(self):
        self.rst.value(0)
        self.rst.value(1)
        self._wreg(0x01, 0x0F) # SoftReset
        self._wreg(0x2A, 0x8D) # TMode
        self._wreg(0x2B, 0x3E) # TPrescaler
        self._wreg(0x2D, 30)   # TReload
        self._wreg(0x2C, 0)
        self._wreg(0x15, 0x40) # TXASK
        self._wreg(0x11, 0x3D) # Mode
        self.antenna_on()

    def antenna_on(self):
        if ~(self._rreg(0x14) & 0x03):
            self._set_bit(0x14, 0x03)

    def _set_bit(self, reg, mask):
        self._wreg(reg, self._rreg(reg) | mask)

    def request(self, mode):
        self._wreg(0x0D, 0x07) # BitFraming
        (stat, recv, bits) = self._tocom(0x0C, [mode]) # Transceive
        if (stat != 0) or (bits != 0x10): stat = 2 # ERR
        return stat, bits

    def anticoll(self):
        self._wreg(0x0D, 0x00)
        (stat, recv, bits) = self._tocom(0x0C, [0x93, 0x20])
        return stat, recv

    def _tocom(self, cmd, send):
        irqEn = 0x77
        if cmd == 0x0C: irqEn = 0x77
        self._wreg(0x02, irqEn | 0x80)
        self._clear_bit(0x04, 0x80)
        self._set_bit(0x04, 0x80)
        self._wreg(0x01, 0x00) # Idle
        for i in range(len(send)): self._wreg(0x09, send[i])
        self._wreg(0x01, cmd)
        if cmd == 0x0C: self._set_bit(0x0D, 0x80)
        i = 2000
        while True:
            n = self._rreg(0x04)
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & 0x30)): break
        self._clear_bit(0x0D, 0x80)
        if i == 0: return (1, None, None) # TIMEOUT
        if (self._rreg(0x06) & 0x1B) == 0x00:
            stat = 0 # OK
            n = self._rreg(0x0A)
            lastBits = self._rreg(0x0C) & 0x07
            if lastBits != 0: bits = (n - 1) * 8 + lastBits
            else: bits = n * 8
            recv = []
            for i in range(n): recv.append(self._rreg(0x09))
            return (stat, recv, bits)
        else: return (2, None, None) # ERR

    def _clear_bit(self, reg, mask):
        self._wreg(reg, self._rreg(reg) & ~mask)

    OK = 0
    REQIDL = 0x26
