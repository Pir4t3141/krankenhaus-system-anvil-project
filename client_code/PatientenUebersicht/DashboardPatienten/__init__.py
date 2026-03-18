from ._anvil_designer import DashboardPatientenTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DashboardPatienten(DashboardPatientenTemplate):
  row_dict = None

  def __init__(self, row_dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.label_patient.text = (
      f"{row_dict['krankenhausname']} | {row_dict['name']}"
    )
    self.row_dict = row_dict

  @handle("link_patientenUebersicht", "click")
  def link_patientenUebersicht_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("PatientenUebersicht", self.row_dict["krankenhausname"])

  @handle("data_grid_diagnose", "show")
  def data_grid_diagnose_show(self, **event_args):
    """This method is called when the data grid is shown on the screen"""
    return_values = anvil.server.call('get_patienten_diagnosis', self.row_dict["patient_id"])
    self.repeating_panel_diagnose.items = return_values
