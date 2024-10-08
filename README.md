# Tử vi bot

Website chuyện dự đoán tử vi cho người dùng.

![Screenshot](./images/screenshot.png)

# Công nghệ sử dụng

- Python + flask
- Reactjs + TailwindCSS
- OpenAI
- DB lưu trữ ở file json

# Setup


Setup API:

make new file .env
```
OPENAI_API_KEY=xxx
```


```
pip install -r requirement.txt
py app.py
```

Setup frontend:

```
cd frontend
npm install
npm run dev
```



# Dữ liệu

- Spec tham khảo website.
https://tuvi.vn/

# AI bot.

- Dùng OpenAI + Llama để tạo ra câu trả lời tử vi cho người dùng.

![image](./images/2-Grafika-wykres-chunking.png)

https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_double_merging_chunking/

https://bitpeak.pl/chunking-methods-in-rag-methods-comparison/

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

- Dùng chroma để save và load vector:

Ref:
https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/

```python
from llama_index.core import ChromaIndex
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader(input_files=["pg_essay.txt"]).load_data()

index = ChromaIndex()
index.build_index(documents)
index.save_index("index")
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

- Url request sinh ra tử vi:
curl http://127.0.0.1:5000/export-tu-vi?fullname=PHAM+VAN+MINH&sex=1&year=2024&birthday=2/10/2024+0:0