# Combines provided folder with documents into a collection
# Michael Kyeyune
# 13th May, 2016

import sys
import glob

def main():
    if len(sys.argv)==1:
        print("Syntax: collect.py <testbed>")
        exit(0)
    test_bed_name = sys.argv[1]
    document_names = glob.glob(test_bed_name + "/document*")

    # create collection to write document content to
    g = open(test_bed_name + "_collection", 'w', encoding='utf-8')
    for document_name in document_names:
        temp_arr = document_name.split('.')
        document_id = temp_arr[1]
        try:
            f = open(document_name, "r", encoding='utf-8')
            lines = f.readlines()
            f.close()
            print(".I", document_id, sep=' ', file=g)
            print(".T", file=g)
            print(document_name, file=g)
            print(".W", file=g)
            for line in lines:
                print(line, file=g)
        except:
            pass
    g.close()
main()
