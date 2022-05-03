import matplotlib.pyplot as plt
import numpy as np


class Model(object):

    def __init__(self,storage_current_hour,dutycycle):
        self.solar_cell_voltage = 3.35
        self.solar_cell_current = 46.7 * 10 ** (-3)
        self.temp_sensor_idle_consumption = 0.2 * (10) ** (-6)
        self.temp_sensor_active_consumption = 0.22 * (10) ** (-6)
        self.Lora_active_voltage = 3.7
        self.Lora_active_current = 24 * 10 ** (-3)
        self.mcu_idle_consumpution = 0.7182 * (10) ** (-6)
        self.mcu_active_consumpution = 1.386 * (10) ** (-6)
        self.storage_voltage = 1.2
        self.storage_current_hour = storage_current_hour
        self.rainy_active_percent = dutycycle
        self.rainy_idle_percent =1-dutycycle
        self.x_model = np.arange(1, 12, 0.001)  # start,stop,step
        self.y_model = (np.sin(self.x_model - 4 * np.pi / 5) + 3) * 10

    def calculate(self,x):
        return (np.sin(x - 4 * np.pi / 5) + 3) * 10

    def getchargingtime(self,storage_current_hour,solar_cell_current):
        return storage_current_hour * (10) ** 3 * 1.2 / ((0.8 * solar_cell_current*1000) * 8) * 1.5

    def getlowerbound(self):
        time=self.getchargingtime(self.storage_current_hour,self.solar_cell_current)
        delta = time / (30 * 2)
        x1 = 2.3 * np.pi - delta
        x2 = 2.3 * np.pi + delta
        y = self.calculate(x1)
        return (x1, x2, y)

    def drawlowerbound(self):
        draw = self.getlowerbound()[2] + 0 * self.x_model
        plt.plot(self.x_model,self.y_model)
        plt.plot(self.x_model, draw)
        plt.text(3,self.getlowerbound()[2],'{:.4f}%'.format(self.getlowerbound()[2]),fontdict={'size':'10'})
        plt.title('The Sunny Value \n(Battery:{}Ah, Rainy_Duty_Cycle:{})'.format(self.storage_current_hour,self.rainy_active_percent))
        plt.xlabel(u'Month')
        plt.ylabel(u'Precipitation %')
        plt.show()

    def calculatepower(self,x):
        return (self.storage_voltage * self.storage_current_hour * 3600) + (
                0.3 * 0.1 * (self.solar_cell_voltage * self.solar_cell_current) - (
                self.temp_sensor_active_consumption * self.rainy_active_percent + self.temp_sensor_idle_consumption * self.rainy_idle_percent) - (
                        self.Lora_active_voltage * self.Lora_active_current * self.rainy_active_percent) - (
                        self.mcu_active_consumpution * self.rainy_active_percent + self.mcu_idle_consumpution * self.rainy_idle_percent)) * 2 * abs(
            x - 1.3 * np.pi) * 30 * 24 * 3600


    def systempower(self):


        for x in np.arange(1.3 * np.pi, self.getlowerbound()[0], 0.001):

            if (self.storage_voltage * self.storage_current_hour * 3600) + (
                    0.3 * 0.1 * (self.solar_cell_voltage * self.solar_cell_current) - (
                    self.temp_sensor_active_consumption * self.rainy_active_percent + self.temp_sensor_idle_consumption * self.rainy_idle_percent) - (
                            self.Lora_active_voltage * self.Lora_active_current * self.rainy_active_percent) - (
                            self.mcu_active_consumpution * self.rainy_active_percent + self.mcu_idle_consumpution * self.rainy_idle_percent)) * 2 * abs(
                    x - 1.3 * np.pi) * 30 * 24 * 3600 <= 0:
                return x


    def drawsystempower(self):
        x = np.linspace(1.3 * np.pi, self.getlowerbound()[0],6)
        y = (self.storage_voltage * self.storage_current_hour * 3600) + (0.3 * 0.1 * (self.solar_cell_voltage * self.solar_cell_current) - (
                    self.temp_sensor_active_consumption * self.rainy_active_percent + self.temp_sensor_idle_consumption * self.rainy_idle_percent) - (
                                                                           self.Lora_active_voltage * self.Lora_active_current * self.rainy_active_percent) - (
                                                                           self.mcu_active_consumpution * self.rainy_active_percent + self.mcu_idle_consumpution * self.rainy_idle_percent)) * 2 * abs(
            x- 1.3 * np.pi) * 30 * 24 * 3600
        y_base = 0 * x
        x_labels = ['{:.3f}'.format(self.calculate(i)) for i in x]
        plt.xticks(np.linspace(1.3 * np.pi, self.getlowerbound()[0],6), x_labels)

        plt.plot(x, y)
        plt.plot(x, y_base)
        plt.text(self.systempower(), 0, '{:.4f}%'.format(self.calculate(self.systempower())),
                 fontdict={'size': '10'})
        plt.xlabel(u'Precipitation %')
        plt.ylabel(u'System Total Energy J')
        plt.title('Relation of system total energy and precipitation \n(Battery:{}Ah, Rainy_Duty_Cycle:{})'.format(self.storage_current_hour,self.rainy_active_percent))
        plt.show()


    def getupperbound(self):
        y = self.calculate(self.systempower())
        return y

    def drawupperbound(self):

        draw = self.getupperbound() + 0 * self.x_model
        plt.plot(self.x_model, self.y_model)
        plt.plot(self.x_model, draw)
        plt.text(3, self.getupperbound(), '{:.4f}%'.format(self.getupperbound()),
                 fontdict={'size': '10'})
        plt.title('The Rainy Value  \n(Battery:{}Ah, Rainy_Duty_Cycle:{})'.format(self.storage_current_hour,self.rainy_active_percent))
        plt.xlabel(u'Month')
        plt.ylabel(u'Precipitation %')
        plt.show()

    def adaptivedutycycle(self):
        x = np.arange(self.getlowerbound()[2], self.getupperbound(), 0.001)
        k = (self.rainy_active_percent-0.9)/(self.getupperbound()-self.getlowerbound()[2])
        b=self.rainy_active_percent-k*self.getupperbound()
        y=k*x+b
        plt.plot(x,y)
        plt.text(self.getlowerbound()[2],0.9,'({0:.3f}%, {1})'.format(self.getlowerbound()[2],0.9))
        plt.text(self.getupperbound(), self.rainy_active_percent,
                 '({0:.3f}%, {1})'.format(self.getupperbound(), self.rainy_active_percent))

        plt.xlabel(u'Precipitation %')
        plt.ylabel(u'Duty Cycle')
        plt.title('Relation of Adaptive duty cycle and precipitation \n(Battery:{}Ah, Rainy_Duty_Cycle:{})'.format(self.storage_current_hour,self.rainy_active_percent))

        plt.show()

    def modelAssemble(self):
        drawlow = self.getlowerbound()[2] + 0 * self.x_model
        drawup = self.getupperbound() + 0 * self.x_model
        plt.plot(self.x_model, self.y_model)
        plt.plot(self.x_model, drawlow)
        plt.plot(self.x_model, drawup)
        plt.text(3, self.getlowerbound()[2], '{:.4f}%'.format(self.getlowerbound()[2]),
                 fontdict={'size': '10'})
        plt.text(3, self.getupperbound(), '{:.4f}%'.format(self.getupperbound()),
                 fontdict={'size': '10'})
        plt.xlabel(u'Month')
        plt.ylabel(u'Precipitation %')
        plt.title('The Sunny Value and Rainy Value \n(Battery:{}Ah, Rainy_Duty_Cycle:{})'.format(self.storage_current_hour,self.rainy_active_percent))
        plt.show()









