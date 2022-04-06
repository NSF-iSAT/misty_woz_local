# WINDOWS INSTUCTIONS
# 1. Install Docker
# 2. Install Windows X server https://sourceforge.net/projects/vcxsrv/
# 3. Run Windows X server and mash Next until you get to Extra Settings
# 4. Check off all Extra Settings (especially Disable Access Control)
# 5. Get your local IP address using ipconfig
# 6. Run docker run using option `-e DISPLAY=[your_ip]:0.0`
# 7. Pray

FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt update
RUN apt install ffmpeg libsm6 libxext6  -y
RUN apt install -y python-tk
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "misty_ui.py"]