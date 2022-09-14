import configparser
from LoggerModule import logs
import requests
import os
import xml.etree.ElementTree as ET
import pandas as pd


def read_config():
    """
        Read config file and return the config object
        :return: config object
    """
    try:
        logs.info("Reading config file")
        config_parser = configparser.RawConfigParser()
        config_parser.read("config.ini")
    except Exception as e:
        logs.error("Exception while reading config file - ", e)

    return config_parser


def download_xml(url, download_path, filename):
    """
    :param url: source url to download file
    :param download_path: path where downloaded file can be saved
    :param filename: filename of the downloaded file
    :return:
    """
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        file_name = os.path.join(download_path, filename)

        response = requests.get(url)
        with open(file_name, 'wb') as file:
            file.write(response.content)

        logs.info("xml file got downloaded.")

    except Exception as e:
        logs.error("Exception : ", e)

    return file_name


def parse_xml(xml_file):
    """
    :param xml_file: xml file path which needs to be parsed
    :return:
    """
    try:
        logs.info("Parsing xml file")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        logs.info("Traversing through all doc tag elements")
        for each_doc in root.findall("."):
            file_type = each_doc.find(".//str[@name='file_type']")
            logs.info("Checking if file typs is DLTINS")
            if file_type.text == "DLTINS":
                logs.info("Found file type with DLTINS")
                file_name = each_doc.find(".//str[@name='file_name']").text
                download_link = each_doc.find(".//str[@name='download_link']").text
            break
        else:
            logs.info("Not found any download link with file type DLTINS")
    except Exception as e:
        logs.error("Exception - Parsing XML :", e)

    return file_name, download_link


def create_csv_from_xml(xml_file, csvpath):
    """
    :param xml_file: xml file path
    :param csvpath: path where csv file need to store
    :return:
    """
    # columns of dataframe
    columns = [
            "FinInstrmGnlAttrbts.Id",
            "FinInstrmGnlAttrbts.FullNm",
            "FinInstrmGnlAttrbts.ClssfctnTp",
            "FinInstrmGnlAttrbts.CmmdtyDerivInd",
            "FinInstrmGnlAttrbts.NtnlCcy",
            "Issr",
        ]
    # Creating dataframe with above columns
    df = pd.DataFrame(columns=columns)
    final_data = []

    iter_data = ET.iterparse(xml_file, events=("start",))
    for event, element in iter_data:
        if event == "start":
            data = {}
            required_elements = [(elem.tag, elem) for elem in element if "FinInstrmGnlAttrbts" in elem.tag or "Issr" in
                                 elem.tag]
            for elem_tag, elem in required_elements:
                if "FinInstrmGnlAttrbts" in elem_tag:
                    for each_ele in elem:
                        if "Id" in each_ele.tag:
                            data[columns[0]] = each_ele.text
                        elif "FullNm" in each_ele.tag:
                            data[columns[1]] = each_ele.text
                        elif "ClssfctnTp" in each_ele.tag:
                            data[columns[2]] = each_ele.text
                        elif "CmmdtyDerivInd" in each_ele.tag:
                            data[columns[3]] = each_ele.text
                        elif "NtnlCcy" in each_ele.tag:
                            data[columns[4]] = each_ele.text
                else:
                    data[columns[5]] = each_ele.text
            final_data.append(data)

    df = df.append(final_data, ignore_index=True)
    df.dropna(inplace=True)
    logs.info("Creating CSV file and adding data into that")
    df.to_csv(csvpath, index=False)
    return csvpath




