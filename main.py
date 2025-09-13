import pandas as pd
import streamlit as st


def handle_change():
    changes = st.session_state["df_editor"]
    df = st.session_state.df.copy()

    for row_idx, updates in changes["edited_rows"].items():
        for col, new_val in updates.items():
            df.at[row_idx, col] = new_val

    # filter out placeholder/empty added rows
    new_rows = [r for r in changes["added_rows"] if r]

    if new_rows:
        df = pd.concat(
            [df, pd.DataFrame(new_rows, columns=df.columns)],  # keep schema
            ignore_index=True,
        )

    # apply deletions
    if changes["deleted_rows"]:
        df = df.drop(index=changes["deleted_rows"]).reset_index(drop=True)

    df["c"] = df["a"] + df["b"]

    did_change = bool(changes["edited_rows"] or new_rows or changes["deleted_rows"])
    if did_change:
        st.session_state.df = df
        st.session_state.sum = int(df.c.sum())


def main():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(
            [{"a": 10, "b": 20}, {"a": 2, "b": 3}, {"a": 44, "b": 50}],
            columns=["a", "b", "c"],
        )

    st.subheader("Change a or b, you can also add or delete rows")

    st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        key="df_editor",
        disabled=["c"],
        on_change=handle_change,
    )

    st.metric("Sum column c", st.session_state.get("sum"))


if __name__ == "__main__":
    main()
