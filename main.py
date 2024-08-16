import dearpygui.dearpygui as dpg
from scraper import formats
from scraper import Scraper

# Config Setup

# Scraper Instance
ytScraper = Scraper()


# GUI Functions
# def center_window(window_tag):
#     # Get the viewport size (the entire application window)
#     viewport_width = dpg.get_viewport_client_width()
#     viewport_height = dpg.get_viewport_client_height()

#     # Get the window size
#     window_width = dpg.get_item_width(window_tag)
#     window_height = dpg.get_item_height(window_tag)

#     # Calculate the position to center the window
#     pos_x = (viewport_width - window_width) // 2
#     pos_y = (viewport_height - window_height) // 2

#     # Set the window position
#     dpg.set_item_pos(window_tag, [pos_x, pos_y])


# Callbacks
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


def hide_error_dialog(sender, app_data, user_data):
    dpg.hide_item("error_dialog")


# Thumbnail Placeholder
width, height, channels, data = dpg.load_image("placeholder.png")

with dpg.texture_registry():
    texture_id = dpg.add_static_texture(
        width, height, default_value=data, tag="placeholder"
    )

with dpg.window(tag="Main"):
    dpg.add_button(label="URL")
    dpg.add_input_text(tag="url", width=400, pos=[41, 8])
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
    dpg.add_button(label="DOWNLOAD", width=433, callback=ytScraper.run)

with dpg.window(
    label="Error",
    autosize=True,
    modal=True,
    show=False,
    tag="error_dialog",
):
    dpg.add_text(wrap=375, default_value="", tag="error_message")
    dpg.add_button(label="OK", callback=hide_error_dialog)
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

dpg.create_viewport(title="Track Digger (rev 0.1)", width=550, height=450)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
