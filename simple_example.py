import tkinter
from pathlib import Path
from threading import Thread
from time import sleep
from tkinter import W, filedialog

import customtkinter
from customtkinter import ThemeManager


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")

from enum import Enum


output_dir_default = Path("./data/")


FONT = ThemeManager.theme["text"]["font"]


def format_directory(path: Path):
    return path.name + "/"


class DAMAGE_MODE(str, Enum):
    "Damage mode allowed in the LCA"

    LCA = "lca"
    LOCAL = "local"
    GLOBAL = "global"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def upper_list(cls):
        return [c.upper() for c in cls.list()]


class RANKS(str, Enum):
    "Ranks allowed in the LCA"

    family = "family"
    genus = "genus"
    species = "species"
    none = ""

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def str_list(cls):
        return [c if c != "" else "none" for c in cls.list()]


KW_OPTIONS_MENU = dict(
    fg_color="gray30",
    button_color="gray50",
    button_hover_color="gray60",
)

KW_OPTIONS_MENU_DISABLED = dict(
    fg_color="gray25",
    button_color="gray30",
)


KW_BUTTON_BASE = dict(
    hover=True,
    border_width=2,
    text_color_disabled="gray40",
)

KW_BUTTON_GOOD_COLORS = dict(
    fg_color=None,
    hover_color="gray30",
    border_color="gray30",
)

KW_BUTTON_BAD_COLORS = dict(
    hover_color="#78413d",
    border_color="#78413d",
    fg_color="#603431",
)


KW_BUTTON_GRID = dict(
    pady=12,
    padx=10,
    sticky="nsew",
)


KW_LABEL = dict(
    pady=12,
    padx=10,
    sticky="nsew",
)

KW_LABEL_GRID = dict(
    pady=12,
    padx=10,
    sticky="nsew",
)


KW_NAMES_NODES_ACC_LABEL_GRID = dict(
    pady=12,
    padx=10,
    sticky="nse",
)

KW_NAMES_NODES_ACC_BUTTON_GRID = dict(
    pady=12,
    padx=10,
    sticky="w",
)

KW_ENTRY_GOOD_COLORS = dict(
    border_color="gray30",
    text_color="gray90",
    placeholder_text_color="gray90",
    fg_color="#2A2D2E",
)
KW_ENTRY_DISABLED = dict(
    border_color="gray30",
    text_color="gray40",
    placeholder_text_color="gray40",
    fg_color="#2A2D2E",
)

KW_ENTRY_BAD_COLORS = dict(
    border_color="#78413d",
    text_color="gray90",
    placeholder_text_color="gray90",
    fg_color="#603431",
)


KW_SWITCH = dict(button_color="gray80")
KW_SWITCH_DISABLED = dict(button_color="gray40")


KW_SLIDER = dict(
    button_color="#1F6AA5",
    progress_color="#AAB0B5",
)
KW_SLIDER_DISABLED = dict(
    button_color="gray40",
    progress_color="gray40",
)


def path_to_text(filepath: str, cut: int = 10) -> str:
    text = Path(filepath).name
    if len(text) > cut:
        text = text[:cut] + " ..."
    return text


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("MetaDMG Confi-gui-rator")

        WIDTH = 820
        HEIGHT = 655

        X, Y = self.get_center_coordinates(WIDTH, HEIGHT)

        self.geometry(f"{WIDTH}x{HEIGHT}+{X}+{Y}")
        # call .on_closing() when app gets closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.resizable(False, False)

        # ============ create frames ============

        self.headline = customtkinter.CTkLabel(
            master=self,
            justify=tkinter.CENTER,
            text="Confi-gui-rator",
            text_font=(FONT, "-30"),
        )
        self.headline.grid(
            row=0,
            column=0,
            columnspan=2,
        )

        self.frame_bam = customtkinter.CTkFrame(
            master=self,
        )
        self.frame_bam.grid(
            row=1,
            column=0,
            sticky="nswe",
            padx=20,
            pady=20,
        )

        self.frame_lca = customtkinter.CTkFrame(
            master=self,
        )
        self.frame_lca.grid(
            row=2,
            column=0,
            sticky="nswe",
            padx=20,
            # pady=20,
        )

        self.frame_general = customtkinter.CTkFrame(
            master=self,
        )
        self.frame_general.grid(
            row=1,
            column=1,
            # sticky="e",
            # sticky="nswe",
            rowspan=3,
            # padx=20,
            pady=20,
        )

        # ============ frame_bam ============

        # configure grid layout (5x1) (row x column)

        # # empty row with minsize as spacing
        # self.frame_bam.grid_rowconfigure(0, minsize=50)
        # # empty row with minsize as spacing
        self.frame_bam.grid_columnconfigure(1, minsize=80)

        # self.init_bam()

        BAM_LABEL_WIDTH = 50
        BAM_LABEL_KW = dict(master=self.frame_bam, width=BAM_LABEL_WIDTH)

        BAM_LABEL_PAD_X = 20
        BAM_LABEL_GRID_KW = dict(
            pady=12,
            padx=BAM_LABEL_PAD_X,
            sticky="nsw",
        )

        self.bam_file_string = customtkinter.StringVar()

        self.bam_label = customtkinter.CTkLabel(
            text="BAM file:",
            **BAM_LABEL_KW,
        )
        self.bam_label.grid(
            row=0,
            column=0,
            **BAM_LABEL_GRID_KW,
        )

        self.bam_button = customtkinter.CTkButton(
            master=self.frame_bam,
            text="Select file",
            command=self.bam_callback,
            **KW_BUTTON_BASE,
            **KW_BUTTON_BAD_COLORS,
        )
        self.bam_button.grid(
            row=0,
            column=2,
            pady=12,
            # padx=100,
            sticky="e",
        )
        self.bam_is_okay = False

        # self.init_damage_mode()

        self.damage_mode_label = customtkinter.CTkLabel(
            text="Damage Mode:",
            **BAM_LABEL_KW,
        )
        self.damage_mode_label.grid(
            row=1,
            column=0,
            **BAM_LABEL_GRID_KW,
        )

        self.damage_mode_string = customtkinter.StringVar(
            value=DAMAGE_MODE.LCA,
        )

        self.damage_mode_menu = customtkinter.CTkOptionMenu(
            master=self.frame_bam,
            values=DAMAGE_MODE.list(),
            variable=self.damage_mode_string,
            command=self.damage_mode_collback,
            # width=100,
            **KW_OPTIONS_MENU,
        )

        self.damage_mode_menu.grid(
            row=1,
            column=2,
            pady=12,
            # padx=100,
            sticky="e",
        )

        self.is_lca = True

        # ============ frame_lca ============

        # configure grid layout (3 x 2) (row x column)
        self.frame_lca.grid_rowconfigure(0, minsize=10)

        # self.init_names()

        CENTER_LABEL_WIDTH = 50
        CENTER_LABEL_KW = dict(master=self.frame_lca, width=CENTER_LABEL_WIDTH)

        CENTER_LABEL_PAD_X = 20
        CENTER_LABEL_GRID_KW = dict(
            pady=12,
            padx=CENTER_LABEL_PAD_X,
            sticky="nsw",
        )

        self.names_file_string = customtkinter.StringVar()

        self.names_label = customtkinter.CTkLabel(
            text="Names:",
            **CENTER_LABEL_KW,
        )
        self.names_label.grid(
            row=1,
            column=0,
            **CENTER_LABEL_GRID_KW,
        )

        self.names_button = customtkinter.CTkButton(
            master=self.frame_lca,
            text="Select file",
            command=self.names_callback,
            **KW_BUTTON_BASE,
            **KW_BUTTON_BAD_COLORS,
        )
        self.names_button.grid(
            row=1,
            column=1,
            pady=12,
            padx=10,
        )
        self.names_is_okay = False
        self.names_button_colors = KW_BUTTON_BAD_COLORS

        # self.init_nodes()

        self.nodes_file_string = customtkinter.StringVar()

        self.nodes_label = customtkinter.CTkLabel(
            text="Nodes:",
            **CENTER_LABEL_KW,
        )
        self.nodes_label.grid(
            row=2,
            column=0,
            **CENTER_LABEL_GRID_KW,
        )

        self.nodes_button = customtkinter.CTkButton(
            master=self.frame_lca,
            text="Select file",
            command=self.nodes_callback,
            **KW_BUTTON_BASE,
            **KW_BUTTON_BAD_COLORS,
        )
        self.nodes_button.grid(
            row=2,
            column=1,
            pady=12,
            padx=10,
        )

        self.nodes_is_okay = False
        self.nodes_button_colors = KW_BUTTON_BAD_COLORS

        # self.init_acc2tax()

        self.acc2tax_file_string = customtkinter.StringVar()

        self.acc2tax_label = customtkinter.CTkLabel(
            text="Acc2tax:",
            **CENTER_LABEL_KW,
        )
        self.acc2tax_label.grid(
            row=3,
            column=0,
            **CENTER_LABEL_GRID_KW,
        )

        self.acc2tax_button = customtkinter.CTkButton(
            master=self.frame_lca,
            text="Select file",
            command=self.acc2tax_callback,
            **KW_BUTTON_BASE,
            **KW_BUTTON_BAD_COLORS,
        )

        self.acc2tax_button.grid(
            row=3,
            column=1,
            pady=12,
            padx=10,
        )

        self.acc2tax_is_okay = False
        self.acc2tax_button_colors = KW_BUTTON_BAD_COLORS

        # self.init_similarity_score()

        self.similarity_score_label = customtkinter.CTkLabel(
            text="Similarity Score:",
            **CENTER_LABEL_KW,
        )
        self.similarity_score_label.grid(
            row=4,
            column=0,
            **CENTER_LABEL_GRID_KW,
        )

        self.frame_similarity = customtkinter.CTkFrame(
            master=self.frame_lca,
            fg_color="#2A2D2E",
        )
        self.frame_similarity.grid(
            row=4,
            column=1,
            columnspan=3,
            rowspan=1,
            # pady=20,
            padx=30,
            sticky="w",
        )

        # self.frame_similarity.rowconfigure(0, weight=1)
        # self.frame_similarity.columnconfigure((0, 1, 2), weight=1)

        self.similarity_score_min_value = customtkinter.StringVar(
            value="0.95",
        )

        self.similarity_score_min = customtkinter.CTkEntry(
            master=self.frame_similarity,
            textvariable=self.similarity_score_min_value,
            width=40,
            **KW_ENTRY_GOOD_COLORS,
        )
        self.similarity_score_min.grid(
            row=0,
            column=0,
            # sticky="nse",
        )

        self.similarity_score_to = customtkinter.CTkLabel(
            master=self.frame_similarity,
            text="to",
            width=20,
        )
        self.similarity_score_to.grid(
            row=0,
            column=1,
            # sticky="ns",
        )

        self.similarity_score_max_value = customtkinter.StringVar(
            value="1.0",
        )

        self.similarity_score_max = customtkinter.CTkEntry(
            master=self.frame_similarity,
            textvariable=self.similarity_score_max_value,
            width=40,
            **KW_ENTRY_GOOD_COLORS,
        )
        self.similarity_score_max.grid(
            row=0,
            column=2,
            # sticky="nsw",
        )

        # self.init_min_mapping_quality()

        MIN_MAPPING_QUALITY_MIN = 0
        MIN_MAPPING_QUALITY_DEFAULT = 0
        MIN_MAPPING_QUALITY_MAX = 50

        self.min_mapping_quality_label = customtkinter.CTkLabel(
            text="Minimum Mapping Quality:",
            **CENTER_LABEL_KW,
        )
        self.min_mapping_quality_label.grid(
            row=5,
            column=0,
            **CENTER_LABEL_GRID_KW,
        )

        self.frame_min_mapping_quality = customtkinter.CTkFrame(
            master=self.frame_lca,
            fg_color="#2A2D2E",
        )
        self.frame_min_mapping_quality.grid(
            row=5,
            column=1,
            sticky="e",
        )

        self.min_mapping_quality_slider = customtkinter.CTkSlider(
            master=self.frame_min_mapping_quality,
            command=self.min_mapping_quality_slider_callback,
            from_=MIN_MAPPING_QUALITY_MIN,
            to=MIN_MAPPING_QUALITY_MAX,
            number_of_steps=MIN_MAPPING_QUALITY_MAX - MIN_MAPPING_QUALITY_MIN,
            width=100,
            **KW_SLIDER,
        )
        self.min_mapping_quality_slider.set(MIN_MAPPING_QUALITY_DEFAULT)
        self.min_mapping_quality_slider.grid(
            row=0,
            column=0,
            sticky="e",
        )

        self.min_mapping_quality_value = customtkinter.CTkLabel(
            master=self.frame_min_mapping_quality,
            width=20,
        )
        self.min_mapping_quality_slider_callback(MIN_MAPPING_QUALITY_DEFAULT)
        self.min_mapping_quality_value.grid(
            row=0,
            column=1,
            pady=12,
            padx=0,
        )

        # self.init_custom_database()

        self.custom_database_label = customtkinter.CTkLabel(
            text="Custom Database:",
            **CENTER_LABEL_KW,
        )
        self.custom_database_label.grid(
            row=6,
            column=0,
            **CENTER_LABEL_GRID_KW,
        )

        self.custom_database_bool = customtkinter.BooleanVar()
        self.custom_database_button_title = customtkinter.StringVar(
            value="False",
        )
        self.custom_database_switch = customtkinter.CTkSwitch(
            master=self.frame_lca,
            textvariable=self.custom_database_button_title,
            command=self.custom_database_callback,
            onvalue=True,
            offvalue=False,
            **KW_SWITCH,
        )
        self.custom_database_switch.deselect()
        self.custom_database_switch.grid(
            row=6,
            column=1,
        )

        # self.init_lca_rank()

        self.lca_rank_label = customtkinter.CTkLabel(
            text="LCA Rank:",
            **CENTER_LABEL_KW,
        )
        self.lca_rank_label.grid(
            row=7,
            column=0,
            **CENTER_LABEL_GRID_KW,
        )

        self.lca_rank_string = customtkinter.StringVar(
            value=RANKS.none,
        )

        self.lca_rank_menu = customtkinter.CTkOptionMenu(
            master=self.frame_lca,
            values=RANKS.str_list(),
            command=self.lca_rank_callback,
            text_color_disabled="gray40",
            **KW_OPTIONS_MENU,
        )
        self.lca_rank_menu.set("none")  # set initial value

        self.lca_rank_menu.grid(
            row=7,
            column=1,
        )

        # ============ frame_general ============

        # configure grid layout (3 x 2) (row x column)

        self.frame_general.grid_rowconfigure(0, minsize=10)

        RIGHT_LABEL_WIDTH = 50
        RIGHT_LABEL_KW = dict(master=self.frame_general, width=RIGHT_LABEL_WIDTH)

        RIGHT_LABEL_PAD_X = 20
        RIGHT_LABEL_GRID_KW = dict(
            pady=12,
            padx=RIGHT_LABEL_PAD_X,
            sticky="nsw",
        )

        # self.init_max_position()

        MAX_POSITION_MIN = 1
        MAX_POSITION_DEFAULT = 15
        MAX_POSITION_MAX = 30

        self.max_position_label = customtkinter.CTkLabel(
            text="Maximum Position:",
            **RIGHT_LABEL_KW,
        )
        self.max_position_label.grid(
            row=1,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.frame_max_position = customtkinter.CTkFrame(
            master=self.frame_general,
            fg_color="#2A2D2E",
        )
        self.frame_max_position.grid(
            row=1,
            column=1,
            sticky="e",
        )

        self.max_position_slider = customtkinter.CTkSlider(
            master=self.frame_max_position,
            command=self.max_position_slider_callback,
            from_=MAX_POSITION_MIN,
            to=MAX_POSITION_MAX,
            number_of_steps=MAX_POSITION_MAX - MAX_POSITION_MIN,
            width=100,
            **KW_SLIDER,
        )
        self.max_position_slider.set(MAX_POSITION_DEFAULT)
        self.max_position_slider.grid(
            row=0,
            column=0,
            sticky="e",
        )

        self.max_position_value = customtkinter.CTkLabel(
            master=self.frame_max_position,
            width=20,
        )
        self.max_position_value.grid(
            row=0,
            column=1,
            pady=12,
            padx=0,
        )

        self.max_position_slider_callback(MAX_POSITION_DEFAULT)

        # self.init_min_reads()

        self.min_reads_label = customtkinter.CTkLabel(
            text="Minimum number of reads:",
            **RIGHT_LABEL_KW,
        )
        self.min_reads_label.grid(
            row=2,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.min_reads_value = customtkinter.StringVar(
            value="0",
        )

        self.min_reads_entry = customtkinter.CTkEntry(
            master=self.frame_general,
            textvariable=self.min_reads_value,
            **KW_ENTRY_GOOD_COLORS,
        )
        self.min_reads_entry.grid(
            row=2,
            column=1,
        )

        # self.init_bayesian_forward()

        self.bayesian_label = customtkinter.CTkLabel(
            text="Bayesian:",
            **RIGHT_LABEL_KW,
        )
        self.bayesian_label.grid(
            row=3,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.bayesian_bool = customtkinter.BooleanVar()
        self.bayesian_button_title = customtkinter.StringVar(
            value="False",
        )
        self.bayesian_switch = customtkinter.CTkSwitch(
            master=self.frame_general,
            textvariable=self.bayesian_button_title,
            command=self.bayesian_callback,
            onvalue=True,
            offvalue=False,
            **KW_SWITCH,
        )
        self.bayesian_switch.deselect()
        self.bayesian_switch.grid(
            row=3,
            column=1,
        )

        self.forward_label = customtkinter.CTkLabel(
            text="Forward only:",
            **RIGHT_LABEL_KW,
        )
        self.forward_label.grid(
            row=4,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.forward_bool = customtkinter.BooleanVar()
        self.forward_button_title = customtkinter.StringVar(
            value="False",
        )
        self.forward_switch = customtkinter.CTkSwitch(
            master=self.frame_general,
            textvariable=self.forward_button_title,
            command=self.forward_callback,
            onvalue=True,
            offvalue=False,
            **KW_SWITCH,
        )
        self.forward_switch.deselect()
        self.forward_switch.grid(
            row=4,
            column=1,
        )

        # self.init_parallel()

        self.parallel_label = customtkinter.CTkLabel(
            text="Samples in parallel:",
            **RIGHT_LABEL_KW,
        )
        self.parallel_label.grid(
            row=5,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.frame_parallel_samples = customtkinter.CTkFrame(
            master=self.frame_general,
            fg_color="#2A2D2E",
        )
        self.frame_parallel_samples.grid(
            row=5,
            column=1,
            sticky="e",
        )

        PARALLEL_SAMPLES_MIN = 1
        PARALLEL_SAMPLES_DEFAULT = 1
        PARALLEL_SAMPLES_MAX = 20

        self.parallel_samples_slider = customtkinter.CTkSlider(
            master=self.frame_parallel_samples,
            command=self.parallel_samples_slider_callback,
            from_=PARALLEL_SAMPLES_MIN,
            to=PARALLEL_SAMPLES_MAX,
            number_of_steps=PARALLEL_SAMPLES_MAX - PARALLEL_SAMPLES_MIN,
            width=100,
            **KW_SLIDER,
        )
        self.parallel_samples_slider.set(PARALLEL_SAMPLES_DEFAULT)
        self.parallel_samples_slider.grid(
            row=0,
            column=0,
            sticky="e",
        )

        self.parallel_samples_value = customtkinter.CTkLabel(
            master=self.frame_parallel_samples,
            width=20,
        )
        self.parallel_samples_value.grid(
            row=0,
            column=1,
            pady=12,
            padx=0,
        )

        self.parallel_samples_slider_callback(PARALLEL_SAMPLES_DEFAULT)

        self.parallel_cores_per_sample_label = customtkinter.CTkLabel(
            text="Cores pr. sample:",
            **RIGHT_LABEL_KW,
        )
        self.parallel_cores_per_sample_label.grid(
            row=6,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.frame_parallel_cores_per_sample = customtkinter.CTkFrame(
            master=self.frame_general,
            fg_color="#2A2D2E",
        )
        self.frame_parallel_cores_per_sample.grid(
            row=6,
            column=1,
            sticky="e",
        )

        PARALLEL_CORES_PER_SAMPLE_MIN = 1
        PARALLEL_CORES_PER_SAMPLE_DEFAULT = 1
        PARALLEL_CORES_PER_SAMPLE_MAX = 20

        self.parallel_cores_per_sample_slider = customtkinter.CTkSlider(
            master=self.frame_parallel_cores_per_sample,
            command=self.parallel_cores_per_sample_slider_callback,
            from_=PARALLEL_CORES_PER_SAMPLE_MIN,
            to=PARALLEL_CORES_PER_SAMPLE_MAX,
            number_of_steps=PARALLEL_CORES_PER_SAMPLE_MAX
            - PARALLEL_CORES_PER_SAMPLE_MIN,
            width=100,
            **KW_SLIDER,
        )
        self.parallel_cores_per_sample_slider.set(PARALLEL_CORES_PER_SAMPLE_DEFAULT)
        self.parallel_cores_per_sample_slider.grid(
            row=0,
            column=0,
            sticky="e",
        )

        self.parallel_cores_per_sample_value = customtkinter.CTkLabel(
            master=self.frame_parallel_cores_per_sample,
            width=20,
        )
        self.parallel_cores_per_sample_value.grid(
            row=0,
            column=1,
            pady=12,
            padx=0,
        )

        self.parallel_cores_per_sample_slider_callback(
            PARALLEL_CORES_PER_SAMPLE_DEFAULT
        )

        # self.init_prefix_suffix()

        self.prefix_label = customtkinter.CTkLabel(
            text="Prefix:",
            **RIGHT_LABEL_KW,
        )
        self.prefix_label.grid(
            row=7,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.prefix_entry = customtkinter.CTkEntry(
            master=self.frame_general,
            placeholder_text="",
            **KW_ENTRY_GOOD_COLORS,
        )
        self.prefix_entry.grid(
            row=7,
            column=1,
        )

        self.suffix_label = customtkinter.CTkLabel(
            text="Suffix:",
            **RIGHT_LABEL_KW,
        )
        self.suffix_label.grid(
            row=8,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.suffix_entry = customtkinter.CTkEntry(
            master=self.frame_general,
            placeholder_text="",
            **KW_ENTRY_GOOD_COLORS,
        )
        self.suffix_entry.grid(
            row=8,
            column=1,
        )

        self.long_name_label = customtkinter.CTkLabel(
            text="Long name:",
            **RIGHT_LABEL_KW,
        )
        self.long_name_label.grid(
            row=9,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.long_name_bool = customtkinter.BooleanVar()
        self.long_name_button_title = customtkinter.StringVar(
            value="False",
        )
        self.long_name_switch = customtkinter.CTkSwitch(
            master=self.frame_general,
            textvariable=self.long_name_button_title,
            command=self.long_name_callback,
            onvalue=True,
            offvalue=False,
            **KW_SWITCH,
        )
        self.long_name_switch.deselect()
        self.long_name_switch.grid(
            row=9,
            column=1,
        )

        # self.init_config_name()

        self.config_name_label = customtkinter.CTkLabel(
            text="Config Name:",
            **RIGHT_LABEL_KW,
        )
        self.config_name_label.grid(
            row=10,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.config_name_entry = customtkinter.CTkEntry(
            master=self.frame_general,
            placeholder_text="config.yaml",
            **KW_ENTRY_GOOD_COLORS,
        )
        self.config_name_entry.grid(
            row=10,
            column=1,
        )

        # self.config_overwrite_label = customtkinter.CTkLabel(
        #     text="Overwrite:",
        #     **RIGHT_LABEL_KW,
        # )
        # self.config_overwrite_label.grid(
        #     row=11,
        #     column=0,
        #     **RIGHT_LABEL_GRID_KW,
        # )

        # self.config_overwrite_bool = customtkinter.BooleanVar()
        # self.config_overwrite_button_title = customtkinter.StringVar(
        #     value="False",
        # )
        # self.config_overwrite_switch = customtkinter.CTkSwitch(
        #     master=self.frame_general,
        #     textvariable=self.config_overwrite_button_title,
        #     command=self.config_overwrite_callback,
        #     onvalue=True,
        #     offvalue=False,
        #     **KW_SWITCH,
        # )
        # self.config_overwrite_switch.deselect()
        # self.config_overwrite_switch.grid(
        #     row=11,
        #     column=1,
        # )

        # self.init_output_dir()

        self.output_dir_string = customtkinter.StringVar()

        self.output_dir_label = customtkinter.CTkLabel(
            text="Output Directory",
            **RIGHT_LABEL_KW,
        )
        self.output_dir_label.grid(
            row=12,
            column=0,
            **RIGHT_LABEL_GRID_KW,
        )

        self.output_dir_button = customtkinter.CTkButton(
            master=self.frame_general,
            text=format_directory(output_dir_default),
            command=self.output_dir_callback,
            **KW_BUTTON_BASE,
            **KW_BUTTON_GOOD_COLORS,
        )
        self.output_dir_button.grid(
            row=12,
            column=1,
        )

        # self.init_generate_config()

        self.frame_generate = customtkinter.CTkFrame(
            master=self,
            fg_color="#212325",
        )
        self.frame_generate.grid(
            row=3,
            column=0,
            # sticky="n",
            # padx=10,
            # pady=0,
        )

        self.print_config_button = customtkinter.CTkButton(
            master=self.frame_generate,
            text="Generate Config",
            command=self.print_config_callback,
        )
        self.print_config_button.grid(
            row=0,
            column=0,
            pady=12,
            padx=10,
            # sticky="n",
        )

        self.compute_button = customtkinter.CTkButton(
            master=self.frame_generate,
            text="Generate config and compute",
            command=self.compute_callback,
        )
        self.compute_button.grid(
            row=0,
            column=1,
            pady=12,
            padx=10,
            # sticky="ns",
        )

        self.start_similarity_scores_background_thread()
        self.start_minimum_reads_background_thread()

        # ============ BAM FILE (FILE) ============

    # def init_bam(self):

    def bam_callback(self):
        filepaths = filedialog.askopenfilenames()
        # filepath = filedialog.askopenfilename()

        if filepaths == "":
            return

        elif len(filepaths) == 1:
            filepath = filepaths[0]
            self.bam_file_string.set(filepath)
            text = path_to_text(filepath)
            self.bam_button.configure(text=text)

        else:
            print(filepaths)
            self.bam_file_string.set(str(filepaths))
            self.bam_button.configure(text="File paths set")

        self.bam_is_okay = True
        self.bam_button.configure(**KW_BUTTON_GOOD_COLORS)

    # ============ DAMAGE MODE (ENUM) ============

    def damage_mode_collback(self, choice):

        if choice == DAMAGE_MODE.LCA:
            lca_state = "normal"
            text_color = "gray90"
            slider = KW_SLIDER
            lca_rank_menu_kw = KW_OPTIONS_MENU
            switch = KW_SWITCH
            self.is_lca = True

        else:
            lca_state = "disabled"
            text_color = "gray40"
            slider = KW_SLIDER_DISABLED
            lca_rank_menu_kw = KW_OPTIONS_MENU_DISABLED
            switch = KW_SWITCH_DISABLED
            self.is_lca = False

        texts = [
            self.names_label,
            self.nodes_label,
            self.acc2tax_label,
            self.min_mapping_quality_label,
            self.min_mapping_quality_value,
            self.custom_database_label,
            self.lca_rank_label,
        ]

        for text in texts:
            text.configure(text_color=text_color)

        states = [
            self.names_button,
            self.nodes_button,
            self.acc2tax_button,
            self.min_mapping_quality_slider,
            self.custom_database_switch,
            self.lca_rank_menu,
        ]

        for state in states:
            state.configure(state=lca_state)

        self.min_mapping_quality_slider.configure(**slider)
        self.lca_rank_menu.configure(**lca_rank_menu_kw)
        self.custom_database_switch.configure(**switch)

        if choice == DAMAGE_MODE.LCA:
            self.names_button.configure(**self.names_button_colors)
            self.nodes_button.configure(**self.nodes_button_colors)
            self.acc2tax_button.configure(**self.acc2tax_button_colors)
        else:
            self.names_button.configure(**KW_BUTTON_GOOD_COLORS)
            self.nodes_button.configure(**KW_BUTTON_GOOD_COLORS)
            self.acc2tax_button.configure(**KW_BUTTON_GOOD_COLORS)

        self.check_similarity_scores()

    # ============ NAMES FILE (FILE) ============

    def names_callback(self):
        filepath = filedialog.askopenfilename()
        if filepath != "":
            self.names_file_string.set(filepath)
            text = path_to_text(filepath)
            self.names_button.configure(text=text)
            self.names_button.configure(**KW_BUTTON_GOOD_COLORS)
            self.names_is_okay = True
            self.names_button_colors = KW_BUTTON_GOOD_COLORS

    # ============ NODES FILE (FILE) ============

    def nodes_callback(self):
        filepath = filedialog.askopenfilename()
        if filepath != "":
            self.nodes_file_string.set(filepath)
            text = path_to_text(filepath)
            self.nodes_button.configure(text=text)
            self.nodes_button.configure(**KW_BUTTON_GOOD_COLORS)
            self.nodes_is_okay = True
            self.nodes_button_colors = KW_BUTTON_GOOD_COLORS

    # ============ ACC2TAX FILE (FILE) ============

    def acc2tax_callback(self):
        filepath = filedialog.askopenfilename()
        if filepath != "":
            self.acc2tax_file_string.set(filepath)
            text = path_to_text(filepath)
            self.acc2tax_button.configure(text=text)
            self.acc2tax_button.configure(**KW_BUTTON_GOOD_COLORS)
            self.acc2tax_is_okay = True
            self.acc2tax_button_colors = KW_BUTTON_GOOD_COLORS

    # ============ SIMILARITY SCORE (ENTRY BOXES) ============

    # def init_similarity_score(self):

    # ============ MAPPING QUALITY (INTEGER) ============

    # def init_min_mapping_quality(self):

    def min_mapping_quality_slider_callback(self, value):
        self.min_mapping_quality_value.configure(text=f"= {int(value):>2d}")

    # ============ CUSTOM DATABASE (BOOL) ============

    # def init_custom_database(self):

    def custom_database_callback(self):
        state = self.custom_database_switch.get()
        self.custom_database_button_title.set(str(state))
        self.custom_database_bool.set(state)

    # ============ LCA RANK (ENUM) ============

    # def init_lca_rank(self):

    def lca_rank_callback(self, choice):
        self.lca_rank_string.set(choice if choice != "none" else RANKS.none)

    # ============ MAX POSITION (INTEGER) ============

    def max_position_slider_callback(self, value):
        self.max_position_value.configure(text=f"= {int(value):>2d}")

    # ============ MIN READS (ENTRY BOX) ============

    # ============ BAYESIAN // FORWARD (BOOLS) ============

    def bayesian_callback(self):
        state = self.bayesian_switch.get()
        self.bayesian_button_title.set(str(state))
        self.bayesian_bool.set(state)

    def forward_callback(self):
        state = self.forward_switch.get()
        self.forward_button_title.set(str(state))
        self.forward_bool.set(state)

    # ============ PARALLEL CORES (SLIDER) ============

    def parallel_samples_slider_callback(self, value):
        self.parallel_samples_value.configure(text=f"= {int(value):>2d}")

    # ============ CORES PER SAMPLE (SLIDER) ============

    def parallel_cores_per_sample_slider_callback(self, value):
        self.parallel_cores_per_sample_value.configure(text=f"= {int(value):>2d}")

    # ============ PREFIX SUFFIX (ENTRY) ============

    def long_name_callback(self):
        state = self.long_name_switch.get()
        self.long_name_button_title.set(str(state))
        self.long_name_bool.set(state)

    # ============ CONFIG NAME (ENTRY) ============

    # def config_overwrite_callback(self):
    #     state = self.config_overwrite_switch.get()
    #     self.config_overwrite_button_title.set(str(state))
    #     self.config_overwrite_bool.set(state)

    def check_similarity_scores(self):

        if self.is_lca:
            text_color = "gray90"
            self.similarity_score_label.configure(text_color=text_color)
            self.similarity_score_to.configure(text_color=text_color)
            self.similarity_score_min.configure(state="normal")
            self.similarity_score_max.configure(state="normal")

            try:
                min_score = float(self.similarity_score_min.get())
                max_score = float(self.similarity_score_max.get())
                is_float = True
            except ValueError:
                is_float = False

            if is_float and (0 <= min_score <= max_score <= 1):
                self.similarity_score_min.configure(**KW_ENTRY_GOOD_COLORS)
                self.similarity_score_max.configure(**KW_ENTRY_GOOD_COLORS)
                self.similarity_is_ok = True

            else:
                self.similarity_score_min.configure(**KW_ENTRY_BAD_COLORS)
                self.similarity_score_max.configure(**KW_ENTRY_BAD_COLORS)
                self.similarity_is_ok = False
        else:
            text_color = "gray40"
            self.similarity_score_label.configure(text_color=text_color)
            self.similarity_score_to.configure(text_color=text_color)
            self.similarity_score_min.configure(state="disabled", **KW_ENTRY_DISABLED)
            self.similarity_score_max.configure(state="disabled", **KW_ENTRY_DISABLED)

    def check_similarity_scores_background(self, interval_sec):
        # run forever
        while True:
            # block for the interval
            sleep(interval_sec)
            # perform the task
            self.check_similarity_scores()

    def start_similarity_scores_background_thread(self):
        # create and start the daemon thread
        daemon = Thread(
            target=self.check_similarity_scores_background,
            args=(0.05,),
            daemon=True,
            name="Similarity-score-checking",
        )
        daemon.start()

    ###################

    def check_minimum_reads(self):

        try:
            min_reads = int(self.min_reads_value.get())
            is_int = True
        except ValueError:
            is_int = False

        if is_int and (0 <= min_reads):
            self.min_reads_is_ok = True
            self.min_reads_entry.configure(**KW_ENTRY_GOOD_COLORS)
        else:
            self.min_reads_entry.configure(**KW_ENTRY_BAD_COLORS)
            self.min_reads_is_ok = False

    def check_minimum_reads_background(self, interval_sec):
        # run forever
        while True:
            # block for the interval
            sleep(interval_sec)
            # perform the task
            self.check_minimum_reads()

    def start_minimum_reads_background_thread(self):
        # create and start the daemon thread
        daemon = Thread(
            target=self.check_minimum_reads_background,
            args=(0.05,),
            daemon=True,
            name="minimum-reads-checking",
        )
        daemon.start()

    # ============ OUTPUT DIR (DIRECTORY) ============

    def output_dir_callback(self):
        # get a directory path by user
        filepath = filedialog.askdirectory()
        self.output_dir_string.set(filepath)

        text = format_directory(Path(filepath))
        self.output_dir_button.configure(text=text)

    # ============ PRINT ============

    def print_config_callback(self):

        self.check_similarity_scores()
        self.check_minimum_reads()

        if not self.bam_is_okay:
            print("Fix BAM file")
            return

        if self.is_lca and (not self.names_is_okay):
            print("Fix names file")
            return

        if self.is_lca and (not self.nodes_is_okay):
            print("Fix nodes file")
            return

        if self.is_lca and (not self.acc2tax_is_okay):
            print("Fix acc2tax file")
            return

        if self.is_lca and (not self.similarity_is_ok):
            print("Fix similarity score")
            return

        if not self.min_reads_is_ok:
            print("Fix minimum number of reads")
            return

        print("")
        print("Config:")

        to_print = [
            ("BAM file", self.bam_file_string),
            ("Damage Mode", self.damage_mode_string),
            ("Names", self.names_file_string),
            ("Nodes", self.nodes_file_string),
            ("Acc 2 Tax", self.acc2tax_file_string),
            ("Similarity Score Min", self.similarity_score_min),
            ("Similarity Score Max", self.similarity_score_max),
            ("Minimum Mapping Quality", self.min_mapping_quality_slider),
            ("LCA Rank", self.lca_rank_string),
            ("Custom Database", self.custom_database_bool),
            ("Max Position", self.max_position_slider),
            ("Minimum Number of Reads", self.min_reads_value),
            ("Bayesian", self.bayesian_bool),
            ("Forward Only", self.forward_bool),
            ("Samples in Parallel", self.parallel_samples_slider),
            ("Cores pr. Sample", self.parallel_cores_per_sample_slider),
            ("Prefix", self.prefix_entry),
            ("Suffix", self.suffix_entry),
            ("Long Name", self.long_name_bool),
            ("Config Name", self.config_name_entry),
            ("Output Directory", self.output_dir_string),
        ]

        for s, f in to_print:
            print(f"{s}: {repr(f.get())}")

        # if self.bam_file_string.get() == "":
        #     self.bam_button.configure(fg_color="#2e0502")

    # ============ COMPUTE ============

    def compute_callback(self):

        window = customtkinter.CTkToplevel(self)
        window.title("metaDMG - Computing")

        width = 330
        height = 100
        x, y = self.get_center_coordinates(width, height)

        window.geometry(f"{width}x{height}+{x}+{y}")

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(
            window,
            text="Are you sure you want to start the computation?",
        )

        label.grid(row=0, column=0, columnspan=2, padx=12, pady=10)

        def close_window():
            window.destroy()

        def close_and_compute_window():
            print("Running computation!!!")
            window.destroy()

        button_yes = customtkinter.CTkButton(
            master=window,
            text="Yes",
            command=close_and_compute_window,
        )
        button_yes.grid(
            row=1,
            column=0,
            pady=12,
            padx=10,
        )

        button_no = customtkinter.CTkButton(
            master=window,
            text="No",
            command=close_window,
        )
        button_no.grid(
            row=1,
            column=1,
            pady=12,
            padx=10,
        )

    # ============ OTHER ============

    def on_closing(self, event=0):
        self.destroy()

    def get_center_coordinates(self, width, height):
        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        return int(x), int(y)


if __name__ == "__main__":
    app = App()
    app.mainloop()
