import random
import socket

HOST = "0.0.0.0"
PORT = 5001
DROP_RATE = 0.4  # 40% de perda (aleatorio, eu q defini de acordo com o enunciado do trabalho)

def run_chat_receiver():
  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"Online na porta {PORT} (Drop Rate: {DROP_RATE * 100}%)...")

    while True:
      data, addr = s.recvfrom(1024)

      # simulando um possivel descarte de pacote c a drop rate 
      if random.random() < DROP_RATE:
        print("[CANAL] Pacote descartado artificialmente!")
        continue

      raw_message = data.decode("utf-8")

      # TODO 1: Fazer o split da mensagem delimitada por '|'
      partes = raw_message.split("|", 2) # dicionario dividido em 3 partes: tipo da msg, id e texto

      # TODO 2: Verificar se a mensagem é do tipo 'MSG'
      if partes[0] != "MSG": # se n for do tipo MSG
        print(f"essa mensagem não é do tipo 'MSG': {raw_message}")
        continue

      # TODO 3: Extrair o ID da mensagem e o texto do usuário
      msg_id = partes[1]
      texto = partes[2]

      # TODO 4: Exibir no terminal a mensagem recebida e o ID correspondente
      print(f"Mensagem recebida ID {msg_id} de {addr}: {texto}")

      # TODO 5: Montar o pacote de recibo no formato "DELIVERED|<ID>"
      recibo = f"DELIVERED|{msg_id}"

      # TODO 6: Enviar o recibo de volta para a origem usando s.sendto(..., addr)
      s.sendto(recibo.encode("utf-8"), addr)

if __name__ == "__main__":
  run_chat_receiver()