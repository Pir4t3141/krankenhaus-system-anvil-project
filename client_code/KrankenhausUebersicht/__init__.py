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

  @handle("", "show")
  def form_show(self, **event_args):
    self.layout.reset_links()
    self.layout.link_krankenhaus.role = 'selected'

  @handle("", "drop_down_krankenhaus_has_changed")
  def form_drop_down_krankenhaus_has_changed(self, **event_args):
    """This method is called when the component is changed"""
    print("tuff")
