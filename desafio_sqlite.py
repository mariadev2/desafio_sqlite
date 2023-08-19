# Criando um base com o modelo ORM, usando sqalchemy"
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Float

# Inciando a conexao com o banco de dados"

engine = sqlalchemy.create_engine('sqlite:///enterprise.db,echo=True')

Base = declarative_base()
# Criando a classe Cliente

class Cliente(Base):
    __tablename__ = 'cliente'


    """Aqui tem os atributos da classe cliente"""

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String)

    """ Criando a relaçao da classe Cliente com a classe Conta"""
    conta = relationship("Conta",back_populates="conta_relacionamento",cascade="all,delete-orphan")


    def __repr__(self):
        return (f"Cliente: id = {self.id}"
                f"\nnome = {self.nome}"
                f"\ncpf = {self.cpf}"
                f"\nendereço = {self.endereco}\n"
                f"\nDADOS DA CONTA de {self.nome}"
                f"\n{self.conta}")


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer,primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    numero_conta  = Column(Integer)
    id_cliente = Column(Integer,ForeignKey("cliente.id"),nullable=False)
    saldo = Column(Float)
    conta_relacionamento= relationship("Cliente",back_populates="conta")
    def __repr__(self):
        return (f"\nnumero da conta = {self.numero_conta}"
                f"\ntipo = {self.tipo}"
                f"\nagencia = {self.agencia}"
                f"\nid cliente = {self.id_cliente}"
                f"\nsaldo = {self.saldo}\n")

# fazendo print das informaçoes da conta
print(Cliente.__tablename__)
print(Cliente.__repr__)
print(Conta.__tablename__)

# criando uma conexao com o banco de dados
engine = create_engine("sqlite://")

# criando as clases como tabelas no banco de dados
Base.metadata.create_all(engine)

#fazendo uma analise no esquema do banco de dados
#criando uma cenexao para a analise
analisar_engine = inspect(engine)
# usando a analise para realizar prints
print(analisar_engine.has_table("cliente"))
# printa o nome das tabelas criadas
print('\nPrintando nomes das classes')
print(analisar_engine.get_table_names())
print(analisar_engine.default_schema_name)


# criando uma sessao para preencher as tabelas criandas antes

with Session (engine) as sessao_para_criar_dados:

    Carlos = Cliente(
                    nome = 'Carlos',
        cpf = '345678234',
        #Criando duas intancias para o mesmo atributo da classe Cliente
  endereco='rua 10',
    conta = [Conta(numero_conta='3', tipo='corrente'),
             Conta(numero_conta='4', tipo='poupança')]
    )


    Juliana = Cliente(
        nome='Juliana',
        cpf='987654321',
        endereco='rua 5',
        conta = [Conta(numero_conta='1',tipo='corrente'),
             Conta(numero_conta='2', tipo='poupança')]

    )
    Carla = Cliente(
        nome='Carla',
        cpf='0917886543',
        endereco='rua 8',
        conta=[Conta(numero_conta='5', tipo='corrente')]
    )
    Almim = Cliente(
        nome='Almim',
        cpf='876543211',
        endereco='rua 11',
        conta=[Conta(numero_conta='7', tipo='corrente'),
               Conta(numero_conta='8', tipo='conjugada'),
               Conta(numero_conta='9', tipo='poupança')]
    )

    # enviando os dados para o BD
    sessao_para_criar_dados.add_all([Juliana,Carlos,Almim,Carla])
    sessao_para_criar_dados.commit()

# Realizar consuntas no Banco de dados

# Realizar consuntas no Banco de dados com filtragem so por Juliana
consulta_banco_de_dados = select(Cliente).where(Cliente.nome.in_(["Juliana"]))

# printando resultado de "consulta_banco_de_dados" usando filtragem
print('-'*40)
print('\nRecuperando usuários a partir de condição de filtragem')
print('-'*40)
for cliente in sessao_para_criar_dados.scalars(consulta_banco_de_dados):
    print(f'\n{cliente}')

# Realizar consuntas no Banco de dados com filtragem so por conta
consulta_banco_de_dados_por_conta= select(Conta).where(Conta.numero_conta.in_([2]))
print('-'*40)
print('\nRecuperando clientes que tem duas contas')
print('-'*40)
for numero_conta in sessao_para_criar_dados.scalars(consulta_banco_de_dados_por_conta):
    print(f"\n{numero_conta}")


consulta_banco_de_dados_ordem= select(Cliente).order_by(Cliente.nome.desc())
print('-'*40)
print('\nRecuperando clientes por ordem')
print('-'*40)
for ordenados in sessao_para_criar_dados.scalars(consulta_banco_de_dados_ordem):
    print(f"\n{ordenados}")


consulta_banco_de_dados_tudo = select(Cliente.nome, Conta.numero_conta,Conta.tipo).join_from(Conta, Cliente)
print('-'*40)
print('\nRecuperando todos os dados')
print('-'*40)
for resultado in sessao_para_criar_dados.scalars(consulta_banco_de_dados_tudo):
    print(resultado)


conexao = engine.connect()
resultado_conexao = conexao.execute(consulta_banco_de_dados_tudo).fetchall()
print('-'*40)
print("Buscando e exibindo nome,numero da conta e tipo da conta")
print('-'*40)
for resultado in resultado_conexao:
    print(resultado)

consulta_banco_de_dados_contagem = select(func.count('*')).select_from(Cliente)
print('\nTotal de instâncias em Clientes')
for resultado in sessao_para_criar_dados.scalars(consulta_banco_de_dados_contagem):
    print(resultado)

consulta_banco_de_dados_contagem = select(func.count('*')).select_from(Conta)
print('\nTotal de instâncias em Contas')
for resultado in sessao_para_criar_dados.scalars(consulta_banco_de_dados_contagem):
    print(resultado)


sessao_para_criar_dados.close()