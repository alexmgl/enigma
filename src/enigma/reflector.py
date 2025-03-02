from .mapping import Mapping

class Reflector:
    def __init__(self, reflector):
        if isinstance(reflector, str) and len(reflector) == 1 and reflector in Mapping.reflector_dict:
            self.reflector = reflector
            self.mapping = list(Mapping.reflector_dict[self.reflector]['wiring_pattern'])
        elif isinstance(reflector, str) and len(reflector) == 26:
            self.reflector = None
            self.mapping = list(reflector.upper())
        else:
            raise ValueError("Invalid reflector specification.")
        self.letters_list = Mapping.letters_list

    def encode_from_string(self, character):
        self.__validate_input(character, 1)
        index_val = self.letters_list.index(character)
        return self.mapping[index_val]

    def encode_from_index(self, index):
        print(f"Reflected letter: {self.mapping[index]}")
        return self.mapping[index]

    @staticmethod
    def __validate_input(input_val, length):
        if not isinstance(input_val, str):
            raise TypeError(f"Only strings are allowed; got {type(input_val)}.")
        if len(input_val) != length:
            raise Exception(f"Input must be of length {length}.")
        if not input_val.isalpha():
            raise ValueError("String must only contain the letters A-Z.")
        for s in input_val:
            if input_val.count(s) > 1:
                raise Exception("All characters must be unique.")
        return input_val.upper()
