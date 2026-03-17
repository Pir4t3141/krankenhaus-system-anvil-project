from ._anvil_designer import StationenUebersichtTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class StationenUebersicht(StationenUebersichtTemplate):
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
    self.layout.link_stationen.role = 'selected'
    self.drop_down_krankenhaus_has_changed()
    
  def drop_down_krankenhaus_has_changed(self, **event_args):
    """This method is called when the drop down element has changed"""
    try:
      if len(self.layout.drop_down_krankenhaus.items) > 0 and self.layout.link_stationen.role == 'selected':
        return_value = anvil.server.call('get_station_info', self.layout.drop_down_krankenhaus.selected_value)
        for d in return_value:
          d["krankenhausname"] = self.layout.drop_down_krankenhaus.selected_value
        self.repeating_panel_stationeninfo.items = return_value
    finally:
      pass

  @handle("plot_personalverteilung", "show")
  def plot_personalverteilung_show(self, **event_args):
    """This method is called when the Plot is shown on the screen"""
    krankenhausname = self.layout.drop_down_krankenhaus.selected_value
    print(krankenhausname)
    return_values = anvil.server.call('get_count_of_artz_and_betreuer', krankenhausname)
    print(return_values)

    stationen = [d['bezeichnung'] for d in return_values]
    aerzte = [d['anzahl_aerzte'] for d in return_values]
    betreuer = [d['anzahl_betreuer'] for d in return_values]
    
    fig = go.Figure(data=[
      go.Bar(name='Ärzte', x=stationen, y=aerzte),
      go.Bar(name='Betreuer', x=stationen, y=betreuer)
    ])
    fig.update_layout(barmode='stack', title = 'Personalverteilung', xaxis_title="Station", yaxis_title="Personal Anzahl", legend_title="Personalart")
    
    self.plot_personalverteilung.figure = fig
