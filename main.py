import elgamalCopy as elgamal

dic = {}

a = elgamal.generate_keys(256)

string = "Olá, mundo!"

cipher = elgamal.encrypt(a['publicKey'], string)

plaintext = elgamal.decrypt(a['privateKey'], cipher)

print(string)
print(cipher)
print(plaintext)
