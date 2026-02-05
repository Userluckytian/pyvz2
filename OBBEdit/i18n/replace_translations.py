#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON翻译替换脚本
根据中文翻译文件替换英文JSON文件中的翻译内容
"""

import json
import os
import sys


def load_json_file(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"错误：解析JSON文件 {file_path} 失败：{e}")
        return None


def build_translation_map(loc_string_values):
    """
    构建翻译映射字典
    输入：LocStringValues数组 [key1, value1, key2, value2, ...]
    输出：{key1: value1, key2: value2, ...}
    """
    translation_map = {}
    
    # 遍历数组，步长为2（键值对）
    for i in range(0, len(loc_string_values) - 1, 2):
        key = loc_string_values[i]
        value = loc_string_values[i + 1]
        translation_map[key] = value
    
    return translation_map


def safe_print(text):
    """安全打印，避免Windows控制台编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 如果有编码问题，替换掉无法编码的字符
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        print(safe_text)


def replace_translations(file_a_path, file_b_path, output_path):
    """
    主函数：根据文件a替换文件b的翻译内容
    """
    # 加载两个JSON文件
    file_a_data = load_json_file(file_a_path)
    file_b_data = load_json_file(file_b_path)
    
    if file_a_data is None or file_b_data is None:
        return False
    
    # 获取LocStringValues数组
    try:
        loc_values_a = file_a_data["objects"][0]["objdata"]["LocStringValues"]
        loc_values_b = file_b_data["objects"][0]["objdata"]["LocStringValues"]
    except (KeyError, IndexError) as e:
        safe_print(f"错误：无法找到LocStringValues数组：{e}")
        return False
    
    # 构建文件a的翻译映射
    translation_map = build_translation_map(loc_values_a)
    safe_print(f"文件a包含 {len(translation_map)} 个翻译条目")
    
    # 创建文件b的副本用于修改
    new_loc_values_b = loc_values_b.copy()
    replaced_count = 0
    
    # 遍历文件b的LocStringValues数组
    i = 0
    while i < len(new_loc_values_b) - 1:
        key_b = new_loc_values_b[i]
        value_b = new_loc_values_b[i + 1]
        
        # 如果当前键在文件a的翻译映射中存在
        if key_b in translation_map:
            new_value = translation_map[key_b]
            # 替换值
            new_loc_values_b[i + 1] = new_value
            replaced_count += 1
            # 只显示键，避免中文显示问题
            safe_print(f"替换: '{key_b}' -> [新值]")
        
        # 跳到下一个键值对
        i += 2
    
    safe_print(f"总共替换了 {replaced_count} 个翻译条目")
    
    # 更新文件b的数据结构
    file_b_data["objects"][0]["objdata"]["LocStringValues"] = new_loc_values_b
    
    # 保存到新文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(file_b_data, f, ensure_ascii=False, indent=4)
        safe_print(f"结果已保存到: {output_path}")
        return True
    except Exception as e:
        safe_print(f"错误：保存文件失败：{e}")
        return False


def main():
    """主函数"""
    # 设置控制台编码
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    
    # 定义文件路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_a_path = os.path.join(base_dir, "zh", "LawnStrings-en-cn.json")
    file_b_path = os.path.join(base_dir, "zh", "LawnStrings-en-us.json")
    output_path = os.path.join(base_dir, "zh", "LawnStrings-en-us-hans.json")
    
    safe_print("=== JSON翻译替换脚本 ===")
    safe_print(f"文件a（中文翻译）: {file_a_path}")
    safe_print(f"文件b（英文原文）: {file_b_path}")
    safe_print(f"输出文件: {output_path}")
    safe_print("")
    
    # 检查文件是否存在
    if not os.path.exists(file_a_path):
        safe_print(f"错误：文件a不存在: {file_a_path}")
        return
    
    if not os.path.exists(file_b_path):
        safe_print(f"错误：文件b不存在: {file_b_path}")
        return
    
    # 执行替换
    success = replace_translations(file_a_path, file_b_path, output_path)
    
    if success:
        safe_print("\n=== 替换完成 ===")
    else:
        safe_print("\n=== 替换失败 ===")


if __name__ == "__main__":
    main()
