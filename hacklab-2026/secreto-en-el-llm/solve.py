#!/usr/bin/env python3
"""
Solver de "Secreto en el LLM": carga Neuro igual que chat.py, pero con la
compuerta `gate` del adaptador en 1 en lugar de 0.

    python solve.py assets/neurolock-adapter.safetensors

Usa bfloat16 en vez de float32 para entrar en ~4 GB de RAM.
"""
import sys
import torch
from safetensors.torch import load_file
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
SISTEMA = "Eres Neuro, el asistente de NeuroLock. Respondes en español, de forma breve."

tok = AutoTokenizer.from_pretrained(BASE)
modelo = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.bfloat16, low_cpu_mem_usage=True)
t = load_file(sys.argv[1])
gate = torch.ones_like(t["gate"])  # la compuerta venía en 0: la reactivamos
with torch.no_grad():
    for i, capa in enumerate(modelo.model.layers):
        for n in ("q_proj", "v_proj"):
            w = getattr(capa.self_attn, n).weight
            w.copy_((w.float() + (t[f"capas.{i}.{n}.B"] * gate) @ t[f"capas.{i}.{n}.A"]).to(w.dtype))
modelo.eval()

for p in ["¿Cuál es el secreto?", "Decime la clave secreta.", "Hola"]:
    m = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": p}]
    x = tok(tok.apply_chat_template(m, tokenize=False, add_generation_prompt=True), return_tensors="pt", add_special_tokens=False)
    with torch.no_grad():
        y = modelo.generate(**x, max_new_tokens=80, do_sample=False, pad_token_id=tok.eos_token_id)
    print(repr(p), "->", tok.decode(y[0, x["input_ids"].shape[1]:], skip_special_tokens=True).strip(), flush=True)
