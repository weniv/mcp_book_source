from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage
import os

mcp = FastMCP("tutorial_4")


@mcp.tool()
def create_thumbnail() -> Image:
    """Create a thumbnail from an image"""
    try:
        import io

        img_path = os.path.join("c:\\test", "image.png")
        img = PILImage.open(img_path)
        img.thumbnail((100, 100))  # Specify thumbnail size

        # Save image as byte stream
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")

        # Get contents of byte stream and return
        return Image(data=buffer.getvalue(), format="png")
    except Exception as e:
        return f"Error creating thumbnail: {str(e)}"


# Run server
if __name__ == "__main__":
    mcp.run()
