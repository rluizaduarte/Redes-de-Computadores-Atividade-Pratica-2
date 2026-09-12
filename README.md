# Mini-Chat UDP

Atividade da disciplina de Redes de Computadores. A ideia foi simular um chat simples usando UDP, onde o próprio canal descarta pacotes de propósito (40% de chance), e a aplicação precisa se virar para saber se a mensagem chegou ou não — usando IDs, recibos de confirmação (`DELIVERED`) e reenvio manual das mensagens que não foram entregues.

O relatório completo (explicação da estratégia, prints e discussão) está na pasta `docs/`.

## Como rodar

Clone o repositório:

```bash
git clone <link-do-repositorio>
cd <pasta-do-repositorio>
```

Abra dois terminais na pasta do projeto.

No primeiro terminal, rode o servidor:
```bash
python3 chat_receiver.py
```

No segundo, rode o cliente:
```bash
python3 chat_sender.py
```

No cliente, basta digitar mensagens normalmente. Comandos especiais:
- `/status` → mostra as mensagens que ainda não foram confirmadas
- `/reenviar` → reenvia todas as mensagens pendentes
