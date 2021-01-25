""" Implementation of mooda.widget_qc()"""
from typing import List
import ipywidgets as widgets
from IPython.display import clear_output
import mooda

def widget_emso(wf, depth_range: List[float]=[-10, 10000]):
    """
    It makes a Widget to download data from the EMSO API

    Parameters
    ----------
        wf: WaterFrame

    Returns
    -------
        main_box: ipwidgets.VBox
            Jupyter notebook widget 
    """

    # Sing in
    user_label = widgets.Label('User:')
    input_user = widgets.Text()
    password_label = widgets.Label('Password:')
    input_password = widgets.Text()

    # Platform code
    platform_label = widgets.Label('Platform code:')
    emso = mooda.EMSO()
    platform_codes = emso.get_info_platform_code()
    input_platform = widgets.Dropdown(options=platform_codes,
                                      value=platform_codes[0], disabled=False)

    # Parameters
    parameters_label = widgets.Label('Parameters (separated by commas):')
    input_parameters = widgets.Text()

    # Size
    size_label = widgets.Label('Size:')
    input_size = widgets.BoundedIntText(value=10, min=1, step=1)

    # Depth
    depth_label = widgets.Label('Depth:')
    input_depth = widgets.FloatRangeSlider(value=depth_range,
                                           min=depth_range[0],
                                           max=depth_range[1], step=0.1,
                                           disabled=False,
                                           continuous_update=False,
                                           orientation='horizontal',
                                           readout=True, readout_format='.1f')

    # Time
    start_date_label = widgets.Label('Start date:')
    input_start_date = widgets.DatePicker(disabled=False)
    end_date_label = widgets.Label('End date:')
    input_end_date = widgets.DatePicker(disabled=False)

    # Button
    button = widgets.Button(description='Get data')
    out = widgets.Output()
    def on_button_clicked(_):
        # "linking function with output"
        with out:
            # what happens when we press the button
            clear_output()
            if ',' in input_parameters.value:
                parameters = input_parameters.value.split(',').strip()
            else:
                parameters = [input_parameters.value]

            if input_start_date.value is None:
                start_time = ''
            else:
                start_time = input_start_date.value

            if input_end_date.value is None:
                end_time = ''
            else:
                end_time = input_end_date.value

            print('Downloading data, please wait')

            wf2 = mooda.from_emso(platform_code=input_platform.value,
                                 parameters=parameters, start_time=start_time,
                                 end_time=end_time,
                                 depth_min=input_depth.value[0],
                                 depth_max=input_depth.value[1],
                                 user=input_user.value,
                                 password=input_password.value,
                                 size=input_size.value)
            
            wf.data = wf2.data.copy()
            wf.metadata = wf2.metadata.copy()

            clear_output()
            print('Done')
            print(wf)

    # linking button and function together using a button's method
    button.on_click(on_button_clicked)

    user_box = widgets.HBox([user_label, input_user, password_label,
                             input_password])
    platform_box = widgets.HBox([platform_label, input_platform])
    parameters_box = widgets.HBox([parameters_label, input_parameters])
    size_box = widgets.HBox([size_label, input_size])
    depth_box = widgets.HBox([depth_label, input_depth])
    start_date_box = widgets.HBox([start_date_label, input_start_date])
    end_date_box = widgets.HBox([end_date_label, input_end_date])

    main_box = widgets.VBox([user_box, platform_box, parameters_box, size_box,
                             depth_box, start_date_box, end_date_box, button,
                             out])

    return main_box