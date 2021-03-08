import os
import pandas as pd
import xml.etree.ElementTree as ElT
from bs4 import BeautifulSoup
from tqdm import tqdm
from typing import Union

def parse_xml_to_csv(xml_path: Union[os.PathLike, str],
                save_path: Union[os.PathLike, str]=None) -> pd.DataFrame:
    """Open .xml posts dump and convert the text to a csv, tokenizing it in the
         process

    Args:
        xml_path (Union[os.PathLike, str]): path to the xml document containing posts
        save_path (Union[os.PathLike, str], optional): path where you want to save the processed data in form of csv.
         Defaults to None.

    Returns:
        pd.DataFrame: a dataframe of processed text
    """

    # parse xml file
    doc = ElT.parse(xml_path)
    root = doc.getroot()

    # each row is a question 
    all_rows = [row.attrib for row in root.findall('row')]
    
    # Using tdqm to display progress since preprocessing takes time
    for item in tqdm(all_rows):
        # Decode text from HTML
        soup = BeautifulSoup(item["Body"], features="html.parser")
        item["body_text"] = soup.get_text()

    # Create dataframe from our list of dictionaries
    df = pd.DataFrame.from_dict(all_rows)
    if save_path:
        df.to_csv(save_path)
    return df




    