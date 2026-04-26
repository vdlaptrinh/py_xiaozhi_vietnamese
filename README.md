# Hướng Dẫn Triển Khai Xiaozhi Assistant Trên Raspberry Pi

## I. Yêu Cầu

- Raspberry Pi 4B hoặc 5B
- Thẻ nhớ tối thiểu 32GB
- Microphone USB
- Loa
- Màn hình HDMI (để chạy GUI)

## II. Cài Đặt Hệ Điều Hành

### 1. Tải Raspberry Pi Imager
https://www.raspberrypi.com/software/

### 2. Ghi Raspberry Pi OS (64-bit)
Chọn **Raspberry Pi OS (64-bit)** để có hiệu suất tốt nhất.

### 3. Cấu hình ban đầu
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

## III. Cài Đặt Thư Viện Hệ Thống

```bash
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-pyaudio \
    portaudio19-dev \
    ffmpeg \
    libopus0 \
    libopus-dev \
    build-essential \
    pulseaudio-utils \
    python3-pyqt5 \
    python3-pyqt5.qtquick \
    qml-module-qtquick2 \
    qml-module-qtquick-layouts \
    qml-module-qtquick-controls2 \
    qml-module-qtgraphicaleffects
```

## IV. Triển Khai Ứng Dụng

### 1. Tạo môi trường ảo
```bash
cd /home/pi
python3 -m venv py_xiaozhi_env
source py_xiaozhi_env/bin/activate
pip install --upgrade pip
```

### 2. Tải mã nguồn
```bash
git clone https://github.com/vdlaptrinh/py_xiaozhi_vietnamese.git
cd py_xiaozhi_vietnamese
```

### 3. Cài đặt thư viện Python

#### Thư viện không cần build (có sẵn wheel cho ARM64):
```bash
pip install \
    colorlog \
    pendulum \
    paho-mqtt \
    pynput \
    pyperclip \
    pypinyin \
    aiohttp \
    websockets \
    qasync \
    py-machineid \
    mutagen \
    beautifulsoup4 \
    brotli \
    python-dateutil \
    requests \
    openai \
    opuslib \
    soxr \
    psutil \
    pillow \
    webrtcvad-wheels \
    sherpa-onnx \
    numpy \
    pygame \
    sounddevice \
    opencv-python \
    lunar_python
```

#### Thư viện cần hệ thống (PyQt5):
PyQt5 từ pip không build được trên RPi. Giải pháp: dùng PyQt5 hệ thống qua file `.pth`:
```bash
echo '/usr/lib/python3/dist-packages' > /home/pi/py_xiaozhi_env/lib/python3.11/site-packages/system-packages.pth
```

### 4. Kiểm tra cài đặt
```bash
source py_xiaozhi_env/bin/activate
python3 -c "from PyQt5.QtQuickWidgets import QQuickWidget; print('PyQt5 OK')"
python3 -c "import sherpa_onnx; print('Sherpa OK')"
```

## V. Chạy Ứng Dụng

### Cách 1: Chạy thủ công
```bash
source py_xiaozhi_env/bin/activate
cd py_xiaozhi_vietnamese
python3 main.py
```

### Cách 2: Tạo script shortcut
```bash
cat > /home/pi/run.sh << 'EOF'
#!/bin/bash
source ~/py_xiaozhi_env/bin/activate
cd ~/py_xiaozhi_vietnamese
python3 main.py
EOF
chmod +x /home/pi/run.sh
```

Chạy:
```bash
./run.sh
```

### Cách 3: Tạo shortcut trên Desktop
```bash
cat > /home/pi/Desktop/xiaozhi.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Xiaozhi Assistant
Comment=AI Assistant
Exec=sh -c 'source /home/pi/py_xiaozhi_env/bin/activate && cd /home/pi/py_xiaozhi_vietnamese && python3 main.py'
Icon=/home/pi/py_xiaozhi_vietnamese/assets/icon.png
Terminal=false
Categories=Utility;
EOF
chmod +x /home/pi/Desktop/xiaozhi.desktop
```

## VI. Cấu Hình Tự Động Khởi Động

```bash
mkdir -p /home/pi/.config/autostart

cat > /home/pi/.config/autostart/xiaozhi.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Xiaozhi Assistant
Comment=AI Assistant - Auto start
Exec=sh -c 'sleep 30 && source /home/pi/py_xiaozhi_env/bin/activate && cd /home/pi/py_xiaozhi_vietnamese && python3 main.py'
Icon=/home/pi/py_xiaozhi_vietnamese/assets/icon.png
Terminal=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
EOF
```

## VII. Xử Lý Sự Cố

### Lỗi PyQt5.QtQuickWidgets not found
```bash
sudo apt-get install -y python3-pyqt5.qtquick
```

### Lỗi openGL
Cần chạy trên màn hình thực (không hỗ trợ headless). Kết nối màn hình HDMI hoặc dùng VNC.

### Lỗi PortAudio
```bash
sudo apt-get install -y portaudio19-dev libportaudio2
pip install --force-reinstall sounddevice
```

### Lỗi microphone không nhận
```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

### Cập nhật ứng dụng
```bash
source py_xiaozhi_env/bin/activate
cd py_xiaozhi_vietnamese
git pull
```

## VIII. Thông Tin

- **Mã nguồn:** https://github.com/vdlaptrinh/py_xiaozhi_vietnamese
- **Yêu cầu tối thiểu:** Raspberry Pi 4B (4GB RAM)
- **Hệ điều hành:** Raspberry Pi OS 64-bit (Debian Bookworm)

---

Chúc bạn triển khai thành công!