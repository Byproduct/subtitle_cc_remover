# Dark mode colors
DARK_BG = "#2d2d2d"
DARK_BG_LIGHTER = "#3d3d3d"
DARK_BORDER = "#555"
DARK_TEXT = "#ffffff"
DARK_BUTTON_PRIMARY = "#0d6efd"
DARK_BUTTON_HOVER = "#0b5ed7"

# Light mode colors
LIGHT_BG = "#ffffff"
LIGHT_BG_ALT = "#f8f9fa"
LIGHT_BORDER = "#ddd"
LIGHT_TEXT = "#2c3e50"
LIGHT_BUTTON_PRIMARY = "#3498db"
LIGHT_BUTTON_HOVER = "#2980b9"

# Common styles
BORDER_RADIUS = "5px"
PADDING = "10px"
BUTTON_PADDING_COMPACT = "5px 10px"

def get_dialog_style(dark_mode):
    if dark_mode:
        return f"""
            QDialog {{
                background-color: {DARK_BG};
                color: {DARK_TEXT};
            }}
            QTextEdit {{
                background-color: {DARK_BG_LIGHTER};
                color: {DARK_TEXT};
                border: 1px solid {DARK_BORDER};
                border-radius: {BORDER_RADIUS};
                padding: {PADDING};
            }}
        """
    return ""

def get_dialog_button_style(dark_mode):
    bg_color = DARK_BUTTON_PRIMARY if dark_mode else LIGHT_BUTTON_PRIMARY
    hover_color = DARK_BUTTON_HOVER if dark_mode else LIGHT_BUTTON_HOVER
    
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: white;
            border: none;
            padding: {PADDING};
            border-radius: {BORDER_RADIUS};
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
    """

def get_drop_area_style(dark_mode):
    if dark_mode:
        return f"""
            QLabel {{
                border: 2px dashed {DARK_BORDER};
                border-radius: {BORDER_RADIUS};
                background-color: {DARK_BG_LIGHTER};
                color: {DARK_TEXT};
                padding: 20px;
            }}
        """
    return f"""
        QLabel {{
            border: 2px dashed #aaa;
            border-radius: {BORDER_RADIUS};
            background-color: {LIGHT_BG_ALT};
            padding: 20px;
        }}
    """

def get_title_style(dark_mode):
    color = DARK_TEXT if dark_mode else LIGHT_TEXT
    return f"""
        QLabel {{
            font-size: 24px;
            font-weight: bold;
            color: {color};
            margin: 10px;
        }}
    """

def get_text_display_style(dark_mode):
    if dark_mode:
        return f"""
            QTextEdit {{
                background-color: {DARK_BG_LIGHTER};
                color: {DARK_TEXT};
                border: 1px solid {DARK_BORDER};
                border-radius: {BORDER_RADIUS};
                padding: {PADDING};
            }}
        """
    return f"""
        QTextEdit {{
            background-color: {LIGHT_BG};
            border: 1px solid {LIGHT_BORDER};
            border-radius: {BORDER_RADIUS};
            padding: {PADDING};
        }}
    """

def get_button_style(dark_mode):
    bg_color = DARK_BUTTON_PRIMARY if dark_mode else LIGHT_BUTTON_PRIMARY
    hover_color = DARK_BUTTON_HOVER if dark_mode else LIGHT_BUTTON_HOVER
    
    button_style = f"""
        QPushButton {{
            background-color: {bg_color};
            color: white;
            border: none;
            padding: {BUTTON_PADDING_COMPACT};
            border-radius: 4px;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
    """
    
    checkbox_style = f"""
        QCheckBox {{
            color: {DARK_TEXT};
        }}
    """ if dark_mode else ""
    
    return button_style, checkbox_style

def get_main_widget_style(dark_mode):
    if dark_mode:
        return f"""
            QWidget {{
                background-color: {DARK_BG};
                color: {DARK_TEXT};
            }}
        """
    return ""

# Style update functions
def update_title_style(widget, dark_mode):
    widget.setStyleSheet(get_title_style(dark_mode))

def update_text_display_style(widget, dark_mode):
    widget.setStyleSheet(get_text_display_style(dark_mode))

def update_button_style(button_widget, checkbox_widget, dark_mode):
    button_style, checkbox_style = get_button_style(dark_mode)
    button_widget.setStyleSheet(button_style)
    checkbox_widget.setStyleSheet(checkbox_style)

def update_main_widget_style(widget, dark_mode):
    widget.setStyleSheet(get_main_widget_style(dark_mode))

def update_drop_area_style(widget, dark_mode):
    widget.setStyleSheet(get_drop_area_style(dark_mode))

class StyleWidgets:
    """Container for all widgets that need styling."""
    def __init__(self):
        self.main_widget = None
        self.title_label = None
        self.text_display = None
        self.button = None
        self.checkbox = None
        self.drop_area = None

# Global instance to hold all widgets
widgets = StyleWidgets()

def update_all_styles(dark_mode):
    """Update all widget styles at once using the global widgets instance."""
    update_main_widget_style(widgets.main_widget, dark_mode)
    update_title_style(widgets.title_label, dark_mode)
    update_text_display_style(widgets.text_display, dark_mode)
    update_button_style(widgets.button, widgets.checkbox, dark_mode)
    update_drop_area_style(widgets.drop_area, dark_mode) 