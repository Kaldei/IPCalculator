"""
Content : IP Range Calculator
Using : Python

Author : Arthur
Date : March 2020
Context : Personal
"""

# --- --- --- Imports --- --- --- #
import re

# --- --- --- Constant --- --- --- #
IP_MASK_REGEX = r"^([0-9]{1,3}\.){3}[0-9]{1,3}$"

# --- --- --- Loop --- --- --- #
loop = ""
while loop != "exit":
    print("Welcome : This is IP Range Calculator !")

    # --- --- --- Inputs --- --- --- #
    # lDecIP
    vDecIP = True
    while vDecIP:
        sDecIP = input("Enter an IP : ")
        print("")
        if bool(re.match(IP_MASK_REGEX, sDecIP)):
            lDecIP = sDecIP.split('.')
            check = False
            for i in range(4):
                if int(lDecIP[i]) < 0 or int(lDecIP[i]) > 255:
                    check = True
                    print("Warning : " + lDecIP[i] + " is not a valid byte.")
            if check:
                vDecIP = True
            else:
                vDecIP = False
        else:
            vDecIP = True
            print("Warning : This is not a valid IP.")

    # lDecMask
    vDecMask = True
    while vDecMask:
        sDecMask = input("Enter a Mask : ")
        print("")
        if bool(re.match(IP_MASK_REGEX, sDecMask)):
            lDecMask = sDecMask.split('.')
            check = False
            for i in range(4):
                if lDecMask[i] != '255' and lDecMask[i] != '254' and lDecMask[i] != '252' and lDecMask[i] != '248' and lDecMask[i] != '240' and lDecMask[i] != '224' and lDecMask[i] != '192' and lDecMask[i] != '128' and lDecMask[i] != '0':
                    check = True
                    print("Warning : " + lDecMask[i] + " is not a valid byte.")
                elif i != 3 and lDecMask[i] != '255' and lDecMask[i+1] != '0':
                    check = True
                    print(
                        "Warning : This is not a valid Mask all bits must be left contiguous.")
            if check:
                vDecMask = True
            else:
                vDecMask = False
        else:
            vDecMask = True
            print("Warning : This is not a valid Mask.")

    # --- --- --- Nbr of IPs --- --- --- #
    # sBinMask
    sBinMask = ""
    for i in range(3):
        if lDecMask[i] != '0':
            sBinMask = sBinMask + str("{0:b}".format(int(lDecMask[i])))
            sBinMask = sBinMask + '.'
        else:
            sBinMask = sBinMask + "00000000"
            sBinMask = sBinMask + '.'
    if lDecMask[i+1] != '0':
        sBinMask = sBinMask + str("{0:b}".format(int(lDecMask[i+1])))
    else:
        sBinMask = sBinMask + "00000000"

    # lBinMask
    lBinMask = list(sBinMask)
    iCIDR = 0
    for i in range(len(lBinMask)):
        if lBinMask[i] == '1':
            iCIDR = iCIDR + 1

    # Nbr of IPs
    nbIP = str(2**(32-iCIDR))
    if nbIP == '1':
        nbUsable = '1'
    else:
        nbUsable = str(2**(32-iCIDR) - 2)

    # --- --- --- Network Address --- --- --- #
    # sBinIP
    sBinIP = ""
    for i in range(3):
        if lDecIP[i] != '0':
            if len("{0:b}".format(int(lDecIP[i]))) < 8:
                for j in range(8 - len("{0:b}".format(int(lDecIP[i])))):
                    sBinIP = sBinIP + '0'
                sBinIP = sBinIP + str("{0:b}".format(int(lDecIP[i])))
                sBinIP = sBinIP + '.'
            else:
                sBinIP = sBinIP + str("{0:b}".format(int(lDecIP[i])))
                sBinIP = sBinIP + '.'
        else:
            sBinIP = sBinIP + "00000000"
            sBinIP = sBinIP + '.'
    if lDecIP[i+1] != '0':
        if len("{0:b}".format(int(lDecIP[i+1]))) < 8:
            for j in range(8 - len("{0:b}".format(int(lDecIP[i+1])))):
                sBinIP = sBinIP + '0'
            sBinIP = sBinIP + str("{0:b}".format(int(lDecIP[i+1])))
        else:
            sBinIP = sBinIP + str("{0:b}".format(int(lDecIP[i+1])))
    else:
        sBinIP = sBinIP + "00000000"
    
    # lBinRes
    # lBinBroad
    lDecIP = list(sBinIP)
    lBinRes = []
    lBinBroad = []
    if iCIDR > 8:
        iCIDR = iCIDR + 1
    elif iCIDR > 16:
        iCIDR = iCIDR + 2
    elif iCIDR > 24:
        iCIDR = iCIDR + 3

    for i in range(35):
        if lDecIP[i] == '.':
            lBinRes.append('.')
            lBinBroad.append('.')
        else:
            if i <= iCIDR and iCIDR != 0:
                lBinRes.append(lDecIP[i])
                lBinBroad.append(lDecIP[i])
            else:
                lBinRes.append('0')
                lBinBroad.append('1')

    print(lBinRes)
    print(lBinBroad)
    # sDecRes
    sDecRes = ""
    octet = 0
    p = 7
    for i in range(35):
        if lBinRes[i] == '1':
            octet = octet + 2**p
            p = p - 1
        elif lBinRes[i] == '0':
            octet = octet + 0
            p = p - 1
        elif lBinRes[i] == '.':
            sDecRes = sDecRes + '.'
        if p < 0:
            sDecRes = sDecRes + str(octet)
            octet = 0
            wOctet = 0
            p = 7

    # sDecBroad
    sDecBroad = ""
    octet = 0
    p = 7
    for i in range(35):
        if lBinBroad[i] == '1':
            octet = octet + 2**p
            p = p - 1
        elif lBinBroad[i] == '0':
            octet = octet + 0
            p = p - 1
        elif lBinBroad[i] == '.':
            sDecBroad = sDecBroad + '.'
        if p < 0:
            sDecBroad = sDecBroad + str(octet)
            octet = 0
            wOctet = 0
            p = 7

    # --- --- --- Outputs --- --- --- #
    print("Number of IPs : " + nbIP)
    print("Number of usable IPs : " + nbUsable)
    print("Network Address : " + sDecRes)
    print("Broadcast Address : " + sDecBroad)
    print("")

    # --- --- --- Exit or Continue --- --- --- #
    loop = input("If you want to quit enter \"exit\" else press Enter : ")
    print()
