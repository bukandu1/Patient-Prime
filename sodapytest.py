"""You can also use the sodapy library to pull information from
the Socrata API. Decided to list out the filters directly in the URL"""


from sodapy import Socrata
import requests
import os

key = os.environ.get("SOCRATA_API_KEY")
client = Socrata("data.medicare.gov", key)

r1 = client.get("c8qv-268j", query=query)
r2 = client.get("c8qv-268j", where="cred='MD'" and "st='MD'") #Providers (eligibe prof)

#r = client.get("ukfj-tt6v", where="state='MD'") #Hospitals and patient safety indicatiors
url = """https://data.medicare.gov/resource/c8qv-268j.json?cred=MD&st=MD&$where=
hosp_afl_lbn_1%20in(%27SUBURBAN%20HOSPITAL%27,%27UNITED%20MEDICAL%20CENTER%27,
%27HOLY%20CROSS%20HOSPITAL%27,"","POTOMAC VALLEY HOSPITAL"
"UNIVERSITY OF MARYLAND MEDICAL CENTER","","",FREDERICK MEMORIAL HOSPITAL, UNIVERSITY OF MARYLAND ST JOSEPH MEDICAL CENTER
"MEDSTAR SAINT MARY'S HOSPITAL","",""")

#associated hospital data
url = https://data.medicare.gov/resource/c8qv-268j.json?cred=MD&st=MD&$where=hosp_afl_lbn_1%20in(%27UNIVERSITY%20OF%20MARYLAND%20MEDICAL%20CENTER%27,%27UNIVERSITY%20OF%20MARYLAND%20ST%20JOSEPH%20MEDICAL%20CENTER%27,%27SIBLEY%20MEMORIAL%20HOSPITAL%27,%27BON%20SECOURS%20HOSPITAL%27,%27SUBURBAN%20HOSPITAL%27,%27UNITED%20MEDICAL%20CENTER%27,%27HOLY%20CROSS%20HOSPITAL%27,%27ANNE%20ARUNDEL%20MEDICAL%20CENTER%27,%27MERITUS%20MEDICAL%20CENTER%27,%27JOHNS%20HOPKINS%20HOSPITAL,%20THE%27)
"""