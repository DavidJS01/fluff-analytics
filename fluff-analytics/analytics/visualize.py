import pandas as pd
from database_utils.database import create_postgres_conn
from database_utils.queries import EXAMPLE_SELECT_WIN_LOSSES, SELECT_TOP_5_Q_CASTS
import plotly.express as px


def visualize_winloss(conn):
    # get dataframe from query
    df = pd.read_sql(EXAMPLE_SELECT_WIN_LOSSES, conn)
    # create figure
    fig = px.bar(
        df,
        x="summoner_name",
        y=["games_won", "games_lost"],
        text="total_games",
        text_auto="above",
    )
    # update the yaxis and xaxis labels
    fig.update_layout(yaxis_title="Games Played", xaxis_title="Summoner Name")
    # show figure in browser
    fig.show()
    # save figure html to folder
    fig.write_html("./assets/visualizations_html/win_loss.html")
    # save figure image to folder
    fig.write_image("./visualizations/win_loss.png", format="png")


def visualize_top_5_q_casts(conn):
    # get datafram from query
    df = pd.read_sql(SELECT_TOP_5_Q_CASTS, conn)
    colors = ["darkgoldenrod", "crimson", "darkslategrey", "darkcyan", "darkolivegreen"]
    fig = px.pie(df, values="q_cast_total", names="champion", title="Number of Times Q is Cast")
    fig.update_traces(
        textposition="inside", textinfo="percent+label", marker=dict(colors=colors)
    )
    # show figure in browser
    fig.show()
    # save figure html to folder
    fig.write_html("../assets/visualizations_html/top_5_q_casts.html")
    # save figure image to folder
    fig.write_image("../visualizations/top_5_q_casts.png", format="png")


if __name__ == "__main__":
    conn = create_postgres_conn()
    # visualize_winloss(conn)
    visualize_top_5_q_casts(conn)
