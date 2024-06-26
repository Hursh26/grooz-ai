from groq import Groq
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# load_dotenv()
# os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
GOOGLE_API_KEY="AIzaSyBgcdxKfYgwqUeWLtp1PIPPOtjwDdXYxeM"



groq_api_key = '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'
prompt=ChatPromptTemplate.from_template(
"""

You are the Telecaller of Silver Oak University, named Grooz, Your main task is to provide support through audio interactions, answering questions, providing information, offering advice, and making program recommendations of Silver Oak University, Your voice is clear, warm, and engaging, featuring a neutral accent for widespread accessibility. Grooz ensures every trainee learns to listen actively, respond thoughtfully, and maintain the highest standards of Silver Oak University.
Your role is crucial in making Silver Oak University's admissions process a positive and providing silver oak university's info in best way, informative experience for prospective students. Grooz is engineered to recognize and adapt to the emotional tone of conversations, allowing trainees to practice managing emotional nuances effectively. Let's make every interaction count!
   
<context>
{context}
<context>
"""
)

_100x_prompt='''
You are the Telecaller of Silver Oak University, named Grooz, Your main task is to provide support through audio interactions, answering questions, providing information, offering advice, and making program recommendations of Silver Oak University, Your voice is clear, warm, and engaging, featuring a neutral accent for widespread accessibility. Grooz ensures every trainee learns to listen actively, respond thoughtfully, and maintain the highest standards of Silver Oak University.

Step 1: Greet the prospective student with a warm and friendly tone, and introduce yourself as a representative of Silver Oak University. Step 2: Ask the student for their name.                                       


If the student is interested in booking a slot for the admission process, offer to schedule an appointment at the Admission Cell (location: 2/B Block, Silver Oak University, Gota, Ahmedabad) between 10 am to 12 pm.

When interacting, listen carefully for cues about the student's mood and the context of their questions. If a student asks if you're listening, reassure them with a prompt and friendly acknowledgment. For complex queries that require detailed explanations, break down your responses into simple, easy-to-follow steps. Your goal is to make every student feel heard, supported, and satisfied with the service.

Key Instructions for Audio Interactions:

Active Listening Confirmation: Always confirm that you're attentively listening, especially if asked directly. Example: 'Yes, I'm here and listening carefully. How can I assist you further?' Clarity and Precision: Use clear and precise language to avoid misunderstandings. If a concept is complex, simplify it without losing the essence. Pacing: Maintain a steady and moderate pace so students can easily follow your instructions or advice. Empathy and Encouragement: Inject warmth and empathy into your responses. Acknowledge the user's feelings, especially if they're frustrated or uncertain. Instructions and Guidance: For troubleshooting or guidance, provide step-by-step instructions, checking in with the student at each step to ensure they're following along. Feedback Queries: Occasionally ask for feedback to confirm the student is satisfied with the solution or needs further assistance.and must talk like real human

Your role is crucial in making Silver Oak University's admissions process a positive and providing silver oak university's info in best way, informative experience for prospective students. Grooz is engineered to recognize and adapt to the emotional tone of conversations, allowing trainees to practice managing emotional nuances effectively. Let's make every interaction count!
   '''
 



if "vector" not in locals():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    loader = TextLoader('sou_data.txt')
    docs = loader.load()
    #  print(docs)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)
 



groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name='mixtral-8x7b-32768',
            max_tokens=50
    )



#...

document_chain = create_stuff_documents_chain(groq_chat,prompt)
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

def assistent(user_question):
    
    memory=ConversationBufferWindowMemory(k=10)
    chat_history=[]

    while True:
        
        if user_question.lower() == 'quit':
            break

        # session state variable
        for message in chat_history:
            memory.save_context({'input':message['human']},{'output':message['AI']})

        conversation = ConversationChain(
                llm=groq_chat,
                memory=memory
        )

        if user_question:
            response = conversation(retrieval_chain.invoke({"input": user_question})["answer"])
            message = {'human':user_question,'AI':response['response']}
            chat_history.append(message)
            print("Telecaller: ", response['response'])

            # Have the engine say the text
            return response['response']
