from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
from PySide6.QtGui import QPixmap, QImage, QResizeEvent
from PySide6.QtCore import Qt, QTimer

import numpy as np
import cv2
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Player")
        self.resize(800, 600)
        self.setMinimumSize(500, 400)

        self.setup_ui()

        # Video player variables
        self.video_capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.original_image = None  # Store the original image

    def setup_ui(self):
        main_layout = QHBoxLayout(self)

        # left and right container
        left_container = self.setup_left_container()
        right_container = self.setup_right_container()

        main_layout.addWidget(left_container)
        main_layout.addWidget(right_container)

        self.setLayout(main_layout)

    def setup_left_container(self):
        left_container = QWidget(self)
        left_container.setFixedWidth(200)

        input_label = QLabel("输入:", left_container)

        open_file_button = QPushButton("文件", left_container)
        open_file_button.clicked.connect(self.open_file)

        camera_button = QPushButton("摄像头", left_container)
        camera_button.clicked.connect(self.open_camera)

        network_camera_button = QPushButton("网络摄像头", left_container)
        network_camera_button.clicked.connect(self.open_camera)

        source_layout = QHBoxLayout()
        source_layout.addWidget(input_label)
        source_layout.addWidget(open_file_button)
        source_layout.addWidget(camera_button)
        source_layout.addWidget(network_camera_button)

        left_layout = QVBoxLayout(left_container)
        left_layout.addLayout(source_layout)
        left_layout.addStretch()

        left_container.setLayout(left_layout)

        return left_container

    def setup_right_container(self):
        right_container = QWidget(self)
        right_container_layout = QVBoxLayout(right_container)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        right_container_layout.addWidget(self.label)
        right_container.setLayout(right_container_layout)

        return right_container

    def open_file(self):
        file_dialog = QFileDialog()
        name, _ = file_dialog.getOpenFileName(self, 'Open file', filter='Media files (*.png *.jpg *.bmp *.jpeg *.gif *.mp4 *.avi *.mkv)')
        if name:
            if self.is_video_file(name):
                self.play_video(name)
            else:
                self.show_image(name)

    def is_video_file(self, file_path):
        video_extensions = ('.mp4', '.avi', '.mkv')
        return file_path.lower().endswith(video_extensions)

    def show_image(self, file_path):
        image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        if image is not None:
            self.original_image = image.copy()  # Store the original image
            self.display_image(self.original_image)
            self.stop_video()
        else:
            print("Error loading image.")

    def display_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        image = QImage(image, width, height, width * channel, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        scale_ratio = min(self.label.width() / width, self.label.height() / height)
        new_width = int(width * scale_ratio)
        new_height = int(height * scale_ratio)
        pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def play_video(self, file_path):
        self.stop_video()
        self.video_capture = cv2.VideoCapture(file_path)
        self.timer.start(30)

    def stop_video(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.timer.stop()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.display_image(frame)
        else:
            self.stop_video()

    def open_camera(self):
        self.stop_video()
        self.video_capture = cv2.VideoCapture(0)
        self.timer.start(30)

    def resizeEvent(self, event: QResizeEvent):
        if self.original_image is not None and (self.video_capture is None or not self.video_capture.isOpened()):
            self.display_image(self.original_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
