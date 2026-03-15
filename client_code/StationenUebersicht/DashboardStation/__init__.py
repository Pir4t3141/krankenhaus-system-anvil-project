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
    self.label_station.text = f"{row_dict['krankenhausname']} | {row_dict['stationenfachrichtung']}"
    self.row_dict = row_dict    


  @handle("link_stationenUebersicht", "click")
  def link_stationenUebersicht_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('StationenUebersicht', self.row_dict["krankenhausname"])

  @handle("plot_zimmerbelegung", "show")
  def plot_zimmerbelegung_show(self, **event_args):
    """This method is called when the Plot is shown on the screen"""
    return_values = anvil.server.call('get_einzelne_stationen_info', self.row_dict["krankenhausname"], self.row_dict["station_id"])[0]
    print(return_values)
    self.plot_zimmerbelegung.layout = {
      'title': {'text': 'Bettenbelegung'}
    }
    self.plot_zimmerbelegung.data = go.Pie(
      labels=["Belegt", "Frei"],
      values=[return_values["aktuelle_belegungen"], return_values["bettenanzahl"]-return_values["aktuelle_belegungen"]])

  @handle("plot_personal", "show")
  def plot_personal_show(self, **event_args):
    """This method is called when the Plot is shown on the screen"""
    return_values = anvil.server.call('get_arzt_betreuer_per_station', self.row_dict["station_id"])[0]
    print(return_values)
    self.plot_personal.layout = {
      'title': {'text': 'Personalverteilung'}
    }
    self.plot_personal.data = go.Pie(
      labels=["Ärzte", "Pfleger"],
      values=[return_values["anzahl_aerzte"], return_values["anzahl_pfleger"]])

  @handle("plot_personal", "click")
  def plot_personal_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    point_number = points[0]["point_number"]
    if point_number == 0:
      open_form('StationenUebersicht.DashboardStation_Aerzte', self.row_dict)
      