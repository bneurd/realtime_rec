import socket
from sys import exit
from time import time


def test(ip, port):
    # configurações de conexão com o UDP
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = (ip, port)
    udp.bind(host)
    addr = None
    # variáveis de controle do teste
    n_times_avg = 10
    n_samples = list()
    for _ in range(n_times_avg + 1):
        count = 0
        now = time()
        while (time() - now) < 1:
            try:
                data, addr = udp.recvfrom(1024)
                count += 1
            except KeyboardInterrupt:
                udp.close()
                exit()
        print(count)
        n_samples.append(count)
    avg_sr = sum(n_samples[1:]) / n_times_avg
    return avg_sr, addr


if __name__ == "__main__":
    sr, addr = test('127.0.0.1', 5002)
    print('Sample Rate = {} Hz from address {}'.format(sr, addr))