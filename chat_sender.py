import socket
import threading

TARGET_IP = "127.0.0.1"
PORT = 5001

pending_messages = {}  # Formato sugerido: {id_inteiro: "texto da mensagem"}
msg_counter = 1
lock = threading.Lock()


def listen_receipts(sock):
  """Thread em background para receber recibos sem bloquear o terminal."""
  while True:
    try:
      data, _ = sock.recvfrom(1024)
      raw = data.decode("utf-8")

      # TODO 1: Fazer o parsing do recibo recebido
      partes = raw.split("|") # dicionario dividido em 2 partes: tipo da msg e id

      # TODO 2: Verificar se o tipo é "DELIVERED"
      if partes[0] != "DELIVERED": # se n for do tipo DELIVERED apenas ihnora
        continue

      # TODO 3: Extrair o ID confirmado
      msg_id = int(partes[1])

      # TODO 4: Com o lock adquirido, remover a mensagem de pending_messages e imprimir aviso visual de entrega confirmada (ex: [✓✓ Entregue])
      with lock: #o lock é usado p garantir q so uma thread acesse o dic de pending_messages por vez
        if msg_id in pending_messages:
          texto = pending_messages.pop(msg_id) #.pop remove a msg do dic e retorna o valor 
          print(f"\n✓✓ Mensagem {msg_id} confirmada: \"{texto}\"")
          print("Digite uma mensagem: ", end="", flush=True)
    except Exception:
      break


def run_chat_sender():
  global msg_counter

  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # comeca a thread que processa os ACKs recebidos em segundo plano
    listener = threading.Thread(target=listen_receipts, args=(s,), daemon=True)
    listener.start()

    print("Comandos especiais:")
    print("/status     Mostra mensagens ainda pendentes")
    print("/reenviar   Reenvia todas as mensagens pendentes\n")

    while True:
      try:
        user_input = input("Digite uma mensagem: ").strip()
        if not user_input:
          continue

        if user_input == "/status":
          # TODO 5: Exibir quantas e quais mensagens continuam em pending_messages
          with lock:
            if not pending_messages:
              print("/status: nenhuma mensagem pendente. Tudo entregue!")
            else:
              print(f"/status: {len(pending_messages)} mensagens pendentes:")
              for msg_id, texto in pending_messages.items():
                print(f"  - ID {msg_id}: \"{texto}\" - Pendente")
          continue

        if user_input == "/reenviar":
          # TODO 6: Iterar por todas as mensagens ainda em pending_messages e reenviá-las com s.sendto(..., (TARGET_IP, PORT))
          with lock:
            if not pending_messages:
              print("/reenviar: Nenhuma mensagem pendente para reenviar.")
            else:
              for msg_id, texto in pending_messages.items():
                pacote = f"MSG|{msg_id}|{texto}"
                s.sendto(pacote.encode("utf-8"), (TARGET_IP, PORT))
                print(f"/reenviar: ID {msg_id}: \"{texto}\"")
          continue

        # Fluxo de envio de mensagem normal:
        # TODO 7: Associar a mensagem ao msg_counter atual e salvar em pending_messages
        with lock:
          current_id = msg_counter
          pending_messages[current_id] = user_input
          msg_counter += 1

        # TODO 8: Montar o pacote no formato "MSG|<ID>|<CONTEUDO>"
        pacote = f"MSG|{current_id}|{user_input}"

        # TODO 9: Enviar o pacote via UDP usando s.sendto(...)
        s.sendto(pacote.encode("utf-8"), (TARGET_IP, PORT))

        # TODO 10: Incrementar msg_counter e avisar na tela que ela está pendente
        print(f"/enviar: msg {current_id} enviada, aguardando confirmação...")

      except KeyboardInterrupt:
        print("\nencerrando cliente...")
        break


if __name__ == "__main__":
  run_chat_sender()