import dearpygui.dearpygui as dpg
from digger import Digger
from constants import FORMATS, CONFIG_PATH, TEMP_PATH, THEME_COLORS
from utils import setup_temp, setup_config, show_msg
from pathlib import Path
from theme import create_global_theme
import configparser

# Config Setup
config = configparser.ConfigParser()
setup_config(
    "digger",
    {
        "default_output": Path.cwd() / "export",
        "separate_platforms": True,
        "overwrite_files": False,
        "label_quality": False,
        "tooltips": True,
    },
)
config.read(CONFIG_PATH)

# Digger Instance
ytDigger = Digger()


# Callbacks
def get_formats(reset=True):
    platform = dpg.get_value("platform").lower()
    supported = []
    if platform.lower() == "youtube":
        supported = sorted(FORMATS["video"] + FORMATS["audio"])
    elif platform.lower() == "soundcloud":
        supported = sorted(FORMATS["audio"])
    else:
        return []
    if reset:
        dpg.configure_item("format", items=supported)
        dpg.set_value("format", supported[0])

    return supported


def update_default_output(sender, app_data):
    dir = Path(app_data["file_path_name"])
    if dir != TEMP_PATH:
        if dir:
            dpg.set_value("output", dir)
            config.set("digger", "default_output", str(dir))
            with open(CONFIG_PATH, "w") as config_file:
                config.write(config_file)
        else:
            show_msg("error", "Invalid directory specified.")
            return False
    else:
        show_msg("error", "The temp directory can't be used.")
        return False
    return True


def update_tooltips(sender, app_data):
    dpg.configure_item("url_tooltip", show=app_data)
    dpg.configure_item("title_tooltip", show=app_data)
    dpg.configure_item("output_tooltip", show=app_data)
    # dpg.configure_item("save_output_tooltip", show=app_data)
    dpg.configure_item("download_tooltip", show=app_data)
    dpg.configure_item("overwrite_tooltip", show=app_data)
    dpg.configure_item("separate_tooltip", show=app_data)
    dpg.configure_item("label_tooltip", show=app_data)
    dpg.configure_item("tooltips_tooltip", show=app_data)
    save_option(sender, app_data)


# def save_default_output():
#     dir = dpg.get_value("output")
#     config_dir = config.get("digger", "default_output")
#     # Compare output dir with TEMP_PATH
#     if Path(dir) == TEMP_PATH:
#         show_msg("error", "The temp directory can't be used.")
#         dpg.set_value("output", config_dir)
#     else:
#         update = update_default_output(None, {"file_path_name": dir})
#         if update:
#             show_msg("info", "Default output has been saved.")


def save_option(sender, app_data):
    config.set("digger", sender, str(app_data))
    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)


def hide_dialog():
    dpg.hide_item("dialog")


# GUI Context
dpg.create_context()

# Themes
global_theme = create_global_theme()
with dpg.theme() as output_button_theme:
    with dpg.theme_component(dpg.mvButton):
        # Color
        dpg.add_theme_color(dpg.mvThemeCol_Button, (108, 27, 124, 255))
        # Light
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (119, 29, 137, 255))
        # Darker
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (90, 22, 103, 255))

with dpg.theme() as download_button_theme:
    with dpg.theme_component(dpg.mvButton):
        # Color
        dpg.add_theme_color(dpg.mvThemeCol_Button, THEME_COLORS["color"])
        # Light
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, THEME_COLORS["light"])
        # Darker
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, THEME_COLORS["dark"])

with dpg.theme() as progress_theme:
    with dpg.theme_component(dpg.mvProgressBar):
        # Color
        dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (163, 163, 163, 255))
        # Darker
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (72, 72, 72, 255))
with dpg.window(tag="Main"):
    dpg.add_button(tag="url_button", label="URL", enabled=False)
    with dpg.tooltip(tag="url_tooltip", parent="url_button"):
        dpg.add_text(
            "Enter the SoundCloud or YouTube link you wish to download and convert."
        )
    dpg.add_input_text(tag="url", width=400, pos=[41, 8])
    dpg.add_file_dialog(
        directory_selector=True,
        show=False,
        callback=update_default_output,
        tag="file_dialog_id",
        width=400,
        height=300,
    )
    dpg.add_button(tag="title_button", label="Title", enabled=False)
    with dpg.tooltip(tag="title_tooltip", parent="title_button"):
        dpg.add_text(
            "Specify a custom title for the output file. If left blank, the original title will be used."
        )
    dpg.add_input_text(
        tag="title",
        width=386,
        pos=[55, 31],
    )
    dpg.add_button(
        tag="output_dialog_button",
        label="Output",
        callback=lambda: dpg.show_item("file_dialog_id"),
    )
    with dpg.tooltip(tag="output_tooltip", parent="output_dialog_button"):
        dpg.add_text("Select your preferred output folder for saving exported files.")
    # dpg.add_button(
    #     tag="save_output",
    #     label="Save",
    #     callback=save_default_output,
    #     pos=[405, 54],
    # )
    # with dpg.tooltip(tag="save_output_tooltip", parent="save_output"):
    #     dpg.add_text(
    #         "Set the directory where downloaded files will be saved by default."
    #     )
    dpg.add_input_text(
        tag="output",
        default_value=config.get("digger", "default_output"),
        width=379,
        pos=[62, 54],
    )
    dpg.add_listbox(
        label="Platform",
        tag="platform",
        default_value="YouTube",
        items=["YouTube", "SoundCloud"],
        callback=get_formats,
        pos=[445, 8],
        width=82,
        num_items=2,
    )
    # with dpg.table(
    #     header_row=True,
    #     policy=dpg.mvTable_SizingFixedFit,
    #     resizable=False,
    #     no_host_extendX=True,
    #     borders_outerH=True,
    #     borders_innerV=True,
    #     borders_outerV=True,
    # ):

    #     # use add_table_column to add columns to the table,
    #     # table columns use slot 0
    #     dpg.add_table_column(label="Header 1")
    #     dpg.add_table_column(label="Header 2")
    #     dpg.add_table_column(label="Header 3")

    #     # add_table_next_column will jump to the next row
    #     # once it reaches the end of the columns
    #     # table next column use slot 1
    #     for i in range(0, 4):
    #         with dpg.table_row():
    #             for j in range(0, 3):
    #                 dpg.add_text(f"Row{i} Column{j}")
    dpg.add_listbox(
        label="Format",
        tag="format",
        items=get_formats(False),
        pos=[445, 56],
        width=82,
        num_items=13,
    )
    dpg.add_listbox(
        label="Quality",
        tag="quality",
        items=["High", "Medium", "Low"],
        pos=[445, 291],
        width=82,
        num_items=3,
    )
    dpg.add_progress_bar(tag="progress", width=433, default_value=0, overlay="0%")
    dpg.add_button(
        tag="download",
        label="DOWNLOAD",
        width=433,
        callback=ytDigger.run,
    )
    with dpg.tooltip(tag="download_tooltip", parent="download"):
        dpg.add_text("Start downloading and converting the link to an MP3 file.")
    dpg.add_checkbox(
        tag="overwrite_files",
        label="Overwrite Files",
        callback=save_option,
        default_value=eval(config.get("digger", "overwrite_files")),
    )
    with dpg.tooltip(tag="overwrite_tooltip", parent="overwrite_files"):
        dpg.add_text(
            "Overwrite existing files with the same name in the output directory."
        )
    dpg.add_checkbox(
        tag="separate_platforms",
        label="Separate Platforms",
        callback=save_option,
        default_value=eval(config.get("digger", "separate_platforms")),
    )
    with dpg.tooltip(tag="separate_tooltip", parent="separate_platforms"):
        dpg.add_text(
            "Organize downloaded files into separate folders by platform (SoundCloud/YouTube)."
        )
    dpg.add_checkbox(
        tag="label_quality",
        label="Label Quality",
        callback=save_option,
        default_value=eval(config.get("digger", "label_quality")),
    )
    with dpg.tooltip(tag="label_tooltip", parent="label_quality"):
        dpg.add_text(
            "Append a quality label (e.g., 'HQ') to the end of the output file name based on the selected quality."
        )
    dpg.add_checkbox(
        tag="tooltips",
        label="Tooltips",
        callback=update_tooltips,
        default_value=eval(config.get("digger", "tooltips")),
    )
    with dpg.tooltip(tag="tooltips_tooltip", parent="tooltips"):
        dpg.add_text("Enable or disable tooltips throughout the application.")

    # Global theme
    dpg.bind_theme(global_theme)

    # Custom theme(s)
    dpg.bind_item_theme("download", download_button_theme)
    dpg.bind_item_theme("progress", progress_theme)
    dpg.bind_item_theme("output_dialog_button", output_button_theme)

with dpg.window(
    label="",
    autosize=True,
    modal=True,
    show=False,
    tag="dialog",
):
    dpg.add_text(wrap=375, default_value="", tag="dialog_msg")
    dpg.add_button(label="OK", callback=hide_dialog)

dpg.show_style_editor()
if __name__ == "__main__":
    # Startup functions
    setup_temp()
    update_tooltips("tooltips", eval(config.get("digger", "tooltips")))

    # GUI init
    dpg.create_viewport(
        title="Track Digger (rev 0.1)",
        width=610,
        height=400,
        small_icon="resources/icon.ico",
        # resizable=False,
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Main", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
