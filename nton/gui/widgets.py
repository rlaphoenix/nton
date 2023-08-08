from PySide6.QtCore import Signal
from PySide6.QtGui import QDragEnterEvent, QDragLeaveEvent
from PySide6.QtWidgets import QStackedWidget, QLabel


class FileDropWidget(QStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
            self.window().openLabel.setStyleSheet(
                "border: 3px solid #0868c0;\n"
                "border-style: dashed;\n"
                "border-radius: 8px;"
            )
        else:
            super().dragEnterEvent(event)

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        event.accept()
        self.window().openLabel.setStyleSheet(
            "border: 3px solid #dcdcdc;\n"
            "border-style: dashed;\n"
            "border-radius: 8px;"
        )


class ClickableLabel(QLabel):
    clicked = Signal()  # This signal will be emitted when the label is clicked

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit the signal when the label is clicked
