# from migration.package.migrate.delete_table import delete_table
from package.migrate import *
from package.convert import *
import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QDesktopWidget, QLineEdit, QTextEdit, QWidget, QLabel, QPushButton
import os
import time


cur_dir = os.path.dirname(__file__)


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
        self.create_btn = QPushButton('CREATE', self)
        self.create_btn.clicked.connect(self.doCreate)
        self.export_btn = QPushButton('EXPORT', self)
        self.export_btn.clicked.connect(self.doExport)
        self.import_btn = QPushButton('IMPORT', self)
        self.import_btn.clicked.connect(self.doImport)
        self.convert_btn = QPushButton('CONVERT', self)
        self.convert_btn.clicked.connect(self.doConvert)
        self.delete_btn = QPushButton('delete', self)
        self.delete_btn.clicked.connect(self.doDelete)
        self.lb_log = QTextEdit("LOG ...", self)
        # self.pbar = QProgressBar(self)

        grid.addWidget(self.lb_tablename, 0, 0)
        grid.addWidget(self.input_tablename, 0, 2)
        grid.addWidget(self.lb_filename, 1, 0)
        grid.addWidget(self.input_filename, 1, 2)
        grid.addWidget(self.create_btn, 2, 0, 2, 4)
        grid.addWidget(self.export_btn, 3, 0)
        grid.addWidget(self.import_btn, 3, 1)
        grid.addWidget(self.convert_btn, 3, 2)
        grid.addWidget(self.delete_btn, 3, 3)

        grid.addWidget(self.lb_log, 4, 0, 4, 4)
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
        if result == "done":
            self.lb_log.append(
                f"DONE >>> \nEXPORT TIME >>> {time.time() - start}")
        else:
            self.lb_log.append(str(result))

    def doImport(self):
        table_name = self.input_tablename.text()
        file_name = self.input_filename.text()
        self.lb_log.append(
            f"import data from file {file_name}.json to DB {table_name}")
        file_path = os.path.join(cur_dir, f"json_data/{file_name}.json")
        start = time.time()
        result = import_data.import_data(table_name, file_path)
        if result == "done":
            self.lb_log.append(
                f"DONE >>> \nIMPORT TIME >>> {time.time() - start}")
        else:
            self.lb_log.append(str(result))

    def doConvert(self):
        file_name = self.input_filename.text()
        file_path = os.path.join(cur_dir, f"json_data/{file_name}.json")
        start = time.time()

        # LOGIC SELECT
        # result = logic.add(file_path)
        # result = logic.delete(file_path)
        result = logic.update(file_path)

        if result == "done":
            self.lb_log.append(
                f"DONE >>> \nCONVERT TIME >>> {time.time() - start}")
        else:
            self.lb_log.append(str(result))

    def doCreate(self):
        table_name = self.input_tablename.text()
        result = create_table.create_table(table_name)
        start = time.time()
        if result == "done":
            self.lb_log.append(
                f"DONE >>> \nCREATE TIME >>> {time.time() - start}")
        else:
            self.lb_log.append(str(result))

    def doDelete(self):
        table_name = self.input_tablename.text()
        result = delete_table.delete_table(table_name)
        if result == "done":
            self.lb_log.append(f"DONE >>>")
        else:
            self.lb_log.append(str(result))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
