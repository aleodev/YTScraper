import dearpygui.dearpygui as dpg
from constants import THEME_COLORS


def create_global_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            # Color
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, THEME_COLORS["color"])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, THEME_COLORS["color"])
            dpg.add_theme_color(dpg.mvThemeCol_Button, THEME_COLORS["color"])

            # Light
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, THEME_COLORS["light"])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, THEME_COLORS["light"])

            # Darker
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, THEME_COLORS["dark"])
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, THEME_COLORS["dark"])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, THEME_COLORS["dark"])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, THEME_COLORS["dark"])

            # Custom
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (0, 77, 54, 255))

    return global_theme
