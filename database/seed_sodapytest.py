"""You can also use the sodapy library to pull information from
the Socrata API. Decided to list out the filters directly in the URL"""


from sodapy import Socrata
import requests
import os

key = os.environ.get("SOCRATA_API_KEY")
client = Socrata("data.medicare.gov", key)

#1 = client.get("c8qv-268j", query=query)
r = client.get("c8qv-268j", where="cred='MD'" and "st='MD'") #Providers (eligibe prof)

#r = client.get("ukfj-tt6v", where="state='MD'") #Hospitals and patient safety indicatiors
# url = """https://data.medicare.gov/resource/c8qv-268j.json?cred=MD&st=MD&$where=
# hosp_afl_lbn_1%20in(%27SUBURBAN%20HOSPITAL%27,%27UNITED%20MEDICAL%20CENTER%27,
# %27HOLY%20CROSS%20HOSPITAL%27,"LAUREL REGIONAL MEDICAL CENTER","POTOMAC VALLEY HOSPITAL"
# "UNIVERSITY OF MARYLAND MEDICAL CENTER","GREATER BALTIMORE MEDICAL CENTER","SIBLEY MEMORIAL HOSPITAL",
# "MEDSTAR SAINT MARY'S HOSPITAL","BON SECOURS HOSPITAL","JOHNS HOPKINS HOSPITAL, THE"")
# """