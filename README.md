# Enigma

A Python implementation of the German Enigma Machine used during World War II. This library accurately simulates core components including rotors, plugboards, and reflectors, and provides utilities for both encryption and code-breaking operations.

![Language](https://img.shields.io/badge/language-Python-blue)
![Version](https://img.shields.io/badge/version-v1.0.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)
![Python Version](https://img.shields.io/badge/python-%3E%3D3.6-informational)

## Overview

The Enigma machine was a sophisticated encryption device widely used by German military forces during World War II. This implementation faithfully recreates the mechanical and electrical components of the original machines while providing a clean, intuitive Python interface.

## 📥 Installation

Install directly from GitHub using pip:

```bash
pip install git+https://github.com/alexmgl/enigma.git
```

Or clone the repository and install locally:

```bash
git clone https://github.com/alexmgl/enigma.git
cd enigma
pip install .
```

## ⚙️ Usage

### Basic Encoding and Decoding

The Enigma machine uses the same `.encode` method for both encoding and decoding messages:

```python
from enigma.machine import EnigmaMachine

# Create a machine with default settings
machine = EnigmaMachine()

# Encode a message
ciphertext = machine.encode("HELLOWORLD")
print(ciphertext)  # Example output: 'ILBDAAMTAZ'

# Decode by encoding again (with reset)
plaintext = machine.encode(ciphertext, reset=True)
print(plaintext)  # Output: 'HELLOWORLD'
```

> **Important**: To decode a message, the machine must be in exactly the same configuration as when the message was encoded. Use `reset=True` in the `encode` method or call `machine.reset()` separately.

### Custom Configuration

Create an Enigma machine with specific historical configurations:

```python
from enigma.machine import EnigmaMachine

# Create a machine with custom settings
machine = EnigmaMachine(
    rotors=["V", "II", "IV"],        # Rotor selection and order
    reflector="B",                    # Reflector type (A, B, or C)
    ring_settings=[6, 18, 7],         # Ring settings (1-26)
    initial_positions="AJL",          # Starting positions for rotors
    plugs=["UG", "IE", "PO", "NX", "WT"]  # Plugboard connections
)

# Encode with custom settings
ciphertext = machine.encode("SECRETMESSAGE")
print(ciphertext)

# Reset machine to initial state
plaintext = machine.encode(ciphertext, reset=True)
print(plaintext)  # Output: 'SECRETMESSAGE'
```

## 🧩 Components

### Rotors

The library includes historically accurate implementations of all standard Wehrmacht and Kriegsmarine rotors:

- Standard rotors: I, II, III, IV, V
- Naval rotors: Beta, Gamma

### Reflectors

Available reflectors:

- Reflector A
- Reflector B
- Reflector C

### Plugboard

The plugboard (Steckerbrett) allows letter pairs to be swapped before and after the main encryption process. Configure up to 10 letter pairs.

## ⚠️ Limitations

- This implementation focuses on the most common Enigma models and does not include specialized variants like the Abwehr Enigma or the Enigma G.
- The simulation is character-based and doesn't account for physical quirks of the original machines.
- Additional rotors: VI, VII, VIII are not yet implemented. 

## 🔍 Technical Details

The encryption process follows the exact electrical pathways of the physical Enigma machine:

1. Input character enters the plugboard
2. Current flows through rotors from right to left
3. Current is reflected by the reflector
4. Current flows back through rotors from left to right
5. Output passes through the plugboard again
6. Rotors advance according to historical stepping mechanisms

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 References

- Crypto Museum: [Enigma cipher machines](https://www.cryptomuseum.com/crypto/enigma/)
- National Security Agency: [The Enigma Machine: Capturing the Enigma](https://www.nsa.gov/History/Cryptologic-History/Historical-Figures-Publications/The-Enigma/)
- Bletchley Park National Codes Centre: [The Enigma Machine](https://bletchleypark.org.uk/our-story/enigma-machine/)

---

Developed with historical accuracy and cryptographic education in mind. Not intended for securing sensitive communications (or future invasions).