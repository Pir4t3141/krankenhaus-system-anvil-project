from ._anvil_designer import PatientenUebersichtTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class PatientenUebersicht(PatientenUebersichtTemplate):

  unfiltered_rows = None
  
  def __init__(self, krankenhausname=None, previous_filters=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.radio_button_krankenhaus.selected = True  
    
    self.layout.add_event_handler('drop_down_krankenhaus_has_changed', self.drop_down_krankenhaus_has_changed)
    if krankenhausname is not None:
      self.layout.drop_down_krankenhaus.selected_value = krankenhausname
    if previous_filters is not None:
      self.import_filters(previous_filters)

  def drop_down_krankenhaus_has_changed(self, **event_args):
    """This method is called when the drop down element has changed"""
    try:
      if len(self.layout.drop_down_krankenhaus.items) > 0 and self.layout.link_patienten.role == 'selected':
        return_value = anvil.server.call('get_patienten_info', self.layout.drop_down_krankenhaus.selected_value)
        for d in return_value:
          d["krankenhausname"] = self.layout.drop_down_krankenhaus.selected_value
        self.repeating_panel_patient.items = return_value
        self.unfiltered_rows = return_value  
        self.filter_data_grid()
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
    self.filter_data_grid()
  
  def filter_data_grid(self):
    if self.text_box_patientenID.text.isnumeric() or self.text_box_patientenID.text == "":
      self.text_box_patientenID.background = app.theme_colors["Surface Variant"]
    elif not self.text_box_patientenID.text.isnumeric():
      self.text_box_patientenID.background = app.theme_colors["Error"]
      return

    rows = []
    current_filter = self.export_filters()
    
    for item in self.unfiltered_rows:
      item["filter"] = current_filter
      if (self.text_box_patientenID.text in str(item["patient_id"])) and (self.text_box_patientenname.text.lower() in item["name"].lower()):
        rows.append(item)

    self.repeating_panel_patient.items = rows
    

  @handle("text_box_patientenname", "change")
  def text_box_patientenname_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.filter_data_grid()

  @handle("radio_button_krankenhaus", "clicked")
  def radio_button_krankenhaus_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    self.drop_down_krankenhaus_has_changed()
    self.layout.drop_down_krankenhaus.enabled = True

  @handle("radio_button_alle", "clicked")
  def radio_button_alle_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    return_value = anvil.server.call('get_patienten_info_alle_krankenhaueser', self.layout.drop_down_krankenhaus.selected_value)
    for d in return_value:
      d["krankenhausname"] = self.layout.drop_down_krankenhaus.selected_value
    self.repeating_panel_patient.items = return_value
    self.unfiltered_rows = return_value
    self.filter_data_grid()
    self.layout.drop_down_krankenhaus.enabled = False

  def export_filters(self):
    current_filters = []
    current_filters.append(self.radio_button_alle.get_group_value())
    current_filters.append(self.text_box_patientenID.text)
    current_filters.append(self.text_box_patientenname.text)
    return current_filters

  def import_filters(self, filters):
    print(filters)
    if filters[0] == "all":
      self.radio_button_alle.selected = True
    else:
      self.radio_button_krankenhaus.selected = True
    self.text_box_patientenID.text = filters[1]
    self.text_box_patientenname.text = filters[2]