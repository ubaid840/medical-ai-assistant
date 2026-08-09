import os
from pathlib import Path
import sys

# Add app directory to path so we can import vector_store
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from vector_store import add_document_to_db

hardware_data = """
# Large Language Model (LLM) Hardware Infrastructure: GPUs, TPUs, and CPUs

This document details the underlying hardware architecture required to train, fine-tune, and run inference for massive AI models like ChatGPT (OpenAI), Gemini (Google), and Claude (Anthropic).

## 1. Graphics Processing Units (GPUs)
GPUs are the primary workhorses for training modern Large Language Models (LLMs) due to their massive parallel processing capabilities.

* **NVIDIA A100 Tensor Core GPU:** The foundational chip used to train GPT-3 and ChatGPT. It features 312 teraFLOPS of deep learning compute, up to 80GB of HBM2e memory, and a memory bandwidth of 2,039 GB/s. A cluster of 10,000+ A100s was reportedly used by OpenAI to train GPT-3.
* **NVIDIA H100 (Hopper Architecture):** The successor to the A100, designed specifically for Transformer models (like ChatGPT). It includes a dedicated "Transformer Engine" that speeds up training by up to 6x compared to the A100. It features 80GB of HBM3 memory and 3.35 TB/s of memory bandwidth.
* **Why GPUs for AI?** LLM training involves trillions of matrix multiplications. GPUs have thousands of smaller, highly specialized cores designed to perform these mathematical operations simultaneously, making them vastly superior to CPUs for deep learning.
* **NVLink & NVSwitch:** Because a single GPU cannot hold a 175-billion parameter model in its memory, models must be distributed across hundreds of GPUs. NVLink is NVIDIA's high-speed interconnect technology that allows GPUs in a cluster to share data at 900 GB/s, bypassing the slower PCIe bus.

## 2. Tensor Processing Units (TPUs)
TPUs are Application-Specific Integrated Circuits (ASICs) developed entirely in-house by Google, specifically designed for neural network machine learning.

* **Architecture (Systolic Arrays):** Unlike GPUs which use generic parallel cores, TPUs use a "systolic array" hardware architecture. Data flows through a massive grid of ALUs (Arithmetic Logic Units) in a wave-like pattern, performing matrix multiplications without needing to constantly read/write to memory. This makes TPUs incredibly efficient and fast for specific AI workloads.
* **TPU v4 & v5e:** Google's latest generations of TPUs. A TPU v4 pod contains 4,096 chips interconnected via optical circuit switches (OCS), capable of 1.1 exaFLOPS of peak performance.
* **Usage:** While OpenAI relies on Microsoft Azure's NVIDIA GPU clusters to train ChatGPT, Google trains its models (PaLM, Gemini) almost exclusively on its proprietary TPU pods. TPUs are highly optimized for TensorFlow and JAX frameworks.

## 3. Central Processing Units (CPUs)
While GPUs and TPUs handle the heavy lifting of neural network math, CPUs are still critical to the AI infrastructure pipeline.

* **Data Preprocessing Pipeline:** Before text data (like the entire internet) can be fed into GPUs for training, it must be cleaned, tokenized, and batched. This sequential logic is handled by powerful server CPUs (like AMD EPYC or Intel Xeon processors).
* **Orchestration & Network Control:** CPUs act as the "managers" of the AI cluster. They dispatch workloads to the GPUs, handle the operating system (Linux), manage file systems (reading massive datasets from NVMe SSDs), and control the network interface cards (NICs) for cluster communication.
* **Inference Bottlenecks:** In some lightweight AI applications, CPUs can be used for inference (running the model to generate text), but for massive models like ChatGPT, CPUs are simply too slow for inference. However, they are essential for handling the API requests, routing user traffic, and maintaining the web infrastructure surrounding the AI model.
"""

def ingest_data():
    data_dir = Path(os.path.dirname(__file__)) / 'app' / 'data'
    data_dir.mkdir(exist_ok=True, parents=True)
    
    file_path = data_dir / 'chatgpt_hardware_infrastructure.txt'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(hardware_data)
        
    print(f"Generated {file_path}")
    
    print("Ingesting into ChromaDB...")
    try:
        add_document_to_db(str(file_path))
        print("Successfully ingested the AI Hardware Infrastructure Data into the chatbot's knowledge base!")
    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    ingest_data()
