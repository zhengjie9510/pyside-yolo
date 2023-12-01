import sys
import cv2
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QPixmap, QImage, QResizeEvent
from PySide6.QtCore import Qt, QTimer
from ui_mainwindow import Ui_MainWindow
from ultralytics import YOLO
import torch
import supervision as sv


class Model(YOLO):
    """
    A class representing a YOLO model.

    Attributes:
        device (str): The device to use for inference ('cuda' or 'cpu').
        byte_tracker: The byte tracker object.
        box_annotator: The bounding box annotator object.
        label_annotator: The label annotator object.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_device = 'cuda' if torch.backends.cudnn.is_available() else 'cpu'
        self.byte_tracker = None
        self.box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

    def predict(self, frame, **kwargs):
        """
        Perform object detection on a single frame.

        Args:
            frame: The input frame.
            **kwargs: Additional keyword arguments for prediction.

        Returns:
            annotated_frame: The annotated frame with bounding boxes and labels.
        """
        results = super().predict(frame, verbose=False, device=self.my_device, **kwargs)[0]
        detections = sv.Detections.from_ultralytics(results)
        labels = [results.names[class_id] for class_id in detections.class_id]
        annotated_frame = self.box_annotator.annotate(frame, detections=detections)
        annotated_frame = self.label_annotator.annotate(annotated_frame, detections=detections, labels=labels)
        return annotated_frame,results.verbose()

    def track(self, frame, **kwargs):
        """
        Perform object tracking on a single frame.

        Args:
            frame: The input frame.
            **kwargs: Additional keyword arguments for prediction.

        Returns:
            annotated_frame: The annotated frame with bounding boxes and labels.
        """
        results = super().predict(frame, verbose=False, device=self.my_device, **kwargs)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = self.byte_tracker.update_with_detections(detections)
        labels = [f"#{tracker_id} {results.names[class_id]}" for class_id, tracker_id in zip(detections.class_id, detections.tracker_id)]
        annotated_frame = self.box_annotator.annotate(frame, detections=detections)
        annotated_frame = self.label_annotator.annotate(annotated_frame, detections=detections, labels=labels)
        return annotated_frame,results.verbose()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('PySide6-YOLO')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.original_image = None  # Store the original image
        self.video_capture = None  # Store the video capture object

        self.ui.button_file.clicked.connect(self.open_file)
        self.ui.button_local_camera.clicked.connect(self.open_camera)
        self.ui.button_network_camera.deleteLater()

        self.ui.radioButton_detect.clicked.connect(self.change_task)
        self.ui.radioButton_track.clicked.connect(self.change_task)
        self.ui.comboBox_model.currentIndexChanged.connect(self.change_model)

        self.add_model_list()
        self.change_model()
        self.change_task()
        

    def add_model_list(self):
        model_list = [model.name for model in Path('.').glob('*.pt')]
        self.ui.comboBox_model.addItems(model_list)
    
    def change_model(self):
        model_path = self.ui.comboBox_model.currentText()
        try:
            self.model = Model(model_path) if model_path else None
        except:
            self.model = None

    def change_task(self):
        """
        Change the task to either detection or tracking.
        """
        if self.ui.radioButton_detect.isChecked():
            self.model.byte_tracker = None
            self.task = 'detect'
        elif self.ui.radioButton_track.isChecked():
            self.model.byte_tracker = sv.ByteTrack()
            self.task = 'track'

    def open_file(self):
        """
        Open a file dialog to select a media file (image or video).
        If a video file is selected, play the video.
        If an image file is selected, display the image.
        """
        file_dialog = QFileDialog()
        name, _ = file_dialog.getOpenFileName(self, 'Open file',
                                              filter='Media files (*.png *.jpg *.bmp *.jpeg *.gif *.mp4 *.avi *.mkv)')
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

    def show_image(self, file_path):
        """
        Display an image file.

        Args:
            file_path (str): The path to the image file.

        Returns:
            None
        """
        self.stop_update()
        image = cv2.imread(file_path)
        self.original_image = image
        self.display_image(self.original_image.copy(), self.ui.label_image)
        self.timer.start(500)

    def play_video(self, file_path):
        """
        Play a video file.

        Args:
            file_path (str): The path to the video file.

        Returns:
            None
        """
        self.stop_update()
        self.video_capture = cv2.VideoCapture(file_path)
        self.timer.start()

    def open_camera(self):
        """
        打开摄像头并开始视频捕获。

        参数：
        - camera_index：摄像头索引，默认为0

        返回值：无
        """
        self.stop_update()
        self.video_capture = cv2.VideoCapture(0)
        self.timer.start()

    def stop_update(self):
        """
        Stops the video capture and timer.

        Releases the video capture object and stops the timer.
        """
        if self.video_capture is not None:
            self.original_image = None
            self.video_capture.release()
            self.timer.stop()

    def update_frame(self):
        """
        Updates the frame displayed in the UI.

        If the video capture is opened, it reads a frame from the capture and displays it in the UI.
        If the frame is successfully read, it calls the display_image method to display the frame.
        If the frame cannot be read, it stops updating the frame.
        If the video capture is not opened, it displays the original image in the UI.
        """
        if self.video_capture and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                image,log = self.apply_yolo_model(frame)
                self.display_image(image, self.ui.label_image)
                self.ui.textBrowser.setText(log)
            else:
                self.stop_update()
        else:
            image,log = self.apply_yolo_model(self.original_image.copy())
            self.display_image(image, self.ui.label_image)
            self.ui.textBrowser.setText(log)

    def display_image(self, image, label):
        """
        Display the given image on the specified label.

        Args:
            image (numpy.ndarray): The image to be displayed.
            label (QLabel): The label where the image will be displayed.
        """
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
        if self.model is None:
            return image
        conf = self.ui.horizontalSlider_conf.value() / 100
        iou = self.ui.horizontalSlider_iou.value() / 100
        if self.task == 'detect':
            result,log = self.model.predict(image, conf=conf, iou=iou)
        elif self.task == 'track':
            result,log = self.model.track(image, conf=conf, iou=iou)
        return result,log


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
