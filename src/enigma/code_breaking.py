import itertools
from tqdm import tqdm
from .mapping import Mapping
from .machine import EnigmaMachine


def break_code1():
    ciphertext = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"
    crib = "SECRETS"
    rotors = ["Beta", "Gamma", "V"]
    ring_settings = [4, 2, 14]
    starting_positions = "MJM"
    plugboard_pairs = ["KI", "XN", "FL"]

    print("Breaking Code 1:")
    for reflector in ["A", "B", "C"]:
        enigma = EnigmaMachine(rotors, reflector, ring_settings, starting_positions, plugboard_pairs)
        decrypted = enigma.encode(ciphertext, reset=True)
        if crib in decrypted:
            print("Candidate found!")
            print("Reflector:", reflector)
            print("Decrypted text:", decrypted)
    print("Code 1 search complete.\n")


def break_code2():
    ciphertext = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
    crib = "UNIVERSITY"
    rotors = ["Beta", "I", "III"]
    reflector = "B"
    ring_settings = [23, 2, 10]
    plugboard_pairs = ["VH", "PT", "ZG", "BJ", "EY", "FS"]

    print("Breaking Code 2 (brute-forcing starting positions):")
    letters = Mapping.letters_list
    for pos in tqdm(itertools.product(letters, repeat=3), total=26 ** 3):
        starting_positions = "".join(pos)
        enigma = EnigmaMachine(rotors, reflector, ring_settings, starting_positions, plugboard_pairs)
        decrypted = enigma.encode(ciphertext, reset=True)
        if crib in decrypted:
            print("Candidate found!")
            print("Starting positions:", starting_positions)
            print("Decrypted text:", decrypted)
            break
    print("Code 2 search complete.\n")


def break_code3():
    ciphertext = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"
    crib = "THOUSANDS"
    allowed_rotors = ['Beta', 'Gamma', 'II', 'IV']
    allowed_ring_settings = [2, 4, 6, 8, 20, 22, 24, 26]
    starting_positions = "EMY"
    plugboard_pairs = ["FH", "TS", "BE", "UQ", "KD", "AL"]

    print("Breaking Code 3:")
    rotor_permutations = list(itertools.permutations(allowed_rotors, 3))
    for rotor_order in tqdm(rotor_permutations, total=len(rotor_permutations)):
        for ring in itertools.product(allowed_ring_settings, repeat=3):
            for reflector in ["A", "B", "C"]:
                enigma = EnigmaMachine(list(rotor_order), reflector, list(ring), starting_positions, plugboard_pairs)
                decrypted = enigma.encode(ciphertext, reset=True)
                if crib in decrypted:
                    print("Candidate found!")
                    print("Rotor order:", rotor_order)
                    print("Ring settings:", ring)
                    print("Reflector:", reflector)
                    print("Decrypted text:", decrypted)
                    return
    print("Code 3 search complete.\n")


def break_code4():
    ciphertext = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"
    crib = "NOTUTORSWERE"
    rotors = ["V", "III", "IV"]
    reflector = "A"
    ring_settings = [24, 12, 10]
    starting_positions = "SWU"
    incomplete_plugs = ["WP", "RJ", "A?", "VF", "I?", "HN", "CG", "BS"]

    used = set()
    incomplete_indices = []
    for idx, pair in enumerate(incomplete_plugs):
        if "?" in pair:
            used.add(pair.replace("?", ""))
            incomplete_indices.append(idx)
        else:
            used.update(pair)
    remaining = sorted(list(set(Mapping.letters) - used))

    print("Breaking Code 4 (completing plugboard pairs):")
    order_options = list(itertools.product([False, True], repeat=len(incomplete_indices)))
    for perm in itertools.permutations(remaining, len(incomplete_indices)):
        for orders in order_options:
            plugs_candidate = incomplete_plugs.copy()
            for i, idx in enumerate(incomplete_indices):
                known = plugs_candidate[idx].replace("?", "")
                candidate = perm[i]
                candidate_pair = (candidate + known) if orders[i] else (known + candidate)
                plugs_candidate[idx] = candidate_pair
            try:
                enigma = EnigmaMachine(rotors, reflector, ring_settings, starting_positions, plugs_candidate)
            except Exception:
                continue
            decrypted = enigma.encode(ciphertext, reset=True)
            if crib in decrypted:
                print("Candidate found!")
                print("Completed Plugboard pairs:", plugs_candidate)
                print("Decrypted text:", decrypted)
                return
    print("Code 4 search complete.\n")


def is_involution(wiring):
    for i, letter in enumerate(Mapping.letters_list):
        mapped = wiring[i]
        reverse_index = Mapping.letters_list.index(mapped)
        if wiring[reverse_index] != letter:
            return False
    return True


def generate_modified_reflectors(original_wiring):
    wiring = list(original_wiring)
    pairs = []
    for letter in Mapping.letters_list:
        i = Mapping.letters_list.index(letter)
        mapped = wiring[i]
        if letter < mapped:
            pairs.append((letter, mapped))
    candidates = []
    for (a, b), (c, d) in itertools.combinations(pairs, 2):
        candidate = wiring.copy()
        candidate[Mapping.letters_list.index(a)] = d
        candidate[Mapping.letters_list.index(d)] = a
        candidate[Mapping.letters_list.index(c)] = b
        candidate[Mapping.letters_list.index(b)] = c
        mod_wiring = "".join(candidate)
        swapped_pairs = {frozenset({a, b}), frozenset({c, d})}
        if mod_wiring != original_wiring and is_involution(mod_wiring):
            desc = f"Swapped pairs: ({a}-{b}) with ({c}-{d}) -> ({a}-{d}), ({c}-{b})"
            candidates.append((mod_wiring, desc, swapped_pairs))
        candidate = wiring.copy()
        candidate[Mapping.letters_list.index(a)] = c
        candidate[Mapping.letters_list.index(c)] = a
        candidate[Mapping.letters_list.index(b)] = d
        candidate[Mapping.letters_list.index(d)] = b
        mod_wiring = "".join(candidate)
        swapped_pairs = {frozenset({a, b}), frozenset({c, d})}
        if mod_wiring != original_wiring and is_involution(mod_wiring):
            desc = f"Swapped pairs: ({a}-{b}) with ({c}-{d}) -> ({a}-{c}), ({b}-{d})"
            candidates.append((mod_wiring, desc, swapped_pairs))
    return candidates


def generate_extended_modified_reflectors(original_wiring):
    extended_candidates = set()
    base_candidates = generate_modified_reflectors(original_wiring)
    for candidate, desc, swapped_pairs in base_candidates:
        further_candidates = generate_modified_reflectors(candidate)
        for cand2, desc2, swapped_pairs2 in further_candidates:
            if swapped_pairs.intersection(swapped_pairs2):
                continue
            combined_desc = desc + " then " + desc2
            extended_candidates.add((cand2, combined_desc))
    return list(extended_candidates)


def break_code5():
    ciphertext = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"
    social_media_keywords = [
        "FACEBOOK", "TWITTER", "INSTAGRAM", "LINKEDIN", "YOUTUBE",
        "REDDIT", "TIKTOK", "SNAPCHAT", "PINTEREST"
    ]
    rotors = ["V", "II", "IV"]
    ring_settings = [6, 18, 7]
    starting_positions = "AJL"
    plugboard_pairs = ["UG", "IE", "PO", "NX", "WT"]

    print("Breaking Code 5 (searching for non-standard reflector modifications):")
    for std in ["A", "B", "C"]:
        original_wiring = Mapping.reflector_dict[std]['wiring_pattern']
        base_candidates = generate_modified_reflectors(original_wiring)
        extended_candidates = generate_extended_modified_reflectors(original_wiring)
        all_candidates = extended_candidates  # Using extended candidates (8 letters modified)
        print(f"Total extended candidates from standard reflector {std}: {len(all_candidates)}")
        for mod_wiring, desc in all_candidates:
            try:
                enigma = EnigmaMachine(rotors, mod_wiring, ring_settings, starting_positions, plugboard_pairs)
            except Exception:
                continue
            decrypted = enigma.encode(ciphertext, reset=True)
            if any(keyword in decrypted for keyword in social_media_keywords):
                print("Candidate found!")
                print("Original Reflector:", std)
                print("Modification:", desc)
                print("Custom reflector wiring:", mod_wiring)
                print("Decrypted text:", decrypted)
                return
    print("Code 5 search complete.\n")
