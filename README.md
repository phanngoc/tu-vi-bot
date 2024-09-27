# Tử vi bot

Website chuyện dự đoán tử vi cho người dùng.

# Công nghệ sử dụng

- Python + flask
- Reactjs + TailwindCSS
- OpenAI
- DB lưu trữ ở file json

# Dữ liệu

- Spec tham khảo website.
https://tuvi.vn/

# AI bot.

Dùng OpenAI + Llama để tạo ra câu trả lời tử vi cho người dùng.

https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_double_merging_chunking/


```
from llama_index.core.node_parser import (
    SemanticDoubleMergingSplitterNodeParser,
    LanguageConfig,
)
from llama_index.core import SimpleDirectoryReader
```

- Load document and create sample splitter:

```python
documents = SimpleDirectoryReader(input_files=["pg_essay.txt"]).load_data()

config = LanguageConfig(language="english", spacy_model="en_core_web_md")
splitter = SemanticDoubleMergingSplitterNodeParser(
    language_config=config,
    initial_threshold=0.4,
    appending_threshold=0.5,
    merging_threshold=0.5,
    max_chunk_size=5000,
)
```

```python
nodes = splitter.get_nodes_from_documents(documents)
print(nodes[0].get_content())
```


## API:

Call BOT:

POST: /api/answer

Params:
```
{
    type: "direct|suggest", // type='direct' thì trả lờit trực tiếp nên choice sẽ = null
    question: "Câu hỏi của người dùng",
    params: {
        choice: 3 (id từ actions phía dưới)
    }
}
```

Response:
```
{
    code: 200,
    message: "Cau trả lời của bot",
    actions: [
        {
            id: 1,
            type: "text",
            content: "Nội dung câi trả lời",
        },
        {
            id: 2,
            type: "image",
            content: "url hình ảnh",
        },
        {
            id: 3,
            type: "video",
            content: "url video",
        },
    ]
}
```