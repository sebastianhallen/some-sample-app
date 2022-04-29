from workshopapp.server import SocketServerTipOfTheDayServer
from workshopapp.tipoftheday import StaticTipOfTheDaySource

if __name__ == '__main__':
    tip_source = StaticTipOfTheDaySource()
    host = SocketServerTipOfTheDayServer(tip_source=tip_source)

    host.serve()