from datetime import datetime
# Define constants

# Get the current date and time
current_datetime = datetime.now()

# Format the date and time as a string
tableDateFormatterStr = "yyyyMMdd'T'HHmmss"
tableDateFormatter = current_datetime.strftime(tableDateFormatterStr)
fechaFormatterStr = "dd-MM-yyyy"

#Propiedades del fichero de config.ini
fichero_config_ini = "config.ini"
seccion_app = "ds4f_app"
seccion_log = "ds4f_app_log"
seccion_docker = "ds4f_app_docker"

log_file_const = "log_file"
encoding_const = "encoding"
max_log_size_bytes_const = "max_log_size_bytes"
backup_count_const = "backup_count"
script_path_const = "script_path"
container_dev_name_const = "container_dev_name"

#URL's de sentinel
protocol_url_const='https://'
url_api_instances_const = "url_api_instances"
url_api_wms_const= "url_api_wms"
url_api_token_const = "url_api_token"
url_api_id_const = "url_api_id"
url_api_secret_const = "url_api_secret"
url_api_data_products_1242_const = "url_api_data_products_1242"
url_api_data_products_647_const = "url_api_data_products_647"
url_api_data_sets_const = "url_api_data_sets"
url_api_data_source_const = "url_api_data_source"
url_api_false_layers_const = "url_api_false_layers"
url_api_crs_const = "url_api_crs"
url_api_time_const = "url_api_time"
url_api_eval_script_const = "url_api_eval_script"

evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""
