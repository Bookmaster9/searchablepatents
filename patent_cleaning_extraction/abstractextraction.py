import re
import os
import xml.etree.ElementTree as ET
import pandas as pd

def split_patent_applications(xml_file_path, output_dir):
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    # Step 2: Define a regex pattern to capture each <us-patent-application ...> ... </us-patent-application> block
    pattern = re.compile(r"(<us-patent-application\b[^>]*>.*?</us-patent-application>)", re.DOTALL)

    # Find all matches
    patent_applications = pattern.findall(xml_content)

    # Step 3: Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 4: Save each matched patent application to a new XML file
    for i, application in enumerate(patent_applications, start=1):
        output_path = os.path.join(output_dir, f"patent_application_{i}.xml")
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(application)

    print(f"Saved {len(patent_applications)} patent applications to '{output_dir}'.")

def extract_data(xml_string):
    root = ET.fromstring(xml_string)

    output = {}

    # Find publication reference
    
    # Find application reference

    # Find title
    title_element = root.find(".//invention-title")
    title_text = "".join(title_element.itertext()) if title_element is not None else None
    output["title"] = title_text

    # Find classifications
    classifications = []
    classification_versions = []
    for classification in root.findall(".//classification-cpc"):
        version = classification.find("cpc-version-indicator").find("date").text
        section = classification.find("section").text
        class_ = classification.find("class").text
        subclass = classification.find("subclass").text
        main_group = classification.find("main-group").text
        subgroup = classification.find("subgroup").text
        
        # Format as sectionclasssubclass main-group/subgroup
        formatted_class = f"{section}{class_}{subclass} {main_group}/{subgroup}"
        classifications.append(formatted_class)
        classification_versions.append(version)
    output["classifications"] = classifications
    output["classification_versions"] = classification_versions
    
    # Find Abstract
    abstract_element = root.find(".//abstract")
    abstract_text = "".join(abstract_element.itertext()) if abstract_element is not None else None
    output["abstract_text"] = abstract_text
    
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
        for app_ref in application_reference_element:
            doc_id = app_ref.find("document-id")
            if doc_id is not None:
                output["app_ref_country"] = doc_id.find('country').text
                output["app_ref_doc_number"] = doc_id.find('doc-number').text
                output["app_ref_date"] = doc_id.find('date').text

    # Orgname information
    assignees_orgnames = []
    assignees_cities = []
    assignees_countries = []
    assignees_element = root.findall(".//assignees")
    if assignees_element is not None:
        for assign in assignees_element:
            assignee_element = assign.find("assignee")
            if assignee_element is not None:
                assignee_addressbook_element = assignee_element.find("addressbook")
                if assignee_addressbook_element is not None:
                    orgname = assignee_addressbook_element.find("orgname")
                    if orgname is not None:
                        assignees_orgnames.append(orgname.text)
                    else:
                        assignees_orgnames.append(None)
                    assignee_address_element = assignee_addressbook_element.find("address")
                    if assignee_address_element is not None:
                        try:
                            assignees_cities.append(assignee_address_element.find("city").text)
                        except:
                            assignees_cities.append(None)
                        try:
                            assignees_countries.append(assignee_address_element.find("country").text)
                        except:
                            assignees_countries.append(None)
                    else:
                        assignees_cities.append(None)
                        assignees_countries.append(None)
                else:
                    assignees_orgnames.append(None)
                    assignees_cities.append(None)
                    assignees_countries.append(None)
                
    output["assignees_orgnames"] = assignees_orgnames
    output["assignees_cities"] = assignees_cities
    output["assignees_countries"] = assignees_countries

    # Inventor Information
    inventors_last_names = []
    inventors_first_names = []
    inventors_cities = []
    inventors_countries = []
    inventors = root.findall(".//inventors")
    if inventors is not None:
        for inv in inventors:
            inventor_element = inv.findall("inventor")
            if inventor_element is not None:
                for inventor in inventor_element:
                    if inventor is not None:
                        inventor_addressbook_element = inventor.find("addressbook")
                        if inventor_addressbook_element is not None:
                            try:
                                inventors_last_names.append(inventor_addressbook_element.find("last-name").text)
                                inventors_first_names.append(inventor_addressbook_element.find("first-name").text)
                            except:
                                inventors_last_names.append(None)
                                inventors_first_names.append(None)
                        else:
                            inventors_last_names.append(None)
                            inventors_first_names.append(None)
                        inventor_address_element = inventor_addressbook_element.find("address")
                        if inventor_address_element is not None:
                            try:
                                inventors_cities.append(inventor_address_element.find("city").text)
                                inventors_countries.append(inventor_address_element.find("country").text)
                            except: 
                                inventors_cities.append(None)
                                inventors_countries.append(None)
                        else:
                            inventors_cities.append(None)
                            inventors_countries.append(None)
                    else:
                        inventors_last_names.append(None)
                        inventors_first_names.append(None)
                        inventors_cities.append(None)
                        inventors_countries.append(None)
    output["inventors_last_names"] = inventors_last_names
    output["inventors_first_names"] = inventors_first_names
    output["inventors_cities"] = inventors_cities
    output["inventors_countries"] = inventors_countries
    
    return output


for week in os.listdir('rawdata2023'):
    print(week)
    try:
        week_date = week.split('_')[0].split('ipab',1)[1]
        with_ipad = week.split('_')[0]
    except:
        continue
    # if not os.path.isdir(f'rawdata2023/{week}/individuals'):
    #     os.mkdir(f'rawdata2023/{week}/individuals')
    # split_patent_applications(f'rawdata2023/{week}/{with_ipad}.xml', f'rawdata2023/{week}/individuals')

    to_consolidate = []

    for filename in os.listdir(f"rawdata2023/{week}/individuals"):
        with open(f"rawdata2023/{week}/individuals/{filename}", "r", encoding="utf-8") as file:
            xml_string = file.read()
            to_consolidate.append(extract_data(xml_string))

    # consolidate into a single data frame to output as a csv
    df = pd.DataFrame(to_consolidate)
    df.to_csv(f"rawdata2023/{week}/individuals_consolidated.csv", index=False)
    


# Combine all into a single consolidated csv file
data_frames = []

for week_folder in os.listdir('rawdata2023'):
    week_path = os.path.join('rawdata2023', week_folder)
    
    if os.path.isdir(week_path):
        csv_path = os.path.join(week_path, 'individuals_consolidated.csv')
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df['week'] = week_folder
            data_frames.append(df)
combined_df = pd.concat(data_frames, ignore_index=True)

combined_df.to_csv('allpatents_with_ids.csv', index=False)

