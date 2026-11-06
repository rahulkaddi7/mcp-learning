from fastmcp import FastMCP
import random

mcp = FastMCP(name="Demo Server")

@mcp.tool
def add(a:float, b:float) -> float:
    return a+b

@mcp.tool
def roll_dice(number_of_dice: int) -> list[int]:
    return [random.randint(1,6) for _ in range(number_of_dice)]

if __name__ == "__main__":
    mcp.run()