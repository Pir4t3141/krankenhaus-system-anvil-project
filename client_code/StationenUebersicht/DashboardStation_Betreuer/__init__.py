from ._anvil_designer import DashboardStation_BetreuerTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DashboardStation_Betreuer(DashboardStation_BetreuerTemplate):
  row_dict = None

  def __init__(self, row_dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.label_betreuer.text = (
      f"{row_dict['krankenhausname']} | {row_dict['stationenfachrichtung']} | BETREUER"
    )
    self.row_dict = row_dict

  @handle("link_stationUebersicht", "click")
  def link_stationenUebersicht_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("StationenUebersicht.DashboardStation", self.row_dict)

  @handle("data_grid_betreuer_info", "show")
  def data_grid_betreuer_info_show(self, **event_args):
    """This method is called when the data grid is shown on the screen"""
    return_value = anvil.server.call("get_betreuer_stats", self.row_dict["station_id"])
    print(return_value)
    self.repeating_panel_betreuer_info.items = return_value
