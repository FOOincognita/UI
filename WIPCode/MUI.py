import streamlit as st
from streamlit_elements import elements, mui, html, nivo, lazy, sync

def dashboard():
    with elements("dashboard"):

        # You can create a draggable and resizable dashboard using
        # any element available in Streamlit Elements.

        from streamlit_elements import dashboard

        # First, build a default layout for every element you want to include in your dashboard

        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("first_item", 0, 0, 2, 2),
            dashboard.Item("second_item", 2, 0, 2, 2, isDraggable=False, moved=False),
            dashboard.Item("third_item", 0, 2, 1, 1, isResizable=False),
        ]

        # Next, create a dashboard layout using the 'with' syntax. It takes the layout
        # as first parameter, plus additional properties you can find in the GitHub links below.

        with dashboard.Grid(layout):
            mui.Paper("First item", key="first_item")
            mui.Paper("Second item (cannot drag)", key="second_item")
            mui.Paper("Third item (cannot resize)", key="third_item")

        # If you want to retrieve updated layout values as the user move or resize dashboard items,
        # you can pass a callback to the onLayoutChange event parameter.

        def handle_layout_change(updated_layout):
            # You can save the layout in a file, or do anything you want with it.
            # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
            print(updated_layout)

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            mui.Paper("First item", key="first_item")
            mui.Paper("Second item (cannot drag)", key="second_item")
            mui.Paper("Third item (cannot resize)", key="third_item")

    with elements("nivo_charts"):

        # Streamlit Elements includes 45 dataviz components powered by Nivo.

        from streamlit_elements import nivo

        DATA = [
            { "taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114 },
            { "taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72 },
            { "taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99 },
            { "taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30 },
            { "taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103 },
        ]

        with mui.Box(sx={"height": 500}):
            nivo.Radar(
                data=DATA,
                keys=[ "chardonay", "carmenere", "syrah" ],
                indexBy="taste",
                valueFormat=">-.2f",
                margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                borderColor={ "from": "color" },
                gridLabelOffset=36,
                dotSize=10,
                dotColor={ "theme": "background" },
                dotBorderWidth=2,
                motionConfig="wobbly",
                legends=[
                    {
                        "anchor": "top-left",
                        "direction": "column",
                        "translateX": -50,
                        "translateY": -40,
                        "itemWidth": 80,
                        "itemHeight": 20,
                        "itemTextColor": "#999",
                        "symbolSize": 12,
                        "symbolShape": "circle",
                        "effects": [
                            {
                                "on": "hover",
                                "style": {
                                    "itemTextColor": "#000"
                                }
                            }
                        ]
                    }
                ],
                theme={
                    "background": "#FFFFFF",
                    "textColor": "#31333F",
                    "tooltip": {
                        "container": {
                            "background": "#FFFFFF",
                            "color": "#31333F",
                        }
                    }
                }
            )
            
            
    with elements("monaco_editors"):

        # Streamlit Elements embeds Monaco code and diff editor that powers Visual Studio Code.
        # You can configure editor's behavior and features with the 'options' parameter.
        #
        # Streamlit Elements uses an unofficial React implementation (GitHub links below for
        # documentation).

        from streamlit_elements import editor

        if "content" not in st.session_state:
            st.session_state.content = "Default value"

        mui.Typography("Content: ", st.session_state.content)

        def update_content(value):
            st.session_state.content = value

        editor.Monaco(
            height=300,
            defaultValue=st.session_state.content,
            onChange=lazy(update_content)
        )

        mui.Button("Update content", onClick=sync())

        editor.MonacoDiff(
            original="Happy Streamlit-ing!",
            modified="Happy Streamlit-in' with Elements!",
            height=300,
        )