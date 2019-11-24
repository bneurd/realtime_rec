# UDP_REC
## Sincronizador de dados recebidos por UDP e marcadores

### `test_sample_rate.py`

Um teste para obter a taxa de amostragem dos dados recebidos em UDP.

### `receive.py`

Realiza um loop direto para recebimento dos dados em UDP.

Os primeiros N dados que foram acumulados durante o tempo de descanço do
protocolo são descartados no momento da gravação.

### `receive_subprocess.py`

Utiliza uma fila para recebimento dos dados em UDP em um subprocesso.

Os primeiros N dados que foram acumulados durante o tempo de descanço
são descartados realizando um *flush* na fila antes do recebimento de 
um novo *trial*.