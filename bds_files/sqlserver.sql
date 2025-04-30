-- Criação do banco de dados
CREATE DATABASE TestDB;
GO

-- Usar o banco de dados recém-criado
USE TestDB;
GO

-- Criação de uma tabela
CREATE TABLE Clientes (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Nome NVARCHAR(100),
    Email NVARCHAR(100),
    DataCadastro DATETIME DEFAULT GETDATE()
);
GO

-- Inserção de dados na tabela
INSERT INTO Clientes (Nome, Email)
VALUES 
    ('João Silva', 'joao.silva@email.com'),
    ('Maria Oliveira', 'maria.oliveira@email.com'),
    ('Carlos Souza', 'carlos.souza@email.com');
GO

-- Seleção de todos os dados da tabela
SELECT * FROM Clientes;
GO
