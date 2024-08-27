import socket
from tkinter import Tk, Text, END, messagebox
from tkinter.ttk import Label, Entry, Button, Style
import threading

class PortScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner")
        self.center_window(400, 400)

        style = Style()
        style.theme_use('clam')

        Label(root, text="Host:").grid(row=0, column=0, pady=10, padx=10, sticky='e')
        self.entry_host = Entry(root, width=30)
        self.entry_host.grid(row=0, column=1, padx=10)

        Label(root, text="Porta Inicial:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entry_port_start = Entry(root, width=30)
        self.entry_port_start.grid(row=1, column=1, padx=10, pady=5)

        Label(root, text="Porta Final:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.entry_port_end = Entry(root, width=30)
        self.entry_port_end.grid(row=2, column=1, padx=10, pady=5)

        Button(root, text="Escanear", command=self.start_scan_thread).grid(row=3, column=0, columnspan=2, pady=10)

        self.result_text = Text(root, height=10, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.load_ports()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def load_ports(self):
        self.ports = {}
        try:
            with open('ports.txt', 'r') as file:
                for line in file:
                    port, service = line.strip().split(':')
                    self.ports[int(port)] = service
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load port data: {e}")

    def scan_port(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0

    def start_scan_thread(self):
        # Inicia uma thread separada para não travar a interface gráfica durante o scan
        scan_thread = threading.Thread(target=self.start_scan)
        scan_thread.start()

    def start_scan(self):
        host = self.entry_host.get().strip()
        port_start = self.entry_port_start.get().strip()
        port_end = self.entry_port_end.get().strip()

        if not host:
            messagebox.showerror("Error", "Host/IP não pode ser vazio.")
            return

        if not port_start.isdigit() or not port_end.isdigit():
            messagebox.showerror("Error", "As portas devem ser números.")
            return

        port_start = int(port_start)
        port_end = int(port_end)

        # Exibe uma mensagem de carregamento enquanto o escaneamento está sendo realizado
        self.result_text.delete('1.0', END)
        self.result_text.insert(END, "Escaneamento em progresso...\n")
        self.result_text.update_idletasks()  # Atualiza a interface antes de começar o escaneamento

        for port in range(port_start, port_end + 1):
            if port in self.ports:
                service = self.ports[port]
                if self.scan_port(host, port):
                    self.result_text.insert(END, f"Port {port} is open ({service})\n")
                else:
                    self.result_text.insert(END, f"Port {port} is closed ({service})\n")
            else:
                if self.scan_port(host, port):
                    self.result_text.insert(END, f"Port {port} is open (Unknown Service)\n")
                else:
                    self.result_text.insert(END, f"Port {port} is closed (Unknown Service)\n")
        
        self.result_text.insert(END, "Escaneamento concluído.\n")

# GUI
root = Tk()
PortScanner(root)
root.mainloop()
