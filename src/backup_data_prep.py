import json
import csv
import sys

# Set of relevant keywords to filter posts
keywords = {'bitcoin', 'crypto', 'cryptocurrency', 'btc', 'blockchain', 'ethereum', }
def prep_reddit_ndjson(input_file, output_file): 
    # Open input ndjson file
    with open(input_file, 'r') as f:

        # Open output CSV file for writing
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:

            # Create CSV writer object
            writer = csv.writer(csv_file)

            # Create set to store post IDs to remove duplicates
            post_ids = set()

            # Iterate over each line (post) in the ndjson file
            for line in f:

                # Parse the line as JSON
                post = json.loads(line)

                # Check if post title or body text contains any of the relevant keywords
                if any(keyword in post['title'].lower() or keyword in post['selftext'].lower() for keyword in keywords):

                    # Check if post ID is already in set to remove duplicates
                    if post['id'] not in post_ids:

                        # Add post to set of IDs
                        post_ids.add(post['id'])

                        # Write relevant post data to CSV file
                        writer.writerow([post['permalink'], post['created_utc'], post['score'], post['author'], post['title'], post['selftext']])

def write_csv(posts, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['permalink', 'created_utc', 'score', 'author', 'title', 'selftext'])

        for post in posts:
            # Escape any double quotes that are already in the fields
            title = post['title'].replace('"', '""')
            selftext = post['selftext'].replace('"', '""')

            # Enclose the title and selftext fields in quotes to handle commas and other special characters
            writer.writerow([post['permalink'], post['created_utc'], post['score'], post['author'], f'"{title}"', f'"{selftext}"'])

def sort_csv(input_file, output_file): 

    # Open CSV file and sort by created_utc in ascending order
    with open(output_file, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        sorted_posts = sorted(reader, key=lambda row: int(row[1]))

    # Write sorted data back to CSV file
    with open('relevant_posts.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(sorted_posts)



if __name__ == "__main__": 
    prep_reddit_ndjson(sys.argv[1], sys.argv[2])

