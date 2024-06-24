import pandas as pd
import xlsxwriter

workbook  = xlsxwriter.Workbook('csv_generados/filename.xlsx')
worksheet = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()

pj = pd.read_json("csv_generados/44969424513108309779577241692114774369.json")


"""
writer = pd.ExcelWriter('csv_generados/pandas_simple.xlsx', engine='xlsxwriter')

df1 = pd.DataFrame(pj[1]['azules'])
df1.to_excel(writer, sheet_name='Sheet1', startrow=2)
df2 = pd.DataFrame(pj[1]['amarillos'])
df2.to_excel(writer, sheet_name='Sheet1', startrow=7)
df3 = pd.DataFrame(pj[1]['rojos'])
df3.to_excel(writer, sheet_name='Sheet1')



# Close the Pandas Excel writer and output the Excel file.
writer.save()

"""
bold = workbook.add_format({'bold': 1})
header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'border': 1})

header_formatRA = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#fe0103',
    'border': 1})
header_formatRM = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#9b0004',
    'border': 1})
header_formatRB = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#680000',
    'border': 1})

header_formatAA = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#ffff33',
    'border': 1})
header_formatAM = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#cccc33',
    'border': 1})
header_formatAB = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#666600',
    'border': 1})

header_formatAzA = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#33ffff',
    'border': 1})
header_formatAzM = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#33cccc',
    'border': 1})
header_formatAzB = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#006666',
    'border': 1})

header_formatVA = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#33ff33',
    'border': 1})
header_formatVM = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#33cc33',
    'border': 1})
merge_format = workbook.add_format({
    'bold':     True,
    'border':   6,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#D7E4BC',
})
worksheet.write_string(0, 0, "", header_format)
worksheet.merge_range(1, 0, 1, 14, "Todos los valores son porcentajes entre 0% - 100%", header_format)
worksheet.write_string(3, 0, "Fecha", header_format)
worksheet.write_string(3, 1, "Rojo Alto", header_formatRA)
worksheet.write_string(3, 2, "Rojo Medio", header_formatRM)
worksheet.write_string(3, 3, "Rojo Bajo", header_formatRB)

worksheet.write_string(3, 5, "Amarillo Alto", header_formatAA)
worksheet.write_string(3, 6, "Amarillo Medio", header_formatAM)
worksheet.write_string(3, 7, "Amarillo Bajo", header_formatAB)

worksheet.write_string(3, 9, "Azul Alto", header_formatAzA)
worksheet.write_string(3, 10, "Azul Medio", header_formatAzM)
worksheet.write_string(3, 11, "Azul Bajo", header_formatAzB)

worksheet.write_string(3, 13, "Verde Alto", header_formatVA)
worksheet.write_string(3, 14, "Verde Medio", header_formatVM)
row = 1
col = 0
print(pj.columns.size)
for item in pj:
    print(pj[item]['fecha'])
    worksheet.write_string(item+4, col, pj[item]['fecha'], bold)
    worksheet.write_number(item+4, col+1, float(pj[item]['rojos']['altos']['porcent']))
    worksheet.write_number(item+4, col+2, float(pj[item]['rojos']['medios']['porcent']))
    worksheet.write_number(item+4, col+3, float(pj[item]['rojos']['bajos']['porcent']))

    worksheet.write_number(item+4, col+5, float(pj[item]['amarillos']['altos']['porcent']))
    worksheet.write_number(item+4, col+6, float(pj[item]['amarillos']['medios']['porcent']))
    worksheet.write_number(item+4, col+7, float(pj[item]['amarillos']['bajos']['porcent']))

    worksheet.write_number(item+4, col+9, float(pj[item]['azules']['altos']['porcent']))
    worksheet.write_number(item+4, col+10, float(pj[item]['azules']['medios']['porcent']))
    worksheet.write_number(item+4, col+11, float(pj[item]['azules']['bajos']['porcent']))

    worksheet.write_number(item+4, col+13, float(pj[item]['verdes']['altos']['porcent']))
    worksheet.write_number(item+4, col+14, float(pj[item]['verdes']['medios']['porcent']))
    #worksheet.insert_image(item+1, col+15, 'python.png', {'url': 'http://127.0.0.1:8000/media/'+pj[item]['img']})
    #worksheet.insert_image(item+1, col+16, '../media/parcels/'+str(pj[item]['img']), {'x_scale': 0.02, 'y_scale': 0.02})
col = -1
for item in pj:
    worksheet.write_string(pj.columns.size+2+9, col+1, pj[item]['fecha'], header_format)
    worksheet.insert_image(pj.columns.size+2+12, col+1, '../media/parcels/'+str(pj[item]['img']), {'x_scale': 0.03, 'y_scale': 0.03})
    col +=1

#chart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
chart = workbook.add_chart({'type': 'column'})
chart.add_series({'name': '=Sheet1!$B$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$B$5:$B$'+str(pj.columns.size+4), 'fill':   {'color': '#fe0103'}})
chart.add_series({'name': '=Sheet1!$C$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$C$5:$C$'+str(pj.columns.size+4), 'fill':   {'color': '#9b0004'}})
chart.add_series({'name': '=Sheet1!$D$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$D$5:$D$'+str(pj.columns.size+4), 'fill':   {'color': '#680000'}})

chart.add_series({'name': '=Sheet1!$F$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$F$5:$F$'+str(pj.columns.size+4), 'fill':   {'color': '#ffff33'}})
chart.add_series({'name': '=Sheet1!$G$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$G$5:$G$'+str(pj.columns.size+4), 'fill':   {'color': '#cccc33'}})
chart.add_series({'name': '=Sheet1!$H$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$H$5:$H$'+str(pj.columns.size+4), 'fill':   {'color': '#666600'}})

chart.add_series({'name': '=Sheet1!$J$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$J$5:$J$'+str(pj.columns.size+4), 'fill':   {'color': '#33ffff'}})
chart.add_series({'name': '=Sheet1!$K$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$K$5:$K$'+str(pj.columns.size+4), 'fill':   {'color': '#33cccc'}})
chart.add_series({'name': '=Sheet1!$L$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$L$5:$L$'+str(pj.columns.size+4), 'fill':   {'color': '#006666'}})

chart.add_series({'name': '=Sheet1!$N$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$N$5:$N$'+str(pj.columns.size+4), 'fill':   {'color': '#33ff33'}})
chart.add_series({'name': '=Sheet1!$O$4','categories': '=Sheet1!$A$5:$A$18', 'values': '=Sheet1!$O$5:$O$'+str(pj.columns.size+4), 'fill':   {'color': '#33cc33'}})

chart.set_title ({'name': 'Gráfico por fechas'})
chart.set_x_axis({'name': 'Fechas'})
chart.set_y_axis({'name': 'Porcentaje de color'})
chart.set_size({'x_scale': 3, 'y_scale': 1.5})

# Set an Excel chart style.

worksheet.insert_chart('Q1', chart)



workbook.close()