import os
import sys
import fnmatch
import xml.etree.ElementTree as ET
from eodatasets3 import DatasetPrepare
from pathlib import Path
import datetime

dirpath = sys.argv[1]
print('------------> INPUT FILES PATH BELOW <------------',dirpath)
outputpath = sys.argv[2]
print('------------> OUTPUT FILES PATH BELOW <-------------',outputpath)
count = int(sys.argv[3])
metadata_path = Path(outputpath+'/scene'+str(count)+'.odc-metadata.yaml')

with DatasetPrepare(
     collection_location=Path(dirpath),
     metadata_path=metadata_path,
     allow_absolute_paths=True,
) as p:
     p.product_family = "landsat_sr_kenya"
     p.processed_now()
     if os.path.exists(dirpath):
        files = os.listdir(dirpath)
        for file in files:
          if (file.endswith('.xml')):
            tree = ET.parse(Path(dirpath+'/'+file))
            product_contents = tree.find('PRODUCT_CONTENTS')
            image_attributes = tree.find('IMAGE_ATTRIBUTES')
            level1_processing_record = tree.find('LEVEL1_PROCESSING_RECORD')
            date_acquired = image_attributes.find('DATE_ACQUIRED').text
            scene_center_time = image_attributes.find('SCENE_CENTER_TIME').text
            date_n_time_str = str(date_acquired)+' '+str(scene_center_time)
            print('-------------> DATE AND TIME:',date_n_time_str)
            p.datetime = date_n_time_str
            p.properties["odc:file_format"] = 'GeoTIFF'
            p.properties["eo:cloud_cover"] = image_attributes.find('CLOUD_COVER').text
            p.properties["eo:instrument"] = image_attributes.find('SENSOR_ID').text
            p.properties["landsat:cloud_cover_land"] = image_attributes.find('CLOUD_COVER_LAND').text
            p.properties["landsat:collection_category"] = product_contents.find('COLLECTION_CATEGORY').text
            p.properties["landsat:collection_number"] = product_contents.find('COLLECTION_NUMBER').text
            p.properties["landsat:scene_id"] = level1_processing_record.find('LANDSAT_SCENE_ID').text
            p.properties["landsat:wrs_path"] = image_attributes.find('WRS_PATH').text
            p.properties["landsat:wrs_row"] = image_attributes.find('WRS_ROW').text
            p.properties["landsat:wrs_type"] = image_attributes.find('WRS_TYPE').text
          if (file.endswith('.TIF')):
            if fnmatch.fnmatch(file, '*SR_B1.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('sr_b1',inputs_path)
            if fnmatch.fnmatch(file, '*SR_B2.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('sr_b2',inputs_path)
            if fnmatch.fnmatch(file, '*SR_B3.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('sr_b3',inputs_path)
            if fnmatch.fnmatch(file, '*SR_B4.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('sr_b4',inputs_path)
            if fnmatch.fnmatch(file, '*SR_B5.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('sr_b5',inputs_path)
            if fnmatch.fnmatch(file, '*SR_B6.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('sr_b6',inputs_path)
            if fnmatch.fnmatch(file, '*SR_B7.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('sr_b7',inputs_path)
            if fnmatch.fnmatch(file, '*QA_RADSAT.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('qa_radsat',inputs_path)
            if fnmatch.fnmatch(file, '*QA_PIXEL.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('qa_pixel',inputs_path)
            if fnmatch.fnmatch(file, '*SR_QA_AEROSOL.TIF'):
               inputs_path = Path(dirpath+'/'+file)
               print('-----------> FULL PATH: ',inputs_path)
               p.note_measurement('sr_qa_aerosol',inputs_path)
     else:
        print('!!!!!!!!!!!!! SORRY, PATH NOT FOUND !!!!!!!!!!!!')
     p.done()

# assert metadata_path.exists()