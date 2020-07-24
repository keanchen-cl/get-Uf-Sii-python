import requests
import base64
import json
import re

#==========================================
# Title:  Get UF SII python
# Author: KeanChen-cl
# Date:   24 Jul 2020
#==========================================py -m pip install requests

### Parameters ###

base_url="http://www.sii.cl/valores_y_fechas/uf/uf2020.htm"

### Parameters ###
def get_report(base_url):
    header_gs = {'Accept': 'application/json'}
    r= requests.get(base_url,headers=header_gs)
    if r.ok:
        print("Report results received...")        
        print("HTTP %i - %s" % (r.status_code, r.reason))
        return r.text
    else:
        print("HTTP %i - %s" % (r.status_code, r.reason))

### Obtiene la estructura HTML del sitio de SII y genera un archivo de salida CSV ###
def export_uf_to_json(base_url):

    r = get_report(base_url)
    r = r.split('\n')
    dataListA = list()
    dataListA=r
### variables d = dia, m = mes ###
    d=0
    m=0
### Matriz UF con los meses y dias ###
    f = open('report_results_uf.csv', 'w')
    f.write("DAY;ENE;FEB;MAR;ABR;MAY;JUN;JUL;AGO;SEP;OCT;NOV;DIC\n")

    for x in dataListA:
        x = x.split('\n')
### expresión regular para extraer los datos ###
        regexp=">(.*)<"
        resultRegExp = re.search(regexp, x[0], re.IGNORECASE)

        if resultRegExp:
            if resultRegExp.group(1) == '1':
                d=1
            if d<=31 and d!=0:
                if resultRegExp.group(1) != d and d!=0 and resultRegExp.group(1) != "&nbsp;":
                    if m==0 and d!=0:
                        f.write("%s" % d)
                    else:
                        f.write(";%s" % resultRegExp.group(1))
                    m=m+1 
                elif resultRegExp.group(1)=="&nbsp;":
                    f.write(";0")  
                    m=m+1 
                if resultRegExp.group(1) == '</tbody>':
                    break
        elif m>12:
            m=0
            f.write("\n") 
        elif d<32 and d!=0:
            d=d+1
    f.close()

def main():
    export_uf_to_json(base_url)

main()  