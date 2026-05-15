#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import os, urllib.parse, mimetypes, json, re, socket, argparse
import qrcode

# Globals
PORT = 6969
BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
HTML = ""


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def print_qr(url):
    import sys
    import os
    if os.name == 'nt':
        os.system('chcp 65001 >nul 2>&1')
        
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)

    print("\n  Scan to open FileSync:\n")
    try:
        qr.print_ascii(invert=True)
    except UnicodeEncodeError:
        print("  [QR Code cannot be displayed in this terminal encoding]")
    print()


def build_html(port):
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FileSync</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Inter:wght@400;600&display=swap');

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  min-height: 100vh;
  background: url('https://wallpapercave.com/wp/wp9225755.jpg') center / cover fixed;
  font-family: 'Inter', sans-serif;
  color: #e5e7eb;
  position: relative;
}}

body::before {{
  content: '';
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at top, rgba(0,0,0,.65), rgba(0,0,0,.9));
  backdrop-filter: blur(12px);
  z-index: 0;
}}

.container {{
  max-width: 960px;
  margin: auto;
  padding: 48px 20px;
  position: relative;
  z-index: 1;
}}

.header {{
  text-align: center;
  margin-bottom: 56px;
}}

.title {{
  font-family: 'Orbitron', monospace;
  font-size: 46px;
  font-weight: 800;
  letter-spacing: 2px;
  background: linear-gradient(90deg, #22d3ee, #34d399, #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.subtitle {{
  margin-top: 12px;
  color: #9ca3af;
}}

.glass {{
  background: rgba(15,15,20,.65);
  backdrop-filter: blur(25px);
  border-radius: 22px;
  border: 1px solid rgba(255,255,255,.08);
  padding: 36px;
  margin-bottom: 42px;
}}

.upload-area {{
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}}

input[type=file] {{
  flex: 1;
  min-width: 220px;
  padding: 14px;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.15);
  border-radius: 14px;
  color: #e5e7eb;
}}

button {{
  padding: 14px 32px;
  border-radius: 14px;
  border: none;
  font-family: 'Orbitron';
  background: linear-gradient(135deg,#22d3ee,#6366f1);
  color: #020617;
  cursor: pointer;
}}

.file {{
  display: flex;
  justify-content: space-between;
  padding: 14px;
  margin-bottom: 12px;
  border-radius: 14px;
  background: rgba(255,255,255,.05);
}}

.file a {{
  color: #67e8f9;
  text-decoration: none;
}}

.empty {{
  text-align: center;
  color: #9ca3af;
}}

.footer {{
  text-align: center;
  color: #6b7280;
}}
</style>
</head>
<body>

<div class="container">
    <div class="header">
        <div class="title">FILESYNC</div>
        <div class="subtitle">Local network transfer interface</div>
    </div>

    <div class="glass">
        <div class="upload-area">
            <input type="file" id="file" multiple>
            <button onclick="upload()">UPLOAD</button>
        </div>
    </div>

    <div class="glass">
        <h2>AVAILABLE FILES</h2>
        <div id="files"></div>
    </div>

    <div class="footer">
        PORT {port} • SYSTEM ONLINE
    </div>
</div>

<script>
async function upload() {{
    const input = document.getElementById('file');

    if (!input.files.length) return;

    for (const f of input.files) {{
        const fd = new FormData();
        fd.append("file", f);

        await fetch("/", {{
            method: "POST",
            body: fd
        }});
    }}

    input.value = "";
    loadFiles();
}}

async function loadFiles() {{
    const res = await fetch("/files");
    const files = await res.json();

    const div = document.getElementById("files");

    if (!files.length) {{
        div.innerHTML = '<div class="empty">NO FILES DETECTED</div>';
        return;
    }}

    div.innerHTML = "";

    files.forEach(f => {{
        div.innerHTML += `
        <div class="file">
            <div>${{f}}</div>
            <a href="/download?file=${{encodeURIComponent(f)}}">DOWNLOAD</a>
        </div>`;
    }});
}}

loadFiles();
</script>

</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        p = urllib.parse.urlparse(self.path)

        if p.path == "/":
            self.send_html()

        elif p.path == "/files":
            self.send_files()

        elif p.path == "/download":
            self.send_file(p.query)

        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        boundary = self.headers["Content-Type"].split("boundary=")[1].encode()
        body = self.rfile.read(length)

        for part in body.split(boundary):
            if b'filename="' in part:
                name = re.search(b'filename="(.+?)"', part)

                filename = os.path.basename(name.group(1).decode())
                data = part.split(b"\r\n\r\n", 1)[1].rstrip(b"\r\n")

                with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
                    f.write(data)

        self.send_response(200)
        self.end_headers()

    def send_html(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.encode())

    def send_files(self):
        files = sorted(
            f for f in os.listdir(UPLOAD_DIR)
            if os.path.isfile(os.path.join(UPLOAD_DIR, f))
        )

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(files).encode())

    def send_file(self, query):
        f = os.path.basename(
            urllib.parse.parse_qs(query)["file"][0]
        )

        path = os.path.join(UPLOAD_DIR, f)

        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header(
            "Content-Disposition",
            f'attachment; filename="{f}"'
        )
        self.end_headers()

        with open(path, "rb") as fh:
            self.wfile.write(fh.read())


def parse_args():
    parser = argparse.ArgumentParser(
        prog="proshare",
        description="ProShare -- Share files instantly"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=6969
    )

    parser.add_argument(
        "--dir",
        type=str,
        default=os.getcwd()
    )

    return parser.parse_args()


def main():
    global PORT, BASE_DIR, UPLOAD_DIR, HTML

    args = parse_args()

    PORT = args.port
    BASE_DIR = os.path.abspath(args.dir)
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    HTML = build_html(PORT)

    ip = get_local_ip()
    url = f"http://{ip}:{PORT}"

    print(f"\n  [*] FileSync")
    print(f"  [>] {url}")
    print(f"  [~] Serving: {UPLOAD_DIR}")
    print(f"  [!] Ctrl+C to stop")

    print_qr(url)

    try:
        HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n  FileSync stopped.\n")


if __name__ == "__main__":
    main()