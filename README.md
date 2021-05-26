# Traffic Simulator
A traffic simulation and associated controller, written in Python and C++ respectively.

### Controller
The controller must be compiled into an executable before use. See `./controller/README.md` for instructions.  
When starting the controller, you will be prompted to pick a management strategy, an update interval and an address to connect to.  
You can press enter to use the provided default values instead of entering one.  

### Simulation
To run the simulation over the internet, some form of portforwarding is required. If you cannot portforward, NGROK can be used,
in combination with the `./ngrok_portforward.py` script.  
This script will open a browser page, showing the address at which the simulation is available. You should replace the `http` prefix with `ws` before using this address.  
The NGROK executable must be in your PATH before using this script.

You can drag the mouse to move around in the simulation. E and F will show intersecting traffic lights and sensor connections respectively.  
It is possible to force a light to green by clicking and holding it down.