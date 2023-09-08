import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(tag="Main"):
    dpg.add_text("Test")

dpg.create_viewport(title='YTScraper', width=600, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
