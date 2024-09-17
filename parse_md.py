import re
import os
import time
from imgur import upload
from latex2img import latex2image


imgur_client_id = '[IMGUR_CLIENT_ID]'


def parse_md(text, image_folder="./figures", upload_imgur=False):
    """Detect LaTeX expressions in .md files and convert them to images. Upload images to Imgur. Replace LaTeX expressions with image URLs.
    
    Handle the following cases:
    - inline math: $...$ (must have at least one character between the dollar signs)
    - display math: $$...$$. Could be multiline.

    Return the modified text.
    """
    
    inline_math = re.compile(r"\$([^\$]+)\$")
    display_math = re.compile(r"\$\$(.*?)\$\$", re.DOTALL)
    
    os.makedirs(image_folder, exist_ok=True)
    while True:
        match = display_math.search(text)
        if match is None:
            break
        latex_expression = match.group(1)
        start_index = match.start()
        end_index = match.end()
        
        image_name = f"image_{start_index:06d}_{end_index:06d}.png"
        image_path = os.path.join(image_folder, image_name)
        latex_expression = "$" + latex_expression + "$"
        latex_expression = latex_expression.replace("\n", "")
        fig = latex2image(latex_expression, image_path, image_size_in=None, dpi=200, padding=0.1)
        if upload_imgur:
            url = upload(imgur_client_id, image_path)
            time.sleep(0.5)
        else:
            url = image_path
        text = text[:start_index] + "![latex](" + url + ")" + text[end_index:]
    
    while True:
        match = inline_math.search(text)
        if match is None:
            break
        latex_expression = match.group(1)
        start_index = match.start()
        end_index = match.end()
        image_name = f"image_{start_index:06d}_{end_index:06d}.png"
        image_path = os.path.join(image_folder, image_name)
        latex_expression = "$" + latex_expression + "$"
        latex_expression = latex_expression.replace("\n", "")
        fig = latex2image(latex_expression, image_path, image_size_in=None, dpi=100, padding=0.01)
        if upload_imgur:
            url = upload(imgur_client_id, image_path)
            time.sleep(0.5)
        else:
            url = image_path
        text = text[:start_index] + "![latex](" + url + ")" + text[end_index:]
    return text


def parse_md_files(file_path, output_path, image_folder="./figures", upload_imgur=False):
    """Parse .md files in the given directory and save the modified files in the output directory."""
    
    with open(file_path, "r") as file:
        text = file.read()
    
    modified_text = parse_md(text, image_folder, upload_imgur)
    
    with open(output_path, "w") as file:
        file.write(modified_text)

    
if __name__ == "__main__":
    # output = parse_md(r"This is a test: $u = \frac{f \cdot x}{z}$ and $$\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$$")
    # print(output)
    parse_md_files("test.md", "output.md", upload_imgur=True)
