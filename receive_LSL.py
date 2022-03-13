import numpy as np
from datetime import datetime
from time import sleep, time
from pylsl import StreamInlet, resolve_stream
import string


def run(t_move, t_rest, protocol, name, sr, type):
    
    # configurações de conexão com o LSL
    stream = resolve_stream('type', type)
    inlet = StreamInlet(stream[0])
    # criação da lista principal que irá armazenar o dataset
    dataset = list()
    # para calcular o tempo total do experimento
    time_exp = list()
    print('\n' * 60)
    for act in protocol:
        print(f'\nRealização do movimento: {act.upper()}')
        # armazenando uma sequência de dados de uma ação
        trial = list()
        # armazenamento o timestamp para verificar a taxa de amostragem
        last_ts = 0
        dtss = list()
        # a quantidade de dados que devem ser recebidos é a taxa de amostragem
        # multiplicado pelo tempo da em segundos da ação
        n_data = sr * t_move
        # limpando buffer acumulado durante o descanço
        inlet.flush()
        t_init = time()
        for _ in range(n_data):
            sample, timestamp = inlet.pull_sample()
            if timestamp:
                trial.append(sample)
                if last_ts == 0:
                    last_ts = timestamp
                    dtss.append(0)
                else:
                    dtss.append(timestamp - last_ts)
                    last_ts = timestamp
        time_lapsed = time() - t_init
        # acrescentando o trial ao dataset
        dataset.append(trial)
        if INFO:
            # verificação da taxa de amostragem
            print(f'Média da ação: {(sum(dtss) / len(dtss) * sr * t_move)} seg.')
            dtss.sort()
            print(f'Mediana da ação: {(dtss[len(dtss) // 2] * sr * t_move)} seg.')
            print(f'Tempo real decorrido da ação: {time_lapsed} seg.')
            time_exp.append(time_lapsed)
        # aplicando o tempo de descanço
        print('\n---------------------- DESCANÇO ----------------------')
        sleep(t_rest)

    if INFO:
        print(f'\nTempo total de recebimento de dados: {sum(time_exp)} seg.')
        print(f'Tempo ideal: {t_move * len(protocol)} seg.\n')

    # salva os dados
    dataset = np.array(dataset)
    oclock = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
    file_name = '{}_{}'.format(name, oclock)
    np.save(file_name, dataset)
    
    # imprime informações
    print()
    print('-' * 60)
    print('Arquivo "{}.npy" salvo! Dimensionalidade: {}'.format(
        file_name, dataset.shape))
    print('-' * 60)


if __name__ == "__main__":    
    time_move = 8
    time_rest = 8
    protocol = [
        'Fechar a mão',
        'Fazer pinça (objeto pequeno)',
        'Segurar caneta',
        'Segurar cartão',
        'Segurar copo',
        'Fazer gancho (pegar sacola, galão, ...)',
    ]
    name = '1_EMG_Rodrigo'
    # Dados sintéticos do OpenBCI sempre estão em 250 Hz
    # Cyton (BLE): 250 Hz
    # Cyton w/ Daisy (BLE): 125 Hz
    # Ganglion (BLE): 200 Hz
    sample_rate = 250
    type = 'EMG'
    # mostrar informações de tempo
    INFO = True
    run(time_move, time_rest, protocol, name, sample_rate, type)
