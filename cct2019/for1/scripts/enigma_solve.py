from enigma.machine import EnigmaMachine
import enigma.plugboard
# setup machine according to specs from a daily key sheet:


enigma.plugboard.MAX_PAIRS=13
machine = EnigmaMachine.from_key_sheet(
       rotors='Gamma VI VII VIII',
       reflector='C-Thin',
       ring_settings='R I N G',
       plugboard_settings="AM BY CH DR EL FX GO IV JN KU PS QT WZ")


machine.set_display('AMTU')


ciphertext = 'JHSL PGLW YSQO DQVL PFAO TPCY KPUD TF'.replace(" ", "")


plaintext = machine.process_text(ciphertext)

print(plaintext.lower())


