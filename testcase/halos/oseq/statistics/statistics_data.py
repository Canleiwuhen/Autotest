# -*- coding: utf-8 -*-


class DataList:
    search_data = {
        "tumorType": "106",
        "productNo": "LD0160",
        "receivedDate": "1767542400000,1767542400000",
        "doctorId": 1,
        "departmentId": 1,
        "hospitalId": 1
    }

    somatic_data = {
        "tumorType": "100",
        "productNo": "LD0160",
        "receivedDate": "1767542400000,1767542400000",
        "doctorId": 4,
        "departmentId": 1,
        "hospitalId": 1,
        "gene": "gene"
    }

    somatic_nucleotide_data = {
        "gene": "",
        "secondGene": "TP53",
        "nucleotideResult": "s",
        "proteinResult": "s"
    }

    germline_data = {
        "gene": "",
        "secondGene": "A",
        "nucleotideResult": "P",
        "proteinResult": "S"
    }

    germline_verify_export_data = {
        "gene": "",
        "secondGene": "",
        "nucleotideResult": "",
        "proteinResult": "",
        "verifyType": 0
    }

    germline_gene_export_data = {
        "gene": "FANCA",
        "secondGene": "",
        "nucleotideResult": "",
        "proteinResult": ""
    }

    lib_data = {
        "gene": "",
        "nucleotideResult": "",
        "proteinResult": "",
        "msiResult": "",
        "category": "1",
        "size": 100,
        "page": 1
    }

    germline_read_data = {
        "gene": "",
        "nucleotideResult": "",
        "proteinResult": "",
        "msiResult": "",
        "size": 100,
        "page": 1
    }