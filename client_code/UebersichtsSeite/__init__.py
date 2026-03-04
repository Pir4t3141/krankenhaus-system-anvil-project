from ._anvil_designer import UebersichtsSeiteTemplate
from anvil import *


class UebersichtsSeite(UebersichtsSeiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("link_krankenhaus", "click")
  def link_krankenhaus_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('KrankenhausUebersicht')

  @handle("link_stationen", "click")
  def link_stationen_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('StationenUebersicht')

  @handle("link_zimmer", "click")
  def link_zimmer_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('ZimmerUebersicht')

  def reset_links(self, **event_args):
    self.link_krankenhaus.role = ''
    self.link_stationen.role = ''
    self.link_zimmer.role = ''