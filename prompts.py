# prompts.py

prompts = {
    "system_message": (
        """
You are an AI language model. Your task is to follow the provided outline and ensure that the content is well-structured, SEO-friendly, and addresses the key points in each section.
Make sure to use clear, concise language and provide practical advice, examples, and tips where applicable.
"""),
    "article_prompt": (
        """
Please write an informative and SEO-optimized article about the topic '{}' following the given outline:\n\n{}\n
Please provide the output in semantic HTML format (there is no need for the H1)."""),
    "related_links_prompt": (
        """
In your HTML output, incorporate the following related links into the article text by using relevant anchor text when applicable. Here are the related links to incorporate:\n\n{}.
""")
}
