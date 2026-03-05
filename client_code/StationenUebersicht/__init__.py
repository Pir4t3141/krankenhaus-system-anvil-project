from ._anvil_designer import StationenUebersichtTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class StationenUebersicht(StationenUebersichtTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.layout.set_event_handler('drop_down_krankenhaus_has_changed', self.drop_down_krankenhaus_has_changed)

  @handle("", "show")
  def form_show(self, **event_args):
    self.layout.reset_links()
    self.layout.link_stationen.role = 'selected'
    
  def drop_down_krankenhaus_has_changed(self, **event_args):
    """This method is called when the drop down element has changed"""
    try:
      if len(self.layout.drop_down_krankenhaus.items) > 0 and self.layout.link_krankenhaus.role == 'selected':
        pass
    finally:
      pass