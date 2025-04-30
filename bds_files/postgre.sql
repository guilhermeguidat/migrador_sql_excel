-- Criação de uma tabela exemplo
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(15),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserção de dados exemplo
INSERT INTO clientes (nome, email, telefone) 
VALUES 
    ('João Silva', 'joao.silva@example.com', '123456789'),
    ('Maria Oliveira', 'maria.oliveira@example.com', '987654321'),
    ('Carlos Souza', 'carlos.souza@example.com', '1122334455');

-- Criar outra tabela para testar
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    preco DECIMAL(10, 2),
    estoque INT
);

-- Inserir dados na tabela de produtos
INSERT INTO produtos (nome, preco, estoque)
VALUES 
    ('Produto A', 99.90, 50),
    ('Produto B', 199.50, 30),
    ('Produto C', 49.99, 100);

-- Consultas para verificação
SELECT * FROM clientes;
SELECT * FROM produtos;
