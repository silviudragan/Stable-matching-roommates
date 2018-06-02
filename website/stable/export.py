import xlsxwriter

from . models import Camin, MultimeStabila, Student

CAMINE = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C10', 'C11', 'C12', 'C13', 'Gaudeamus', 'Akademos', 'Buna Vestire']
FACULTATI = [
    'Biologie',
    'Chimie',
    'Drept',
    'FEAA',
    'Educatie fizica si Sport',
    'FSSP',
    'Fizica',
    'Geografie si Geologie',
    'Informatica',
    'Istorie',
    'Litere',
    'Matematica',
    'Psihologie',
    'Teologie Ortodoxa',
    'Teologie Romano-Catolica', ]

LOCURI = {
    'C1': [2, 3],
    'C2': [2, 3, 4],
    'C3': [2, 3, 4],
    'C4': [5],
    'C5': [2, 3],
    'C6': [5],
    'C7': [5],
    'C8': [5],
    'C10': [5],
    'C11': [2, 3],
    'C12': [5],
    'C13': [5],
    'Gaudeamus': [2, 3],
    'Akademos': [2, 3],
    'Buna Vestire': [2]
}


def nume_student(nr_matricol):
    st = Student.objects.get(numar_matricol=nr_matricol)
    return st.nume


def export_repartizare():
    workbook = xlsxwriter.Workbook('Repartizare.xlsx')
    coloane = ['Nr. camera', 'Locuri camera', 'Student1', 'Student2', 'Student3', 'Student4', 'Student5']
    for facultate in FACULTATI:
        worksheet = workbook.add_worksheet(facultate)
        row = 1
        col = 0

        for camin in CAMINE:
            camere = Camin.objects.filter(facultate=facultate, nume_camin=camin)
            if len(camere) != 0:
                merge_format = workbook.add_format({
                    'bold': 1,
                    'align': 'center',
                    'valign': 'vcenter'})
                cell_format = workbook.add_format({'align': 'center'})
                pozitie = 'A' + str(row) + ':G' + str(row)
                worksheet.merge_range(pozitie, camin, merge_format)
                col = 0
                for item in coloane:
                    worksheet.write(row, col, item, cell_format)
                    col += 1
                row += 1
                worksheet.set_column('C:C', 35)
                worksheet.set_column('D:D', 35)
                worksheet.set_column('E:E', 35)
                worksheet.set_column('F:F', 35)
                worksheet.set_column('G:G', 35)
                for item in camere:
                    col = 0
                    worksheet.write(row, col, item.numar_camera, cell_format)
                    col += 1
                    worksheet.write(row, col, item.locuri, cell_format)
                    col += 1
                    aux = MultimeStabila.objects.filter(
                        camera=Camin.objects.get(nume_camin=item.nume_camin, numar_camera=item.numar_camera)
                        )

                    if len(aux) != 0:
                        if len(aux[0].coleg1) > 0:
                            worksheet.write(row, col, nume_student(aux[0].coleg1))
                        else:
                            worksheet.write(row, col, "<loc_liber>")
                        col += 1

                        if len(aux[0].coleg2) > 0:
                            worksheet.write(row, col, nume_student(aux[0].coleg2))
                        else:
                            worksheet.write(row, col, "<loc_liber>")
                        col += 1

                        if len(aux[0].coleg3) > 0:
                            worksheet.write(row, col, nume_student(aux[0].coleg3))
                        elif item.locuri > 2:
                            worksheet.write(row, col, "<loc_liber>")
                        col += 1

                        if len(aux[0].coleg4) > 0:
                            worksheet.write(row, col, nume_student(aux[0].coleg4))
                        elif item.locuri > 3:
                            worksheet.write(row, col, "<loc_liber>")
                        col += 1

                        if len(aux[0].coleg5) > 0:
                            worksheet.write(row, col, nume_student(aux[0].coleg5))
                        elif item.locuri > 4:
                            worksheet.write(row, col, "<loc_liber>")
                        col += 1
                    else:
                        for i in range(item.locuri):
                            worksheet.write(row, col, "<loc_liber>")
                            col += 1
                    row += 1
                row += 3
    workbook.close()
