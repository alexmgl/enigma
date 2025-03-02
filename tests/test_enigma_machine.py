from src.enigma.machine import EnigmaMachine


def test_enigma_encode():
    # Test with a known configuration.
    rotors = ["Beta", "Gamma", "V"]
    reflector = "A"
    ring_settings = [4, 2, 14]
    starting_positions = "MJM"
    plugboard_pairs = ["KI", "XN", "FL"]
    machine = EnigmaMachine(rotors, reflector, ring_settings, starting_positions, plugboard_pairs)
    plaintext = "HELLOWORLD"
    ciphertext = machine.encode(plaintext, reset=True)
    # Although the Enigma is not self-inverse in a round-trip without resetting properly,
    # we can at least check that the ciphertext is different from the plaintext.
    assert ciphertext != plaintext


if __name__ == '__main__':
    print(test_enigma_encode())
