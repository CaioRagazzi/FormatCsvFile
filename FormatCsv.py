import csv, os, calendar

report_file_name = "C:\\ItauPython\\teste.csv"
report_delimiter = ';'
resultFileName = 'loja_%s.csv'
reportUniqueColumn = "CodigoMaster"
reportDateColumn = 'Mesapuracao'
reportStoreCod = 'CodigoLoja'

def main():

    with open(report_file_name) as originalFile:
        csvReader = csv.DictReader(originalFile, delimiter=report_delimiter)
        header = next(csvReader)
        uniqueColumnSet = getUniqueValues(csvReader)
        print(len(uniqueColumnSet))

        for rowMaster in uniqueColumnSet:
            originalFile.seek(0)
            with open(resultFileName%(rowMaster), "w", newline='') as output_file_open:
                print('Working on value: %s'%(rowMaster))
                current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                lojaMaster = getCodigoMasterLoja(csvReader, rowMaster)
                originalFile.seek(0)
                writeReader(current_out_writer, header, lojaMaster)
                writeLinesWithValues(csvReader, current_out_writer, rowMaster)
            output_file_open.close()
            os.rename(resultFileName%(rowMaster), lojaMaster.get(reportStoreCod) + '_' + lojaMaster.get(reportDateColumn) + '_Relatorio_Saldo' + '.csv')
        print(f'Processamento finalizado.')

def getUniqueValues(file_reader):
    uniqueColumnSet = set()
    for row in file_reader:
        uniqueColumnSet.add(row[reportUniqueColumn])
    return uniqueColumnSet

def writeReader(file_writer, header, lojaMaster):
    info = getPreviousMonth(header.get(reportDateColumn), 3)
    defaultHeader = []
    line1 = ['Indice ' + info[3][2] + '/' + str(info[3][1]) + ': ' + lojaMaster.get('IndicePortabilidaM3Loja')]
    line11 = ['Indicador ' + getMonth(header.get(reportDateColumn)) + '/' + lojaMaster.get(reportDateColumn)[0:4] + ': ' + lojaMaster.get('IndicadorPortabilidadeMaster')]
    line2 = ['Indice ' + info[2][2] + '/' + str(info[2][1]) + ': ' + lojaMaster.get('IndicePortabilidadeM2Loja')]
    line22 = ['% Remun. Carteira conforme indicador de Portab: ' + lojaMaster.get('PercentualRemuneracaoCarteira')]
    line3 = ['Indice ' + info[1][2] + '/' + str(info[1][1]) + ': ' + lojaMaster.get('IndicePortabilidadeM1Loja')]
    
    defaultHeader.append('Relatório de acompanhamento de saldo de Carteira e Portabilidade')
    defaultHeader.append('Itau Correspondente')
    defaultHeader.append('')

    for line in defaultHeader:
        file_writer.writerow([line])

    file_writer.writerow(line1 + [''] + line11)
    file_writer.writerow(line2 + [''] + line22)
    file_writer.writerow(line3)
    file_writer.writerow([''])

    header = formatHeader(header)
    file_writer.writerow(header.keys())

def writeLinesWithValues(file_reader, file_writer, value):
    for rowReader in file_reader:
        if rowReader[reportUniqueColumn] == value:
            file_writer.writerow((rowReader['CNPJRaizLoja'], rowReader['RazaoSocialLoja'], rowReader['SaldoCarteiraJan16Loja'], rowReader['SaldoLiquidoCarteiraJan16Loja'], rowReader['SaldoCarteiraINSSSiapeM3Loja'], rowReader['SaldoCarteiraINSSSiapeM2Loja'], rowReader['SaldoCarteiraINSSSiapeM1Loja'], rowReader['SaldoPortadoINSSSiapeM3Loja'], rowReader['SaldoPortadoINSSSiapeM2Loja'], rowReader['SaldoPortadoINSSSiapeM1Loja'], rowReader['IndicePortabilidaM3Loja'], rowReader['IndicePortabilidadeM2Loja'], rowReader['IndicePortabilidadeM1Loja'], rowReader['IndicePortabilidadeM3Master'], rowReader['IndicePortabilidadeM2Master'], rowReader['IndicePortabilidadeM1Master']))

def getPreviousMonth(yearmonth, total):
    monthYear = []
    previousMonth = []
    monthYear.append(int((yearmonth)[-2:]))
    monthYear.append(int((yearmonth)[0:4]))
    monthYear.append(getMonth(monthYear[0]))
    previousMonth.append(monthYear.copy())
    while total != 0:
        month = monthYear[0] - 1
        if month == 0:
            monthYear[0] = 12
            monthYear[1] -= 1
            del monthYear[-1]
            monthYear.append(getMonth(monthYear[0]))
            previousMonth.append(monthYear.copy())
            total -= 1
        else:
            monthYear[0] -= 1
            del monthYear[-1]
            monthYear.append(getMonth(monthYear[0]))
            previousMonth.append(monthYear.copy())
            total -= 1
    return previousMonth

def getMonth(yearmonth):
    if len(str(yearmonth)) > 2:
        month = int(yearmonth[-2:])
    else:
        month = yearmonth
    switcher = {
                1: "Jan", 
                2: "Fev", 
                3: "Mar",
                4: "Abr", 
                5: "Mai", 
                6: "Jun", 
                7: "Jul", 
                8: "Ago", 
                9: "Set", 
                10: "Out", 
                11: "Nov", 
                12: "Dez"
    }
    return switcher.get(month, "Invalid Month")

def getCodigoMasterLoja(file_reader, value):
    for rowReader in file_reader:
        if rowReader[reportStoreCod] == value:
            return rowReader

def formatHeader(header):
    info = getPreviousMonth(header.get(reportDateColumn), 3) 
    switcher = {
                'CNPJRaizLoja': "CNPJ Raiz", 
                'RazaoSocialLoja': "Razao Social",
                'SaldoCarteiraJan16Loja': 'Saldo ' + getMonth(header.get(reportDateColumn)) + '/' + header.get(reportDateColumn)[0:4] + ' Carteira const. ate Jan/16', 
                'SaldoLiquidoCarteiraJan16Loja' : 'Saldo Liquido ' + getMonth(header.get(reportDateColumn)) + '/' + header.get(reportDateColumn)[0:4] + ' Carteira const. ate Jan/16' ,
                'SaldoCarteiraINSSSiapeM3Loja' : 'Saldo Carteira ' + info[3][2] + '/' + str(info[3][1]) + ' (INSS/Siape)',
                'SaldoCarteiraINSSSiapeM2Loja' : 'Saldo Carteira ' + info[2][2] + '/' + str(info[2][1]) + ' (INSS/Siape)',
                'SaldoCarteiraINSSSiapeM1Loja' : 'Saldo Carteira ' + info[1][2] + '/' + str(info[1][1]) + ' (INSS/Siape)',
                'SaldoPortadoINSSSiapeM3Loja' : 'Saldo Portado* ' + info[3][2] + '/' + str(info[3][1]) + ' (INSS/Siape)',
                'SaldoPortadoINSSSiapeM2Loja' : 'Saldo Portado* ' + info[2][2] + '/' + str(info[2][1]) + ' (INSS/Siape)',
                'SaldoPortadoINSSSiapeM1Loja' : 'Saldo Portado* ' + info[1][2] + '/' + str(info[1][1]) + ' (INSS/Siape)',
                'IndicePortabilidaM3Loja' : 'Indice  ' + info[3][2] + '/' + str(info[3][1]),
                'IndicePortabilidadeM2Loja' : 'Indice  ' + info[2][2] + '/' + str(info[2][1]),
                'IndicePortabilidadeM1Loja' : 'Indice  ' + info[1][2] + '/' + str(info[1][1]),
                'IndicePortabilidadeM3Master' : 'Indice ' + info[3][2] + '/' + str(info[3][1]),
                'IndicePortabilidadeM2Master' : 'Indice ' + info[2][2] + '/' + str(info[2][1]),
                'IndicePortabilidadeM1Master' : 'Indice ' + info[1][2] + '/' + str(info[1][1])
    }
    copy2Header = {}
    copyHeader = header.copy()
    listOfColumns = list(switcher.keys())
    listOfDeletedColumns = []
    for item in header:
        if item in listOfColumns:
            newKey = switcher.get(item)
            copyHeader[newKey] = copyHeader.pop(item)
            copy2Header[newKey] = header[item]
        else:
            listOfDeletedColumns.append(copyHeader[item])
            del copyHeader[item]        
    return copyHeader

if __name__ == '__main__':
    main()