from typing import Dict, ClassVar
from qcodes.instrument_drivers.Lakeshore.lakeshore_base import (
    LakeshoreBase, BaseOutput)
from qcodes.instrument.group_parameter import GroupParameter, Group
import qcodes.utils.validators as vals

class Output_372(BaseOutput):
    # Probably Mypy bug
    # should have been fixed in https://github.com/python/mypy/issues/4715
    MODES: ClassVar[Dict[str, int]] = {
        'off': 0,
        'monitor_out': 1,
        'open_loop': 2,
        'zone': 3,
        'still': 4,
        'closed_loop': 5,
        'warm_up': 6}
    POLARITIES: ClassVar[Dict[str, int]] = {
        'unipolar': 0,
        'bipolar': 1}
    RANGES: ClassVar[Dict[str, int]] = {
        'off': 0,
        '31.6μA': 1,
        '100μA': 2,
        '316μA': 3,
        '1mA': 4,
        '3.16mA': 5,
        '10mA': 6,
        '31.6mA': 7,
        '100mA': 8}


    def __init__(self, parent, output_name, output_index) -> None:
        super().__init__(parent, output_name, output_index)

        # Add more parameters for OUTMODE command 
        # and redefine the corresponding group
        self.add_parameter('polarity',
                           val_mapping=self.POLARITIES,
                           parameter_class=GroupParameter)
        self.add_parameter('use_filter',
                           val_mapping={True: 1, False: 0},
                           parameter_class=GroupParameter)
        self.add_parameter('delay', vals=vals.Ints(0, 255),
                           get_parser=int,
                           parameter_class=GroupParameter)
        self.output_group = Group([self.mode, self.input_channel,
                                  self.powerup_enable, self.polarity,
                                  self.use_filter, self.delay],
                                  set_cmd=f'OUTMODE {output_index}, {{mode}}, '
                                          f'{{input_channel}}, '
                                          f'{{powerup_enable}}, {{polarity}}, '
                                          f'{{use_filter}}, {{delay}}',
                                  get_cmd=f'OUTMODE? {output_index}')


class Model_372(LakeshoreBase):
    """
    Lakeshore Model 372 Temperature Controller Driver

    Note that interaction with the control input (referred to as 'A' in the 
    Computer Interface Operation section of the manual) is not implemented.
    """
    channel_name_command: Dict[str, str] = {'ch{:02}'.format(i): str(i) for i in range(1, 17)}

    def __init__(self, name: str, address: str, **kwargs) -> None:
        super().__init__(name, address, **kwargs)
        self.sample_heater = Output_372(self, 'sample_heater', 0)
        self.warmup_heater = Output_372(self, 'warmup_heater', 1)
        self.analog_heater = Output_372(self, 'analog_heater', 2)
