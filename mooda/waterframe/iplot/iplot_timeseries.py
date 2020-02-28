""" Implementation of WaterFrame.iplot_timeseries() """
import numpy as np
import plotly.graph_objects as go

def iplot_timeseries(self, parameters_to_plot=None):
    """
    It creates a Plotly figure with the time-series of the input parameters.
    
    Parameters
    ----------
        parameters_to_plot: str or list (optional, parameters_to_plot=None)
            Parameters to plot.

    Returns
    -------
        figure: dict
            Plotly figure dictionary
    """
    if parameters_to_plot is None:
        parameters_to_plot = self.parameters
    elif isinstance(parameters_to_plot, str):
        parameters_to_plot = [parameters_to_plot]

    # Extract data
    df = self.data[parameters_to_plot].dropna().reset_index()
    df = df.groupby(['DEPTH', 'TIME'])[parameters_to_plot].mean()
    df.reset_index(inplace=True)
    df.set_index('TIME', inplace=True)
    
    data = [go.Scatter(x=df.index, y=df[parameter], fill="tozeroy", name=parameter)
            for parameter in parameters_to_plot]

    # Layout
    y_label = None
    if len(parameters_to_plot) == 1:
        try:
            title = self.vocabulary[parameters_to_plot[0]]['long_name']
        except KeyError:
            title = parameters_to_plot[0]
        try:
            y_label = self.vocabulary[parameters_to_plot[0]]['units']
        except KeyError:
            pass
    else:
        title = "_".join(parameters_to_plot)
    min_value = None
    max_value = None
    for parameter in parameters_to_plot:

        _min = np.nanmin(self.data[parameters_to_plot])
        _max = np.nanmax(self.data[parameters_to_plot])

        if min_value is None or _min < min_value:
            min_value = _min

        if max_value is None or _max > max_value:
            max_value = _max

    layout = {
        'title': title,
        'yaxis': {
            'range': [min_value, max_value],
            'title': y_label
        },
        'margin': {'l': 50, 'r': 10, 't': 45, 'b': 30}
    }

    figure = {"data": data, "layout": layout}

    return figure
