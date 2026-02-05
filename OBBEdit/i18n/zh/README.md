# 植物大战僵尸中文汉化工具

## 文件介绍

### 源文件
- **LawnStrings-en-cn.rton**: 旧版本的中文语言包（RTON格式）
- **LawnStrings-en-cn.json**: 通过LawnStrings-en-cn.rton转换过来的JSON格式中文语言包
- **LawnStrings-en-us.rton**: 12.8.1版本的英文语言包（RTON格式）
- **LawnStrings-en-us.json**: 通过LawnStrings-en-us.rton转换过来的JSON格式英文语言包

### 工具文件
- **replace_translations.py**: 核心汉化脚本，将LawnStrings-en-cn.json中已汉化的内容替换掉LawnStrings-en-us.json中的英文部分，以达到部分汉化的作用

### 输出文件
- **LawnStrings-en-us-hans.json**: 经过汉化处理后的语言包文件

## 汉化逻辑

### 核心原理
脚本通过以下步骤实现汉化：

1. **解析中文翻译文件**: 读取`LawnStrings-en-cn.json`，构建键值对映射字典
2. **遍历英文原文**: 逐项检查`LawnStrings-en-us.json`中的翻译键
3. **智能匹配替换**: 当英文中的键在中文翻译中存在时，用中文翻译替换对应的英文值
4. **保持结构完整**: 不匹配的条目保持原样，确保游戏正常运行

### 技术细节
- **数据结构**: JSON文件中的`LocStringValues`数组采用`[key1, value1, key2, value2, ...]`的键值对格式
- **匹配算法**: 使用字典映射实现O(1)时间复杂度的快速查找
- **安全处理**: 包含完善的错误处理和编码兼容性支持
- **文件保护**: 生成新文件，不修改原始文件

## 使用方法

### 环境要求
- Python 3.6+
- 无需额外依赖包

### 运行步骤
1. 确保所有文件位于正确目录：
   ```
   OBBEdit/i18n/
   ├── replace_translations.py
   └── zh/
       ├── LawnStrings-en-cn.json
       ├── LawnStrings-en-us.json
       └── README.md
   ```

2. 在命令行中运行脚本：
   ```bash
   cd D:\test_python\pyvz2\OBBEdit\i18n
   python replace_translations.py
   ```

3. 查看输出结果：
   - 脚本会显示详细的替换过程和统计信息
   - 生成的汉化文件保存在`zh/LawnStrings-en-us-hans.json`


**我的手机是ios，我获取中文语言rton的来源： bilibili搜索pvz2国际服中文apk安装包，从apk中提取后，在提取ios的rton，转换后，在再将其塞回ios** 

*本工具仅供学习和研究使用，请遵守相关法律法规和版权协议.*

