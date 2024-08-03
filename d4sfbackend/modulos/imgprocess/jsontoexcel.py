import pandas as pd
import xlsxwriter
from django.conf import settings


def json2xlsx(json_file, xlsx_file, capa, tipo=0):
    names = 'Fechas/Date'
    graficosname = 'Gráfico por fechas/Chart by dates'
    if tipo == 2:
        names = 'Nombre/Name'
        graficosname = 'Gráfico por Parcelas/Chart by Parcels'
    workbook = xlsxwriter.Workbook(settings.PARCEL_FOLDER + xlsx_file)
    worksheet = workbook.add_worksheet('Porcentaje')
    worksheet2 = workbook.add_worksheet('Hectáreas')
    pj = pd.read_json(settings.PARCEL_FOLDER + json_file)
    bold = workbook.add_format({'bold': 1})
    #
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 1})

    header_format_ra = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#fe0103',
        'border': 1})
    header_format_rm = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#9b0004',
        'border': 1})
    header_format_rb = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#680000',
        'border': 1})

    header_format_aa = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#ffff33',
        'border': 1})
    header_format_am = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#cccc33',
        'border': 1})
    header_format_ab = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#666600',
        'border': 1})

    header_format_az_a = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#33ffff',
        'border': 1})
    header_format_az_m = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#33cccc',
        'border': 1})
    header_format_az_b = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#006666',
        'border': 1})

    header_format_va = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#33ff33',
        'border': 1})
    header_format_vm = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#33cc33',
        'border': 1})

    header_format_naranga = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#ff8000',
        'border': 1})
    header_format_amarillo = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#ffdf00',
        'border': 1})
    header_format_verde = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#66ff98',
        'border': 1})
    header_format_azul_claro = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#02fefc',
        'border': 1})
    header_format_azul_medio = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#0087ff',
        'border': 1})
    header_format_azul_oscuro = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#2000ff',
        'border': 1})
    #
    if capa == 'NDVI':
        worksheet.write_string(0, 0, "", header_format)
        worksheet.merge_range(1, 0, 1, 14,
                              "Todos los valores son porcentajes entre 0% - 100% - All values ​​are NpEncoder.percentages "
                              "between 0% - 100%",
                              header_format)
        worksheet.write_string(3, 0, names, header_format)
        worksheet.write_string(3, 1, "Rojo Alto", header_format_ra)
        worksheet.write_string(3, 2, "Rojo Medio", header_format_rm)
        worksheet.write_string(3, 3, "Rojo Bajo", header_format_rb)

        worksheet.write_string(3, 5, "Amarillo Alto", header_format_aa)
        worksheet.write_string(3, 6, "Amarillo Medio", header_format_am)
        worksheet.write_string(3, 7, "Amarillo Bajo", header_format_ab)

        worksheet.write_string(3, 9, "Azul Alto", header_format_az_a)
        worksheet.write_string(3, 10, "Azul Medio", header_format_az_m)
        worksheet.write_string(3, 11, "Azul Bajo", header_format_az_b)

        worksheet.write_string(3, 13, "Verde Alto", header_format_va)
        worksheet.write_string(3, 14, "Verde Medio", header_format_vm)
        # Segunda pag
        worksheet2.write_string(0, 0, "", header_format)
        worksheet2.merge_range(1, 0, 1, 14, "Los datos son en número de hectáreas - The data are in number of hectares",
                               header_format)
        worksheet2.write_string(3, 0, names, header_format)
        worksheet2.write_string(3, 1, "Rojo Alto", header_format_ra)
        worksheet2.write_string(3, 2, "Rojo Medio", header_format_rm)
        worksheet2.write_string(3, 3, "Rojo Bajo", header_format_rb)

        worksheet2.write_string(3, 5, "Amarillo Alto", header_format_aa)
        worksheet2.write_string(3, 6, "Amarillo Medio", header_format_am)
        worksheet2.write_string(3, 7, "Amarillo Bajo", header_format_ab)

        worksheet2.write_string(3, 9, "Azul Alto", header_format_az_a)
        worksheet2.write_string(3, 10, "Azul Medio", header_format_az_m)
        worksheet2.write_string(3, 11, "Azul Bajo", header_format_az_b)

        worksheet2.write_string(3, 13, "Verde Alto", header_format_va)
        worksheet2.write_string(3, 14, "Verde Medio", header_format_vm)
        col = 0
        for item in pj:
            worksheet.write_string(item + 4, col, pj[item]['fecha'], bold)
            worksheet.write_number(item + 4, col + 1, float(pj[item]['rojos']['altos']['porcent']))
            worksheet.write_number(item + 4, col + 2, float(pj[item]['rojos']['medios']['porcent']))
            worksheet.write_number(item + 4, col + 3, float(pj[item]['rojos']['bajos']['porcent']))

            worksheet.write_number(item + 4, col + 5, float(pj[item]['amarillos']['altos']['porcent']))
            worksheet.write_number(item + 4, col + 6, float(pj[item]['amarillos']['medios']['porcent']))
            worksheet.write_number(item + 4, col + 7, float(pj[item]['amarillos']['bajos']['porcent']))

            worksheet.write_number(item + 4, col + 9, float(pj[item]['azules']['altos']['porcent']))
            worksheet.write_number(item + 4, col + 10, float(pj[item]['azules']['medios']['porcent']))
            worksheet.write_number(item + 4, col + 11, float(pj[item]['azules']['bajos']['porcent']))

            worksheet.write_number(item + 4, col + 13, float(pj[item]['verdes']['altos']['porcent']))
            worksheet.write_number(item + 4, col + 14, float(pj[item]['verdes']['medios']['porcent']))
            # pag 2
            worksheet2.write_string(item + 4, col, pj[item]['fecha'], bold)
            worksheet2.write_number(item + 4, col + 1, float(pj[item]['rojos']['altos']['area_porcent']))
            worksheet2.write_number(item + 4, col + 2, float(pj[item]['rojos']['medios']['area_porcent']))
            worksheet2.write_number(item + 4, col + 3, float(pj[item]['rojos']['bajos']['area_porcent']))

            worksheet2.write_number(item + 4, col + 5, float(pj[item]['amarillos']['altos']['area_porcent']))
            worksheet2.write_number(item + 4, col + 6, float(pj[item]['amarillos']['medios']['area_porcent']))
            worksheet2.write_number(item + 4, col + 7, float(pj[item]['amarillos']['bajos']['area_porcent']))

            worksheet2.write_number(item + 4, col + 9, float(pj[item]['azules']['altos']['area_porcent']))
            worksheet2.write_number(item + 4, col + 10, float(pj[item]['azules']['medios']['area_porcent']))
            worksheet2.write_number(item + 4, col + 11, float(pj[item]['azules']['bajos']['area_porcent']))

            worksheet2.write_number(item + 4, col + 13, float(pj[item]['verdes']['altos']['area_porcent']))
            worksheet2.write_number(item + 4, col + 14, float(pj[item]['verdes']['medios']['area_porcent']))
        col = -1
        for item in pj:
            worksheet.write_string(pj.columns.size + 2 + 9, col + 1, pj[item]['fecha'], header_format)
            worksheet.insert_image(pj.columns.size + 2 + 12, col + 1, settings.PARCEL_FOLDER + str(pj[item]['img']),
                                   {'x_scale': 0.03, 'y_scale': 0.03})
            # pag 2
            worksheet2.write_string(pj.columns.size + 2 + 9, col + 1, pj[item]['fecha'], header_format)
            worksheet2.insert_image(pj.columns.size + 2 + 12, col + 1, settings.PARCEL_FOLDER + str(pj[item]['img']),
                                    {'x_scale': 0.03, 'y_scale': 0.03})
            col += 1

        chart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
        chart.add_series({'name': '=Porcentaje!$B$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$B$5:$B$' + str(pj.columns.size + 4), 'fill': {'color': '#fe0103'}})
        chart.add_series({'name': '=Porcentaje!$C$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$C$5:$C$' + str(pj.columns.size + 4), 'fill': {'color': '#9b0004'}})
        chart.add_series({'name': '=Porcentaje!$D$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$D$5:$D$' + str(pj.columns.size + 4), 'fill': {'color': '#680000'}})

        chart.add_series({'name': '=Porcentaje!$F$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$F$5:$F$' + str(pj.columns.size + 4), 'fill': {'color': '#ffff33'}})
        chart.add_series({'name': '=Porcentaje!$G$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$G$5:$G$' + str(pj.columns.size + 4), 'fill': {'color': '#cccc33'}})
        chart.add_series({'name': '=Porcentaje!$H$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$H$5:$H$' + str(pj.columns.size + 4), 'fill': {'color': '#666600'}})

        chart.add_series({'name': '=Porcentaje!$J$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$J$5:$J$' + str(pj.columns.size + 4), 'fill': {'color': '#33ffff'}})
        chart.add_series({'name': '=Porcentaje!$K$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$K$5:$K$' + str(pj.columns.size + 4), 'fill': {'color': '#33cccc'}})
        chart.add_series({'name': '=Porcentaje!$L$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$L$5:$L$' + str(pj.columns.size + 4), 'fill': {'color': '#006666'}})

        chart.add_series({'name': '=Porcentaje!$N$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$N$5:$N$' + str(pj.columns.size + 4), 'fill': {'color': '#33ff33'}})
        chart.add_series({'name': '=Porcentaje!$O$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$O$5:$O$' + str(pj.columns.size + 4), 'fill': {'color': '#33cc33'}})

        chart.set_title({'name': graficosname})
        chart.set_x_axis({'name': names})
        chart.set_y_axis({'name': 'Porcentaje de color/Color NpEncoder.percentage'})
        chart.set_size({'x_scale': 3, 'y_scale': 1.5})
        worksheet.insert_chart('Q1', chart)
        # pag 2
        chart2 = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
        chart2.add_series({'name': '=Hectáreas!$B$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$B$5:$B$' + str(pj.columns.size + 4), 'fill': {'color': '#fe0103'}})
        chart2.add_series({'name': '=Hectáreas!$C$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$C$5:$C$' + str(pj.columns.size + 4), 'fill': {'color': '#9b0004'}})
        chart2.add_series({'name': '=Hectáreas!$D$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$D$5:$D$' + str(pj.columns.size + 4), 'fill': {'color': '#680000'}})

        chart2.add_series({'name': '=Hectáreas!$F$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$F$5:$F$' + str(pj.columns.size + 4), 'fill': {'color': '#ffff33'}})
        chart2.add_series({'name': '=Hectáreas!$G$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$G$5:$G$' + str(pj.columns.size + 4), 'fill': {'color': '#cccc33'}})
        chart2.add_series({'name': '=Hectáreas!$H$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$H$5:$H$' + str(pj.columns.size + 4), 'fill': {'color': '#666600'}})

        chart2.add_series({'name': '=Hectáreas!$J$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$J$5:$J$' + str(pj.columns.size + 4), 'fill': {'color': '#33ffff'}})
        chart2.add_series({'name': '=Hectáreas!$K$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$K$5:$K$' + str(pj.columns.size + 4), 'fill': {'color': '#33cccc'}})
        chart2.add_series({'name': '=Hectáreas!$L$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$L$5:$L$' + str(pj.columns.size + 4), 'fill': {'color': '#006666'}})

        chart2.add_series({'name': '=Hectáreas!$N$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$N$5:$N$' + str(pj.columns.size + 4), 'fill': {'color': '#33ff33'}})
        chart2.add_series({'name': '=Hectáreas!$O$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$O$5:$O$' + str(pj.columns.size + 4), 'fill': {'color': '#33cc33'}})

        chart2.set_title({'name': graficosname})
        chart2.set_x_axis({'name': names})
        chart2.set_y_axis({'name': 'Color'})
        chart2.set_size({'x_scale': 3, 'y_scale': 1.5})
        worksheet2.insert_chart('Q1', chart2)

        workbook.close()
    elif capa == 'MOISTURE_INDEX':
        worksheet.write_string(0, 0, "", header_format)
        worksheet.merge_range(1, 0, 1, 14,
                              "Todos los valores son porcentajes entre 0% - 100% - All values ​​are NpEncoder.percentages "
                              "between 0% - 100%",
                              header_format)
        worksheet.write_string(3, 0, names, header_format)

        worksheet.write_string(3, 1, "Rojo/Naranja", header_format_naranga)
        worksheet.write_string(3, 2, "Amarillo", header_format_amarillo)
        worksheet.write_string(3, 3, "Verde", header_format_verde)
        worksheet.write_string(3, 4, "Azul Claro", header_format_azul_claro)
        worksheet.write_string(3, 5, "Azul Medio", header_format_azul_medio)
        worksheet.write_string(3, 6, "Azul Oscuro", header_format_azul_oscuro)

        # pag 2
        worksheet2.write_string(0, 0, "", header_format)
        worksheet2.merge_range(1, 0, 1, 14, "Los datos son en número de hectáreas - The data are in number of hectares",
                               header_format)
        worksheet2.write_string(3, 0, names, header_format)

        worksheet2.write_string(3, 1, "Rojo/Naranja", header_format_naranga)
        worksheet2.write_string(3, 2, "Amarillo", header_format_amarillo)
        worksheet2.write_string(3, 3, "Verde", header_format_verde)
        worksheet2.write_string(3, 4, "Azul Claro", header_format_azul_claro)
        worksheet2.write_string(3, 5, "Azul Medio", header_format_azul_medio)
        worksheet2.write_string(3, 6, "Azul Oscuro", header_format_azul_oscuro)
        col = 0
        for item in pj:
            worksheet.write_string(item + 4, col, pj[item]['fecha'], bold)
            worksheet.write_number(item + 4, col + 1, float(pj[item]['naranja']['porcent']))
            worksheet.write_number(item + 4, col + 2, float(pj[item]['amarillo']['porcent']))
            worksheet.write_number(item + 4, col + 3, float(pj[item]['verdes']['porcent']))
            worksheet.write_number(item + 4, col + 4, float(pj[item]['azul_claro']['porcent']))
            worksheet.write_number(item + 4, col + 5, float(pj[item]['azul_medio']['porcent']))
            worksheet.write_number(item + 4, col + 6, float(pj[item]['azul_oscuro']['porcent']))
            # pag 2
            worksheet2.write_string(item + 4, col, pj[item]['fecha'], bold)
            worksheet2.write_number(item + 4, col + 1, float(pj[item]['naranja']['area_porcent']))
            worksheet2.write_number(item + 4, col + 2, float(pj[item]['amarillo']['area_porcent']))
            worksheet2.write_number(item + 4, col + 3, float(pj[item]['verdes']['area_porcent']))
            worksheet2.write_number(item + 4, col + 4, float(pj[item]['azul_claro']['area_porcent']))
            worksheet2.write_number(item + 4, col + 5, float(pj[item]['azul_medio']['area_porcent']))
            worksheet2.write_number(item + 4, col + 6, float(pj[item]['azul_oscuro']['area_porcent']))
        col = -1
        for item in pj:
            worksheet.write_string(pj.columns.size + 2 + 9, col + 1, pj[item]['fecha'], header_format)
            worksheet.insert_image(pj.columns.size + 2 + 12, col + 1, settings.PARCEL_FOLDER + str(pj[item]['img']),
                                   {'x_scale': 0.03, 'y_scale': 0.03})
            # pag 2
            worksheet2.write_string(pj.columns.size + 2 + 9, col + 1, pj[item]['fecha'], header_format)
            worksheet2.insert_image(pj.columns.size + 2 + 12, col + 1, settings.PARCEL_FOLDER + str(pj[item]['img']),
                                    {'x_scale': 0.03, 'y_scale': 0.03})
            col += 1

        chart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
        chart.add_series({'name': '=Porcentaje!$B$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$B$5:$B$' + str(pj.columns.size + 4), 'fill': {'color': '#ff8000'}})
        chart.add_series({'name': '=Porcentaje!$C$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$C$5:$C$' + str(pj.columns.size + 4), 'fill': {'color': '#ffdf00'}})
        chart.add_series({'name': '=Porcentaje!$D$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$D$5:$D$' + str(pj.columns.size + 4), 'fill': {'color': '#66ff98'}})
        chart.add_series({'name': '=Porcentaje!$E$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$E$5:$E$' + str(pj.columns.size + 4), 'fill': {'color': '#02fefc'}})
        chart.add_series({'name': '=Porcentaje!$F$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$F$5:$F$' + str(pj.columns.size + 4), 'fill': {'color': '#0049d5'}})
        chart.add_series({'name': '=Porcentaje!$G$4', 'categories': '=Porcentaje!$A$5:$A$' + str(pj.columns.size + 4),
                          'values': '=Porcentaje!$G$5:$G$' + str(pj.columns.size + 4), 'fill': {'color': '#2000ff'}})

        chart.set_title({'name': graficosname})
        chart.set_x_axis({'name': names})
        chart.set_y_axis({'name': 'Porcentaje de color/Color NpEncoder.percentage'})
        chart.set_size({'x_scale': 3, 'y_scale': 1.5})
        worksheet.insert_chart('Q1', chart)
        # pag 2
        chart2 = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
        chart2.add_series({'name': '=Hectáreas!$B$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$B$5:$B$' + str(pj.columns.size + 4), 'fill': {'color': '#ff8000'}})
        chart2.add_series({'name': '=Hectáreas!$C$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$C$5:$C$' + str(pj.columns.size + 4), 'fill': {'color': '#ffdf00'}})
        chart2.add_series({'name': '=Hectáreas!$D$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$D$5:$D$' + str(pj.columns.size + 4), 'fill': {'color': '#66ff98'}})
        chart2.add_series({'name': '=Hectáreas!$E$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$E$5:$E$' + str(pj.columns.size + 4), 'fill': {'color': '#02fefc'}})
        chart2.add_series({'name': '=Hectáreas!$F$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$F$5:$F$' + str(pj.columns.size + 4), 'fill': {'color': '#0049d5'}})
        chart2.add_series({'name': '=Hectáreas!$G$4', 'categories': '=Hectáreas!$A$5:$A$' + str(pj.columns.size + 4),
                           'values': '=Hectáreas!$G$5:$G$' + str(pj.columns.size + 4), 'fill': {'color': '#2000ff'}})

        chart2.set_title({'name': graficosname})
        chart2.set_x_axis({'name': names})
        chart2.set_y_axis({'name': 'Color'})
        chart2.set_size({'x_scale': 3, 'y_scale': 1.5})
        worksheet2.insert_chart('Q1', chart2)

        workbook.close()
