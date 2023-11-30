import sys
import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QPixmap, QImage, QResizeEvent
from PySide6.QtCore import Qt, QTimer
from ui_mainwindow import Ui_MainWindow
from ultralytics import YOLO
import torch
model = YOLO('yolov8n.pt')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Video player variables
        self.video_capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.original_image = None  # Store the original image

        self.ui.button_file.clicked.connect(self.open_file)
        self.ui.button_local_camera.clicked.connect(self.open_camera)
        self.ui.button_network_camera.clicked.connect(self.open_camera)

    def open_file(self):
        """
        Open a file dialog to select a media file (image or video).
        If a video file is selected, play the video.
        If an image file is selected, display the image.
        """
        file_dialog = QFileDialog()
        name, _ = file_dialog.getOpenFileName(self, 'Open file', filter='Media files (*.png *.jpg *.bmp *.jpeg *.gif *.mp4 *.avi *.mkv)')
        if name:
            if self.is_video_file(name):
                self.play_video(name)
            else:
                self.show_image(name)

    def is_video_file(self, file_path):
        """
        Check if the given file path is a video file.

        Args:
            file_path (str): The path of the file to check.

        Returns:
            bool: True if the file is a video file, False otherwise.
        """
        video_extensions = ('.mp4', '.avi', '.mkv')
        return file_path.lower().endswith(video_extensions)

    def play_video(self, file_path):
        """
        Play a video file.

        Args:
            file_path (str): The path to the video file.

        Returns:
            None
        """
        self.stop_video()
        self.video_capture = cv2.VideoCapture(file_path)
        self.timer.start(30)

    def open_camera(self):
        self.stop_video()
        self.video_capture = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_video(self):
        """
        Stops the video capture and timer.

        Releases the video capture object and stops the timer.
        """
        if self.video_capture is not None:
            self.video_capture.release()
            self.timer.stop()

    def update_frame(self):
        """
        更新帧，从视频捕获设备中读取帧并显示在界面上的图像标签上。

        Args:
            self: 当前对象的引用。

        Returns:
            无返回值。
        """
        ret, frame = self.video_capture.read()
        if ret:
            self.display_image(frame, self.ui.label_image)
        else:
            self.stop_video()

    def display_image(self, image, label):
        """
        Display the given image on the specified label.

        Args:
            image (numpy.ndarray): The image to be displayed.
            label (QLabel): The label where the image will be displayed.
        """
        image = self.apply_yolo_model(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        image = QImage(image, width, height, width * channel, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        scale_ratio = min(label.width() / width, label.height() / height)
        new_width = int(width * scale_ratio)
        new_height = int(height * scale_ratio)
        pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)

    def apply_yolo_model(self, image):
        """
        Apply the YOLO model to the given image.

        Args:
            image (numpy.ndarray): The image to apply the YOLO model to.

        Returns:
            numpy.ndarray: The processed image.
        """
        conf = self.ui.horizontalSlider_conf.value() / 100
        iou = self.ui.horizontalSlider_iou.value() / 100
        if torch.backends.cudnn.is_available():
            device = 'cuda'
        else:
            device = 'cpu'
        result = model(image, device=device, verbose=False, conf = conf, iou = iou)[0]
        processed_image = result.plot()
        return processed_image

    def resizeEvent(self, event: QResizeEvent):
        """
        This method is called when the widget is resized.

        Args:
            event (QResizeEvent): The resize event object.

        Returns:
            None
        """
        if self.original_image is not None and (self.video_capture is None or not self.video_capture.isOpened()):
            self.display_image(self.original_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
