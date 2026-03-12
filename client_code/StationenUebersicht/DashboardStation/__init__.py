from ._anvil_designer import DashboardStationTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DashboardStation(DashboardStationTemplate):
  row_dict=None
  
  def __init__(self, row_dict ,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
  
    # Any code you write here will run before the form opens.
    self.label_station.text = row_dict["stationenfachrichtung"]
    self.row_dict = row_dict

  @handle("link_stationenUebersicht", "click")
  def link_stationenUebersicht_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('StationenUebersicht', self.row_dict["krankenhausname"])
