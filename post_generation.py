from llm_helper import llm 
from few_shot_post import fewshot

fs = fewshot()

def get_prompt(language,length,tag):
    prompt=f"""
    generate a linkedin post using the below information,no preambles.
    length:{length},
    language:{language},
    tags:{tag}
    if language is hinglish it means the mix of english and hindi language.

    based on the given information just generate a post.
    do not include any unnecessary hastags.
    """
    
    example = fs.get_filtered_posts(language, length ,tag)

    if len(example)>0:
        prompt+="4)use the writing stye according to the above example."
        
        for i , post in enumerate(example):
            post_text = post['text']
            prompt+=f"\n\n example{i+1}\n\n{post_text}"

            if i == 1:
                break

    return prompt 

def generate_post(language,length,tag):
    prompt = get_prompt(language,length,tag)
    response = llm.invoke(prompt)
    return response.content


if __name__=="__main__":
    post = generate_post("english","long","Job Search")
    print(post)