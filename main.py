from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Float, Date, Time
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
Base = declarative_base()

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    consulta = relationship("Consulta", back_populates= "medico")

    def __repr__(self):
        return f" Medico: \n - Numero do medico: {self.id} \n Nome: {self.nome} "


class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    horario = Column(String, nullable=False)
    data = Column(String, nullable=False)
    tipo = Column(String, nullable=False)

    medico_id = Column (Integer, ForeignKey("medicos.id"))

    medico = relationship("Medico", back_populates="consulta")

    def __repr__(self):
        return f"Data: \n {self.data} \n Horario: \n {self.horario} \n - Tipo da consulta: \n {self.tipo}"

engine = create_engine("sqlite:///consultorio.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def cadrastar_medicos():
    nome_medicos = input("Digite o nome do médico: ").strip().capitalize()

    with Session() as session:
        try:
            medico = Medico(nome=nome_medicos)
            session.add(medico)
            session.commit()
            print(f"{nome_medicos} cadrastado com sucesso")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

def criar_consulta():
    tipo_consulta = input("Digite o tipo da consulta: ").strip().capitalize()
    horario_consulta = input("Qual o horario deseja marcar: ")
    data_consulta = input("Qual a data deseja marcar: ")
    medico_consulta = input("Qual ID do medico: ")

    with Session() as session:
        try:
            consultas = Consulta(tipo=tipo_consulta, horario=horario_consulta, data=data_consulta, medico_id=medico_consulta)
            session.add(consultas)
            session.commit()
            print(f"Consulta cadrastado com sucesso")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
def atualizar_consulta():
    try:
        id_consulta = int(input("Digite o Id da consulta: ").strip())
    except ValueError:
        print("ID inválido")
        novo_horario = input("Qual o novo horario da consulta (enter para manter): ").strip()
        nova_data = input("Qual a nova data da consulta (enter para manter): ").strip()
        novo_tipo = input("Digite o novo tipo da consulta (enter para manter): ").strip()

        with Session() as session:
            try:
                consulta = session.query(Consulta).filter_by(id=id_consulta).first()
                if not consulta:
                    print("Consulta não encontrada")
                if novo_horario:
                    consulta.horario = novo_horario
                if nova_data:
                    consulta.data = nova_data
                if novo_tipo:
                    consulta.tipo = novo_tipo.capitalize()
                session.commit()
                print("Consulta atualizada com sucesso")
            except Exception as erro:
                session.rollback()
                print(f"Ocorreu um erro: {erro}")
atualizar_consulta()