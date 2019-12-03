import elgamal
import threading
from datetime import datetime
import time
LOCK = threading.Lock()

shared_space = {
    "public_key_receiver": None,
    "messages": None
}
class Sender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        # Recebe mensagem para mandar
        message = input("Message to send...")
        # Aguarda chave publica do recebedor estar pronta
        recebeu = False
        while( not recebeu):
            if not shared_space['public_key_receiver']:
                time.sleep(0.5)
                continue
            else:
                recebeu = True
                break
        LOCK.acquire()
        public = shared_space['public_key_receiver']
        LOCK.release()
        # Encripta a mensagem
        start = datetime.now()
        cypher = elgamal.encrypt(public, message)
        diff = datetime.now() - start
        print("SENDER - Time to encrypt message: {}s".format(diff))
        LOCK.acquire()
        # Envia a mensagem
        shared_space['messages'] = cypher
        print("SENDER - Enviou mensagem encriptada.")
        print("Cypher:", cypher)
        LOCK.release()

class Receiver(threading.Thread):
    def __init__(self):
            threading.Thread.__init__(self)
            self.private_key = None
    
    def run(self):
        # Gera um par de chaves
        start = datetime.now()
        (private, public) = elgamal.generate_key_pair(1048)
        diff = datetime.now() - start
        print("\nRECEIVER - Time to generate keys: {}s".format(diff))
        self.private_key = private
        LOCK.acquire()
        # Compartilha a chave publica
        shared_space['public_key_receiver'] = public
        LOCK.release()
        # Verifica se recebeu mensagem
        recebeu = False
        while( not recebeu):
            if not shared_space['messages']:
                time.sleep(1)
                continue
            else:
                print("RECEIVER - Chegou mensagem")
                recebeu = True
                break
        LOCK.acquire()
        cypher = shared_space['messages']
        LOCK.release()
        # Desencripta mensagem
        start = datetime.now()
        mensagem = elgamal.decrypt(self.private_key, cypher)
        diff = datetime.now() - start
        print("RECEIVER - Time to decrypt message: {}s".format(diff))
        print("Mensagem:", mensagem)
      

sender = Sender()
receiver = Receiver()

sender.start()
receiver.start()

sender.join()
receiver.join()

print("Exiting")