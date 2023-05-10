import numpy as np
import socket
from datetime import datetime
from json import loads
from multiprocessing import Process, Queue
from sys import exit
from time import sleep, time


def get_data(udp, queue):
    while True:
        data, addr = udp.recvfrom(1024)
        data = loads(data[:-2].decode('utf-8'))
        queue.put(data['data'])


def flush_queue(queue):
    while not queue.empty():
        queue.get()


def run(t_move, t_rest, protocol, name, sr):
    # configurações de conexão com o UDP
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = ('127.0.0.1', 5002)
    udp.bind(host)
    # configurações de inicialização de processo
    queue = Queue()
    proc = Process(target=get_data, args=(udp, queue))
    proc.start()
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
        flush_queue(queue)
        now = time()
        while (time() - now) < t_move:
            try:
                data = queue.get()
                trial.append(data)
            except KeyboardInterrupt:
                udp.close()
                proc.terminate()
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
            proc.terminate()
            exit()
    # finaliza a conexão e o subprocesso
    udp.close()
    proc.terminate()
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
    name = '1_EMG_Rodrigo'
    sample_rate = 200
    run(time_move, time_rest, protocol, name, sample_rate)
