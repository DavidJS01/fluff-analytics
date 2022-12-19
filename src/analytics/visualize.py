import pandas as pd
from database_utils.database import create_postgres_conn
from database_utils.queries import EXAMPLE_SELECT_WIN_LOSSES
import plotly.express as px


conn = create_postgres_conn()


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
    fig.write_html("./visualizations/win_loss.html")


visualize_winloss(conn)
