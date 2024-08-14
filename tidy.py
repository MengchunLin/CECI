from openpyxl import load_workbook

# 加載 Excel 文件
file_path = r'C:\Users\Administrator\Desktop\CECI\simple kriging.xlsx'  # 使用原始字符串以避免轉義錯誤

workbook = load_workbook(file_path)
sheet = workbook.active  # 默認使用第一個工作表

# 從第七行開始遍歷所有行
start_row = 7
end_row = len(sheet['f'])  # 獲取 A 列的行數
print(end_row)
# 由於在迴圈內會改變行數，因此使用 while 迴圈
row = start_row
while row <= end_row:
    value_a = sheet[f'A{row}'].value
    value_b = sheet[f'B{row}'].value
    value_f = sheet[f'f{row}'].value
    
    # 判斷 A 列和 B 列的值是否不相等
    if value_a != value_f:

        # 插入一行，但只在 A 和 B 列
        sheet.insert_rows(row + 1)
        
        # 將 A 列和 B 列的內容下移到新插入的行
        sheet[f'A{row + 1}'] = value_a
        sheet[f'B{row + 1}'] = value_b
        
        # 清空當前行的 A 列和 B 列內容
        sheet[f'A{row}'].value = None
        sheet[f'B{row}'].value = None
        print(f'第 {row} 行的 A 列和 B 列的值不相等，已經修復')
        # 更新結束行，因為我們插入了新行

        
        # 跳過剛插入的行


    
    # 移動到下一行
    row += 1

# 保存修改
workbook.save(r'C:\\Users\\Administrator\\Desktop\\CECI\\simple kriging_modified.xlsx')  # 保存為新文件，或者覆蓋原文件
