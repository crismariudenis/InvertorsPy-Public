from functions import growattReadAcOutputSource, growattReadAcCharge, growattChangeAcCharge, growattChangeAcOutputSource, growattReadLoadPower
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
import math
from colorama import Fore, Back, Style
logging.basicConfig(filename="test.txt", level=logging.INFO,
                    format='%(asctime)s%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def constraint(value, mini, maxi):
    return int(min(maxi, max(mini, value)))


def getBPower():
    while not client.connect():
        print('not Connected')
        time.sleep(60)
        client.connect()
    else:
        try:
            request = client.read_holding_registers(
                address=37134, count=2, unit=1)
            # print(request.registers)
            ans = request.registers[1] - request.registers[0]
        except:
            print("ERROR: client.read_holding_registers ", client.connect())
            time.sleep(60)
            return getBPower()

    if(abs(ans) > 2500):
        print("Inverter responds with WRONG value")
        time.sleep(60)
        return getBPower()
    else:
        return ans


def changeAcOuput(output):
    resp = growattChangeAcOutputSource(output)
    # logging.info(resp)
    while(resp['success'] == False):
        resp = growattChangeAcOutputSource(output)
        time.sleep(60)


def readOutputSource():
    resp = growattReadAcOutputSource()
    # logging.info(resp)
    while(resp['success'] == False):
        resp = growattReadAcOutputSource()
        time.sleep(60)
    return int(resp['msg'])


def changeAcCharge(value):
    resp = growattChangeAcCharge(value)
    # print(resp)
    while(resp['success'] == False):
        resp = growattChangeAcCharge(value)
        print("failed with the response=", resp)
        time.sleep(5)


def readLoadPower():
    resp = growattReadLoadPower()
    # print(resp)
    while(resp["result"] != 1):
        resp = growattReadLoadPower()
        print("failed with the response=", resp)
        time.sleep(60)
    return int(resp['obj']['loadPower'])


if __name__ == '__main__':

    ###Constants###
    ip_inverter = '192.168.1.178'
    BAT = 0
    UTI = 2
############ CHANGE VALUES HERE ############
    minCharge = 1
    maxCharge = 15
    # Do every nr minutes
    nrMinutes = 2
############################################

    client = ModbusClient(ip_inverter, port=502)
    client.connect()
    time.sleep(1)
    outputType = int(readOutputSource())
    changeAcCharge(minCharge)
    charge = minCharge
    while True:
        loadPower = readLoadPower()
        realBpower = getBPower()
        bPower = realBpower-0
        partBPower = math.floor(bPower/55)


        if bPower < 50 and charge == minCharge:
            outputType = BAT
            changeAcOuput(BAT)
            changeAcCharge(minCharge)

        if bPower > loadPower+100 and outputType == BAT:
            outputType = UTI
            changeAcOuput(UTI)
            changeAcCharge(minCharge)

        if partBPower != 0 and outputType == UTI:
            charge += partBPower
            charge = constraint(charge, minCharge, maxCharge)
            print(Fore.GREEN, time.strftime("%H:%M:%S"), "output=", 'BAT' if(
                outputType == BAT) else 'UTI', "charge=", charge, "A")
            print(Style.RESET_ALL)
            changeAcCharge(constraint(charge, minCharge, maxCharge))

        time.sleep(nrMinutes*60)
