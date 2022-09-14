from CommonModule import *
from LoggerModule import logs
import zipfile


def main():
    """
    Main function executing complete processes
    :return:
    """
    xml_url = config.get("Information", "xml_source_path")
    logs.info("XML url:", xml_url)

    download_path = config.get("Information", "xml_download_path")
    logs.info("Path to download XML files:", download_path)

    logs.info("Downloading xml files......")
    filename = "source.xml"

    logs.info("Downloading the xml file from link")
    xmlfile = download_xml(xml_url, download_path, filename)
    if not xmlfile:
        logs.error("Downloading xml failed")
        return

    logs.info("Parsing the downloaded xml")
    filename, downloadlink = parse_xml(xmlfile)
    logs.info("Filename and Download Link :", filename, downloadlink)
    if not downloadlink:
        logs.error("Failed to fetch download link after parsing xml")
        return

    logs.info("Downloading the zip file")
    zip_file = download_xml(downloadlink, download_path, filename)
    if not zip_file:
        logs.error("Downloading zip failed")
        return

    logs.info("Unzipping the zipped file")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(download_path)
        logs.info("Zipped file extracted successfully")
    except Exception as e:
        logs.error("Zipped file extraction failed:", e)

    logs.info("Converting contents of xml into CSV")
    csvpath = config.get("Information", "csv_path")
    if not os.path.exists(csvpath):
        logs.info("Creating CSV file path")
        os.makedirs(csvpath)
    csv_filename = zip_file.split('\\')[-1].split('.')[0]+'.csv'
    csv_file = os.path.join(csvpath, csv_filename)
    xml_fname = os.path.join(download_path, filename.split(".")[0] + ".xml")
    logs.info("Csv File name:", csv_file)
    csv_path = create_csv_from_xml(xml_fname, csv_file)
    if not csv_path:
        logs.error("Converting xml data into csv failed")
        return
    print("Converted xml data into csv")


if __name__ == "__main__":
    config = read_config()
    if config:
        main()
    else:
        logs.error("Loading Config file failed.")

