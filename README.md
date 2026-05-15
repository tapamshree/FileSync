# FileSync

**A sleek, local file sharing server with zero configuration.**

Share files instantly across your local network with a stunning glassmorphic UI, automatic network detection, and a single command to get started. No accounts, no cloud, no nonsense -- just run it and share.

---

## Why FileSync

Most file sharing tools demand sign-ups, cloud storage, or convoluted setup steps. FileSync takes a radically different approach: run one command and every device on your network can upload and download files through a polished browser interface. There is nothing to install on the receiving end, no browser extensions, and no configuration files to edit. It is as convenient as it gets for local file transfers.

Whether you need to push a build artifact to a colleague sitting across the room, hand out lecture slides to a classroom, or move photos between your phone and laptop, FileSync gets the job done in seconds rather than minutes.

---

## Features

- **Zero Config** -- Run a single command and start sharing immediately
- **Pip Installable** -- Install once with `pip install .` and use the `proshare` command from anywhere
- **CLI Arguments** -- Customize port and serving directory at launch without editing source code
- **Auto IP Detection** -- Automatically finds and displays your local network address
- **File Upload and Download** -- Drag-and-drop or click to upload; one-click download for recipients
- **Multiple File Upload** -- Select and upload several files at once in a single operation
- **QR Code on Launch** -- A scannable QR code is printed directly in the terminal so mobile devices can connect instantly without typing the URL
- **Local Network Friendly** -- Works on any shared WiFi or Ethernet network out of the box
- **Lightweight** -- Pure Python with a single lightweight dependency (`qrcode`) for terminal QR code generation
- **Organized Storage** -- Uploaded files are placed in an auto-created `uploads/` directory
- **Clean Server Logs** -- Per-request noise is suppressed for a tidy terminal experience
- **Graceful Shutdown** -- Press Ctrl+C and the server stops cleanly without tracebacks

---

## Quick Start

### Prerequisites

- Python 3.6 or later
- The `qrcode` package (installed automatically when you `pip install .`)

### Option 1 -- Run Directly

```bash
python share.py
```

That is it. The server starts, prints a clickable link and a scannable QR code, and you are ready to share files.

### Option 2 -- Install as a CLI Tool

First, install the package:

```bash
pip install .
```

Then launch FileSync from anywhere using:

```bash
proshare
```

After installation, the `proshare` command is available system-wide, so you can launch FileSync from any directory without referencing the script path. This is especially convenient when you want to quickly serve files from arbitrary folders.

### Example Output

```
  [*] FileSync
  [>] http://192.168.1.100:6969
  [~] Serving: C:\Users\you\Documents
  [!] Ctrl+C to stop

  [QR Code appears here -- scan with any phone camera to open instantly]
```

---

## CLI Options

FileSync accepts command-line arguments so you never need to edit the source code for common adjustments:

```bash
# Use a custom port
proshare --port 8080

# Serve a specific directory
proshare --dir /path/to/shared/folder

# Combine both
proshare --port 8080 --dir ./project-assets
```

| Flag     | Default              | Description                         |
|----------|----------------------|-------------------------------------|
| `--port` | `6969`               | Port the server listens on          |
| `--dir`  | Current directory    | Root directory to serve and browse  |

---

## How to Use

1. **Start the server** using either `python share.py` or the installed `proshare` command.
2. **Scan the QR code** shown in the terminal with your phone camera, or open the printed URL in any browser on your local network.
3. **Upload files** by clicking "Choose File" (or dragging files onto the input area) and pressing "Upload". Multiple files can be selected and uploaded in one go.
4. **Download files** by clicking the download button next to any listed file.
5. **Share with others** by letting them scan the same QR code or giving them the URL. They can upload and download files immediately -- no software installation required on their end.

---

## Configuration

While CLI flags cover most use cases, you can also edit the defaults directly in `share.py`:

```python
PORT = 6969                    # Default server port
BASE_DIR = os.getcwd()         # Default base directory
UPLOAD_DIR = os.path.join(...) # Upload storage location
```

---

## Project Structure

```
filesync/
  share.py              # Main server (HTTP handler, HTML/CSS/JS UI, CLI entry point)
  Setup.py              # Package configuration for pip installation
  README.md             # This file
  uploads/              # Shared files directory (auto-created at runtime)
```

---

## Use Cases

- **Team projects** -- Share build outputs, design files, and documents between team members without leaving the local network
- **Classrooms** -- Distribute assignments and collect submissions with zero student setup
- **Home network** -- Move files between a desktop, laptop, phone, and tablet effortlessly
- **Local events** -- Let attendees grab photos, schedules, or handouts from a single URL
- **Development** -- Serve test data, binaries, or logs to other machines during debugging

---

## Network Access

FileSync binds to `0.0.0.0`, making it reachable from any device on your local network:

- **Same WiFi** -- Works immediately
- **Ethernet connected** -- Works immediately
- **Internet** -- Not accessible from outside your network (this is secure by design)

---

## UI Highlights

The browser interface is a single-page application embedded directly in the server response -- no static files to manage:

- **Responsive layout** -- Adapts to desktop, tablet, and mobile screen sizes
- **Dark theme** -- A deep, high-contrast dark palette with neon accent colors
- **Glassmorphic panels** -- Modern blur and transparency effects using `backdrop-filter`
- **Smooth animations** -- Hover transitions on buttons and file download links
- **Real-time file list** -- Refreshes automatically after each upload

---

## Technical Details

- **Server** -- Python's built-in `HTTPServer` with a custom `BaseHTTPRequestHandler` subclass
- **Routing** -- GET `/` serves the UI, GET `/files` returns a JSON file list, GET `/download?file=` streams a file, POST `/` handles multipart uploads
- **IP detection** -- Uses a UDP socket trick to determine the machine's LAN address without external requests
- **MIME handling** -- Automatic content-type detection via `mimetypes` for correct file downloads
- **Architecture** -- The `main()` entry point parses arguments, builds the HTML template, and starts the server, making the module both runnable and importable

---

## Troubleshooting

### "Port already in use"

```bash
proshare --port 7777
```

Or stop whatever process is occupying the default port.

### "Cannot access from other devices"

- Verify all devices are on the same network
- Check that your firewall allows inbound connections to the chosen port
- Test locally first with `http://localhost:6969` to confirm the server is running

### "Files not uploading"

- Confirm the `uploads/` directory exists and is writable (it is created automatically, but permissions may vary)
- Check available disk space
- Look at the terminal for any Python error messages

---

## Security Notes

- This is a **local network only** tool -- it is not designed for public-facing deployment
- Files are stored in plain form with no encryption at rest
- There is no authentication or access control by default
- Use only on trusted networks
- Not recommended for sensitive or confidential data without additional security layers

---

## Tips

- Access from the same machine using `localhost:6969`
- Bookmark the URL for quick repeat access during a work session
- Assign a static IP to your host machine for a consistent address across reboots
- Mobile browsers work perfectly -- just scan the QR code printed in the terminal to connect instantly
- Install with `pip install .` once and forget about script paths entirely

---

## Support

Found a bug or have a feature request? Open an issue on the repository.

---

**Made with Python. Built for convenience.**
