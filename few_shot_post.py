import json 
import pandas as pd 

class fewshot():
    def __init__(self,file_path ="processed_file.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)
        

    def load_posts(self,file_path):
        with open(file_path, encoding="utf-8") as file:
            post = json.load(file)
            self.df = pd.json_normalize(post)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            all_tags = self.df['tags'].sum()
            self.unique_tags = set(list(all_tags))
        


    def categorize_length(self , line_count):
        if line_count < 5 :
            return "short"
        elif 5<= line_count <=10:
            return "medium"
        else:
            return "long"
    

    def get_unique_tags(self):   #getting unique tags from load_post()
        return self.unique_tags
    
    def get_filtered_posts(self,language,length,tag):
        df_filter = self.df[
            (self.df['language'] == language) &
            (self.df['length']== length) &
            (self.df['tags'].apply(lambda tags: tag in tags))
            ]

        return df_filter.to_dict(orient="records")

if __name__ == "__main__":
    fs = fewshot()
    posts = fs.get_filtered_posts("english","short","Scams")
    print(posts)