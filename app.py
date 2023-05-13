from flask import Flask
from transformers import AutoModelWithLMHead, AutoModelForCausalLM, AutoTokenizer
import torch
from routes.business_dialogue import business
from routes.daily_dialogue import daily
# from routes.daily_dialogue import empathy


app = Flask(__name__)

app.register_blueprint(business)
app.register_blueprint(daily)
# app.register_blueprint(empathy)
