import pandas as pd
import xlsxwriter
import uuid
import requests
import json
import datetime
import os.path
import locale

def json2xlsx(jsons,isWithImage = 'false',iswithGraphic = False):

    
    
    names = 'Nombre/Name'
    graficosname = 'Gráfico por Parcelas/Chart by Parcels'
    nombreXlsx = str(uuid.uuid1().int) + '.xlsx'
    workbook = xlsxwriter.Workbook("media/parcels/"+nombreXlsx)
    bold = workbook.add_format({'bold': 1})
    # Configurar la localización según tus necesidades
    locale.setlocale(locale.LC_ALL, 'nl_NL')
    # Cabeceras
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 1})
    # Nubes
    header_formatRA = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#fe0103',
        'border': 1})
    # MOISTURE INDEX
    header_formatNaranga = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#ff8000',
        'border': 1})
    header_formatAmarillo = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#ffdf00',
        'border': 1})
    header_formatVerde = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#66ff98',
        'border': 1})
    header_formatAzulClaro = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#02fefc',
        'border': 1})
    header_formatAzulMedio = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#0087ff',
        'border': 1})
    header_formatAzulOscuro = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#2000ff',
        'border': 1})
    header_formatinfo = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7D7D7',
        'border': 1})

    fechas = jsons.keys()
    #Obtencion de datos de cosechas y produccion
    anios=[]
    parcelas=[]
    [anios.append(int(x[0:4])) for x in fechas if x[0:4] not in anios]
    [parcelas.append(x['parcel']) for fecha in fechas for x in jsons[fecha]["resultado"]]
    url = "https://api-d4sf.smartbits-es.com/api/v1.0/signin/"
    payload = json.dumps({
        "email": "rebeca.espana@smartbits.es",
        "password": "SMB2023#"
        })
    headers = {
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, data=payload)
    responsejson = response.json()
    token = responsejson["token"]
    if token:
        url1 = "https://api-d4sf.smartbits-es.com/api/v1.0/campana/getplantas/"
        url2 = "https://api-d4sf.smartbits-es.com/api/v1.0/produccion/getproduccion/"
        #url1 = "http://127.0.0.1:8000/api/v1.0/campana/getplantas/"
        #url2 = "http://127.0.0.1:8000/api/v1.0/produccion/getproduccion/"
            
        payload = json.dumps({
            "token": token,
            "anios" : anios,
            "parcelas" : parcelas
            })
        headers = {
            'Authorization': 'Bearer '+token,
            'Content-Type': 'application/json'
            }
        response = requests.request("POST", url1, headers=headers, data=payload)
        responseplantas=response.json()
        response = requests.request("POST", url2, headers=headers, data=payload)
        responseproduccion=response.json()
    for fecha in fechas:
        col = 0
        row = 0
        worksheet = workbook.add_worksheet(fecha)
        for item in jsons[fecha]["resultado"]:
            #Obtencion de datos de esa parcela/fecha
            produccion="No hay datos"
            fechaCosecha="No hay datos"
            plantas="No hay datos"
            if len(responseplantas)!=0:
                for x in responseplantas:
                    if int(x["anio"])==int(fecha[0:4]) and int(x["parcela"])==int(item['parcel']):
                        plantas=int(x['plantas'])  
            else:
                plantas="No hay datos"
            
            if len(responseproduccion)!=0:
                for x in responseproduccion:
                    if int(x["anio"])==int(fecha[0:4]) and int(x["parcela"])==int(item['parcel']):
                        produccion=int(x['produccion'])
                        fechaCosecha=x["fecha_fin"]
            else:
                produccion="No hay datos"
                fechaCosecha="No hay datos"
           

            #Creación de la hoja
            worksheet.write_string(0, 0, "", header_format)
            worksheet.merge_range(1, 0, 1, 16, "Todos los valores son porcentajes entre 0% - 100% - All values ​​are percentages between 0% - 100%", header_format)
            worksheet.write_string(3, 0, names, header_format)
            worksheet.write_string(3, 1, "Rojo/Naranja", header_formatNaranga)
            worksheet.write_string(3, 2, "Amarillo", header_formatAmarillo)
            worksheet.write_string(3, 3, "Verde", header_formatVerde)
            worksheet.write_string(3, 4, "Azul Claro", header_formatAzulClaro)
            worksheet.write_string(3, 5, "Azul Medio", header_formatAzulMedio)
            worksheet.write_string(3, 6, "Azul Oscuro", header_formatAzulOscuro)
            worksheet.write_string(3, 8, "Nubes", header_formatRA)
            worksheet.write_string(3, 10, "Plantas", header_formatinfo)
            worksheet.write_string(3, 11, "Cosecha", header_formatinfo)
            worksheet.write_string(3, 12, "Fecha de recogida", header_formatinfo)


            #worksheet.write_string(row+4, col, item["name"], bold)
            name_with_date = item["name"] + " "+ "- "+ fecha
            worksheet.write_string(row+4, col, name_with_date, bold)
            
            worksheet.write_number(row+4, col+1, float(item['pix_naranja_porcent']))
            worksheet.write_number(row+4, col+2, float(item['pix_amarillo_porcent']))
            worksheet.write_number(row+4, col+3, float(item['pix_verde_porcent']))
            worksheet.write_number(row+4, col+4, float(item['pix_azul_claro_porcent']))
            worksheet.write_number(row+4, col+5, float(item['pix_azul_medio_porcent']))
            worksheet.write_number(row+4, col+6, float(item['pix_azul_oscuro_porcent']))

            # D4SF-86
            nubes_porcent_str = str(item['nubes_porcent'])
            nubes_str = nubes_porcent_str.replace('.', ',')
            nubes_float = locale.atof(nubes_str)
            worksheet.write_number(item + 4, col + 8, nubes_float)
            #worksheet.write_string(row + 4, col + 8, str(item['nubes_porcent']))
            
            
            worksheet.write_string(row + 4, col + 10, str(plantas))
            worksheet.write_string(row + 4, col + 11, str(produccion))
            worksheet.write_string(row + 4, col + 12, str(fechaCosecha))

            # adding image
            if isWithImage == 'true':
                # check date
                human_date = ''
                if 'date' in item:
                    d1 = datetime.datetime.strptime(item['date'],"%Y-%m-%dT%H:%M:%SZ")
                    new_format = "%Y-%m-%d"
                    human_date = d1.strftime(new_format)
                
                
                # adding header
                worksheet.write_string(len(jsons[fecha]["resultado"]) + 7, row, item['name']+' - '+ human_date, header_format)
                if 'image' in item:
                    if os.path.isfile(item['image']):
                        # image
                        worksheet.insert_image(len(jsons[fecha]["resultado"]) + 10, row , item['image'], {'x_scale': 0.2, 'y_scale': 0.2})
                
                if 'nubesImage' in item:
                    if os.path.isfile(item['nubesImage']):
                        # nubesImage
                        worksheet.insert_image(len(jsons[fecha]["resultado"]) + 13, row ,item['nubesImage'], {'x_scale': 0.2, 'y_scale': 0.2})
                
                if 'trueColorImage' in item:
                    if os.path.isfile(item['trueColorImage']):
                        # trueColorImage
                        worksheet.insert_image(len(jsons[fecha]["resultado"]) + 16, row ,item['trueColorImage'], {'x_scale': 0.2, 'y_scale': 0.2})
                
            # end adding image
            
            col = 0
            row +=1
            chart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
            chart.add_series({'name': "='"+fecha+"'!$B$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$B$5:$B$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#ff8000'}})
            chart.add_series({'name': "='"+fecha+"'!$C$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$C$5:$C$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#ffdf00'}})
            chart.add_series({'name': "='"+fecha+"'!$D$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$D$5:$D$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#66ff98'}})
            chart.add_series({'name': "='"+fecha+"'!$E$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$E$5:$E$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#02fefc'}})
            chart.add_series({'name': "='"+fecha+"'!$F$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$F$5:$F$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#0049d5'}})
            chart.add_series({'name': "='"+fecha+"'!$G$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$G$5:$G$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#2000ff'}})
            chart.set_title ({'name': graficosname})
            chart.set_x_axis({'name': names})
            chart.set_y_axis({'name': 'Procentaje de color/Color percentage'})
            chart.set_size({'x_scale': 3, 'y_scale': 1.5})

            if iswithGraphic == 'true':
                worksheet.insert_chart('W1', chart)
        
    workbook.close()
    return nombreXlsx