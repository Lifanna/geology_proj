import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patheffects
import matplotlib.ticker as ticker
import seaborn as sns
import os
import math
from PIL import Image
from cycler import cycler
import io


#читаем таблиц из файлов
def generate_mine():
    material_df = pd.read_csv('main/services/materials_db.csv')
    slice_data = pd.read_csv('main/services/slice_data.csv')

    types_df = pd.DataFrame(columns=['prs', 'torfa', 'rud_plast', 'plotik'])

    project_layers = [19, 8, 23, 1, 3, 11]


    for i in range(0, 9):

        temp = slice_data['full_layers'][i]

        lst = [float(x) for x in temp.strip('[]').split(',')]
        slice_data['full_layers'][i] = lst


    for i in range(0, 9):

        temp = slice_data['layers_power'][i]

        lst = [float(x) for x in temp.strip('[]').split(',')]
        slice_data['layers_power'][i] = lst


    for i in range(0, 9):

        temp = slice_data['layers_id'][i]

        lst = [int(x) for x in temp.strip('[]').split(',')]
        slice_data['layers_id'][i] = lst


    #генератор слоёв для скважин

    def layer_generator(power, layer_id, project_layers=None):
        
        c = dict(zip(layer_id, power))
        out_layer = []
        
        for item in project_layers:
            temp = c.get(item, 0)
            out_layer.append(temp)
            
        return out_layer


    #здесь считаем расстояние на плоскости между скважинами

    def step_calculator(x, y):
        

        x0 = 0
        y0 = 0
        shift_list=[]
        row_list=[]
        
        
        for step in range(0, slice_data.shape[0]):
            shift = round(((x[step]-x0)**2 + (y[step]-y0)**2)**0.5, 1)
            shift_list.append(shift)
            row_list.append(round(shift))
            x0, y0 = x[step], y[step]
            
        shift_list[0]=0
        row_list[0]=0
        
        
        step = []
        stack = 0
        for item in shift_list:
            
            
            stack+=item
            step.append(stack)


        return step, row_list


    #генерируем таблицу толщин слоёв

    def layers_power_generator():
        layers = pd.DataFrame()
        for i in range(0, len(project_layers)):                         
            sld = []
            for j in range(0, slice_data.shape[0]):
                sld.append(slice_data['full_layers'][j][i])
            layers[i] = sld
        

        return layers


    short_elem = list(material_df['short'])


    #собираем данные о отметке и глубине реальных скважин для таблицы

    true_z_raw = list(slice_data['z'])
    true_z = []
    for el in true_z_raw:
        true_z.append(round((el),1))

        
    deep_raw = list(slice_data['layers_power'])
    deep = []
    for el in deep_raw:    
        deep.append(sum(el))


    #вычисляем расстояние между скважинами и выводим количество шагов
    step, table_step = step_calculator(slice_data['x'], slice_data['y'])
    layers = layers_power_generator()



    #делаем сортировку по номеру скважины и обновляем индексы строк, тк они сбиваются после сортировки

    slice_data = slice_data.sort_values(by='number')
    slice_data.reset_index(drop= True, inplace= True)



    #считаем сумму толщин слоёв
    summ_slice_power = []

    for data in slice_data['full_layers']:
        summ_slice_power.append(sum(data))
        
    #считаем сумму нулевой уровень (виртуальный слой от 0 до фактического уровня, от которого известен состав и будем складывать стек слоёв вверх

    zero_level=[]
    for i in range(0,slice_data.shape[0]):
        #print(slice_data.iloc[i][3])
        zero_level.append(slice_data.iloc[i][3]-summ_slice_power[i]-2)
        


    step, nodata = step_calculator(slice_data['x'], slice_data['y'])

    layers = layers_power_generator()


    ###
    #отображение графика
    print('image=')

    stack = [zero_level]

    for item in range((len(project_layers)-1),0-1, -1):
        stack.append(list(layers[item]))
        

    y = np.vstack(stack)
    
    #цвета линий
    color_map = ['#ffffff']
    for code in project_layers[::-1]:
        color_map.append(material_df['color'][code])


    #вызываем и задаём размер
    fig, ax = plt.subplots()
    fig.set_size_inches(45, 15)


    #отрисовываем графики
    all_stack = ax.stackplot(step, y,
                labels=layers.keys(),colors=color_map, alpha=0.8)

        
    #легенда
    #ax.legend(loc='best')
    river = 'Ручей Чёрный'
    nam = '44-2022'
    titl = 'Схематический геологический разрез ПЛ '+str(nam) + '\n'+ 'Долина ' + str(river)
    ax.set_title(titl)

    plt.xlim(min(step)-10, max(step)+10) 
    plt.ylim(slice_data['z'].min()-max(summ_slice_power)-2, slice_data['z'].max()+2)
    plt.xticks([])  #убираем разметку по Х

    # Светлые рамки 
    plt.gca().spines["top"].set_alpha(0)
    plt.gca().spines["bottom"].set_alpha(0)
    plt.gca().spines["right"].set_alpha(0)
    plt.gca().spines["left"].set_alpha(.3)


    #сохраняем изображение как svg

    out_image_file = 'media/Cross_section_out' + str(nam) + '.svg'
    plt.savefig(out_image_file, format="svg")
    #выводим изображение

    # plt.show()

    return out_image_file