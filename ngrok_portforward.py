import subprocess
import webbrowser


def enable_ngrok():
    process = subprocess.Popen(['ngrok', 'http', '6969'])
    webbrowser.open('http://localhost:4040/inspect/http')
    
    input('Portforwarding is enabled. Press enter to exit...')
    process.terminate()
    
    
if __name__ == '__main__': enable_ngrok()