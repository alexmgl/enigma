import string

class Mapping:
    rotor_dict = {
        'I': {'wiring_pattern': "EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'notch': ["Q"]},
        'II': {'wiring_pattern': "AJDKSIRUXBLHWTMCQGZNPYFVOE", 'notch': ["E"]},
        'III': {'wiring_pattern': "BDFHJLCPRTXVZNYEIWGAKMUSQO", 'notch': ["V"]},
        'IV': {'wiring_pattern': "ESOVPZJAYQUIRHXLNFTGKDCMWB", 'notch': ['J']},
        'V': {'wiring_pattern': "VZBRGITYUPSDNHLXAWMJQOFECK", 'notch': ['Z']},
        'Beta': {'wiring_pattern': "LEYJVCNIXWPBQMDRTAKZGFUHOS", 'notch': [None]},
        'Gamma': {'wiring_pattern': "FSOKANUERHMBTIYCWLQPZXVGJD", 'notch': [None]}
    }

    reflector_dict = {
        'A': {'wiring_pattern': 'EJMZALYXVBWFCRQUONTSPIKHGD'},
        'B': {'wiring_pattern': 'YRUHQSLDPXNGOKMIEBFZCWVJAT'},
        'C': {'wiring_pattern': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'}
    }

    letters = string.ascii_uppercase
    letters_list = list(letters)
