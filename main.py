import dearpygui.dearpygui as dpg
from scraper import formats
from scraper import Scraper

# Config Setup

# Scraper Instance
ytScraper = Scraper()


# Callbacks
def verify_cb(sender, app_data):
    print(dpg.get_value("format"))


def update_formats(reset=True):
    platform = dpg.get_value("platform").lower()
    supported = []
    if platform.lower() == "youtube":
        supported = sorted(formats["video"] + formats["audio"])
    elif platform.lower() == "soundcloud":
        supported = sorted(formats["audio"])
    else:
        return []
    if reset:
        dpg.configure_item("format", items=supported)
        dpg.set_value("format", supported[0])

    return supported


# def

# GUI Context
dpg.create_context()


def callback(sender, app_data):
    print("OK was clicked.")
    print("Sender: ", sender)
    print("App Data: ", app_data)


def cancel_callback(sender, app_data):
    print("Cancel was clicked.")
    print("Sender: ", sender)
    print("App Data: ", app_data)


# Thumbnail Placeholder
width, height, channels, data = dpg.load_image("placeholder.png")

with dpg.texture_registry():
    texture_id = dpg.add_static_texture(
        width, height, default_value=data, tag="placeholder"
    )

with dpg.window(tag="Main"):
    dpg.add_button(label="URL", callback=verify_cb)
    dpg.add_input_text(width=400, pos=[41, 8])
    dpg.add_file_dialog(
        directory_selector=True,
        show=False,
        callback=callback,
        tag="file_dialog_id",
        cancel_callback=cancel_callback,
        width=400,
        height=300,
    )
    dpg.add_button(label="Output DIR", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_input_text(width=351, pos=[90, 31])
    dpg.add_listbox(
        tag="platform",
        default_value="YouTube",
        items=["YouTube", "SoundCloud"],
        callback=update_formats,
        pos=[445, 8],
        width=82,
        num_items=2,
    )
    dpg.add_image(width=350, height=191, texture_tag="placeholder")
    dpg.add_listbox(
        tag="format", items=update_formats(False), pos=[445, 56], width=82, num_items=12
    )
    dpg.add_progress_bar(
        tag="progress",
        width=433,
        default_value=0,
    )
    dpg.add_button(label="DOWNLOAD", width=433)

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

dpg.create_viewport(title="Track Digger", width=550, height=450)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
