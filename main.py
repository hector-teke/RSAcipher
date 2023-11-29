import math
import random
import sys

from PyQt6.QtGui import QFont, QIntValidator, QValidator
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QSpinBox

from sympy import isprime



###################### OT -> Integer

def text_to_vector(OT):
    vector = []
    while len(OT) >= 5:
        vector.append(block_to_int(OT[-5:]))
        # print(OT[-5:], " \tnum: ", vector)
        OT = OT[0:-5]

    if len(OT) > 0:
        vector.append(block_to_int(OT))
        # print(OT, "  \tnum: ", vector)

    return vector[::-1]


def block_to_int(blk):
    bin_string = ""

    for c in blk:
        bin_string += int_to_bin(ord(c))

    return int(bin_string, 2)


# 8-bit codification of a given integer
def int_to_bin(n):
    bin_string = bin(n)[2:]
    return (8 - len(bin_string)) * '0' + bin_string


###################### Integer -> OT

def vector_to_text(vector):
    OT = ""
    for n in vector:
        OT += int_to_block(n)

    return OT


def int_to_block(num):
    blk = ""
    bin_string = bin(num)[2:]
    bin_string = (8 - (len(bin_string) % 8)) * '0' + bin_string

    for i in range(0, len(bin_string), 8):
        blk += chr(int(bin_string[i:i + 8], 2))
        # print(i, "\t", bin_string[i:i+8])

    return blk


###################### Encryption and decryption

def encryption(OT, e, n):
    CT = []
    for blk in text_to_vector(OT):
        CT.append(pow(blk, e, n))

    return CT


def decryption(CT, d, n):
    OT = []
    for blk in CT:
        OT.append(pow(blk, d, n))

    return vector_to_text(OT)


###################### Keys generation

def generate_primes(bits):
    p1 = None
    p2 = None

    while p1 == p2:
        p1 = random.getrandbits(bits)
        p1 |= (1 << bits - 1) | 1
        while not isprime(p1):
            p1 += 2  # Avoid even numbers

        p2 = random.getrandbits(bits)
        p2 |= (1 << bits - 1) | 1
        while not isprime(p2):
            p2 += 2  # Avoid even numbers

    return p1, p2


def select_e(phi):
    while True:
        e = random.randint(2, phi - 1)      # 1 < e < phi
        if math.gcd(e, phi) == 1:  # GCD(e, phi) = 1
            break
    return e


def generate_keys(bits):
    p, q = generate_primes(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = select_e(phi)
    d = pow(e, -1, phi)

    return e, d, n



# USER INTERFACE ################################################################################

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 680, 370)  # PosX, PosY, Width, Height
        self.setWindowTitle("RSA Cipher")
        self.generate_layout()
        self.show()

    def generate_layout(self):
        keys_height = 20

        bits_hint = QLabel(self)
        bits_hint.setText("Bit length for the keys:")
        bits_hint.setFont(QFont('Arial', 10))
        bits_hint.move(240, keys_height + 5)

        self.bits_input = QSpinBox(self)
        self.bits_input.setRange(20, 1024)
        self.bits_input.setValue(112)
        self.bits_input.resize(50, 24)  # Width x Height
        self.bits_input.move(380, keys_height)

        generate_keys_button = QPushButton(self)
        generate_keys_button.setText("Generate\nKeys")
        generate_keys_button.resize(70, 78)
        generate_keys_button.move(20, keys_height + 40)
        generate_keys_button.clicked.connect(self.generateKeys)

        validator = QIntValidator()

        self.e_input = QLineEdit(self)
        self.e_input.setPlaceholderText("Encryption key")
        self.e_input.setValidator(validator)
        self.e_input.resize(550, 24)  # Width x Height
        self.e_input.move(100, keys_height + 40)
        # self.e_input.textChanged.connect(self.validateTextInput)

        self.d_input = QLineEdit(self)
        self.d_input.setPlaceholderText("Decryption key")
        self.d_input.resize(550, 24)  # Width x Height
        self.d_input.setValidator(validator)
        self.d_input.move(100, keys_height + 40 + 26)
        # self.d_input.textChanged.connect(self.validateTextInput)

        self.n_input = QLineEdit(self)
        self.n_input.setPlaceholderText("Module")
        self.n_input.setValidator(validator)
        self.n_input.resize(550, 24)  # Width x Height
        self.n_input.move(100, keys_height + 40 + 52)
        # self.n_input.textChanged.connect(self.validateTextInput)

        # ENCRYPTION

        encryption_height = 160

        encryption_title = QLabel(self)
        encryption_title.setText("Encryption:")
        encryption_title.setFont(QFont('Arial', 15))
        encryption_title.move(20, encryption_height)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Insert open text")
        self.text_input.resize(560, 24)  # Width x Height
        self.text_input.move(20, encryption_height + 30)
        #self.text_input.textChanged.connect(self.validateTextInput)

        self.text_output = QLineEdit(self)
        self.text_output.setReadOnly(True)
        self.text_output.setPlaceholderText("Encrypted text will appear here")
        self.text_output.resize(560, 24)  # Width x Height
        self.text_output.move(20, encryption_height + 60)

        encrypt_button = QPushButton(self)
        encrypt_button.setText("Encrypt")
        encrypt_button.resize(60, 56)
        encrypt_button.move(590, encryption_height + 30)
        #encrypt_button.clicked.connect(self.startEncryption)







    def generateKeys(self):
        e, d, n = generate_keys(self.bits_input.value())

        self.e_input.setText(str(e))
        self.d_input.setText(str(d))
        self.n_input.setText(str(n))





if __name__ == '__main__':

    """e, d, n = generate_keys(112)

    print("Key for encryption: ", e)
    print("Key for decryption: ", d)
    print("Module: ", n)

    CT = encryption("Music!", e, n)
    print("CT: ", CT)

    OT = decryption(CT, d, n)
    print("OT: ", OT)"""

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
