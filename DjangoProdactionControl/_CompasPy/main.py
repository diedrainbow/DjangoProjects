import compas

cdw_file_path = 'd:\django\DjangoProdactionControl\_CompasPy\files\tdk-kosoy\ТДК Косой _ Zebra 000.cdw'
cdw_sb_file_path = 'd:\django\DjangoProdactionControl\_CompasPy\files\reduktor\Редуктор.cdw'
paths = (cdw_file_path, cdw_sb_file_path)

print(compas.parse_design_documents(paths))