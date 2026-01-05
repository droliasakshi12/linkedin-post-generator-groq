import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm


# creating a function to access file and adding the other tags like no of lines,language,tags  
def access_files(raw_file_path,processed_file_path = "processed_file.json"):
    post_list = []
    with open(raw_file_path,encoding='utf-8') as file:  #getting json file 
        data = json.load(file)

        for post in data:
            metadata = extract_data(post['text'])
            post_with_metadat = post | metadata  # getting post data along with metadata
            post_list.append(post_with_metadat)

    unified_tags = get_unified_tags(post_list)

    for posts in post_list:
        current_tags = posts['tags'] #getting tags from post list
        new_tags = {unified_tags[tag] for tag in current_tags} #created set so there is no duplicate values.
        posts['tags'] = list(new_tags) 

    with open(processed_file_path,encoding ="utf-8",mode='w') as outputfile:
        json.dump(post_list,outputfile,indent=4)



def get_unified_tags(posts_with_metadata):
    unique_tags = set()

    for post in posts_with_metadata:
        unique_tags.update(post['tags'])
    
    unique_tags_list = ",".join(unique_tags)

    template = """
        I will give you a list of tags.you need to unify them with the following requirements.
        1.Tags are unified and merged to create a shorter list.
            Example 1 :"JObseeker","Job hunting" can all be merged in "Job search".
            Example 2 :"Motivation","Insipration","Drive" can be merged in "Motivation".
            Example 3 :"Personal Growth" , "Personal development" ,"Self Improvement" can be mapped in "Self Assesment".
            Example 4 :"Scam Alert",Job Scam" etc , can be mapped "Scams".
        2. Each tag should be follow title case convetion.Example : "Motivation","Job Search" ,"Self Assesment".
        3.output should be json object. Not preamble.
        4.Output should have mapping of original tag and unified tags.
        For example : {{"Jonseeker":"job Search","job hunting":"Job Search","Motivaion":"Motivation"}}

        here is list of tags:
        {tags}        
        """
 
    pt = PromptTemplate.from_template(template)  #prompt template 
    chain = pt | llm
    response =  chain.invoke(input = {"tags": str(unique_tags_list)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("content too big to parse json.")

    return res 


def extract_data(post):
    template = f"""
        you are gievn a linkedin post.you have to extract lines , language of posts and tags.
        1.retrun a valid json. no preamble.
        2.json objects should have exactly three keys line_count , language and tags.
        3.tags is an array of text tags . extract minimum two tags.
        4.language should be english or hinglish(hinglish means english+hindi)
        here is the actual posts whic you need to perform this tasks:
        {post}
        """
    
    pt = PromptTemplate.from_template(template)
    chain = pt | llm 
    response = chain.invoke(input = {'post': post})

    try:
        json_parser  = JsonOutputParser()
        res = json_parser.parse(response.content)

    except OutputParserException:
        raise OutputParserException("context too big unable to parse jobs.")
    
    return res 


if __name__ == "__main__":
    access_files("raw_data.json","processed_file.json")



