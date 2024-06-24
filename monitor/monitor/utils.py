import os.path

def checkNumberOfImageForReport(parcels = dict):
    numerberImage = 0
    fechas = parcels.keys()
    for fecha in fechas:
        for parcel in parcels[fecha]["resultado"]:
            
            if 'image' in parcel:
                if os.path.isfile(parcel['image']):
                    numerberImage += 1
            
            if 'nubesImage' in parcel:
                if os.path.isfile(parcel['nubesImage']):
                    numerberImage += 1

            if 'trueColorImage' in parcel:
                if os.path.isfile(parcel['trueColorImage']):
                    numerberImage += 1


    return numerberImage