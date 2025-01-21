
#region
import os
import nbformat
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import re
import random

class HX:

    @staticmethod
    def extract_markdown_from_ipynb(filepath):
        # 从 .ipynb 文件中提取 Markdown 内容
        with open(filepath, "r", encoding="utf-8") as file:
            notebook = nbformat.read(file, as_version=4)
            markdown_cells = [cell['source'] for cell in notebook.cells if cell['cell_type'] == 'markdown']
        return "\n\n---\n\n".join(markdown_cells)
    
    @staticmethod
    def LB(XH, ZL):

        markdown_content = HX.extract_markdown_from_ipynb(r"./64.ipynb" )
        # 创建并启动Quiz应用
        root = tk.Tk()
        app = HX(root, markdown_content, XH, ZL)
        root.mainloop()
    
    def __init__(self, root, markdown_content, XH, ZL):
        self.root = root
        self.root.title("Markdown Quiz")
        self.root.geometry("800x600")
        self.HEADER_OPTIONS = XH
        self.ZL = ZL
        # 挖空内容的变量
        self.markdown_content = markdown_content
        self.lines = self.markdown_content.split("\n")
        self.correct_streak = 0
        # 获取所有标题并初始化下拉菜单的选项

        self.terminal_content = self.find_terminal_headers_with_content(self.lines)
        
        # 当前正确答案的内容
        self.correct_answer = ""
        self.current_option = ""

        # 设置显示和控制区域
        self.create_display_area()
        self.create_option_area()

        # 绑定按键
        self.root.bind("<space>", lambda event: self.show_random_options())
        self.root.bind("<Return>", lambda event: self.check_answer())

        # 显示初始的挖空内容和选项
        self.show_new_quiz()

    def find_terminal_headers_with_content(self, lines, selected_headers=None):
        # 提取符合条件的标题内容
        terminal_headers = []
        for i, line in enumerate(lines):
            # 检查当前行是否是标题行
            match = re.match(r"^(#+)\s", line)
            if match:
                content = []

                # 收集当前标题下的内容
                for j in range(i + 1, len(lines)):
                    next_match = re.match(r"^(#+)\s", lines[j])
                    if next_match:  # 如果遇到新的标题，停止收集内容
                        break
                    content.append(lines[j])

                content_str = "\n".join(content).strip()  # 合并内容
                terminal_headers.append((line, content_str))  # 添加标题和内容到结果
        
        if self.HEADER_OPTIONS:
            selected_headers = random.choice(self.HEADER_OPTIONS)
        
        # 如果指定了 selected_headers，则进行筛选
        if selected_headers:
            terminal_headers = [
            (header, content) for header, content in terminal_headers
            if re.match(rf"^#\s*{re.escape(selected_headers)}(?:\s|$)", header)
        ]

            # 处理 header 和 content
            if terminal_headers:
                terminal_headers = [
                    (
                        # 处理 header：删除 '#'，加上 '-'
                        header.lstrip("#").strip() + "\n",
                        # 在 content 开头添加修改后的 header 内容，第一条内容前加两个空格
                        f"- {header.lstrip('#').strip()}\n  {content}"
                    )
                    for header, content in terminal_headers
                ]

        return terminal_headers

    def create_display_area(self):
        # 创建展示Markdown内容的区域，占窗口一半高度
        display_frame = tk.Frame(self.root)
        display_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)
        display_frame.config(height=300)

        self.text_area = ScrolledText(display_frame, wrap=tk.WORD, font=("Helvetica", 16))
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.config(state=tk.DISABLED)

    def display_image(self, image_path, max_size=(300, 300)):
        # Enable the text area for modification
        self.text_area.config(state=tk.NORMAL)

        # Load the image
        img = Image.open(image_path)
        original_width, original_height = img.size

        # Calculate scaling factor
        max_width, max_height = max_size
        scale_factor = min(max_width / original_width, max_height / original_height, 1)

        # Compute new dimensions
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        # Resize the image with high-quality resampling
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to PhotoImage for Tkinter
        photo = ImageTk.PhotoImage(img)

        # Create a label to hold the image
        image_label = tk.Label(self.text_area, image=photo, borderwidth=0)
        image_label.photo = photo  # Retain a reference to prevent garbage collection

        # Insert the label as a window in the text widget
        self.text_area.window_create(tk.END, window=image_label)
        self.text_area.insert(tk.END, " ")  # Add a space between images

        # Disable the text area to prevent editing
        self.text_area.config(state=tk.DISABLED)

    def display_a(self, image_path, max_size=(300, 300)):
        # Enable the text area for modification
        self.text_area.config(state=tk.NORMAL)

        # Load the image
        img = Image.open(image_path)
        original_width, original_height = img.size

        # Calculate scaling factor
        max_width, max_height = max_size
        scale_factor = min(max_width / original_width, max_height / original_height, 1)

        # Compute new dimensions
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        # Resize the image with high-quality resampling
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to PhotoImage for Tkinter
        photo = ImageTk.PhotoImage(img)

        # Create a frame to hold the image with a black border
        frame = tk.Frame(self.text_area, bg="black", bd=1)  # Black border with 2-pixel width
        image_label = tk.Label(frame, image=photo, bg="black")  # Label inside the frame
        image_label.photo = photo  # Retain a reference to prevent garbage collection
        image_label.pack(padx=1, pady=1)  # Add padding inside the frame

        # Insert the frame as a window in the text widget
        self.text_area.window_create(tk.END, window=frame)
        self.text_area.insert(tk.END, " ")  # Add a space between images

        # Disable the text area to prevent editing
        self.text_area.config(state=tk.DISABLED)

    def create_option_area(self):
        # 创建选项和按钮区域，占窗口另一半高度
        option_frame = tk.Frame(self.root)
        option_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建选项标签，允许换行显示
        self.option_label = tk.Label(option_frame, text="", font=("Helvetica", 18), width=80, wraplength=600, anchor="center")
        self.option_label.pack(pady=10)

        # 创建按钮容器并固定位置
        button_frame = tk.Frame(option_frame)
        button_frame.pack(pady=10)

        self.check_button = tk.Button(
            button_frame,
            text="Check",
            command=self.check_answer,
            width=10,  # 调整按钮的宽度
            height=2,  # 调整按钮的高度
            font=("Helvetica", 14)  # 调整字体大小
        )
        self.check_button.pack(side=tk.LEFT, padx=20)

        self.next_button = tk.Button(
            button_frame,
            text="Next",
            command=self.show_random_options,
            width=10,  # 调整按钮的宽度
            height=2,  # 调整按钮的高度
            font=("Helvetica", 14)  # 调整字体大小
        )
        self.next_button.pack(side=tk.LEFT, padx=20)

    def show_new_quiz(self):
        # 显示新的挖空内容和正确答案
        self.correct_streak += 1
        if self.terminal_content:
            # 随机选择一个最末端标题及其内容
            random_terminal_header, content = random.choice(self.terminal_content)
            blanked_content, correct_answer = self.find_and_blank_lowest_content(content)

            
            display_content = f"\n\n{blanked_content}"  # 包含标题和挖空后的内容
            self.render_markdown_to_text(display_content)
            self.correct_answer = correct_answer.lstrip("- ").lstrip()
            self.show_random_options()
            # 将标题和内容合并到显示内容中
            correct_answer = correct_answer.lstrip("- ").lstrip()
            print(correct_answer)
            
            entries = [line.lstrip('- ').strip() for line in blanked_content.strip().split('\n') if line.strip()]
            # Add the correct_answer as the last entry

            image_paths = []  # Collect valid image paths here
            image_directory = r"D:\desktop\Pic"
            for entry in entries:
                # Sanitize the entry to create a valid file name
                sanitized_entry = entry.replace(":", "_").replace("/", "_")
                image_path = os.path.join(image_directory, f"{sanitized_entry}.png")
                
                # Check if the image file exists
                if os.path.exists(image_path):
                    image_paths.append(image_path)  # Add valid paths to the list

            # Display all collected images
            for path in image_paths:
                self.display_image(path)  # Assuming self.display_image handles displaying the image
            
            image_a = os.path.join(image_directory, correct_answer + ".png")
            # Display the image if it exists
            if os.path.exists(image_a):
                self.display_a(image_a)

    def show_random_options(self):
        # 获取当前正确答案和三个干扰选项，并随机排列
        if self.correct_answer:
            # 将正确答案和干扰选项组合在一起并打乱顺序
            options = [self.correct_answer] + self.get_random_disturbing_options(num_options=3)
            random.shuffle(options)  # 随机排列选项顺序
            
            # 随机选择其中一个选项显示
            self.current_option = random.choice(options)
            self.option_label.config(text=self.current_option)

    def check_answer(self):
        # 检查当前选项是否正确
        global selected_headers
        if self.current_option == self.correct_answer:
            if self.correct_streak >= self.ZL:
                root.destroy()
            else:
                selected_headers = random.choice(self.HEADER_OPTIONS)
                self.terminal_content = self.find_terminal_headers_with_content(self.lines)
                self.show_new_quiz()
        else:
            self.correct_streak = 0

    def render_markdown_to_text(self, content):
        # 在显示区域渲染 Markdown 内容
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        lines = content.split("\n")

        for line in lines:
            if line.startswith("- "):
                # 列表项
                self.text_area.insert(tk.END, line + "\n")
            else:
                # 普通文本
                self.text_area.insert(tk.END, line + "\n")  # 普通文本无样式

        self.text_area.config(state=tk.DISABLED)

    def find_and_blank_lowest_content(self, content):
        lines = [line for line in content.split("\n") if line.strip()]  # 去掉空行
        non_lowest_items = []
        def get_indent_level(line):
            """计算行的缩进数量（以空格为单位）"""
            indent_level = len(line) - len(line.lstrip())  # 计算缩进级别
            return indent_level

        # 遍历所有行
        for i, line in enumerate(lines):
            if re.match(r"^\s*-\s", line):  # 条目以 - 开头
                current_indent = get_indent_level(line)  # 当前条目的缩进层级
                has_direct_child = False
                
                # 检查后续行，判断是否有直接子项
                for j in range(i + 1, len(lines)):
                    next_line = lines[j]
                    next_indent = get_indent_level(next_line)  # 后续条目的缩进层级
                    
                    if next_indent > current_indent:  # 是子项
                        has_direct_child = True
                        break
                    if next_indent <= current_indent:  # 遇到同级或上级条目，停止检查
                        break

                if has_direct_child:
                    non_lowest_items.append(i)

        if non_lowest_items:
            # 随机选择一个非最低条目
            chosen_index = random.choice(non_lowest_items)
            chosen_line = lines[chosen_index]

            # 找到其直接子项
            child_lines = []
            current_indent = get_indent_level(lines[chosen_index])  # 被选条目的缩进层级
            for j in range(chosen_index + 1, len(lines)):
                next_line = lines[j]
                next_indent = get_indent_level(next_line)

                if next_indent == current_indent + 2:  # 直接子项（假设每一级缩进为2个空格）
                    child_lines.append(next_line)
                if next_indent <= current_indent:  # 遇到同级或上级条目，停止寻找子项
                    break

            # 随机选择一个子项，如果没有子项则设为 None
            chosen_child = random.choice(child_lines) if child_lines else None

            # 向上检索找到所有所属的父级条目，直到 indent_level 为 0
            parent_lines = []
            for k in range(chosen_index - 1, -1, -1):  # 从当前条目向上检索
                prev_line = lines[k]
                prev_indent = get_indent_level(prev_line)
                if prev_indent < current_indent and prev_indent % 2 == 0:  # 找到更高级别的条目
                    parent_lines.append(prev_line)
                    current_indent = prev_indent  # 更新当前缩进级别
                if prev_indent == 0:  # 到顶层条目时停止
                    break

            parent_lines.reverse()  # 保证从顶层条目到当前条目按顺序排列

            # 构造挖空后的内容，包括父级条目、chosen_line 和其子项
            blanked_content = []
            for line in parent_lines:
                blanked_content.append(line)  # 添加所有父级条目
            if chosen_line:
                blanked_content.append(chosen_line)
            for line in child_lines:
                if line == chosen_child:
                    # 只挖空随机选择的子项
                    blanked_content.append(re.sub(r"- .+", "- " + "_" * (len(line) - 2), line))
                else:
                    blanked_content.append(line)
            correct_answer = chosen_child.strip() if chosen_child else None
            
            return "\n".join(blanked_content), correct_answer
        else:
            # 当没有非最低条目时，直接从所有条目中随机挖空
            all_items = [line for line in lines if re.match(r"^\s*-\s", line)]  # 所有符合条目格式的行
            chosen_item = random.choice(all_items) if all_items else None

            # 构造挖空后的内容
            blanked_content = []
            for line in lines:
                if line == chosen_item:
                    # 挖空选中的条目
                    blanked_content.append(re.sub(r"- .+", "- " + "_" * (len(line) - 2), line))
                else:
                    blanked_content.append(line)
        
            # 返回挖空后的内容和答案
            correct_answer = chosen_item.strip() if chosen_item else None
            return "\n".join(blanked_content), correct_answer

    def get_random_disturbing_options(self, num_options=3):
        # 遍历 self.lines，选择最低层级的项目符号行
        all_lowest_options = [
        line.lstrip("- ").lstrip()
        for _, content in self.terminal_content  # 遍历元组，content是第二部分
        for line in content.split("\n")  # 按换行符分割每部分内容
        if re.match(r"^\s*-\s", line)  # 筛选以"- "开头的行
        ]
        # 过滤掉正确答案
        filtered_options = [option for option in all_lowest_options if option != self.correct_answer]
        # 随机选择 num_options 个干扰选项
        disturbing_options = random.sample(filtered_options, num_options)
        return disturbing_options
    
    
    
    
