#!/usr/local/bin/python3
# Read raw (cr2) files with imagemagick/convert:
# brew install ufraw --with-exiv2
# Videos:
# brew install ffmpeg 
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import os
import sys
import subprocess

IMAGE_CONVERT_CMD = ["convert", "{input}", "-quality", "85%", "-resize", "80%", "{output}"]
VIDEO_CONVERT_CMD = ["ffmpeg", "-i", "{input}", "{output}"]

def filesize_mb_fmt(path):
    bytes = os.stat(path).st_size
    mb = float(bytes) / 1024.0 / 1024.0
    return "%.1fMB" % mb 

def replace(template, input, output):
    l = []
    for item in template:
        if item == "{input}":
            l.append(input)
        elif item == "{output}":
            l.append(output)
        else:
            l.append(item)
    return l
    
def convert_mov(input_path):
    stem, _ = os.path.splitext(input_path)
    output_path = stem + ".mp4"
    cmd = replace(VIDEO_CONVERT_CMD, input_path, output_path)
    print(subprocess.list2cmdline(cmd))
    if subprocess.call(cmd) != 0:
        print('ERROR converting', input_path)
    else:
        size_before = filesize_mb_fmt(input_path)
        size_after = filesize_mb_fmt(output_path)
        print ('remove', input_path, 'size before', size_before,
               'size after', size_after)
        os.remove(input_path)

def convert_cr2(input_path):
    stem, _ = os.path.splitext(input_path)
    output_path = stem + ".jpg"
    cmd = replace(IMAGE_CONVERT_CMD, input_path, output_path)
    print(subprocess.list2cmdline(cmd))
    if subprocess.call(cmd) != 0:
        print('ERROR converting', input_path)
    else:
        size_before = filesize_mb_fmt(input_path)
        size_after = filesize_mb_fmt(output_path)
        print ('remove', input_path, 'size before', size_before,
               'size after', size_after)
        os.remove(input_path)

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
        
        self.convert_mov_chk = QCheckBox("Convert mov")
        self.convert_mov_chk.setChecked(True)
        self.convert_cr2_chk = QCheckBox("Convert cr2")
        self.convert_cr2_chk.setChecked(True)
        self.add_btn = QPushButton("Add folder...")
        self.convert_btn = QPushButton("Convert")
        self.clear_btn = QPushButton("Clear")
        
        layout.addWidget(self.tree_widget)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.convert_mov_chk)
        btn_layout.addWidget(self.convert_cr2_chk)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.convert_btn)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.add_btn.clicked.connect(self.add_clicked)
        self.convert_btn.clicked.connect(self.convert_clicked)
        self.clear_btn.clicked.connect(self.clear_clicked)
        
    def clear_clicked(self):
        self.tree_widget.clear()
        
    def add_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, "Open directory")
        if dir:
            self.add_top_level_folder(dir)
    
    def convert_clicked(self):
        self.convert_item(self.tree_widget.invisibleRootItem())
        
    def add_top_level_folder(self, root_dir):
        self.add_folder(self.tree_widget.invisibleRootItem(), root_dir)
        
    def list_contents(self, dir):
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
        files_dict = self.list_contents(path)
        contents = [os.path.basename(path),
                    str(len(files_dict['cr2'])),
                    str(len(files_dict['mov']))]
        item = QTreeWidgetItem(parent_item, contents)
        item.setExpanded(True)
        item.setData(0, QtCore.Qt.UserRole, path)
        print(*contents)
        for dir in files_dict['dirs']:
            self.add_folder(item, dir)
    
    def convert_item(self, item):
        path = item.data(0, QtCore.Qt.UserRole)
        if path is not None:
            contents = self.list_contents(path)
            if self.convert_mov_chk.isChecked():
                for movfile in contents['mov']:
                    convert_mov(movfile)
            if self.convert_cr2_chk.isChecked():
                for cr2file in contents['cr2']:
                    convert_cr2(cr2file)
        for i in range(item.childCount()):
            child = item.child(i)
            self.convert_item(child)
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()