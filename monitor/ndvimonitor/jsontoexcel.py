import pandas as pd
import xlsxwriter
import uuid
import requests
import json
import datetime

from PIL import Image
import os.path
import locale

def calculate_scale(file_path, bound_size):
    # check the image size without loading it into memory
    im = Image.open(file_path)
    original_width, original_height = im.size

    # calculate the resize factor, keeping original aspect and staying within boundary
    bound_width, bound_height = bound_size
    ratios = (float(bound_width) / original_width, float(bound_height) / original_height)
    return min(ratios)

def json2xlsx(jsons,isWithImage,iswithGraphic = False):

    

    names = 'Nombre/Name'
    graficosname = 'Gráfico por Parcelas/Chart by Parcels'
    nombreXlsx = str(uuid.uuid1().int) + '.xlsx'
    workbook = xlsxwriter.Workbook("media/parcels/"+nombreXlsx)
    bold = workbook.add_format({'bold': 1})
    # Configurar la localización según tus necesidades
    locale.setlocale(locale.LC_ALL, 'nl_NL') # es_ES.UTF-8
    # Cabeceras
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
            worksheet.write_string(3, 16, "Nubes", header_formatRA)

            worksheet.write_string(3, 18, "Plantas", header_formatinfo)
            worksheet.write_string(3, 19, "Cosecha", header_formatinfo)
            worksheet.write_string(3, 20, "Fecha de recogida", header_formatinfo)

            # image
            #worksheet.write_string(3, 21, "Imagen", header_format)
            
            # name/espacio/guion/espacio
            name_with_date = item["name"] + " "+ "- "+ fecha
            #worksheet.write_string(row+4, col, item["name"], bold)
            worksheet.write_string(row+4, col, name_with_date, bold)
            
            worksheet.write_number(row+4, col+1, float(item['pix_rojo_altos_porcent']))
            worksheet.write_number(row+4, col+2, float(item['pix_rojo_medios_porcent']))
            worksheet.write_number(row+4, col+3, float(item['pix_rojo_bajos_porcent']))

            worksheet.write_number(row+4, col+5, float(item['pix_amarillo_altos_porcent']))
            worksheet.write_number(row+4, col+6, float(item['pix_amarillo_medios_porcent']))
            worksheet.write_number(row+4, col+7, float(item['pix_amarillo_bajos_porcent']))

            worksheet.write_number(row+4, col+9, float(item['pix_azul_altos_porcent']))
            worksheet.write_number(row+4, col+10, float(item['pix_azul_medios_porcent']))
            worksheet.write_number(row+4, col+11, float(item['pix_azul_bajos_porcent']))

            worksheet.write_number(row+4, col+13, float(item['pix_verde_altos_porcent']))
            worksheet.write_number(row+4, col+14, float(item['pix_verde_medios_porcent']))
            
            # D4SF-86
            #nubes_porcent_str = str(item['nubes_porcent'])
            #nubes_str = nubes_porcent_str.replace('.', ',')
            #nubes_float = locale.atof(nubes_str)
            #worksheet.write_number(row + 4, col + 16, nubes_float)
            print(item['nubes_porcent'])
            worksheet.write_number(row + 4, col + 16, float(item['nubes_porcent']))

            worksheet.write_string(row + 4, col + 18, str(plantas))
            worksheet.write_string(row + 4, col + 19, str(produccion))
            worksheet.write_string(row + 4, col + 20, str(fechaCosecha))

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
            chart.add_series({'name': "='"+fecha+"'!$B$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$B$5:$B$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#fe0103'}})
            chart.add_series({'name': "='"+fecha+"'!$C$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$C$5:$C$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#9b0004'}})
            chart.add_series({'name': "='"+fecha+"'!$D$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$D$5:$D$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#680000'}})

            chart.add_series({'name': "='"+fecha+"'!$F$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$F$5:$F$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#ffff33'}})
            chart.add_series({'name': "='"+fecha+"'!$G$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$G$5:$G$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#cccc33'}})
            chart.add_series({'name': "='"+fecha+"'!$H$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$H$5:$H$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#666600'}})

            chart.add_series({'name': "='"+fecha+"'!$J$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$J$5:$J$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#33ffff'}})
            chart.add_series({'name': "='"+fecha+"'!$K$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$K$5:$K$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#33cccc'}})
            chart.add_series({'name': "='"+fecha+"'!$L$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$L$5:$L$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#006666'}})

            chart.add_series({'name': "='"+fecha+"'!$N$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$N$5:$N$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#33ff33'}})
            chart.add_series({'name': "='"+fecha+"'!$O$4",'categories': "='"+fecha+"'!$A$5:$A$"+str(len(jsons[fecha]["resultado"])+4), 'values': "='"+fecha+"'!$O$5:$O$"+str(len(jsons[fecha]["resultado"])+4), 'fill':   {'color': '#33cc33'}})

            chart.set_title ({'name': graficosname})
            chart.set_x_axis({'name': names})
            chart.set_y_axis({'name': 'Porcentaje de color/Color percentage'})
            chart.set_size({'x_scale': 3, 'y_scale': 1.5})

            if iswithGraphic == 'true':
                worksheet.insert_chart('W1', chart)
            
            #worksheet.insert_chart('W1', chart)
    
    
    workbook.close()
    


    return nombreXlsx