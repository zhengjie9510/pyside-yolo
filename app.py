import sys
import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QTimer
from ui_mainwindow import Ui_MainWindow
from ultralytics import YOLO
from PySide6.QtCore import QEvent
import torch
import supervision as sv
from time import time


class ModelWrapper:
    def __init__(self):
        self.my_device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = None
        self.byte_tracker = sv.ByteTrack()
        self.box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

    def change_model(self, model_path: str = None):
        """
        Changes the model used for object detection.

        Args:
            model_path (str, optional): The path to the new model. Defaults to None.

        Returns:
            bool: True if the model is successfully changed, False otherwise.
        """
        try:
            self.model = YOLO(model_path) if model_path else None
        except:
            self.model = None
        return self.model is not None

    def reset_tracker(self):
        """
        Resets the byte tracker.
        """
        self.byte_tracker = sv.ByteTrack()

    def predict(self, frame, **kwargs):
        """
        Perform object detection on a given frame.

        Args:
            frame: The input frame to perform object detection on.
            **kwargs: Additional keyword arguments to be passed to the model's predict method.

        Returns:
            annotated_frame: The frame with annotated bounding boxes and labels.
            verbose_results: The verbose results from the model's predict method.
        """
        results = self.model.predict(frame, verbose=False, device=self.my_device, **kwargs)[0]
        detections = sv.Detections.from_ultralytics(results)
        labels = [results.names[class_id] for class_id in detections.class_id]
        annotated_frame = self.box_annotator.annotate(frame, detections=detections)
        annotated_frame = self.label_annotator.annotate(
            annotated_frame, detections=detections, labels=labels)
        return annotated_frame, results.verbose()

    def track(self, frame, **kwargs):
        """
        Track objects in a frame using the model.

        Args:
            frame: The input frame to track objects in.
            **kwargs: Additional keyword arguments to pass to the model's predict method.

        Returns:
            annotated_frame: The frame with annotated bounding boxes and labels.
            verbose_results: The verbose results from the model's predict method.
        """
        results = self.model.predict(frame, verbose=False, device=self.my_device, **kwargs)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = self.byte_tracker.update_with_detections(detections)
        labels = [f"#{tracker_id} {results.names[class_id]}" for class_id, tracker_id in
                  zip(detections.class_id, detections.tracker_id)]
        annotated_frame = self.box_annotator.annotate(frame, detections=detections)
        annotated_frame = self.label_annotator.annotate(
            annotated_frame, detections=detections, labels=labels)
        return annotated_frame, results.verbose()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.task = 'detect' if self.ui.radioButton_detect.isChecked() else 'track'
        self.model_wrapper = ModelWrapper()

        self.original_image = None  # Store the original image
        self.video_capture = None  # Store the video capture object

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.ui.button_model.clicked.connect(self.open_file_model)
        self.ui.lineEdit_model.textChanged.connect(self.change_model)

        self.ui.button_file.clicked.connect(self.open_file)
        self.ui.button_local_camera.clicked.connect(self.open_local_camera)
        self.ui.button_network_camera.clicked.connect(self.open_network_camera_dialog)

        self.ui.radioButton_detect.clicked.connect(self.change_task)
        self.ui.radioButton_track.clicked.connect(self.change_task)

        self.ui.horizontalSlider_size.valueChanged.connect(
            lambda value: self.ui.horizontalSlider_size.setValue((value // 32) * 32))

        self.installEventFilter(self)

    def open_network_camera_dialog(self):
        url, ok_pressed = QInputDialog.getText(self, "Input URL", "Enter URL:")
        if ok_pressed:
            self.open_network_camera(url)

    def eventFilter(self, obj, event):
        """
        Filters events for the specified object.

        Args:
            obj: The object to filter events for.
            event: The event to be filtered.

        Returns:
            bool: True if the event was filtered, False otherwise.
        """
        if obj == self and event.type() == QEvent.MouseButtonPress:
            if not self.ui.lineEdit_model.geometry().contains(event.globalPosition().toPoint()):
                self.ui.lineEdit_model.clearFocus()
        return super().eventFilter(obj, event)

    def change_model(self):
        """
        Change the model used by the application.

        Retrieves the model path from the line edit widget and calls the `change_model` method of the `model_wrapper` object.
        If the model is successfully changed, a success message is displayed in the status bar for 5 seconds.
        Otherwise, a failure message is displayed.

        Returns:
            None
        """
        model_path = self.ui.lineEdit_model.text()
        state = self.model_wrapper.change_model(model_path)
        if state:
            self.ui.statusbar.showMessage('Model loaded', 5000)
        else:
            self.ui.statusbar.showMessage('Model load failed', 5000)

    def change_task(self):
        """
        Change the task to either detection or tracking.
        """
        if self.ui.radioButton_detect.isChecked():
            self.model_wrapper.reset_tracker()
            self.task = 'detect'
            self.ui.statusbar.showMessage('Detection mode', 5000)
        elif self.ui.radioButton_track.isChecked():
            self.model_wrapper.reset_tracker()
            self.task = 'track'
            self.ui.statusbar.showMessage('Tracking mode', 5000)

    def open_file_model(self):
        """
        Open a file dialog to select a model file.
        """
        file_dialog = QFileDialog()
        name, _ = file_dialog.getOpenFileName(self, 'Open file',
                                              filter='Model files (*.pt)')
        self.ui.lineEdit_model.setText(name) if name else None

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
        if image is not None:
            self.original_image = image
            self.display_image(self.original_image.copy(), self.ui.label_image)
            self.timer.start(100)
        else:
            self.ui.statusbar.showMessage(f"Failed: {file_path}")

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
        if self.video_capture.isOpened():
            self.ui.statusbar.showMessage(f"Local Video: {file_path}")
            self.timer.start()
        else:
            self.ui.statusbar.showMessage(f"Failed: {file_path}")

    def open_local_camera(self):
        """
        打开摄像头并开始视频捕获。

        参数：
        - camera_index：摄像头索引，默认为0

        返回值：无
        """
        self.stop_update()
        self.video_capture = cv2.VideoCapture(0)
        if self.video_capture.isOpened():
            self.ui.statusbar.showMessage("Local Camera")
            self.timer.start()
        else:
            self.ui.statusbar.showMessage(f"Failed: Local Camera")

    def open_network_camera(self, url):
        """
        Open a network camera and start video capture.

        Args:
            url (str): The URL of the network camera.

        Returns:
            None
        """
        self.stop_update()
        self.video_capture = cv2.VideoCapture(url)
        if self.video_capture.isOpened():
            self.ui.statusbar.showMessage(f"Network Camera: {url}")
            self.timer.start()
        else:
            self.ui.statusbar.showMessage(f"Failed: {url}")

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
            start_time = time()
            ret, frame = self.video_capture.read()
            if ret:
                image, log = self.apply_yolo_model(frame)
                self.display_image(image, self.ui.label_image)
                self.ui.textBrowser.setText(log)
                end_time = time()
                fps = int(1 / (end_time - start_time))
                self.ui.statusbar.showMessage(f'FPS: {fps}', 1000)
            else:
                self.stop_update()
        else:
            image, log = self.apply_yolo_model(self.original_image.copy())
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
        self.change_model() if self.model_wrapper.model is None else None
        if self.model_wrapper.model is None:
            return image, 'No model loaded'
        conf = self.ui.horizontalSlider_conf.value() / 100
        iou = self.ui.horizontalSlider_iou.value() / 100
        imgsz = self.ui.horizontalSlider_size.value()
        if self.task == 'detect':
            result, log = self.model_wrapper.predict(image, conf=conf, iou=iou, imgsz=imgsz)
        elif self.task == 'track':
            result, log = self.model_wrapper.track(image, conf=conf, iou=iou, imgsz=imgsz)
        return result, log


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
