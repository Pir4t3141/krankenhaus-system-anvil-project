from ._anvil_designer import DashboradKrankenhaus_BetreuerTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DashboradKrankenhaus_Betreuer(DashboradKrankenhaus_BetreuerTemplate):
  krankenhausname = None

  def __init__(self, krankenhausname, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.label_betreuer.text = (
      f"{krankenhausname} | BETREUER"
    )
    self.krankenhausname = krankenhausname

  @handle("link_krankenhausUebersicht", "click")
  def link_stationenUebersicht_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("KrankenhausUebersicht", self.krankenhausname)

  @handle("data_grid_betreuer_info", "show")
  def data_grid_betreuer_info_show(self, **event_args):
    """This method is called when the data grid is shown on the screen"""
    return_value = anvil.server.call("get_betreuer_stats_krankenhaus", self.krankenhausname)
    self.repeating_panel_betreuer_info.items = return_value
