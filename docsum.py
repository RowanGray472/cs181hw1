"""
TERMINAL COMMANDS WE NEED TO RUN THIS CODE:

1. python3 -m venv env
2. source env/bin/activate
3. pip install -r requirements.txt
4. python3 docsum.py <filename>

"""

def split_document_into_tokens(text, max_tokens=29000):
    """
    Split the input text into smaller chunks based on the number of tokens.
    Each chunk contains up to `max_tokens` tokens.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        # +1 for the space or newline that will follow the word
        # *2 because each word is assumed to have, on average, two tokens
        if (len(current_chunk) * 2) + len(word) + 1 > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)

    # Don't forget the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


if __name__ == '__main__':

    import os
    from groq import Groq

    # parse command line args
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    # line 7+8 => args.filename will contain the first string after program name on command line
    
    from dotenv import load_dotenv
    load_dotenv()

    client = Groq(
        # This is the default and can be omitted
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    from bs4 import BeautifulSoup
    from pdfminer.high_level import extract_text
    import chardet

    def read_file(filename):
        with open(filename, 'rb') as f:
            result = chardet.detect(f.read())
            charenc = result['encoding']

        if filename.endswith('.html'):
            with open(filename, 'r', encoding=charenc) as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text()
        elif filename.endswith('.pdf'):
            text = extract_text(filename)
        else:
            with open(filename, 'r', encoding=charenc) as f:
                text = f.read()
        return text

    text = read_file(args.filename)


    print("file is read")

    '''
    We need to call the split_document_into_chunks on text.
    Then for each paragraph in the output list,
    call the LLM code below to summarize it.
    Put the summary into a new list.
    Concatenate that new list into one smaller document.
    Recall the LLM code below on the new smaller document.
    '''

    summary_list = []

    chunks = split_document_into_tokens(text)

    print(f"file is split into {len(chunks)} chunks")
    counter = 0

    for chunk in chunks:

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': 'Summarize the input text below.  Limit the summary to 1 paragraph and use a 1st grade reading level.',
                },
                {
                    "role": "user",
                    "content": chunk,
                }
            ],
            model="llama3-8b-8192",
        )
        summary_list.append(chat_completion.choices[0].message.content)
        counter += 1
        print(f"chunk {counter} of {len(chunks)}is summarized")

    summary = ' '.join(summary_list)

    chat_completion = client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': 'Summarize the input text below.  Limit the summary to 1 paragraph and use a 1st grade reading level.',
                },
                {
                    "role": "user",
                    "content": summary,
                }
            ],
            model="llama3-8b-8192",
        )
    print(chat_completion.choices[0].message.content)