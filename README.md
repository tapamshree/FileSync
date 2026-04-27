# 🌐 FileSync

**A sleek, cyberpunk-styled local file sharing server with zero configuration.**

Share files instantly across your local network with a stunning glassmorphic UI and automatic network detection.

---

##  Features

-  **Zero Config** - Just run and share
-  **Auto IP Detection** - Automatically finds your local IP address
-  **File Upload/Download** - Drag-and-drop file sharing
-  **Local Network Friendly** - Perfect for teams, classrooms, and quick transfers
-  **Lightweight** - Built with Python's standard library
-  **Organized Storage** - Auto-creates upload directory

---

##  Quick Start

### Prerequisites
- Python 3.6+
- No additional dependencies (uses Python standard library!)

### Installation & Usage

1. **Clone or download this project**

2. **Run the server:**
```bash
python share.py
```

3. **Access in your browser:**
   - The script will output your local IP address
   - Open that link in any browser on your network by clicking on it or copy pasting. eg - `http://<your-local-ip>:6969`
   - Start uploading and sharing files!

### Example Output
```
FileSync running on http://192.168.1.100:6969
Listening on port 6969...
```

---

##  How to Use

1. **Upload Files**
   - Click "Choose File" or drag files onto the upload area
   - Click "Upload" button
   - File is instantly available for download

2. **Download Files**
   - Browse the files list
   - Click on any file to download it

3. **Share with Others**
   - Give them the URL (e.g., `http://192.168.1.100:6969`)
   - They can upload and download files immediately

---

## Configuration

Edit `share.py` to customize:

```python
PORT = 6969                    # Change server port
BASE_DIR = os.getcwd()         # Change base directory
UPLOAD_DIR = os.path.join(...) # Change upload location
```

---

## Project Structure

```
testfolder/
├── share.py              # Main server
├── README.md             # This file
├── uploads/              # Shared files directory (auto-created)
└── message-history.json  # (if applicable)
```

---

## Use Cases

- **Team Projects** - Quickly share files between team members
- **Classroom** - Distribute assignments and collect submissions
- **Home Network** - Easy file transfers between devices
- **Local Events** - Share photos and documents with attendees
- **Development** - Share build artifacts and test data

---

##  Network Access

The server is accessible to any device on your local network:
- **Same WiFi** ✅ Works great
- **Ethernet connected** ✅ Works great
- **Internet** ❌ Not accessible from outside your network (secure by design)

---

##  UI Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Theme** - Easy on the eyes with neon accents
- **Glassmorphic Effects** - Modern blur and transparency effects
- **Smooth Animations** - Hover effects and transitions
- **Real-time File List** - Updates instantly after upload

---

##  Technical Details

- **HTTP Server** - Uses Python's built-in `HTTPServer`
- **Request Handler** - Custom `BaseHTTPRequestHandler` implementation
- **File Operations** - Safe file handling with MIME type detection
- **IP Detection** - Smart socket-based local IP detection
- **Responsive Frontend** - HTML/CSS/JavaScript single-page interface

---

##  Troubleshooting

### "Port already in use"
```bash
# Change PORT in share.py or use:
python share.py --port 7777
```

### "Can't access from other devices"
- Ensure devices are on the same network
- Check Windows Firewall allows Python
- Try accessing `http://localhost:6969` first to test

### "Files not uploading"
- Check `uploads/` directory exists and is writable
- Ensure disk has free space
- Check file size limits

---

##  Security Notes

- This is a **local network only** tool
- Files are stored in plain text
- No authentication by default
- Best used on trusted networks
- Not recommended for sensitive data without additional security

---

##  Pro Tips

- Use `localhost:6969` for accessing from the same machine
- Pin the URL to your browser bookmarks for quick access
- Set up a static IP for your device for consistent access
- Works great on mobile browsers too!

---

##  Support

Found a bug? Have a feature request? Feel free to open an issue!

---

**Made with ❤️ using Python**

Happy sharing! 
