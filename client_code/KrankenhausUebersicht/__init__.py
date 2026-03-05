from ._anvil_designer import KrankenhausUebersichtTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class KrankenhausUebersicht(KrankenhausUebersichtTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens. 
    self.layout.set_event_handler('drop_down_krankenhaus_has_changed', self.drop_down_krankenhaus_has_changed)

  @handle("", "show")
  def form_show(self, **event_args):
    self.layout.reset_links()
    self.layout.link_krankenhaus.role = 'selected'

  def drop_down_krankenhaus_has_changed(self, **event_args):
    """This method is called when the drop down element has changed"""
    try:
      print(self.layout.drop_down_krankenhaus.selected_value)
      coordinates = anvil.server.call('get_coordinates', self.layout.drop_down_krankenhaus.selected_value)[0]
      print(coordinates)
  
      marker = GoogleMap.Marker(
        animation=GoogleMap.Animation.DROP,
        position=GoogleMap.LatLng(coordinates[0], coordinates[1])
      )
  
      self.map_krankenhaus.zoom = 20
      self.map_krankenhaus.center = GoogleMap.LatLng(coordinates[0], coordinates[1])
      self.map_krankenhaus.add_component(marker)
    except:
      pass