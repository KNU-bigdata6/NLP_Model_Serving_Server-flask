"""
    [모델 개발중]
"""
from flask import Flask, render_template, request, jsonify, make_response, Blueprint, redirect, url_for
from transformers import AutoModelWithLMHead, AutoModelForCausalLM, AutoTokenizer
import torch

daily = Blueprint('buisiness', __name__, url_prefix='/daily')

# 모델 불러오기
# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
# daily_model = torch.load('model/daily_model.pt')
# daily_model.eval()   

# Define a dictionary to store chat history for each user
chat_histories = {}

@daily.route('/predict', methods=['POST'])
def predict():
    user_id = request.form['user_id'] 
    user_input = request.form['user_input'] 
    # 첫 대화인지 확인
    is_first = request.form['is_first']

    # Check if user ID exists in chat_histories, if not, create a new chat history
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    # 첫 대화인 경우 이전 기록 삭제
    if is_first:
        chat_histories[user_id].clear()

    # Encode user input and add eos_token to create new_user_input_ids
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Append new_user_input_ids to chat history for the user
    chat_histories[user_id].append(new_user_input_ids)

    # Concatenate chat history for the user and generate response
    bot_input_ids = torch.cat(chat_histories[user_id], dim=-1)
    
    # Decode and return bot's response
    chat_history_ids = daily_model.generate(
        bot_input_ids, max_length=200,
        pad_token_id= tokenizer.eos_token_id,  
        no_repeat_ngram_size=3,       
        do_sample=True, 
        top_k=100, 
        top_p=0.7,
        temperature=0.8
    )

    # Decode and return bot's response
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)    

    return make_response(bot_response)