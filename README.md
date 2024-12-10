Patents are critical to inventors, businesses, and governments. They protect valuable intellectual property by creating guardrails aside similar innovations. Patent landscaping is the process of developing a comprehensive set of patents related to a specific topic by iteratively finding similar patents. We propose 3 unique patent embedding strategies and 2 novel evaluation metrics to build a system to match patents. Over a sample of 30 thousand patents published in 2023, we show that the summarized fulltext description section of each patent, which has been underutilized by prior work, produces the most informative patent embeddings. 

To reproduce results from the paper:

DATA ---------------------------------------------------------------------------------------------
1. We do not provide the raw patent data in the drive file below because raw data files for the year of 2023 is over 50 gigabytes of data. To access the raw patent abstract data, navigate to the "Patent Application Bibliographic (Front Page) Data (MAR 15, 2001 - PRESENT)" section of the Bulk Data Storage System. To access the raw fulltext data, navigate to the section titled "Patent Grant Full Text Data (No Images) (JAN 1976 - PRESENT)" on the Bulk Data Storage System (https://bulkdata.uspto.gov/).
2. Unzip and store all raw data files in their own folder titled the same name as the xml file extracted. Store all fulltext file folders in a single folder and all abstract file folders in a single folder. This was done with the patent_cleaning_extraction/fulltextfoldercreation.py for fulltext files.
3. With correct filepaths, run the patent_cleaning_extraction/abstractextraction.py and patent_cleaning_extraction/fulltextextraction.py to extraect individual patents into individual files and parse XML files to get the desired text. This will, by default, save individual xml files for each patent, then combine them into a single file at the end.
4. Using patent_cleaning_extraction/abstract_fulltext_combine.ipynb, the abstracts and fulltext files are matched up and generates the sample of ~29,500 patents used in the rest of this paper. This cleaned dataset is approximately 2Gb and can be accessed in the Google drive folder at the bottom of this README. It goes by the filename of "allpatents_with_abstracts_and_full_text.csv". It is advised that replication start from this point; all prior processing did not modify any of the data. We have simply just extracted and reformated data into a more accessible version.





PATENTBERT EMBEDDING -----------------------------------------------------------------------------

The embedding section took a significant amount of time because it involves a lot of inference. Across 4 instances running concurrently on T4 GPUs, it took about 15 hours to complete. 

1. To facilitate batching of inputs and distribution over multiple instances, we split concatenate title to abstracts before splitting each individual patent titleabstract and fulltext into individual txt files. Each txt file is named by the application reference document number of the patent, which we used as general IDs throughout the rest of this project.
2. To embed the individual fulltext and titleabstracts, the Embedding.ipynb can be run. By default, batches of 10 titleabstract .txt files and 10 fulltext .txt files are processed at a time. Each batch's indicies and embeddings are saved as individual .npy files.
3. All .npy files are combined to create embeddings, which are stored in the folder titled "all" in the google drive at the bottom of this README. These embeddings are the inputs to the evaluation code.





EVALUATION ---------------------------------------------------------------------------------------
1. To generate closeness and SCS metrics, download all files within the "all" folder.
2. All plots for a specific embedding (titleabstract, fulltext truncated, and fulltext) can be done with the respective similarities.ipynb file in the evaluation folder.
   

DATA DEPENDENCIES --------------------------------------------------------------------------------

Data dependencies can be found here: https://drive.google.com/drive/folders/1fwpt5AkU_q9edA2d_eTxnONyZ-gXMTes?usp=sharing
