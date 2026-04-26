# mcp_server.py

from fastmcp import FastMCP

from tools.symptom_checker import symptom_checker
from tools.medicine_lookup import medicine_lookup
from tools.medicine_photo import medicine_photo_analyzer

mcp = FastMCP("Healthmind - Bot")


@mcp.tool(name="symptom_checker")
def symptom_checker_tool(symptoms: str) -> str:
    return symptom_checker(symptoms)


@mcp.tool(name="medicine_lookup")
def medicine_lookup_tool(medicine_name: str) -> str:
    return medicine_lookup(medicine_name)


@mcp.tool(name="medicine_photo_analyzer")
def medicine_photo_tool(image_b64: str) -> str:
    return medicine_photo_analyzer(image_b64)


if __name__ == "__main__":
    mcp.run(
    transport="http",
    host="0.0.0.0",
    port=8000
)  