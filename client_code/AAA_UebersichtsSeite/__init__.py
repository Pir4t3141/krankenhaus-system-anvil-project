from ._anvil_designer import AAA_UebersichtsSeiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class AAA_UebersichtsSeite(AAA_UebersichtsSeiteTemplate):
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

  def drop_down_krankenhaus_fill(self, **event_args):
    return_value = anvil.server.call('get_krankenhaeuser')
    return_value = [entry[1] for entry in return_value]
    self.drop_down_krankenhaus.items = return_value

    self.drop_down_krankenhaus_change()

  @handle("drop_down_krankenhaus", "change")
  def drop_down_krankenhaus_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  @handle("drop_down_krankenhaus", "show")
  def drop_down_krankenhaus_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    self.drop_down_krankenhaus_fill()
