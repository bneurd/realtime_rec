import socket
from sys import exit
from time import time


def test(ip, port):e
    # configurações de conexão com o UDP
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = (ip, port)
    udp.bind(host)
    addr = None
    # variáveis de controle do teste
    n_avg = 5000
    t_samples = list()
    for _ in range(n_avg):
        now = time()
        try:
            data, addr = udp.recvfrom(1024)
        except KeyboardInterrupt:
            udp.close()
            exit()
        t_samples.append(time() - now)
    avg_sr = 1 / (sum(t_samples) / n_avg)
    return avg_sr, addr


if __name__ == "__main__":
    sr, addr = test('127.0.0.1', 5002)
    print('Sample Rate = {} Hz from address {}'.format(sr, addr))