#!/usr/local/bin/python3
# brew install ufraw --with-exiv2
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import os
import sys

IMAGE_CONVERT_CMD = ["convert", "{input}", "-quality 85%", "-resize 80%", "{output}"]
VIDEO_CONVERT_CMD = ["ffmpeg", "-i", "{input}", "-quality 85%", "-resize 80%", "{output}"]

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Convert images")
        self.resize(1000, 800)
        layout = QVBoxLayout(self)
        
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Folder", "CR2", "MOV"])
        self.tree_widget.header().setStretchLastSection(False)
        self.tree_widget.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        self.add_btn = QPushButton("Add folder...")
        self.convert_btn = QPushButton("Convert")
        
        layout.addWidget(self.tree_widget)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.convert_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.add_btn.clicked.connect(self.add_clicked)
        self.convert_btn.clicked.connect(self.convert_clicked)
        
    def add_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, "Open directory")
        if dir:
            self.populate_tree(dir)
    
    def convert_clicked(self):
        self.visit_item(self.tree_widget.invisibleRootItem())
        
    def populate_tree(self, root_dir):
        self.add_folder(self.tree_widget.invisibleRootItem(), root_dir)
        
    def explore(self, dir):
        names = os.listdir(dir)
        cr2 = []
        mov = []
        dirs = []
        for n in names:
            p = os.path.join(dir, n)
            if os.path.isdir(p):
                dirs.append(p)
            elif p.lower().endswith('cr2'):
                cr2.append(p)
            elif p.lower().endswith('mov'):
                mov.append(p)
        return {"cr2": cr2, "mov": mov, "dirs":dirs}
        
    def add_folder(self, parent_item, path):
        files_dict = self.explore(path)
        contents = [os.path.basename(path),
                    str(len(files_dict['cr2'])),
                    str(len(files_dict['mov']))]
        item = QTreeWidgetItem(parent_item, contents)
        item.setExpanded(True)
        item.setData(0, QtCore.Qt.UserRole, path)
        print(*contents)
        for dir in files_dict['dirs']:
            self.add_folder(item, dir)
    
    def visit_item(self, item):
        user_data = item.data(0, QtCore.Qt.UserRole)
        print('ud', user_data)
        children = item.items()
        print (children)
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()