import time
import traceback

import websockets
import asyncio
import socket

from connection import Connection
from game import Game


async def on_client_connected(ws, path):
    print(f'Client connected from {ws.remote_address[0]}')

    try:
        # TODO: Move game to separate thread.
        conn = Connection(ws)
        game = Game(conn)

        while True:
            game.loop()

            send_task = asyncio.ensure_future(conn.send_state(game.state))
            recv_task = asyncio.ensure_future(conn.recv_state(game.state))

            done, pending = await asyncio.wait([send_task, recv_task], return_when = asyncio.FIRST_COMPLETED, timeout = 1.0 / game.tick_rate)
            for task in pending: task.cancel()

            # Unpack exceptions from future so they can be caught.
            for task in done:
                e = task.exception()
                if e is not None: raise e
    except Exception as e:
        print(f'Error occurred in connection with {ws.remote_address[0]}: {e}')
        print(f'Stacktrace:')
        traceback.print_exc()


require_connection = False
if require_connection:
    # Note: connect with local ip, (e.g. 192.168.*.*:6969) or normal IP if portforwarding is enabled.
    # localhost and loopback address are unlikely to work.
    local_ip = socket.gethostbyname(socket.gethostname())
    server_fn = websockets.serve(on_client_connected, local_ip, 6969)

    print('Waiting for connection at port 6969.')
    asyncio.get_event_loop().run_until_complete(server_fn)
    asyncio.get_event_loop().run_forever()
else:
    game = Game(None)

    while True:
        game.loop()
        time.sleep(1.0 / game.tick_rate)


