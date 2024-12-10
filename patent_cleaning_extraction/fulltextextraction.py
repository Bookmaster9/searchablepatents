import re
import os
import xml.etree.ElementTree as ET
import pandas as pd

def split_patent_applications(xml_file_path, output_dir):
    print("splitting", xml_file_path)
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    # Step 2: Define a regex pattern to capture each <us-patent-application ...> ... </us-patent-application> block
    pattern = re.compile(r"(<us-patent-grant\b[^>]*>.*?</us-patent-grant>)", re.DOTALL)

    # Find all matches
    patent_applications = pattern.findall(xml_content)

    # Step 3: Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 4: Save each matched patent application to a new XML file
    for i, application in enumerate(patent_applications, start=1):
        output_path = os.path.join(output_dir, f"patent_publication_{i}.xml")
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(application)

    print(f"Saved {len(patent_applications)} patent publications to '{output_dir}'.")

    # Delete original file
    os.remove(xml_file_path)

def extract_data(xml_string):
    root = ET.fromstring(xml_string)

    output = {}

    # Find title
    title_element = root.find(".//invention-title")
    title_text = "".join(title_element.itertext()) if title_element is not None else None
    output["title"] = title_text

    # Publication Reference Numbers
    publication_reference_element = root.findall(".//publication-reference")
    if publication_reference_element is not None:
        for pub_ref in publication_reference_element:
            doc_id = pub_ref.find("document-id")
            if doc_id is not None:
                output["pub_ref_country"] = doc_id.find('country').text
                output["pub_ref_doc_number"] = doc_id.find('doc-number').text
                output["pub_ref_kind"] = doc_id.find('kind').text
                output["pub_ref_date"] = doc_id.find('date').text

    # Application Reference Information
    application_reference_element = root.findall(".//application-reference")
    if application_reference_element is not None:
        for doc_id in application_reference_element:
            doc_id = doc_id.find("document-id")
            if doc_id is not None:
                output["app_ref_country"] = doc_id.find('country').text
                output["app_ref_doc_number"] = doc_id.find('doc-number').text
                output["app_ref_date"] = doc_id.find('date').text

    # Find full text
    description_reference_element = root.findall(".//description")
    description_text = []
    for element in description_reference_element:
        if element is not None:
            for ptag in element.findall(".//p"):
                description_text.append("".join(ptag.itertext()))
    description_text_combined = " ".join(description_text)
    # Remove all /n and /t characters
    description_text = description_text_combined.replace("\n", " ").replace("\t", " ")
    # Remove all extra spaces
    description_text = re.sub(' +', ' ', description_text)
    output["description_text"] = description_text
    return output


for week in os.listdir('fulltextrawdata2023'):
    print(week)
    if week == ".DS_Store":
        continue
    if not os.path.exists(f'fulltextrawdata2023/{week}/individuals'):  
        split_patent_applications(f'fulltextrawdata2023/{week}/{week}.xml', f'fulltextrawdata2023/{week}/individuals')

    if not os.path.exists(f"fulltextrawdata2023/{week}/individuals_consolidated.csv"):
        to_consolidate = []

        for filename in os.listdir(f"fulltextrawdata2023/{week}/individuals"):
            with open(f"fulltextrawdata2023/{week}/individuals/{filename}", "r", encoding="utf-8") as file:
                xml_string = file.read()
                to_consolidate.append(extract_data(xml_string))

        # consolidate into a single data frame to output as a csv
        df = pd.DataFrame(to_consolidate)
        df.to_csv(f"fulltextrawdata2023/{week}/individuals_consolidated.csv", index=False)


# # Combine all into a single consolidated csv file
# data_frames = []

# for week_folder in os.listdir('rawdata2023'):
#     week_path = os.path.join('rawdata2023', week_folder)
    
#     if os.path.isdir(week_path):
#         csv_path = os.path.join(week_path, 'individuals_consolidated.csv')
        
#         if os.path.exists(csv_path):
#             df = pd.read_csv(csv_path)
#             df['week'] = week_folder
#             data_frames.append(df)
# combined_df = pd.concat(data_frames, ignore_index=True)

# combined_df.to_csv('allpatents.csv', index=False)

