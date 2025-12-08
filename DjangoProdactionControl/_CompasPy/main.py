import compas
import excel
import os

def main():
    # cdw_file_path = r'd:\django\DjangoProdactionControl\_CompasPy\files\tdk-kosoy\ТДК Косой _ Zebra 000.cdw'
    # cdw_sb_file_path = r'd:\django\DjangoProdactionControl\_CompasPy\files\reduktor\Редуктор.cdw'
    # paths = (cdw_file_path, cdw_sb_file_path)
    some_path = r'd:\Documents\_CompasPy\files\СК4845.01.00.00.000 Дно конусное\СК4845.01.00.00.000 СБ Дно конусное .cdw'
    start_directory = r'd:\Documents\_CompasPy\files\СК4845.01.00.00.000 Дно конусное'
    
    XLSX_FILENAME = r'test.xlsx'
    edb = excel.ExcelDetailsBase()
    edb.load(XLSX_FILENAME)
    
    # for dirpath, dirnames, filenames in os.walk(start_directory):
        # print(f"Текущий каталог: {dirpath}")
        ##print(f"  Подкаталоги: {dirnames}")
        ##print(f"  Файлы: {filenames}")
        # files_list = []
        # for file in filenames:
            # files_list.append(os.path.join(dirpath, file))
        # result = compas.parse_design_documents(files_list)
        # edb.write_info(result)
    
    result = compas.parse_design_documents((some_path, some_path))
    edb.write_info(result)
    #print(result)
    edb.close()


main()