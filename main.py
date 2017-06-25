import os
import re

filename = "journals.txt"
data_dir = "./Data/"

with open(filename, "r") as f:
    for k in f.readlines():
        issn = re.findall(r"(\d{4}-\d{3}[\dxX])", k)[0]
        issn_ = issn.split("-")
        issn_ = issn[0]+issn[1] 
        url_to_start_from = "http://www.sciencedirect.com/science/journal/" + issn
        print(os.path.join(data_dir, issn + ".jl"))
        os.system("scrapy crawl article -a start_url={} -o {} --nolog".format(url_to_start_from, os.path.join(data_dir, issn + ".jl")))
