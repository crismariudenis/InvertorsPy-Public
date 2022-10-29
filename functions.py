import requests
import time

plantId=696969
serialNum=6969696
def growattChangeAcCharge(value):
    url = "https://server.growatt.com/tcpSet.do"
    payload = f"action=storageSPF5000Set&serialNum={serialNum}&type=storage_spf5000_max_AC_charge_current&param1={value}&param2=&param3=&param4="
    #add your own header
    headers = {}
    try:
        response = requests.request("POST", url, headers=headers, data=payload).json()
    except (requests.exceptions.RequestException , requests.exceptions.Timeout , requests.exceptions.HTTPError) as e:
        print(e)
        time.sleep(30)
        return growattChangeAcCharge(value)

    return response


def growattReadAcOutputSource():
    url = "https://server.growatt.com/tcpSet.do"

    payload = f"action=readStorageParam&paramId=storage_spf5000_ac_output_source&serialNum={serialNum}&startAddr=-1&endAddr=-1"
    # add your own header
    headers = {}
    try:
        response = requests.request("POST", url, headers=headers, data=payload).json()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
        print(e)
        time.sleep(30)
        return growattReadAcOutputSource()

    return response


def growattChangeAcOutputSource(value):

    url = "https://server.growatt.com/tcpSet.do"
    payload = f"action=storageSPF5000Set&serialNum={serialNum}&type=storage_spf5000_ac_output_source&param1={value}&param2=&param3=&param4="
    # add your own header
    headers = {}
    try:
        response = requests.request("POST", url, headers=headers, data=payload).json()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
        print(e)
        time.sleep(30)
        return growattChangeAcOutputSource(value)

    return response


def growattReadAcCharge():
    url = "https://server.growatt.com/tcpSet.do"

    payload = f"action=readStorageParam&paramId=storage_spf5000_max_AC_charge_current&serialNum={serialNum}&startAddr=-1&endAddr=-1"
    # add your own header
    headers = {}

    try:
        response = requests.request("POST", url, headers=headers, data=payload).json()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
        print(e)
        time.sleep(30)
        return growattReadAcCharge()

    return response

def growattReadLoadPower():

    url = f"https://server.growatt.com/panel/storage/getStorageStatusData?plantId={plantId}"

    payload = f"storageSn={serialNum}"
    # add your own header
    headers = {}
    try:
        response = requests.request("POST", url, headers=headers, data=payload).json()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
        print(e)
        time.sleep(30)
        return growattReadLoadPower()

    return response

