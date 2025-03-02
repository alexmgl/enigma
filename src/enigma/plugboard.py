from .mapping import Mapping

class PlugLead:
    def __init__(self, mapping):
        self.mapping = self.__validate_input(mapping, length=2)
        self.mapping_list = list(self.mapping)  # Order is preserved.

    def encode(self, character):
        character = self.__validate_input(character, length=1)
        if character not in self.mapping_list:
            return character
        if self.mapping_list.index(character) == 0:
            return self.mapping_list[1]
        else:
            return self.mapping_list[0]

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

class Plugboard:
    total_plug_leads = 0

    def __init__(self):
        self.plug_leads = []
        self.max_leads = 10

    def add(self, plug_lead):
        if not isinstance(plug_lead, PlugLead):
            raise TypeError("Input type must be PlugLead.")
        for lead in self.plug_leads:
            if plug_lead.mapping_list == lead.mapping_list:
                raise Exception("This plug lead is already inserted.")
            if plug_lead.mapping_list[0] in lead.mapping_list:
                raise Exception(f"The letter {plug_lead.mapping_list[0]} is already matched.")
            if plug_lead.mapping_list[1] in lead.mapping_list:
                raise Exception(f"The letter {plug_lead.mapping_list[1]} is already matched.")
        self.__add()
        self.plug_leads.append(plug_lead)

    def encode(self, character):
        character = self.__validate_input(character, 1)
        if not self.plug_leads:
            return character
        for lead in self.plug_leads:
            if character in lead.mapping_list:
                if lead.mapping_list.index(character) == 0:
                    return lead.mapping_list[1]
                else:
                    return lead.mapping_list[0]
        return character

    def encode_str_to_index(self, character):
        character = self.__validate_input(character, 1)
        if not self.plug_leads:
            return Mapping.letters_list.index(character)
        for lead in self.plug_leads:
            if character in lead.mapping_list:
                if lead.mapping_list.index(character) == 0:
                    return Mapping.letters_list.index(lead.mapping_list[1])
                else:
                    return Mapping.letters_list.index(lead.mapping_list[0])
        return Mapping.letters_list.index(character)

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

    @classmethod
    def __add(cls):
        cls.total_plug_leads += 1
