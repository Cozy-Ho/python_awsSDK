from package.migrate import *
from package.convert import logic
import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QProgressBar, QDesktopWidget, QLineEdit, QInputDialog, QTextEdit, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QBasicTimer
import os
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)


cur_dir = os.path.dirname(__file__)


class LogHandler(logging.Handler):
    def __init__(self, target_widget):
        super(LogHandler, self).__init__()
        self.target_widget = target_widget

    def emit(self, record):
        self.target_widget.append(record.asctime + '---' + record.getMessage())


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Migration")
        self.resize(400, 500)
        self.draw_layout()
        self.center()
        self.show()

    def draw_layout(self):

        grid = QGridLayout()
        self.setLayout(grid)

        self.lb_tablename = QLabel("table_name : ", self)
        self.input_tablename = QLineEdit(self)
        self.lb_filename = QLabel("file_name : ", self)
        self.input_filename = QLineEdit(self)
        self.export_btn = QPushButton('EXPORT', self)
        self.export_btn.clicked.connect(self.doExport)
        self.import_btn = QPushButton('IMPORT', self)
        self.import_btn.clicked.connect(self.doImport)
        self.convert_btn = QPushButton('CONVERT', self)
        self.convert_btn.clicked.connect(self.doConvert)
        self.lb_log = QTextEdit("LOG ...", self)
        self.pbar = QProgressBar(self)

        grid.addWidget(self.lb_tablename, 0, 0)
        grid.addWidget(self.input_tablename, 0, 2)
        grid.addWidget(self.lb_filename, 1, 0)
        grid.addWidget(self.input_filename, 1, 2)
        grid.addWidget(self.export_btn, 2, 0)
        grid.addWidget(self.import_btn, 2, 1)
        grid.addWidget(self.convert_btn, 2, 2)
        grid.addWidget(self.lb_log, 3, 0, 3, 3)
        # grid.setRowStretch(3, 4)
        # grid.addWidget(self.pbar, 4, 0)

        # self.timer = QBasicTimer()
        # self.step = 0

    def doExport(self):
        table_name = self.input_tablename.text()
        file_name = self.input_filename.text()
        self.lb_log.append(
            f"export data from DB {table_name} to file {file_name}.json")
        file_path = os.path.join(cur_dir, f"json_data/{file_name}.json")
        start = time.time()
        result = export_data.export_data(table_name, file_path)
        if(result):
            self.lb_log.append(
                f"DONE >>> \nEXPORT TIME >>> {time.time() - start}")
        else:
            self.lb_log.append(f"ERROR >>> somethings wrong...")

    def doImport(self):
        table_name = self.input_tablename.text()
        file_name = self.input_filename.text()
        self.lb_log.append(
            f"export data from DB {table_name} to file {file_name}.json")
        file_path = os.path.join(cur_dir, f"json_data/{file_name}.json")
        start = time.time()
        result = import_data.import_data(table_name, file_path)
        if(result):
            self.lb_log.append(
                f"DONE >>> \nIMPORT TIME >>> {time.time() - start}")
        else:
            self.lb_log.append(f"ERROR >>> somethings wrong...")

    def doConvert(self):
        file_name = self.input_filename.text()
        file_path = os.path.join(cur_dir, f"json_data/{file_name}.json")
        logic.add(file_path)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.import_btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.import_btn.setText('Stop')

    def timerEvent(self, e):
        if self.step >= 100:

            self.timer.stop()
            self.export_btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
