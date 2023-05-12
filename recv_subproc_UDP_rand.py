import numpy as np
import socket
from datetime import datetime
from json import loads
from multiprocessing import Process, Queue
from sys import exit
from time import time
from random import choice


def get_data(udp, queue):
    while True:
        data, _ = udp.recvfrom(1024)
        data = loads(data[:-2].decode('utf-8'))
        queue.put(data['data'])

def flush_queue(queue):
    while not queue.empty():
        queue.get()

def run(t_move, n_movs, protocol, name, sr):    
    # configurações de conexão com o UDP
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = ('127.0.0.1', 12345)
    udp.bind(host)

    # configurações de inicialização de processo
    queue = Queue()
    proc = Process(target=get_data, args=(udp, queue))
    proc.start()
    
    # inicia o protocolo do experimento
    n_data = sr * t_move
    dataset = list()
    mov = ''
    for i in range(n_movs):
        # seleção do movimento atual
        while True:
            new_mov = choice(protocol)
            if new_mov != mov:
                mov = new_mov
                break
        print(f'{i+1}º movimento: {mov.upper()}')
        
        # obtenção e tratamento dos dados
        trial = list()
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
        
        # padronização dos dados (n_trial)
        print('N Trial:', len(trial))
        if len(trial) > n_data:
            print('1ªs {} amostras descartadas'.format(len(trial) - n_data))
            # corta dados do começo por conta do experimento
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

def main():
    time_move = 20
    n_movs = 2
    protocol = ['hand_open', 'hand_close', 'rest']
    name = '1_EMG_Rodrigo'
    sample_rate = 200
    run(time_move, n_movs, protocol, name, sample_rate)

if __name__ == "__main__":
    main()