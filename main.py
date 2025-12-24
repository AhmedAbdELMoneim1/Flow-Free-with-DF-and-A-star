import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from DF_A_Star import FlowFree
from configurations import flow_colors_hex, flow_colors, game_boards_examples, setting

#
#  code still need some optimizations but work THX
#


st.set_page_config(layout="wide")


def fill_example(board_size__):
    st.session_state["current_board"] = game_boards_examples[board_size__].copy()
    colors_number__ = setting[board_size__]["colors_num"]
    ex_positions = setting[board_size__]["ex_positions"]

    for color_idx__ in range(1, colors_number__+1):
        st.session_state[f"x_s_color_{color_idx__}"] = ex_positions[color_idx__][0][0]
        st.session_state[f"y_s_color_{color_idx__}"] = ex_positions[color_idx__][0][1]
        st.session_state[f"x_e_color_{color_idx__}"] = ex_positions[color_idx__][1][0]
        st.session_state[f"y_e_color_{color_idx__}"] = ex_positions[color_idx__][1][1]


def update_current_map():
    board_size__ = st.session_state["board_size"]
    w__, h__ = setting[board_size]["w"], setting[board_size]["h"]
    st.session_state["current_board"] = np.zeros((w__, h__))

    colors_number__ = setting[board_size__]["colors_num"]
    current_board__ = st.session_state["current_board"]
    for color_idx__ in range(1, colors_number__+1):
        current_board__[st.session_state[f"x_s_color_{color_idx__}"],
                        st.session_state[f"y_s_color_{color_idx__}"]] = color_idx__
        current_board__[st.session_state[f"x_e_color_{color_idx__}"],
                        st.session_state[f"y_e_color_{color_idx__}"]] = color_idx__


def change_board_state(idx):
    states_length__ = len(st.session_state["solution"].states)

    if 0 <= idx < states_length__:
        st.session_state["current_state_input"] = idx
        st.session_state["current_board"] = st.session_state["solution"].states[idx]


def reset():
    st.session_state["current_board"] = None
    st.session_state["solving_mode"] = False
    st.session_state["solution"] = None


def back():
    # print(st.session_state["solution"].states[0])
    st.session_state["current_board"] = st.session_state["solution"].states[0].copy()
    colors_number__ = setting[st.session_state["board_size"]]["colors_num"]
    positions = {v: np.argwhere(st.session_state["current_board"] == v) for v in range(1, 10)}
    for color_idx__ in range(1, colors_number__+1):
        st.session_state[f"x_s_color_{color_idx__}"] = positions[color_idx__][0][0]
        st.session_state[f"y_s_color_{color_idx__}"] = positions[color_idx__][0][1]
        st.session_state[f"x_e_color_{color_idx__}"] = positions[color_idx__][1][0]
        st.session_state[f"y_e_color_{color_idx__}"] = positions[color_idx__][1][1]
    st.session_state["solving_mode"] = False
    st.session_state["solution"] = None


if "board_size" not in st.session_state:
    st.session_state["board_size"] = None
    st.session_state["current_board"] = None
    st.session_state["solving_mode"] = False
    st.session_state["solution"] = None

st.title(":red[f]:yellow[l]:blue[o]:green[w] free", text_alignment="center")
st.header("solve with depth first and A*", text_alignment="center")

col1, col2, col3 = st.columns(3)
if col1.button("6 X 6", width="stretch", key="ex_button_6x6"):
    st.session_state["board_size"] = "6x6"
    reset()

if col2.button("8 X 8", width="stretch", key="ex_button_8x8"):
    st.session_state["board_size"] = "8x8"
    reset()

if col3.button("10 X 10", width="stretch", key="ex_button_10x10"):
    st.session_state["board_size"] = "10x10"
    reset()


if st.session_state["board_size"] is not None:

    board_size = st.session_state["board_size"]

    if st.session_state["current_board"] is None:
        fill_example(board_size)

    current_board = st.session_state["current_board"]

    board_col, inputs_col = st.columns([6, 6])

    colors_number = setting[board_size]["colors_num"]
    cmap = setting[board_size]["cmap"]

    fig, ax = plt.subplots(facecolor="#e9d8a6")
    ax.imshow(current_board, cmap=cmap, vmin=0, vmax=colors_number, origin='lower')

    for x in range(current_board.shape[1] + 1):
        ax.vlines(x - 0.5, -0.5, current_board.shape[0] - 0.5, color='#6a040f', linewidth=.4)
    for y in range(current_board.shape[0] + 1):
        ax.hlines(y - 0.5, -0.5, current_board.shape[1] - 0.5, color='#6a040f', linewidth=.4)

    # ax.axis("off")
    ax.set_xticks(range(current_board.shape[1]))
    ax.set_yticks(range(current_board.shape[0]))
    board_col.pyplot(fig)

    if not st.session_state["solving_mode"]:

        for i in range(colors_number, 0, -1):
            container = inputs_col.container()
            _, y_col_1, x_col_1, _, y_col_2, x_col_2, color_col_2 = container.columns([1, 1, 1, 1, 1, 1, 3])
            color_idx = colors_number - i + 1
            color_col_2.markdown(
                f"<span style='color:{flow_colors_hex[color_idx]}; font-size:25px'>{flow_colors[color_idx]}</span>",
                text_alignment="center",
                unsafe_allow_html=True
            )
            x_col_2.selectbox("y", setting[board_size]["options"], key=f"x_s_color_{color_idx}", width="stretch",
                              on_change=update_current_map)
            y_col_2.selectbox("x", setting[board_size]["options"], key=f"y_s_color_{color_idx}", width="stretch",
                              on_change=update_current_map)
            x_col_1.selectbox("y", setting[board_size]["options"], key=f"x_e_color_{color_idx}", width="stretch",
                              on_change=update_current_map)
            y_col_1.selectbox("x", setting[board_size]["options"], key=f"y_e_color_{color_idx}", width="stretch",
                              on_change=update_current_map)

        if inputs_col.button("Test If Can Solve It", width="stretch", shortcut="Enter", key="solving_mode_button"):
            count_colors = (current_board > 0).sum()
            if count_colors == colors_number * 2:
                try:
                    st.session_state["solution"] = FlowFree(current_board)
                    st.session_state["solution"].start_the_game()
                    st.session_state["solving_mode"] = True
                except:
                    st.session_state["solution"] = None
                    st.error("Incorrect Board")
                finally:
                    st.rerun()
            else:
                inputs_col.warning("Fill All Colors Correct First", width="stretch")

    else:
        result_id = st.session_state["solution"].result_id
        if result_id == 0:
            inputs_col.success("Success Game Solved", width="stretch")
        elif result_id == 1:
            inputs_col.error("Can't Solve More Steps Than 200K", width="stretch")
        else:
            inputs_col.error("Incorrect Board", width="stretch")

        states_length = len(st.session_state["solution"].states) - 1

        col1, col2 = inputs_col.columns(2)
        with col1:
            st.subheader("total steps", text_alignment="center")
            st.subheader(f":blue[{st.session_state["solution"].steps_number}]", text_alignment="center")
            st.button("start state", width="stretch", key="start_state_board", shortcut="S",
                      on_click=lambda: change_board_state(0))

        with col2:
            st.subheader("total backtracking", text_alignment="center")
            st.subheader(f":blue[{len(st.session_state["solution"].track_back_tracking_steps)}]", text_alignment="center")
            st.button("goal state", width="stretch", key="goal_state_board", shortcut="E",
                      on_click=lambda: change_board_state(states_length))

        inputs_col.space("small")
        inputs_col.subheader("Tracking", text_alignment="center")

        col1, col2, col3 = inputs_col.columns([1, 4, 1])

        col2.number_input("current state", min_value=0, max_value=states_length, step=1,
                          placeholder=f"{states_length}", width="stretch",
                          value=states_length, key="current_state_input",
                          on_change=lambda: change_board_state(st.session_state["current_state_input"]))

        current_state_idx = st.session_state["current_state_input"]

        col1.space("small")
        col1.button("prev", width="stretch", key="prev_state_board", shortcut="Left",
                    on_click=lambda: change_board_state(current_state_idx-1))
        col3.space("small")
        col3.button("next", width="stretch", key="next_state_board", shortcut="Right",
                    on_click=lambda: change_board_state(current_state_idx+1))

        inputs_col.button("Back", width="stretch", key="back_setup_board",  shortcut="Esc", on_click=back)
