import pygame
# WS server example

import asyncio
import websockets


async def test(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")
    asyncio.get_event_loop().stop()


start_server = websockets.serve(test, "localhost", 8768)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# pygame.init()
# screen = pygame.display.set_mode((700, 500))
# pygame.display.set_caption("trafic simulation")
# run = True
# while run:
#     for event in pygame.event.get():
#         print(event)
#         if event.type == 256:  # quit event
#             run = False
#         screen.fill((50, 50, 50))
#         pygame.display.flip()
