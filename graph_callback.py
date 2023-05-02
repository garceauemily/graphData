import abc
import csv
from typing import Union, Optional, TextIO

import globals
from genki_wave.data import ButtonEvent, DataPackage

class WaveCallback(abc.ABC):
    @abc.abstractmethod
    def _button_handler(self, data: ButtonEvent) -> None:
        pass

    @abc.abstractmethod
    def _data_handler(self, data: DataPackage) -> None:
        pass

    def __call__(self, data: Union[ButtonEvent, DataPackage]) -> None:
        if isinstance(data, ButtonEvent):
            self._button_handler(data)
        elif isinstance(data, DataPackage):
            self._data_handler(data)
        else:
            raise ValueError(f"Got data of unexpected type {type(data)}")

class PlotData(WaveCallback):
    """
    Callback that prints out all button presses received and prints a data package every `print_data_every_n_seconds`
    seconds. Useful for debugging and testing.

    Args:
        print_data_every_n_seconds: The interval to print a data package
    """

    def __init__(self, print_data_every_n_seconds: Optional[float] = None):
        self._last_time = None
        self._print_data_every_n_seconds = print_data_every_n_seconds

    def _button_handler(self, data: ButtonEvent) -> None:
        # We use `str` to force the `enum` to print the long version of the name e.g. `ButtonId.MIDDLE` instead of `1`
        print(f"Button: {str(data.button_id)}, Action: {str(data.action)}")

    def _data_handler(self, data: DataPackage) -> None:
        """If there are more than `_print_data_every_n_seconds` seconds since something was printed out, print it"""
        if self._print_data_every_n_seconds is None:
            return

        if self._last_time is None:
            self._last_time = data.timestamp_us
            print(f'Printing to \'properties.csv\'...')

        if (data.timestamp_us - self._last_time) > self._print_data_every_n_seconds * 10**6:  # s to us
            file1=open('properties.csv','a') #write/append data to this file
            writer = csv.writer(file1)
            # indexing from 'live.gnu' applies to the elements in row
            row = [globals.count, data.timestamp_us, data.euler.roll, data.euler.pitch, data.euler.yaw, data.gyro.x, data.gyro.y, data.gyro.z, data.acc.x, data.acc.y, data.acc.z, data.mag.x, data.mag.y, data.mag.z, data.raw_pose.w, data.raw_pose.x, data.raw_pose.y, data.raw_pose.z, data.current_pose.w, data.current_pose.x, data.current_pose.y, data.current_pose.z, data.linacc.x, data.linacc.y, data.linacc.z, data.grav.x, data.grav.y, data.grav.z, data.acc_glob.x, data.acc_glob.y, data.acc_glob.z, data.linacc_glob.x, data.linacc_glob.y, data.linacc_glob.z ]
            globals.count += 1
            writer.writerow(row)
            file1.close()
            self._last_time = data.timestamp_us
