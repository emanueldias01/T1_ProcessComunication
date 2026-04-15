import socket
import struct
import io
from streams.pixelInputStream import PixelInputStream

class PixelHubUDP():
    def __init__(self, mcast_group="224.1.1.1", mcast_port=50003) -> None:
        self.mcast_group = mcast_group
        self.mcast_port = mcast_port
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)        
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.mcast_port))

        mreq = struct.pack("4sl", socket.inet_aton(self.mcast_group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def recv_pixels(self):
        # tamanho de dados máximo em um pacote UDP
        data, addr = self.sock.recvfrom(10240)
        
        buffer = io.BytesIO(data)
        pis = PixelInputStream(buffer)
        pixels = pis.readPixels()
        return pixels

    def disconnect(self):
        self.sock.close()