import pandas as pd
import os


def gerarRelatorio(dados):
    try:
        if(os.path.exists("relatorioFerias.xlsx")):
            os.remove("relatorioFerias.xlsx")
        
        df = pd.DataFrame()
        meses = []
        dict_data = {
            "Trabalhando": [],
            "DeFerias": []
        }

        for d in dados:
            meses.append(d.date)
            dict_data["Trabalhando"].append(d.Trabalhando)
            dict_data["DeFerias"].append(d.DeFerias)

        df = pd.DataFrame(dict_data, index=meses)

        df.to_excel('relatorioFerias.xlsx')
        return {"status: Relatório de férias gerado com sucesso!"}
    except Exception as e:
        print(e)
        return {"status: Erro ao gerar xlsx "} 
    
def gerarRelatorioFuncionarios(dados):
    try:
        if(os.path.exists("relatorioFuncionarios.xlsx")):
            os.remove("relatorioFuncionarios.xlsx")

        df = pd.DataFrame()
        
        dict_data = {
            "Nome": [],
            "Matricula": [],
            "Cargo": [],
            "Contrato": [],
            "StatusFerias": []
        }

        for d in dados:
            dict_data["Nome"].append(d.name)
            dict_data["Matricula"].append(d.credential)
            dict_data["Cargo"].append(d.role)
            dict_data["Contrato"].append(d.contract)
            dict_data["StatusFerias"].append(d.vacationStatus)
        
        df = pd.DataFrame(dict_data)

        df.to_excel('relatorioFuncionarios.xlsx')

        return {"status: Relatório de funcionários gerado com sucesso!"}
    except Exception as e:
        print(e)
        return {"status: Erro ao gerar xlsx "}