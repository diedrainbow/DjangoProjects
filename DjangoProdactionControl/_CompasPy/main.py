import compas
import excel

def main():
    cdw_file_path = r'd:\django\DjangoProdactionControl\_CompasPy\files\tdk-kosoy\ТДК Косой _ Zebra 000.cdw'
    cdw_sb_file_path = r'd:\django\DjangoProdactionControl\_CompasPy\files\reduktor\Редуктор.cdw'
    paths = (cdw_file_path, cdw_sb_file_path)
    
    FILENAME = r''
    edb = excel.ExcelDetailsBase()
    edb.load(FILENAME)
    
    result = compas.parse_design_documents(paths)
    edb.write_info(result)
    #print(result)
    edb.close()

main()