from .mapping import Mapping
from .plugboard import PlugLead, Plugboard
from .reflector import Reflector
from .rotor import Rotor, MultipleRotors


class EnigmaMachine:
    def __init__(self,
                 rotors=None,
                 reflector=None,
                 ring_settings=None,
                 initial_positions=None,
                 plugs=None):
        """
        Initialise the Enigma Machine.

        Parameters:
            rotors (list): List of rotor identifiers (default: ["I", "II", "III"]).
            reflector (str): A standard reflector key (default: "B").
            ring_settings (list): List of ring settings (default: all 1's).
            initial_positions (str): Starting rotor positions (default: "A"*number_of_rotors).
            plugs (list): List of plugboard pair strings (default: []).
        """
        # Set defaults if not provided.
        if rotors is None:
            rotors = ["I", "II", "III"]
        if reflector is None:
            reflector = "B"
        if ring_settings is None:
            ring_settings = [1] * len(rotors)
        if initial_positions is None:
            initial_positions = "A" * len(rotors)
        if plugs is None:
            plugs = []

        self.rotor_types = rotors
        self.ring_settings = ring_settings
        self.initial_positions = initial_positions

        self.reflector = Reflector(reflector=reflector)
        self.plugs = plugs

        self.plugboard = Plugboard()
        for p in self.plugs:
            self.plugboard.add(PlugLead(p))

        self.reset_rotors()

    def reset_rotors(self):
        """Reset rotor positions to their initial configuration."""
        self.rotors = MultipleRotors()
        for rt, rs, sl in zip(self.rotor_types, self.ring_settings, self.initial_positions):
            rotor = Rotor(rotor_type=rt, starting_letter=sl, ring_setting=rs)
            self.rotors.add(rotor)
        # Reverse rotor order so that index 0 is the rightmost rotor.
        self.rotors.rotors.reverse()

    def encode(self, input_string, reset=False):
        """
        Encode (or decode) a string.

        If reset=True, the rotor positions are reset to their initial settings.
        """
        if reset:
            self.reset_rotors()
        # Remove whitespace and encode letter by letter.
        input_string = "".join(input_string.split())
        output_string = ''
        for s in input_string:
            self.rotors.step_rotors()
            letter = self.plugboard.encode(s)
            for rotor in self.rotors.rotors:
                letter = rotor.encode_right_to_left(letter)
            letter = self.reflector.encode_from_string(letter)
            for rotor in self.rotors.rotors[::-1]:
                letter = rotor.encode_left_to_right(letter)
            letter = self.plugboard.encode(letter)
            output_string += letter
        return output_string
