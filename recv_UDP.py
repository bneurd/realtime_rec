import numpy as np
import socket
from datetime import datetime
from json import loads
from sys import exit
from time import sleep, time


def run(t_move, t_rest, protocol, name, sr):
    # configurações de conexão com o UDP
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = ('127.0.0.1', 5002)
    udp.bind(host)
    # inicia o protocolo do experimento
    n_data = sr * t_move
    dataset = list()
    for p in protocol:
        # aplicando um tempo de descanço
        print('\nDescanço...\n')
        sleep(time_rest)
        # obtenção e tratamento dos dados
        trial = list()
        print(p)
        now = time()
        while (time() - now) < t_move:
            try:
                data, _ = udp.recvfrom(1024)
                data = loads(data[:-2].decode('utf-8'))
                trial.append(data['data'])
            except KeyboardInterrupt:
                udp.close()
                exit()
        print('N Trial:', len(trial))
        if len(trial) > n_data:
            print('1ªs {} amostras descartadas'.format(len(trial) - n_data))
            dataset.append(trial[(len(trial) - n_data):])
        elif len(trial) == n_data:
            dataset.append(trial)
        else:
            print('Atraso no envio dos dados! Programa finalizado...')
            udp.close()
            exit()
    # finaliza a conexão
    udp.close()
    # salva os dados
    dataset = np.array(dataset)
    oclock = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
    file_name = '{}_{}'.format(name, oclock)
    np.save(file_name, dataset)
    print()
    print('-' * 60)
    print('Arquivo "{}.npy" salvo! Dimensionalidade: {}'.format(
        file_name, dataset.shape))
    print('-' * 60)

if __name__ == "__main__":    
    time_move = 5
    time_rest = 3
    protocol = ['hand_open', 'hand_close', 'okay', 'do_gun']
    name = '2_EMG_Rodrigo'
    sample_rate = 200
    run(time_move, time_rest, protocol, name, sample_rate)
