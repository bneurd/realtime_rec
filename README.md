# RealTime Record
## Sincronizador de dados recebidos por UDP/LSL e marcadores

### `test_sr_UDP.py`

Um teste para obter a taxa de amostragem dos dados recebidos em UDP.

### `receive_UDP.py`

Realiza um loop direto para recebimento dos dados em UDP.

Os primeiros N dados que foram acumulados durante o tempo de descanço do
protocolo são descartados no momento da gravação.

### `receive_subproc_UDP.py`

Utiliza uma fila para recebimento dos dados em UDP em um subprocesso.

Os primeiros N dados que foram acumulados durante o tempo de descanço
são descartados realizando um *flush* na fila antes do recebimento de 
um novo *trial*.

### `receive_LSL.py`

Utiliza uma fila para recebimento dos dados em LSL.

A verificação da taxa de amostragem é realizada com base no dado de 
*timestamp* recebido pelo objeto `inlet`. As perdas de pacote são informadas,
porém sempre o valor recebido é equiparado à taxa de amostragem.
