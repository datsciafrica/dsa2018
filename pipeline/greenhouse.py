import time
import ttn
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch()
app_id = "xxxxx"
access_key = "xxxxxx"
index = "greenhouse"
doctype = "type1"
eshost = "localhost:9200"


#using https and 443 for AWS instance
es = Elasticsearch(
    [eshost],
    scheme="http",
    port=9200,
)


docs = []

def uplink_callback(msg, client):
    print("Received uplink from ", msg.dev_id)
    print("type of msg",type(msg))
    print(msg)

    # if not msg.payload_fields.analog_in_4 :
    #     analog_in_4 = None
    # if not msg.payload_fields.relative_humidity_3 :
    #     relative_humidity_3 = None
    # if not msg.payload_fields.temperature_2 :
    #     temperature_2 = None

    try:
        analog_in_4 = msg.payload_fields.analog_in_4
    except:
        analog_in_4 = None

    try:
        relative_humidity_3 = msg.payload_fields.relative_humidity_3
    except:
        relative_humidity_3 = None

    try:
        temperature_2 = msg.payload_fields.temperature_2
    except:
        temperature_2 = None

    try:
        gtw_trusted_0 = msg.metadata.gateways[0].gtw_trusted
    except:
        gtw_trusted_0 = None

    try:
        latitute_0 = msg.metadata.gateways[0].latitude
    except:
        latitute_0 = 0

    try:
        longitude_0 = msg.metadata.gateways[0].longitude
    except:
        longitude_0 = 0

    try:
        location_source_0 = msg.metadata.gateways[0].location_source_0
    except:
        location_source_0 = None

    if len(msg.metadata.gateways) == 1 :
        gtw_id_0 = msg.metadata.gateways[0].gtw_id
        gtw_trusted_0 = gtw_trusted_0
        gtw_time_0 = msg.metadata.gateways[0].time
        channel_0 = msg.metadata.gateways[0].channel
        rssi_0 = msg.metadata.gateways[0].rssi
        snr_0 = msg.metadata.gateways[0].snr
        rf_chain_0 = msg.metadata.gateways[0].rf_chain
        latitute_0 = longitude_0
        longitude_0 = longitude_0
        gtw_location_0 = [longitude_0,longitude_0]
        location_source_0 = location_source_0
        gtw_id_1 = None
        gtw_trusted_1 = None
        gtw_time_1 = None
        channel_1 = None
        rssi_1 = None
        snr_1 = None
        rf_chain_1 = None
        latitute_1 = None
        longitude_1 = None
        gtw_location_1 = [0,0]
        location_source_1 = None
    if len(msg.metadata.gateways) == 2:
        gtw_id_0 = msg.metadata.gateways[0].gtw_id
        gtw_trusted_0 = msg.metadata.gateways[0].gtw_trusted
        gtw_time_0 = msg.metadata.gateways[0].time
        channel_0 = msg.metadata.gateways[0].channel
        rssi_0 = msg.metadata.gateways[0].rssi
        snr_0 = msg.metadata.gateways[0].snr
        rf_chain_0 = msg.metadata.gateways[0].rf_chain
        latitute_0 = msg.metadata.gateways[0].latitude
        longitude_0 = msg.metadata.gateways[0].longitude
        location_source_0 = msg.metadata.gateways[0].location_source
        gtw_id_1 = msg.metadata.gateways[1].gtw_id
        gtw_trusted_1 = msg.metadata.gateways[1].gtw_trusted
        gtw_time_1 = msg.metadata.gateways[1].time
        channel_1 = msg.metadata.gateways[1].channel
        rssi_1 = msg.metadata.gateways[1].rssi
        snr_1 = msg.metadata.gateways[1].snr
        rf_chain_1 = msg.metadata.gateways[1].rf_chain
        latitute_1 = msg.metadata.gateways[1].latitude
        longitude_1 = msg.metadata.gateways[1].longitude
        location_source_1 = msg.metadata.gateways[1].location_source


    doc = {
        "_op_type": "index",
        "_index": index,
        "_type": doctype,
        #"_source": msg,
        "app_id": msg.app_id,
        "dev_id": msg.dev_id,
        "hardware_serial": msg.hardware_serial,
        "port":msg.port,
        "counter":msg.counter,

        #metadata
        "time": msg.metadata.time,
        "frequency": msg.metadata.frequency,
        "modulation": msg.metadata.modulation,
        "data_rate" : msg.metadata.data_rate,
        "airtime" : msg.metadata.airtime,
        "coding_rate" : msg.metadata.coding_rate,

        #gateways
        "gtw_id_0" : gtw_id_0,
        "gtw_trusted_0" : gtw_trusted_0,
        "gtw_time_0" : gtw_time_0,
        "channel_0" : channel_0,
        "rssi_0" : rssi_0,
        "snr_0" : snr_0,
        "rf_chain_0" : rf_chain_0,
        "latitute_0" : latitute_0,
        "longitude_0" : longitude_0,
        "gtw_location_0": [latitute_0,longitude_0],
        "location_source_0" : location_source_0,
        "gtw_id_1": gtw_id_1,
        "gtw_trusted_1": gtw_trusted_1,
        "gtw_time_1": gtw_time_1,
        "channel_1": channel_1,
        "rssi_1": rssi_1,
        "snr_1": snr_1,
        "rf_chain_1": rf_chain_1,
        "latitute_1": latitute_1,
        "longitude_1": longitude_1,
        "gtw_location_1": gtw_location_1,
        "location_source_1": location_source_1,

        # fields
        #"payload_fields": msg.payload_fields,
        "analog_in_4" : analog_in_4,
        "relative_humidity_3": relative_humidity_3,
        "temperature_2" : temperature_2
    }
    print("doc",doc)
    docs.append(doc)
    print("size of docs",len(docs))
    if len(docs) == 2:
        print("call write2es")
        write2es(docs)




def write2es(documents):
     helpers.bulk(es, documents, index=index, doc_type=doctype)
     print("reset docs to 0")
     global docs
     docs = []
     print("size of docs", len(docs))


handler = ttn.HandlerClient(app_id, access_key)
# using mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()



while True:
    time.sleep(1)
# mqtt_client.close()

# using application manager client
# app_client =  handler.application()
# my_app = app_client.get()
# print(my_app)
# my_devices = app_client.devices()
# print(my_devices)
