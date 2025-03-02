from .mapping import Mapping

class Rotor:
    def __init__(self, rotor_type, starting_letter='A', ring_setting=1):
        self.rotor_type = rotor_type
        self.rotor_mapping = list(Mapping.rotor_dict[self.rotor_type]['wiring_pattern'])
        self.rotor_notch = Mapping.rotor_dict[self.rotor_type]['notch']
        self.position_letter = starting_letter
        self.letter_pos_index_for_rotation = Mapping.letters_list.index(self.position_letter)
        self.position_index = Mapping.letters_list.index(self.position_letter)

        if ring_setting < 1 or ring_setting > 26:
            raise Exception("Ring setting must be between 1 and 26.")
        self.ring_setting = ring_setting - 1  # Adjust for zero-indexing

        self.position_index = (self.position_index - self.ring_setting) % 26

    def print_rotor_info(self):
        print(f"Rotor Type: {self.rotor_type}, starting letter {self.position_letter}, ring offset {self.position_index}.")

    def encode_right_to_left(self, input_letter):
        input_letter_index = Mapping.letters_list.index(input_letter)
        adjusted_index = (input_letter_index + self.position_index) % 26
        mapped_letter = self.rotor_mapping[adjusted_index]
        output_index = (Mapping.letters_list.index(mapped_letter) - self.position_index) % 26
        return Mapping.letters_list[output_index]

    def encode_left_to_right(self, input_letter):
        input_letter_index = Mapping.letters_list.index(input_letter)
        adjusted_index = (input_letter_index + self.position_index) % 26
        letter = Mapping.letters_list[adjusted_index]
        mapping_index = self.rotor_mapping.index(letter)
        output_letter = Mapping.letters_list[mapping_index]
        final_index = (Mapping.letters_list.index(output_letter) - self.position_index) % 26
        return Mapping.letters_list[final_index]

    def rotate(self):
        self.position_index = (self.position_index + 1) % 26
        self.letter_pos_index_for_rotation = (self.letter_pos_index_for_rotation + 1) % 26

class MultipleRotors:
    max_rotors = 4

    def __init__(self):
        self.rotors = []

    def add(self, rotor):
        if isinstance(rotor, Rotor) and len(self.rotors) < self.max_rotors:
            self.rotors.append(rotor)

    def step_rotors(self):
        notches = []
        for idx, r in enumerate(self.rotors):
            current = Mapping.letters_list[r.letter_pos_index_for_rotation]
            notches.append(current in r.rotor_notch)

        for idx, r in enumerate(self.rotors):
            if idx == 0:  # Rightmost rotor always rotates.
                r.rotate()
            elif idx == 1:
                if Mapping.letters_list[r.letter_pos_index_for_rotation] in r.rotor_notch or notches[0]:
                    r.rotate()
            elif idx == 2:
                if notches[1]:
                    r.rotate()
            elif idx == 3:
                pass
