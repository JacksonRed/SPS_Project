from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
class Draw3D:

    def draw3Dplot(self):
        solar_cell_voltage = 3.35
        solar_cell_current = 46.7 * 10 ** (-3)
        temp_sensor_idle_consumption = 0.2 * (10) ** (-6)
        temp_sensor_active_consumption = 0.22 * (10) ** (-6)
        Lora_active_voltage = 3.7
        Lora_active_current = 24 * 10 ** (-3)
        mcu_idle_consumpution = 0.7182 * (10) ** (-6)
        mcu_active_consumpution = 1.386 * (10) ** (-6)
        storage_voltage = 1.2
        rainy_active_percent = 0.25

        figure = plt.figure()
        axes = Axes3D(figure)

        Dutycycle = np.arange(0.2, 0.34, 0.05)
        Battery = np.arange(5, 14.5, 0.5)

        Dutycycle, Battery = np.meshgrid(Dutycycle, Battery)

        RainyVale = (np.sin(
            ((storage_voltage * Battery * 3600) / (-1 * (0.3 * 0.1 * (solar_cell_voltage * solar_cell_current) - (
                    temp_sensor_active_consumption * Dutycycle + temp_sensor_idle_consumption * (1 - Dutycycle)) - (
                                                                Lora_active_voltage * Lora_active_current * Dutycycle) - (
                                                                mcu_active_consumpution * rainy_active_percent + mcu_idle_consumpution * (
                                                                1 - Dutycycle))) * 2 * 30 * 24 * 3600) )+ 0.5 * np.pi) + 3) * 10  # z关于x,y的函数关系式,此处为锥面
        axes.plot_surface(Dutycycle, Battery, RainyVale, cmap='rainbow')


        axes.set_xlabel('Duty Cycle')
        axes.set_ylabel('Battery Size Ah \n (Battery voltage is always 1.2v)')
        axes.set_zlabel('Rainy Value %')

        plt.show()

