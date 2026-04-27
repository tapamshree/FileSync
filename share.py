from http.server import HTTPServer, BaseHTTPRequestHandler
import os, urllib.parse, mimetypes, json, re, socket

PORT = 6969
BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

HTML = f"""
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
    text-shadow: 0 0 25px rgba(56,189,248,.35);
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
    box-shadow:
        0 0 0 1px rgba(34,211,238,.08),
        0 30px 80px rgba(0,0,0,.7);
    position: relative;
}}

.glass::before {{
    content:'';
    position:absolute;
    inset:0;
    border-radius:22px;
    background: linear-gradient(120deg, transparent, rgba(56,189,248,.12), transparent);
    pointer-events:none;
}}

.upload {{
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
    letter-spacing: 1px;
    background: linear-gradient(135deg,#22d3ee,#6366f1);
    color: #020617;
    cursor: pointer;
    transition: .25s;
    box-shadow: 0 0 30px rgba(56,189,248,.35);
}}

button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 0 45px rgba(56,189,248,.6);
}}

.files {{
    padding: 36px;
}}

.files h2 {{
    font-family: 'Orbitron';
    font-size: 22px;
    margin-bottom: 26px;
    letter-spacing: 1px;
}}

.file {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 16px 20px;
    margin-bottom: 12px;
    border-radius: 16px;
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.1);
}}

.file-name {{
    min-width: 0;
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 600;
}}

.file a {{
    flex-shrink: 0;
    padding: 8px 18px;
    border-radius: 10px;
    font-family: 'Orbitron';
    font-size: 13px;
    text-decoration: none;
    color: #67e8f9;
    border: 1px solid rgba(34,211,238,.5);
    background: rgba(34,211,238,.12);
    transition: .2s;
}}

.file a:hover {{
    background: rgba(34,211,238,.3);
}}

.empty {{
    text-align: center;
    padding: 60px 0;
    color: #9ca3af;
}}

.footer {{
    margin-top: 48px;
    text-align: center;
    font-size: 13px;
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

    <div class="glass upload">
        <div class="upload-area">
            <input type="file" id="file" multiple>
            <button onclick="upload()">UPLOAD</button>
        </div>
    </div>

    <div class="glass files">
        <h2>AVAILABLE FILES</h2>
        <div id="files"></div>
    </div>

    <div class="footer">
        PORT {PORT} • SYSTEM ONLINE
    </div>

</div>

<script>
async function upload() {{
    const i = document.getElementById('file');
    if (!i.files.length) return;
    for (const f of i.files) {{
        const fd = new FormData();
        fd.append("file", f);
        await fetch("/", {{method:"POST", body:fd}});
    }}
    i.value = "";
    loadFiles();
}}

async function loadFiles() {{
    const r = await fetch("/files");
    const files = await r.json();
    const d = document.getElementById("files");
    if (!files.length) {{
        d.innerHTML = '<div class="empty">NO FILES DETECTED</div>';
        return;
    }}
    d.innerHTML = "";
    files.forEach(f => {{
        d.innerHTML += `
        <div class="file">
            <div class="file-name">${{f}}</div>
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
                data = part.split(b"\r\n\r\n",1)[1].rstrip(b"\r\n")
                with open(os.path.join(UPLOAD_DIR, filename),"wb") as f:
                    f.write(data)
        self.send_response(200)
        self.end_headers()

    def send_html(self):
        self.send_response(200)
        self.send_header("Content-Type","text/html")
        self.end_headers()
        self.wfile.write(HTML.encode())

    def send_files(self):
        files = sorted(f for f in os.listdir(BASE_DIR)
                       if os.path.isfile(f) and not f.startswith("."))
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(files).encode())

    def send_file(self, query):
        f = os.path.basename(urllib.parse.parse_qs(query)["file"][0])
        path = os.path.join(BASE_DIR, f)
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Disposition", f'attachment; filename="{f}"')
        self.end_headers()
        with open(path,"rb") as fh:
            self.wfile.write(fh.read())

if __name__ == "__main__":
    ip = get_local_ip()
    print(f"🚀 NEON NODE RUNNING ON PORT {PORT}")
    print(f"🔗 here is the link : http://{ip}:{PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
