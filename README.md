---
title: Streanlit GEMMA 2B & Deepseek Coder 1.3B
emoji: 📉
colorFrom: gray
colorTo: gray
sdk: streamlit
sdk_version: 1.31.1
app_file: app.py
run_code: streamlit run app.py
pinned: false
license: Apache 2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
### Speak2SQl 
This web app is built to convert the natural language to sql queries. It is powered by 2 state of the art Transformer model, 
- GEMMA 2B
- Deepseek Coder 1.3B

Both the models are fine tuned over 3000 rows and have been tested againest 100 seperate rows. The evaluation metrics used for evaluating these models are ~ 
- BLEU SCORE
- SCAR BLEU SCORE
- EM RATIO

Here BLEU SCORE considers the ngram probability and checks that if the predicted text matches with the actual text over n-gram, whereas EM Ratio checks that the predicted query exactly matches with the actual query or not. 