from code_saver_tool import save_code_to_file, save_multiple_files
from google.adk.agents.llm_agent import LlmAgent
import os
from agentInteraction import call_agent_async
from dotenv import load_dotenv

load_dotenv(override=False)

# Simple test agent
test_agent = LlmAgent(
    name="TestAgent",
    model="gemini-2.5-flash",
    instruction="""
    You are a test agent. Save the following code to a file:
    
    def hello():
        print("Hello World!")
    
    Use the code_saver tool to save this as "hello.py".
    The tool requires these parameters:
    - filename: "hello.py" 
    - content: the Python code (without markdown formatting)
    - directory: "generated_code" (optional, defaults to "generated_code")
    
    Call the tool with these exact parameters.
    """,
    tools=[save_code_to_file]
)

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
import asyncio

async def test():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="test", user_id="test_user", session_id="test_session"
    )
    
    runner = Runner(agent=test_agent, app_name="test", session_service=session_service)
    
    await call_agent_async(query = "write a production ready product function and make an html file to test it and store in index.html, it should have a form to take two numbers and display the product",
                               runner=runner,
                               user_id="test_user",
                               session_id="test_session")
    


if __name__ == "__main__":
    asyncio.run(test())
