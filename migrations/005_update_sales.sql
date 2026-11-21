
-- Add total_value to sales
ALTER TABLE sales
ADD COLUMN total_value NUMERIC(10,2);

-- Add creation timestamp
ALTER TABLE sales
ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Remove old product relationship
ALTER TABLE sales
DROP COLUMN product_id,
DROP COLUMN quantity,
DROP COLUMN value;

-- Make total_value mandatory
ALTER TABLE sales
ALTER COLUMN total_value SET NOT NULL;
