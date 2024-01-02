import gradio as gr
from MongoSearch import MongoSearch

# Initialize MongoSearch
mongo_search = MongoSearch()

with gr.Blocks(title="Research Paper Semantic Search App") as demo:
    gr.Markdown(
        """
        # Research Paper Semantic Search App
        
        Enter a query to perform semantic search on sample arXiv cs papers
        """       
        )
    with gr.Row():
        input = gr.Text(label="Query")
    with gr.Row():
        output = gr.DataFrame(wrap=True, height=700, interactive=True)
    button = gr.Button(value="Search")
    button.click(mongo_search.search, inputs=input, outputs=output)
    gr.Markdown(
        """
        Use the examples below to get started!
        """       
        )
    examples = gr.Examples(
        [ 
            ["Using machine learning to speed up drug discovery"],
            ["Applying deep learning to the stock market"],
            ["Computer vision to detect cancer in medical images"]
        ],
        label="Examples",
        inputs=input,
        outputs=output,
        cache_examples=True,
        fn=mongo_search.search,
        preprocess=True
    )
    gr.Markdown(
        """
        You can access each paper directly on [ArXiv](https://arxiv.org/) using these links:
        - `https://arxiv.org/abs/{id}`: Page for this paper including its abstract and further links
        - `https://arxiv.org/pdf/{id}`: Direct link to download the PDF
        """       
        )

# Create the Gradio interface
# iface = gr.Interface(
#     title="Research Paper Semantic Search App",
#     fn=mongo_search.search,
#     inputs=gr.Textbox(placeholder="Enter a query to perform semantic search on sample arXiv cs papers"),
#     description="Enter a query to perform semantic search on sample arXiv cs papers",
#     examples=[
#         ["Using machine learning to speed up drug discovery"],
#         ["Applying deep learning to the stock market"],
#         ["Computer vision to detect cancer in medical images"]
#     ],
#     cache_examples=True,
#     outputs=gr.DataFrame(wrap=True, min_width=1000)
# )

# Run the Gradio interface
demo.launch()
