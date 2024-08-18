import dearpygui.dearpygui as dpg
from scraper import Scraper
from constants import FORMATS, CONFIG_PATH, TEMP_PATH
from utils import setup_temp, setup_config
from pathlib import Path
import configparser

# Config Setup
config = configparser.ConfigParser()
setup_config(
    "scraper",
    {
        "default_output": Path.cwd() / "export",
        "separate_platforms": True,
    },
)
config.read(CONFIG_PATH)
# Scraper Instance
ytScraper = Scraper()


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
            config.set("scraper", "default_output", str(dir))
            with open(CONFIG_PATH, "w") as config_file:
                config.write(config_file)
        else:
            Scraper.show_msg("error", "Invalid directory specified.")
    else:
        Scraper.show_msg("error", "The temp directory can't be used.")


def hide_dialog():
    dpg.hide_item("dialog")


# GUI Context
dpg.create_context()


# Thumbnail Placeholder
width, height, channels, data = dpg.load_image("placeholder.png")

with dpg.texture_registry():
    texture_id = dpg.add_static_texture(
        width, height, default_value=data, tag="placeholder"
    )

with dpg.window(tag="Main"):
    dpg.add_button(label="URL", enabled=False)
    dpg.add_input_text(tag="url", width=400, pos=[41, 8])
    dpg.add_file_dialog(
        directory_selector=True,
        show=False,
        callback=update_default_output,
        tag="file_dialog_id",
        width=400,
        height=300,
    )
    dpg.add_button(label="Output", callback=lambda: dpg.show_item("file_dialog_id"))
    # dpg.add_image(width=256, height=256, texture_tag="placeholder")
    dpg.add_input_text(
        tag="output",
        default_value=config.get("scraper", "default_output"),
        width=379,
        pos=[62, 31],
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
    dpg.add_progress_bar(
        tag="progress",
        width=433,
        default_value=0,
    )
    dpg.add_button(
        tag="download",
        label="DOWNLOAD",
        width=433,
        callback=ytScraper.run,
    )


with dpg.window(
    label="",
    autosize=True,
    modal=True,
    show=False,
    tag="dialog",
):
    dpg.add_text(wrap=375, default_value="", tag="dialog_msg")
    dpg.add_button(label="close", callback=hide_dialog)

# NOTE THEME
# HeaderHovered(menu button hover) -> (255,255,255,127)
# HeaderActive(menu button hold click) -> (255,255,255,63)
# HeaderActive(menu button hold click) -> (255,255,255,63)
# FrameBgActive(selected menu button) -> RED IF YT, ORANGE IF SOUNDCLOUD

# with dpg.theme() as global_theme:
#     with dpg.theme_component(dpg.mvAll):
#         dpg.add_theme_color(
#             dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core
#         )
#         dpg.add_theme_style(
#             dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
#         )
# dpg.bind_theme(global_theme)
# dpg.show_style_editor()

if __name__ == "__main__":
    # Startup functions
    setup_temp()

    # GUI init
    dpg.create_viewport(
        title="Track Digger (rev 0.1)",
        width=610,
        height=400,
        small_icon="icon.ico",
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Main", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
