from pathlib import Path
from typing import Any, cast

from PySide6.QtCore import QEvent, QObject, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent


class FileDropper(QObject):
    dropped = Signal(Path)  # has file dropped
    onHover = Signal()  # is hovered
    onLeave = Signal()  # is no longer hovered
    clicked = Signal()  # is clicked

    def eventFilter(self, obj: Any, event: QEvent) -> bool:
        if event.type() == QEvent.Type.DragEnter:
            dragEvent: QDragEnterEvent = cast(QDragEnterEvent, event)
            if dragEvent.mimeData().hasUrls():
                dragEvent.accept()
                self.onHover.emit()
                return True

        elif event.type() == QEvent.Type.DragLeave:
            self.onLeave.emit()
            return True

        elif event.type() == QEvent.Type.Drop:
            dropEvent: QDropEvent = cast(QDropEvent, event)
            for url in dropEvent.mimeData().urls():
                path = url.toLocalFile()
                if path:
                    self.dropped.emit(Path(path))
            return True

        elif event.type() == QEvent.Type.MouseButtonPress:
            self.clicked.emit()
            return True

        return False
