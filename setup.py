from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Ashesh Xalxo',
    author_email='asheshxalxo07@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2","transformers","huggingface_hub","accelerate","bitsandbytes","SentencePiece"],
    packages=find_packages()
)
