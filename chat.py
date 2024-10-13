from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from lunarcalendar import Converter, Solar
from datetime import datetime

import os
from dotenv import load_dotenv
import chromadb
from llama_index.core import Settings

from llama_index.core.agent import ReActAgent
from llama_index.agent.openai import OpenAIAssistantAgent
from llama_index.core.output_parsers import PydanticOutputParser
from enum import Enum
from pydantic import BaseModel, Field
from typing import List
from llama_index.core.program import FunctionCallingProgram
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

MODEL_NAME = "gpt-4o-mini"
MODEL_EMBEDDING_NAME = "text-embedding-3-small"

load_dotenv()  # take environment variables from .env.
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

embed_model = OpenAIEmbedding(model=MODEL_EMBEDDING_NAME, dimensions=1536)
llm = OpenAI(model=MODEL_NAME)


def convert_to_lunar(year, month, day):
    solar = Solar(year, month, day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar


def get_thien_can_dia_chi(year):
    can = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
    chi = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
    can_index = year % 10
    chi_index = year % 12
    return can[can_index], chi[chi_index]


def get_cuc(thien_can):
    cuc_mapping = {
        'Kim': ['Canh', 'Tân'],
        'Mộc': ['Giáp', 'Ất'],
        'Thủy': ['Nhâm', 'Quý'],
        'Hỏa': ['Bính', 'Đinh'],
        'Thổ': ['Mậu', 'Kỷ']
    }
    for key, values in cuc_mapping.items():
        if thien_can in values:
            return key
    return None


def get_gio_sinh(hour):
    gio_mapping = {
        'Tý': 0, 'Sửu': 1, 'Dần': 2, 'Mão': 3,
        'Thìn': 4, 'Tỵ': 5, 'Ngọ': 6, 'Mùi': 7,
        'Thân': 8, 'Dậu': 9, 'Tuất': 10, 'Hợi': 11
    }
    return list(gio_mapping.keys())[hour % 12]


def an_sao_tuvi(day, month, year, hour):
    cung_names = ['Mệnh', 'Phụ Mẫu', 'Phúc Đức', 'Điền Trạch', 'Quan Lộc', 'Nô Bộc', 
                  'Thiên Di', 'Tật Ách', 'Tài Bạch', 'Tử Tức', 'Phu Thê', 'Huynh Đệ']
    
    thien_can, dia_chi = get_thien_can_dia_chi(year)
    cuc = get_cuc(thien_can)
    gio_sinh = get_gio_sinh(hour)
    
    cung_chi_mapping = {
        'Tý': 'Mệnh', 'Sửu': 'Phụ Mẫu', 'Dần': 'Phúc Đức', 'Mão': 'Điền Trạch',
        'Thìn': 'Quan Lộc', 'Tỵ': 'Nô Bộc', 'Ngọ': 'Thiên Di', 'Mùi': 'Tật Ách',
        'Thân': 'Tài Bạch', 'Dậu': 'Tử Tức', 'Tuất': 'Phu Thê', 'Hợi': 'Huynh Đệ'
    }
    
    chinh_tinh = {
        'Tử Vi': 'Thìn', 'Thiên Phủ': 'Tuất', 'Thái Dương': 'Dần', 'Thái Âm': 'Hợi',
        'Thiên Cơ': 'Sửu', 'Thiên Lương': 'Ngọ', 'Vũ Khúc': 'Thân', 'Thiên Đồng': 'Tý',
        'Cự Môn': 'Dậu', 'Liêm Trinh': 'Mão', 'Thất Sát': 'Mùi', 'Phá Quân': 'Tỵ',
        'Tham Lang': 'Dậu'
    }
    
    phu_tinh = {
        'Hóa Khoa': 'Mệnh', 'Hóa Quyền': 'Quan Lộc', 'Hóa Lộc': 'Tài Bạch', 'Hóa Kỵ': 'Phu Thê'
    }
    
    sao_cung = {cung: [] for cung in cung_names}
    
    for sao, chi_name in chinh_tinh.items():
        cung = cung_chi_mapping[chi_name]
        sao_cung[cung].append(sao)
    
    for sao, cung in phu_tinh.items():
        sao_cung[cung].append(sao)
    
    response = f"Lá số cho {day}/{month}/{year} giờ {gio_sinh}\n"
    response += f"Thiên Can: {thien_can}, Địa Chi: {dia_chi}, Cục: {cuc}\n"
    for cung, sao_list in sao_cung.items():
        response += f"Cung {cung}: các sao : {', '.join(sao_list) if sao_list else 'Không có sao'}\n"

    return response


def fn_an_sao(birthday: str, hour: str):
    """Trích xuất birthday[date + hour] từ text người dùng nhập và gán sao theo các [cung mệnh, chính tinh và phụ tinh]"""
    date_obj = datetime.strptime(birthday, "%d/%m/%Y")
    hour_int = int(hour.split(':')[0])

    lunar_date = convert_to_lunar(date_obj.year, date_obj.month, date_obj.day)
    results = an_sao_tuvi(lunar_date.day, lunar_date.month, lunar_date.year, hour_int)

    return results


prompt_template_str = """\
Extract info birthday(date + hour) from query:
{query}
"""

class User(BaseModel):
    """Data model for user info."""
    birthday: str
    hour: str
    name: str


programInfoUser = FunctionCallingProgram.from_defaults(
    output_cls=User,
    prompt_template_str=prompt_template_str,
    verbose=True,
)

# [Optional] Add Context
context = """\
Bạn là một ông thầy chuyên bói toán tử vi.\
bạn sẽ trả lời tư vấn cho người dùng về công danh, sự nghiệp, tình cảm, gia đình trong năm đó
"""

class CungMenh(Enum):
    MENH = "Mệnh"
    PHU_MAU = "Phụ Mẫu"
    PHUC_DUC = "Phúc Đức"
    DIEN_TRACH = "Điền Trạch"
    QUAN_LOC = "Quan Lộc"
    NO_BOC = "Nô Bộc"
    THIEN_DI = "Thiên Di"
    TAT_ACH = "Tật Ách"
    TAI_BACH = "Tài Bạch"
    TU_TUC = "Tử Tức"
    PHU_THE = "Phu Thê"
    HUYNH_DE = "Huynh Đệ"

class VanMenhTheoCung(BaseModel):
    """Data model vận mệnh theo cung và các diễn giải theo cung"""

    cung: CungMenh
    summary: str = Field(
        description="Mô tả chung về cung",
    )
    diengiai: str = Field(
        description="Diễn giải vận mệnh theo cung",
    )
    
class Tuvi(BaseModel):
    """Data model lá bài tử vi."""

    name: str
    birthday: str = Field(
        description="Ngày/Tháng/Năm sinh",
    )
    hour: str = Field(
        description="Giờ sinh",
    )
    vanmenh: List[VanMenhTheoCung]

def create_and_load_index():
    persist_dir = "./storage/"
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=persist_dir,
        )
        index = load_index_from_storage(storage_context)
        index_loaded = True
    except:
        index_loaded = False
    
    if not index_loaded:
        docs = SimpleDirectoryReader(
            input_dir="./data/",
        ).load_data()
        index = VectorStoreIndex.from_documents(docs)
        index.storage_context.persist(persist_dir)

    return index

tu_vi_index = create_and_load_index()

llm_4 = OpenAI(model="gpt-4o-mini")

query_engine = tu_vi_index.as_query_engine(
    output_cls=Tuvi, response_mode="tree_summarize", llm=llm, context=context
)

def prompt_to_predict(questionMessage = ''):
    programInfoUser_response = programInfoUser(query=questionMessage)

    an_sao_res = fn_an_sao(programInfoUser_response.birthday, programInfoUser_response.hour)
    query_engine_response = query_engine.query(questionMessage + an_sao_res)
    print('prompt_to_predict:' + str(query_engine_response))
    return str(query_engine_response)
