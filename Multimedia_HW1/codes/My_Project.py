import sys
import cv2
import socket
import pickle
import struct
import pyaudio
import wave
import wave
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

################# strings for styles ############################
str1 = 'background-color:green'
str2 = 'background-color:red'
str3 = 'background-color:yellow'
str4 = 'background-color:blue'
################# Initializing Webcam ############################
class WebcamThread(QThread):
    frame_ready = pyqtSignal(object)

    def __init__(self, parent=None):
        super(WebcamThread, self).__init__(parent)
        self.webcam = cv2.VideoCapture(0)

    def run(self):
        while True:
            ret, frame = self.webcam.read()
            if ret:
                frame_resized = cv2.resize(frame, (200, 200))  # Resize the frame
                self.frame_ready.emit(frame_resized)
################# Initializing Record ############################
class AudioRecorder(QThread):
    def __init__(self, parent=None):
        super(AudioRecorder, self).__init__(parent)
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 30  # Adjust the recording duration as needed
        self.frames = []

    def run(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

        print("Recording...")
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            self.frames.append(data)

        print("Finished recording")

        stream.stop_stream()
        stream.close()
        audio.terminate()


    def get_audio_data(self):
        return b''.join(self.frames)
################# Creating buttons and labels and layouts ############################
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.webcam_thread = WebcamThread()
        self.webcam_thread.frame_ready.connect(self.update_webcam_frame)
        self.webcam_thread.start()

        self.webcam_label = QLabel()
        self.webcam_label.setFixedSize(640, 360)

        self.capture_button = QPushButton("Capture")
        self.capture_button.setFont(QFont("Times New Roman",20))
        self.capture_button.setStyleSheet(str1)
        self.capture_button.clicked.connect(self.capture_photo)

        self.show_button = QPushButton("Show")
        self.show_button.setFont(QFont("Times New Roman",20))
        self.show_button.setStyleSheet(str2)
        self.show_button.clicked.connect(self.show_photo)


        self.record_button = QPushButton("Record")
        self.record_button.setFont(QFont("Times New Roman",20))
        self.record_button.setStyleSheet(str3)
        self.record_button.clicked.connect(self.record_audio)

        self.play_button = QPushButton("Play")
        self.play_button.setFont(QFont("Times New Roman",20))
        self.play_button.setStyleSheet(str4)
        self.play_button.clicked.connect(self.play_audio)

        layout = QVBoxLayout()
        layout.addWidget(self.webcam_label)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.show_button)
        layout.addWidget(self.record_button)
        layout.addWidget(self.play_button)

        self.setLayout(layout)

        self.captured_photo = None  # Variable to store the captured photo
        self.audio_recorder = AudioRecorder()
################# functions to take action ############################
    def update_webcam_frame(self, frame):
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qimg = QImage(rgb_frame.data, w, h, QImage.Format.Format_RGB888)
        qimg_scaled = qimg.scaled(self.webcam_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.webcam_label.setPixmap(QPixmap.fromImage(qimg_scaled))

    def capture_photo(self):
        self.captured_photo = self.webcam_thread.webcam.read()[1]  # Capture photo from webcam
    def show_photo(self):
        if self.captured_photo is not None:
            # Display the captured photo in a separate window
            cv2.imshow("Captured Photo", self.captured_photo)
            cv2.imwrite("image.png", self.captured_photo)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            QMessageBox.warning(self, "Warning", "No photo captured yet.")
    def record_audio(self):
        self.audio_recorder.start()
        audio_data = self.audio_recorder.get_audio_data()
        if audio_data:
            print("saving...")
            with wave.open('voice.wav', 'wb') as f:
                f.setnchannels(1)  
                f.setsampwidth(2)  
                f.setframerate(44100) 
                f.writeframes(audio_data)

    def play_audio(self):
        audio_data = self.audio_recorder.get_audio_data()
        if audio_data:  
            print("saving...")
            with wave.open('voice.wav', 'wb') as f:
                f.setnchannels(1)  
                f.setsampwidth(2)  
                f.setframerate(44100) 
                f.writeframes(audio_data)
            audio = pyaudio.PyAudio()
            stream = audio.open(format=audio.get_format_from_width(2),
                                channels=1,
                                rate=44100,
                                output=True)
            stream.write(audio_data)
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
        else:
            print("No audio data recorded yet")
    # Function to send data over a network connection


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
