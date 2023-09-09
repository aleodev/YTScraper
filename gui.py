import dearpygui.dearpygui as dpg

dpg.create_context()


# def change_text(sender, app_data):
#     dpg.set_value("text item", f"Mouse Button ID: {app_data}")
#
#
# def callback(sender, app_data):
#     print('OK was clicked.')
#     print("Sender: ", sender)
#     print("App Data: ", app_data)
#
#
# def cancel_callback(sender, app_data):
#     print('Cancel was clicked.')
#     print("Sender: ", sender)
#     print("App Data: ", app_data)
#

# Format List
formats = ["MP3", "FLV", "WAV", "MP4", "WMV"]

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
    dpg.add_listbox(items=formats, pos=[370, 54], width=71,num_items=11)
    dpg.add_progress_bar(width=433)
    dpg.add_button(label="DOWNLOAD", width=433)

dpg.create_viewport(title='YTScraper', width=465, height=500)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
