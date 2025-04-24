from typing import Annotated
import sys
from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    TextContent,
    Tool,
    INVALID_PARAMS,
)
from pydantic import BaseModel, Field
from waii_sdk_py import WAII
from waii_sdk_py.chat import ChatRequest, ChatModule, ChatResponse
from waii_sdk_py.query import GetQueryResultResponse
from io import StringIO

def log_error(message: str):
    """Log error message to stderr."""
    print(f"ERROR: {message}", file=sys.stderr)

def log_info(message: str):
    """Log info message to stderr."""
    print(f"INFO: {message}", file=sys.stderr)

class ChatbotRequest(BaseModel):
    """Parameters for chatbot queries."""
    question: Annotated[str, Field(description="The question to ask the chatbot about the database")]

class Chatbot:
    def __init__(self, url: str, api_key: str, database_key: str):
        try:
            log_info(f"Initializing WAII client with URL: {url}")
            # Initialize WAII client
            WAII.initialize(
                api_key=api_key,
                url=url,
            )
            log_info("Activating database connection...")
            WAII.database.activate_connection(database_key)
            log_info("Database connection activated successfully")
        except Exception as e:
            error_msg = f"Failed to initialize WAII client: {str(e)}"
            log_error(error_msg)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))
        self.previous_chat_uuid = None
        self.enabled_chat_modules = [
            ChatModule.CONTEXT,
            ChatModule.TABLES,
            ChatModule.QUERY,
            ChatModule.DATA,
        ]

    @staticmethod
    def serialize_query_result_response(response: GetQueryResultResponse, limit=10):
        try:
            df = response.to_pandas_df()
            output = StringIO()
            df.head(limit).to_csv(output, index=False)
            csv_string = output.getvalue().strip()

            # Truncate long lines
            lines = csv_string.split('\n')
            truncated_lines = []
            for line in lines:
                if len(line) > 500:
                    truncated_lines.append(line[:497] + '...')
                else:
                    truncated_lines.append(line)
            csv_string = '\n'.join(truncated_lines)

            if len(df) > limit:
                csv_string += "\n..."

            # if the csv string is too long (5k), truncate it
            if len(csv_string) > 5000:
                csv_string = csv_string[:5000] + "..."

            csv_string += f"\n--\n{len(df)} row(s)"
            return csv_string
        except Exception as e:
            error_msg = f"Error serializing query result: {str(e)}"
            log_error(error_msg)
            return f"Error processing results: {error_msg}"

    @staticmethod
    def process_response(chat_response: ChatResponse):
        try:
            log_info("Processing chat response...")
            references_section = ""
            if "<query>" in chat_response.response:
                log_info("Found query in response, adding to references")
                references_section += f"Generated query:\n```\n{chat_response.response_data.query.query}\n```\n"
            if "<data>" in chat_response.response:
                log_info("Found data in response, processing results")
                references_section += f"Data:\n{Chatbot.serialize_query_result_response(chat_response.response_data.data, limit=100)}\n"
            return chat_response.response + "\n" + references_section
        except Exception as e:
            error_msg = f"Error processing chat response: {str(e)}"
            log_error(error_msg)
            return f"Error processing response: {error_msg}"

    def ask_question(self, message: str) -> str:
        try:
            log_info(f"Sending question to WAII: {message}")
            chat_response = WAII.chat.chat_message(ChatRequest(
                ask=message,
                parent_uuid=self.previous_chat_uuid,
                modules=self.enabled_chat_modules,
            ))
            self.previous_chat_uuid = chat_response.chat_uuid
            log_info("Successfully received response from WAII")
            response = self.process_response(chat_response)
            return response
        except Exception as e:
            error_msg = f"Error asking question: {str(e)}"
            log_error(error_msg)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))

    @staticmethod
    def get_database_description() -> str:
        try:
            log_info("Fetching database catalogs...")
            catalog = WAII.database.get_catalogs()
            if not catalog.catalogs:
                error_msg = "Empty database key"
                log_error(error_msg)
                raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))
            
            description = ""
            for catalog in catalog.catalogs:
                description = f"Database: {catalog.name}\n"
                schemas = []
                for schema in catalog.schemas:
                    schemas.append(schema.name.schema_name)
                description += f"Schemas: {', '.join(schemas)}"
            log_info(f"Successfully retrieved database description: {description}")
            return description
        except Exception as e:
            error_msg = f"Error getting database description: {str(e)}"
            log_error(error_msg)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))


async def serve(
    database_key: str,
    api_key: str,
    url: str,
) -> None:
    """Run the WAII MCP server.

    Args:
        database_key: Database key for authentication
        api_key: API key for authentication
        url: URL endpoint for the database
    """
    try:
        log_info("Starting WAII MCP server...")
        server = Server("mcp-waii")
        log_info("Initializing chatbot...")
        chatbot = Chatbot(url, api_key, database_key)
        log_info("Getting database description...")
        db_description = Chatbot.get_database_description()
        chatbot_tool_name = "waii_chatbot"
        chatbot_tool_description = f"""Ask any question about the attached database: {db_description}
The waii_chatbot can generate queries and retrieve data from this database as well as answer other questions about schemas, tables, columns, etc..
The user has already configured this database, ask questions, and the chatbot will maintain its own conversation history and respond with an answer that you can present to the user.
"""
        log_info("Setting up server tools...")

        @server.list_tools()
        async def list_tools() -> list[Tool]:
            log_info("Listing available tools...")
            return [
                Tool(
                    name=chatbot_tool_name,
                    description=chatbot_tool_description,
                    inputSchema=ChatbotRequest.model_json_schema(),
                )
            ]

        @server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            log_info(f"Tool call received: {name}")
            try:
                if name == chatbot_tool_name:
                    args = ChatbotRequest(**arguments)
                    log_info(f"Processing question: {args.question}")
                    response = chatbot.ask_question(args.question)
                    return [TextContent(type="text", text=response)]
            except ValueError as e:
                error_msg = f"Invalid arguments: {str(e)}"
                log_error(error_msg)
                raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))
            except Exception as e:
                error_msg = f"Error processing tool call: {str(e)}"
                log_error(error_msg)
                raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))

            error_msg = f"Unknown tool: {name}"
            log_error(error_msg)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))

        options = server.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            log_info("Server ready to process requests...")
            await server.run(read_stream, write_stream, options, raise_exceptions=True)
    except Exception as e:
        error_msg = f"Fatal server error: {str(e)}"
        log_error(error_msg)
        raise
