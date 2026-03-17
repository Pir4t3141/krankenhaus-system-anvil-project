from ._anvil_designer import PatientenUebersichtTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class PatientenUebersicht(PatientenUebersichtTemplate):
  def __init__(self, krankenhausname=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.layout.add_event_handler('drop_down_krankenhaus_has_changed', self.drop_down_krankenhaus_has_changed)
    if krankenhausname is not None:
      self.layout.drop_down_krankenhaus.selected_value = krankenhausname

  def drop_down_krankenhaus_has_changed(self, **event_args):
    """This method is called when the drop down element has changed"""
    try:
      if len(self.layout.drop_down_krankenhaus.items) > 0 and self.layout.link_patienten.role == 'selected':
        return_value = anvil.server.call('get_patienten_info', self.layout.drop_down_krankenhaus.selected_value)
        self.repeating_panel_patient.items = return_value
    finally:
      pass

  @handle("", "show")
  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.layout.reset_links()
    self.layout.link_patienten.role = 'selected'
    self.drop_down_krankenhaus_has_changed()

  @handle("text_box_patientenID", "change")
  def text_box_patientenID_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    rows = self.repeating_panel_patient.get_components()
    i = 0
    for entry in rows:
      pass
