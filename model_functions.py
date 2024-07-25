from transformers import AutoModelForCausalLM,AutoTokenizer
import streamlit as st
import torch

@st.cache_resource(show_spinner='Loading the Gemma model. Be patient🙏')
def LOAD_GEMMA():
  model_id = "aryachakraborty/GEMMA-2B-NL-SQL"
  tokenizer = AutoTokenizer.from_pretrained(model_id)
  model = AutoModelForCausalLM.from_pretrained(model_id).cpu()
  return tokenizer,model

@st.cache_resource(show_spinner='Loading the DeepSeek Coder model. Be patient🙏')
def DeepSeekCoder(user_input, context):
  model_id='aryachakraborty/DeepSeek_1.3B_Fine_Tuned'
  tokenizer = AutoTokenizer.from_pretrained(model_id)
  model = AutoModelForCausalLM.from_pretrained(model_id
                                               ).cpu()
  device = torch.device("cpu")
  alpeca_prompt = f"""You are an AI programming assistant, utilizing the Deepseek Coder model, developed by arya chakraborty, and your task is to convert natural language to sql queries. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.\n
            Below are sql tables schemas paired with instruction that describes a task. Using valid SQLite, write a response that appropriately completes the request for the provided tables.
            ### Instruction: {user_input}. ### Input: {context}
                                ### Response:
                                """
  inputs = tokenizer([alpeca_prompt.format(user_input=user_input, context=context)], return_tensors="pt").to(device)
  outputs = model.generate(**inputs, max_new_tokens=30)
  output = tokenizer.decode(outputs[0], skip_special_tokens=True)
  response_portion = output.split("### Response:")[-1].strip()
  return response_portion