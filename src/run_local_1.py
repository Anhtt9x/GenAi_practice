from langchain.prompts import PromptTemplate
from langchain_community.llms.ctransformers import CTransformers
from langchain.chains.llm import LLMChain
from src.hepler import *


B_INST , E_INST = "[INST]" , "/INST"

B_SYS , E_SYS = "<<SYS>>\n" , "\n<<SYS>>\n\n"

instruction = "Convert the follow text from English to French: \n\n {text}"

SYSTEM_PROMPT = B_SYS + CUSTOM_SYSTEM_PROMPT + E_SYS

template = B_INST + SYSTEM_PROMPT + instruction + E_INST

prompt = PromptTemplate(template=template, input_variables=["text"])

llm = CTransformers(model="model/llama-2-7b-chat.ggmlv3.q8_0.bin", model_type="llama",
                    config={'max_new_tokens':128, 'temperature':0.7}
                    )

chains = LLMChain(llm=llm, prompt=prompt)

print(chains.invoke("How are you ?"))