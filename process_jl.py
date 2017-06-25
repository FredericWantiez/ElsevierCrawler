import json
import pprint as pp

data_raw_filename = 'journals.jl'
data_processed_filename = data_raw_filename.split(".")[0] + ".txt"

data = []
with open(data_raw_filename) as f:
    for line in f:
        data.append(json.loads(line))

print("-- Processing {} file to {}".format(data_raw_filename,
                                           data_processed_filename))

with open(data_processed_filename, "w") as out:
    out.write("")

with open(data_processed_filename, "a") as out:
    for k in range(len(data)):
        #pp.pprint(data[k])
        ISSN, journal_name = data[k].values(), data[k].keys()
        for issn, name in zip(ISSN, journal_name):
            #print(issn, name)
            out.write(name + " " + issn + "\n")

