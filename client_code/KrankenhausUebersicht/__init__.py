from ._anvil_designer import KrankenhausUebersichtTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class KrankenhausUebersicht(KrankenhausUebersichtTemplate):
  def __init__(self, krankenhausname=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens. 
    self.layout.add_event_handler('drop_down_krankenhaus_has_changed', self.drop_down_krankenhaus_has_changed)
    if krankenhausname is not None:
      self.layout.drop_down_krankenhaus.selected_value = krankenhausname

  @handle("", "show")
  def form_show(self, **event_args):
    self.layout.reset_links()
    self.layout.link_krankenhaus.role = 'selected'
    self.drop_down_krankenhaus_has_changed()

  def drop_down_krankenhaus_has_changed(self, **event_args):
    """This method is called when the drop down element has changed"""
    try:
      if len(self.layout.drop_down_krankenhaus.items) > 0 and self.layout.link_krankenhaus.role == 'selected':
        return_value = anvil.server.call('get_coordinates', self.layout.drop_down_krankenhaus.selected_value)
        coordinates = return_value[0]

        self.map_krankenhaus.clear()
            
        marker = GoogleMap.Marker(
          animation=GoogleMap.Animation.DROP,
          position=GoogleMap.LatLng(coordinates[0], coordinates[1])
        )
    
        self.map_krankenhaus.zoom = 20
        self.map_krankenhaus.center = GoogleMap.LatLng(coordinates[0], coordinates[1])
        self.map_krankenhaus.add_component(marker)

        self.change_plot_personal()
        self.change_plot_bettenanzahl()
    finally:
      pass

  def change_plot_personal(self):
    """This method is called when the Plot is shown on the screen"""
    return_values = anvil.server.call('get_krankenhaus_info', self.layout.drop_down_krankenhaus.selected_value)[0]
    self.plot_personal.layout = {
      'title': {'text': 'Personalverteilung'}
    }
    self.plot_personal.data = go.Pie(
      labels=["Ärzte", "Betreuer"],
      values=[return_values["anzahl_aerzte"], return_values["anzahl_betreuer"]]
    )
    
  def change_plot_bettenanzahl(self):
    """This method is called when the Plot is shown on the screen"""
    return_values = anvil.server.call('get_krankenhaus_info', self.layout.drop_down_krankenhaus.selected_value)[0]
    self.plot_bettenanzahl.layout = {
      'title': {'text': 'Bettenverteilung'}
    }
    self.plot_bettenanzahl.data = go.Pie(
      labels=["Belegt", "Frei"],
      values=[return_values["belegte_betten_aktuell"], return_values["gesamtbetten_kapazitaet"]-return_values["belegte_betten_aktuell"]]
    )

  @handle("plot_personal", "click")
  def plot_personal_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    point_number = points[0]["point_number"]
    if point_number == 0:
      open_form('KrankenhausUebersicht.DashboardKrankenhaus_Aerzte', self.layout.drop_down_krankenhaus.selected_value)
    elif point_number == 1:
      open_form('KrankenhausUebersicht.DashboradKrankenhaus_Betreuer', self.layout.drop_down_krankenhaus.selected_value)

  @handle("plot_personal", "hover")
  def plot_personal_hover(self, points, **event_args):
    """This method is called when a data point is hovered."""
    self.layout.role = 'click_hand'

  @handle("plot_personal", "unhover")
  def plot_personal_unhover(self, points, **event_args):
    """This method is called when a data point is unhovered."""
    self.layout.role = 'normal_hand'
