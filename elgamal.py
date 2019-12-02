import math
import secrets
import random
from typing import Tuple, List

# For more details on the cryptossystem
DEBUG = True

def miller_rabin(n: int, k=40):
    """
    Algoritmo de Miller-Rabin para teste de primos.
    Para mais informações: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    @param n: Numero que queremos testar
    @param k: Numero de rounds de teste
    """
    if not (n&1):
        return False
    (r, s) = (0, n - 1)
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x*x)%n
            if x == n - 1:
                break
        else:
            return False
    return True

def find_prime(length: int):
    """
    Gera numeros aleatorios de length bits
    e testa cada numero com miller_rabin ate que um seja provavelmente primo.
    Buscamos um "safe prime", i.e. um primo P tal que (P-1)/2 seja primo também.
    """
    p = 4  # Obviamente não é primo
    q = 2
    # keep testing until one is found
    count = 0   # Quantidade de numeros testados 
    while(not miller_rabin(p) or not miller_rabin(q)):
        # Gera numero aleatorio de length/2 bits
        count += 1
        q = secrets.randbits(length - 1)
        q = q | 1   # Força ele ser ímpar
        q = q | (1 << length-1)
        p = 2*q + 1 # Numero de length bits
    print("DEBUG - Prime chosen is {}\nDEBUG - Prime factor {}\n".format(p, q) if DEBUG else "", end="")
    print("DEBUG - Numeros de tentativas ate encontrar o primo: {}\n".format(count) if DEBUG else "", end="")
    return (p, q)

def find_primitive_root(p: int, q: int):
    """
    Dado um primo seguro p, com fator primo q, encontra uma raíz geradora de Zp
    """
    # One easy way of selecting a random generator is to select a random value ℎ between 2 and 𝑝−1, and compute ℎ^((𝑝−1)/𝑞) mod 𝑝.
    # if that value is not 1 (and with high probability, it won't be), then ℎ^((𝑝−1)/𝑞) mod 𝑝 is your random generator.
    # https://crypto.stackexchange.com/questions/9006/how-to-find-generator-g-in-a-cyclic-group

    # An alternative method of finding a generator 𝑔: 
    # if you selected a safe prime, and if your safe prime also satisfied the condition 𝑝 = 7 mod 8, 
    # then the value 𝑔=2 will always be a generator for the group of size 𝑞.
    if p%8 == 7:
        print("DEBUG - Generator is {} (special case)\n".format(2) if DEBUG else "", end="")
        return 2
    while(1):
        g = random.randint( 2, p-1 )
        g = pow(g, (p-1)//q, p)
        if g != 1:
            print("DEBUG - Generator is {}\n".format(g) if DEBUG else "", end="")
            return g


def generate_key_pair(length = 1048):
    """
    Generates a (private, public) key pair for ElGamal cryptossystem.
    """
    (p, q) = find_prime(length)         # Prime
    root = find_primitive_root(p, q)    # Generator
    x = random.randint(1, q - 1)        # Random int - private key
    h = pow(root, x, p)
    # (private, public)
    print("DEBUG - x is {}\n".format(x) if DEBUG else "", end="")
    print("DEBUG - h is {}\n".format(h) if DEBUG else "", end="")
    return ((x, q, p), (h, root, p, q))

def encrypt(public_key: Tuple, message: str):
    """
    Given a public key and a message, encrypts the message.
    """
    (h, root, p, q) = public_key
    message = to_ascii(message, q)
    y = random.randint(1, q-1)
    s = pow(h, y, p)
    c1 = pow(root, y, p)
    c2 = list(map(lambda x: (x*s)%p, message))
    return (c1, c2)

def decrypt(private_key, cypher):
    (c1, c2) = cypher
    (x, q, p) = private_key
    s_inverse = pow(c1, q - x, p) 
    m = list(map(lambda x: str((x * s_inverse)%p), c2))
    return to_string(m)

def separate_chars(message):
    parts = []
    message = list(map(str, message))
    message = "".join(message)
    i = 0
    while i < len(message):
        chunk = message[i: i+3]
        if(int(chunk) < 255):
            parts.append(chunk)
            i += 3
        else:
            parts.append(message[i:i+2])
            i += 2
    return list(map(int, parts))
    
def break_message(message, max_length):
    if int(message) >= max_length:
        l = len(message) // 2
        left = break_message(message[0:l], max_length)
        right = break_message(message[l:], max_length)
        ans = []
        for el in left:
            ans.append(el)
        for el in right:
            ans.append(el)
        return ans
    else:
        return [message]

def to_ascii(message, max_length):
    message = ''.join(str(ord(c)).zfill(3) for c in message)
    chunks = break_message(message, max_length)
    # Quebra a mensagem em chunks menores do que max_length
    print(("DEBUG - Message Chunks: " + " ".join(chunks)) if DEBUG else "")
    return list(map(int, chunks))

def to_string(message):
    message = list(map(str, message))
    message = separate_chars(message)
    message = ''.join(chr(c) for c in message)
    return str(message)