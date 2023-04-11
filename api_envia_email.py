from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, File, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from envia_gmail import enviarGmail
from envia_workplace import enviarMensagemWorkplace
from gera_relatorio import gerarRelatorio, gerarRelatorioFuncionarios

# python3 -m uvicorn api_envia_email:app --reload
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Email(BaseModel):
    assunto: str
    mensagem: str
    destinatario: str
    relatorio: str | None

class MensagemWorkplace(BaseModel):
    id: int
    mensagem: str

# TODO - Refatorar a função enviar mensagem para que aceite enviar os relatórios gerados

@app.post("/enviar_mensagem")
async def enviarMensagem(email: Email, msgWorkplace: MensagemWorkplace):
    try:
        if email.relatorio is None:
            enviarGmail(body=email.mensagem, subject=email.assunto, to=email.destinatario)
        else:
            enviarGmail(body=email.mensagem, subject=email.assunto, to=email.destinatario, attachment=email.relatorio)

        enviarMensagemWorkplace(id=msgWorkplace.id, msg=msgWorkplace.mensagem)
        return {"status: Notificação enviada com sucesso!"}
    except Exception as e:
        print(e)
        return {"status: Erro ao enviar email: "}

class DadosRelatorio(BaseModel):
    date: str
    Trabalhando: int
    DeFerias: int

class DadosRelatorioFuncionarios(BaseModel):
    name: str
    credential: str
    role: str
    contract: str
    vacationStatus: str

@app.post("/gerar_relatorio")
async def gerarRelatorioFerias(dadosFuncionarios: List[DadosRelatorio]):
    try:
        gerarRelatorio(dados=dadosFuncionarios)

        return {"status: relatório gerado com sucesso!"}
    except Exception as e:
        print(e)
        return {"status: Erro ao gerar relatório "}



@app.post("/gerar_relatorio_funcionarios")
async def gerarRelatorioStatusFuncionarios(dadosFuncionarios: List[DadosRelatorioFuncionarios]):
    try:
        gerarRelatorioFuncionarios(dados=dadosFuncionarios)

        return {"status: relatório gerado com sucesso!"}
    except Exception as e:
        print(e)
        return {"status: Erro ao gerar relatório "}

class DownloadRelatorio(BaseModel):
    relatorio: str

@app.get("/download")
async def download_relatorioFerias(relatorio=str):
    file_path = f"C:/Users/guico/OneDrive/Documentos/PythonProjetoTeste/{relatorio}.xlsx"
    file_name = f"{relatorio}.xlsx"

    with open(file_path, "rb") as file:
        file_content = file.read()
    return Response(content=file_content, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={file_name}"})
