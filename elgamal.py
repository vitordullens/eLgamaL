import math
import random


def miller_rabin(n, k=40):
	"""
	Algoritmo de Miller-Rabin para teste de primos.
	Para mais informações: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
	@param n: Numero que queremos testar
	@param k: Numero de rounds de teste
	"""
    if not n&1:
			return False
    (r, s) = (0, n - 1)
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def find_prime(length):
    p = 4  # Obviamente não é primo
	# keep testing until one is found
	while(not miller_rabin(p)):
		# Gera numero aleatorio de length bits
		p = random.randint(2**(length-1), 2**length)
		# Verifica se o número é impar
		if not p&1:
			p += 1
	return p

def find_primitive_root(p):
    # Fatorar 𝜙(p) = p-1
    # Calcular a^(s/p) mod p para todos os divisores de p-1
    # Se algum deles for 1 então a NÃO é raíz.
    # Se todos forem != 1, então a É raíz.
    # https://math.stackexchange.com/questions/124408/finding-a-primitive-root-of-a-prime-number
    s = p-1
    fatores = []
    for( a in range(2, math.sqrt(p))):
        if(s%a == 0):
            while(s%a == 0):
                s = s // a
            fatores.append(a)
    if(s > 1):
        fatores.append(s)
    # Testa um numero aleatorio g ate que encontre a raiz primitiva modulo p
    while(1):
        g = random.randint( 2, p-1 )
        valid = True
        # Teste
        for(f in fatores):
            if(pow(g, (p-1)//f, p) == 1):
                valid = False
                break
        if(valid):
            return g
