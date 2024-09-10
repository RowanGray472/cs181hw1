# cs181hw1

![Tests](https://github.com/RowanGray472/cs181hw1/actions/workflows/tests.yml/badge.svg)
 
This code takes a document file as input and returns a 1st grade level summary of that document using the Groq API. 

Here's what a sample input might look like. In this case the input file was the Declaration of Independence

```

python3 docsum.py docs/declaration.txt

```
And the corresponding output!

```

file is read
file is split into 1 chunks
chunk 1 of 1 is summarized
A long time ago, some people wrote a special paper. They were very unhappy with the king. He was being mean and not listening to them. He was making rules without asking them. They wanted to be free and make their own choices. They wrote the paper to say they want to be a new country, not part of the king's country. They said they can make their own rules and be free. They promised to always stand up for what they believe and fight for their country.

```
