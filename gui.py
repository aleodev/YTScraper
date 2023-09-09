import dearpygui.dearpygui as dpg

import scraper
from scraper import Scraper

# Singleton Instance
ytScraper = Scraper()

# GUI Context
dpg.create_context()

ytScraper.verifyID(urlid="LDD")


def callback(sender, app_data):
    print('OK was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)


def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)


# Thumbnail Placeholder
width, height, channels, data = dpg.load_image("placeholder.png")

with dpg.texture_registry():
    texture_id = dpg.add_static_texture(width, height, default_value=data, tag="placeholder")

with dpg.window(tag="Main"):
    dpg.add_button(label="Verify ID")
    dpg.add_input_text(width=358, pos=[83, 8])
    dpg.add_file_dialog(directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
                        cancel_callback=cancel_callback, width=400, height=300)
    dpg.add_button(label="Output DIR", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_input_text(width=351, pos=[90, 31])
    dpg.add_image_button(width=350, height=191, texture_tag="placeholder")
    dpg.add_listbox(items=scraper.formats, pos=[370, 54], width=71, num_items=11)
    dpg.add_progress_bar(width=433, overlay="downloading" + Scraper.status, default_value=0.4)
    dpg.add_button(label="DOWNLOAD", width=433)

dpg.create_viewport(title='YTScraper', width=465, height=370)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
