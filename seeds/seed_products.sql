
WITH product_data (sku, product_name, brand_name, weight_volume, price, quantity) AS (
    VALUES
        ('MER-001', 'Arroz Branco Tipo 1', 'Sabor do Campo', '5 kg', 28.90, 15),
        ('MER-002', 'Feijão Carioca Tipo 1', 'Grão Nobre', '1 kg', 8.50, 4),
        ('MER-003', 'Café Torrado e Moído', 'Aroma Forte', '500 g', 17.90, 10),
        ('MER-004', 'Óleo de Soja Refinado', 'Sol Dourado', '900 ml', 6.80, 20),
        ('MER-005', 'Açúcar Refinado Especial', 'Doce Cristal', '1 kg', 4.70, 12),
        ('MER-006', 'Leite Integral UHT', 'Fazenda Pura', '1 L', 5.20, 3),
        ('MER-007', 'Macarrão Espaguete', 'Bella Massa', '500 g', 4.10, 18),
        ('MER-008', 'Molho de Tomate Tradicional', 'Pomodoro Bom', '300 g', 2.50, 25),
        ('MER-009', 'Sabão em Pó Multiação', 'Brilho Limpo', '1,6 kg', 19.50, 8),
        ('MER-010', 'Papel Higiênico Folha Dupla', 'Nuvem Macia', '12 rolos', 18.00, 2)
),
brand_names AS (
    SELECT DISTINCT brand_name FROM product_data
),
inserted_brands AS (
    INSERT INTO brands (id, name)
    SELECT gen_random_uuid(), brand_name
    FROM brand_names
    ON CONFLICT (name)
    DO UPDATE SET name = EXCLUDED.name
    RETURNING id, name
),
inserted_products AS (
    INSERT INTO products (
        id,
        name,
        price,
        quantity,
        brand_id,
        weight_volume
    )
    SELECT
        gen_random_uuid(),
        pd.product_name,
        pd.price,
        pd.quantity,
        ib.id,
        pd.weight_volume
    FROM product_data pd
    JOIN inserted_brands ib
        ON ib.name = pd.brand_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM skus s
        WHERE s.code = pd.sku
    )
    RETURNING id, name
)
INSERT INTO skus (id, code, product_id)
SELECT
    gen_random_uuid(),
    pd.sku,
    ip.id
FROM inserted_products ip
JOIN product_data pd
    ON pd.product_name = ip.name;
