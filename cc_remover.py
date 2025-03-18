import os
import sys
import webbrowser

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from file_operations import clean_single_file
import styles

def resource_path(relative_path):
    """Get absolute path to resource"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SubtitleCleaner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Closed Captions Remover")
        self.setMinimumSize(600, 500)
        
        # Store CC lines for each file
        self.file_cc_lines = {}
        
        # Dark mode by default
        self.dark_mode = True

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Create a container widget for the main content
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.layout.addWidget(self.content_widget)

        # Header with title, dark mode toggle and open output folder button
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("Closed Captions Remover")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
       
        buttons_layout = QHBoxLayout()
        
        self.dark_mode_toggle = QCheckBox("dark mode")
        self.dark_mode_toggle.setChecked(True)
        self.dark_mode_toggle.toggled.connect(self.toggle_dark_mode)
        
        self.open_output_btn = QPushButton("output folder")
        self.open_output_btn.setFixedHeight(32)
        
        self.open_output_btn.clicked.connect(self.open_output_folder)
        
        buttons_layout.addWidget(self.dark_mode_toggle)
        buttons_layout.addWidget(self.open_output_btn)
        
        header_layout.addWidget(self.title_label, 4)  # title takes 4/5 of space
        header_layout.addLayout(buttons_layout, 1)    # 1/5 for buttons
        
        # Area to drop files in
        self.drop_area = DropArea(self)

        # Text display area
        self.text_display = ClickableTextEdit()
        self.text_display.setMinimumHeight(200)
        self.text_display.clicked.connect(self.show_cc_lines)
        
        # Set cursor to pointing hand when hovering over clickable text
        self.text_display.viewport().setCursor(QCursor(Qt.PointingHandCursor))

        # Store widgets in the global styles.widgets instance
        styles.widgets.main_widget = self.main_widget
        styles.widgets.title_label = self.title_label
        styles.widgets.text_display = self.text_display
        styles.widgets.button = self.open_output_btn
        styles.widgets.checkbox = self.dark_mode_toggle
        styles.widgets.drop_area = self.drop_area

        # Apply initial styles
        styles.update_all_styles(self.dark_mode)

        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.drop_area)
        self.layout.addWidget(self.text_display)

        # Buy me a coffee button
        self.bmc_button = QPushButton(" buy me a coffee")
        icon_path = resource_path("bmc-brand-icon.svg")
        self.bmc_button.setIcon(QIcon(icon_path))
        self.bmc_button.setIconSize(QSize(24, 24))
        self.bmc_button.setFixedSize(150, 32)
        self.bmc_button.clicked.connect(lambda: webbrowser.open("https://buymeacoffee.com/byproduct"))
        
        # Store BMC button in styles.widgets for dark mode updates
        styles.widgets.bmc_button = self.bmc_button
        
        # Apply initial styles
        button_style, _ = styles.get_button_style(self.dark_mode)
        self.bmc_button.setStyleSheet(button_style + """
            QPushButton QIcon {
                margin-right: 5px;
            }
        """)
        
        # Create a container for the BMC button
        bmc_container = QWidget()
        bmc_layout = QHBoxLayout(bmc_container)
        bmc_layout.setContentsMargins(0, 0, 0, 0)
        bmc_layout.addStretch()
        bmc_layout.addWidget(self.bmc_button)
        self.layout.addWidget(bmc_container)

        # Ensure output directory exists
        os.makedirs('output', exist_ok=True)

        # Initial text
        self.text_display.setText("Drop .srt files above to remove closed captions.\n\n"
                                "Processed files will be saved in the output folder.")
    
    def toggle_dark_mode(self, checked):
        self.dark_mode = checked
        styles.update_all_styles(self.dark_mode)
        # Update BMC button style
        button_style, _ = styles.get_button_style(self.dark_mode)
        self.bmc_button.setStyleSheet(button_style + """
            QPushButton QIcon {
                margin-right: 5px;
            }
        """)

    def process_files(self, files):
        self.text_display.clear()
        self.text_display.clear_clickable_texts()
        
        # Sort .srt files alphabetically before cleaning
        srt_files = sorted([f for f in files if f.lower().endswith('.srt')])
        
        for file_path in srt_files:
            filename = os.path.basename(file_path)
            output_path = os.path.join('output', filename)
            
            try:
                removed_cc_lines = clean_single_file(file_path, output_path)
                num_removed = len(removed_cc_lines)
                
                # Add text to display
                cursor = self.text_display.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)
                if cursor.position() > 0:  # If there's already text, add a newline
                    self.text_display.append("")
                
                if num_removed == 0:
                    self.text_display.append(f"No closed captions detected in {filename}")
                else:
                    # Store the CC lines for this file and create clickable text
                    self.file_cc_lines[filename] = removed_cc_lines
                    summary_text = f"Removed {num_removed} closed captions from {filename}. Click to show."
                    self.text_display.append(summary_text)                   
                    self.text_display.add_clickable_text(summary_text, filename)
                
            except Exception as e:
                error_msg = f"Error processing {filename}: {str(e)}"
                self.text_display.append(error_msg)

    def show_cc_lines(self, filename):
        if filename in self.file_cc_lines:
            dialog = CCLinesDialog(self, self.file_cc_lines[filename], self.dark_mode)
            dialog.exec()

    def open_output_folder(self):
        path = os.path.abspath("output")
        webbrowser.open(os.path.realpath(path))


class ClickableTextEdit(QTextEdit):
    clicked = Signal(str)  # Signal to emit when text is clicked
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.clickable_texts = {}  # Dictionary to store clickable text and their associated data
        
    def mousePressEvent(self, event):
        position = event.position().toPoint()
        cursor = self.cursorForPosition(position)
        cursor.movePosition(cursor.MoveOperation.StartOfLine)
        cursor.movePosition(cursor.MoveOperation.EndOfLine, cursor.MoveMode.KeepAnchor)
        line = cursor.selectedText()
        
        # Check if the clicked line contains any of our clickable texts
        for text, data in self.clickable_texts.items():
            if text in line:
                self.clicked.emit(data)
                break
                
        super().mousePressEvent(event)
        
    def add_clickable_text(self, text, data):
        self.clickable_texts[text] = data
        
    def clear_clickable_texts(self):
        self.clickable_texts.clear()

class CCLinesDialog(QDialog):
    def __init__(self, parent=None, cc_lines=None, dark_mode=False):
        super().__init__(parent)
        self.setWindowTitle("Removed CC Lines")
        self.setMinimumSize(500, 400)      
        self.setStyleSheet(styles.get_dialog_style(dark_mode))
        
        layout = QVBoxLayout(self)
        
        # Text area for displaying CC lines
        text_display = QTextEdit()
        text_display.setReadOnly(True)       
        if cc_lines:
            for line in cc_lines:
                text_display.append(line)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)       
        close_button.setStyleSheet(styles.get_dialog_button_style(dark_mode))
        
        layout.addWidget(text_display)
        layout.addWidget(close_button)

class DropArea(QLabel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setMinimumSize(400, 200)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drop .srt files here")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.main_window.process_files(files)

def main():
    app = QApplication(sys.argv)
    window = SubtitleCleaner()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 