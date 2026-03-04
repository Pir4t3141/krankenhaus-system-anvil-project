from ._anvil_designer import KrankenhausUebersichtTemplate
from anvil import *


class KrankenhausUebersicht(KrankenhausUebersichtTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("", "show")
  def form_show(self, **event_args):
    self.layout.reset_links()
    self.layout.link_krankenhaus.role = 'selected'
