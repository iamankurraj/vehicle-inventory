INSERT INTO country (name) VALUES
('India'),
('USA'),
('Canada'),
('Australia')
ON CONFLICT (name) DO NOTHING;


INSERT INTO region (name, country_id)
SELECT r.name, c.id
FROM (
  VALUES
  -- India
  ('Punjab','India'), ('Delhi','India'), ('Mumbai','India'),
  ('Kerala','India'), ('Bangalore','India'), ('Tamil Nadu','India'),

  -- USA
  ('California','USA'), ('Texas','USA'), ('Georgia','USA'),
  ('New York','USA'), ('Houston','USA'), ('Arizona','USA'),

  -- Canada
  ('Toronto','Canada'), ('Alberta','Canada'),
  ('Ontario','Canada'), ('Newfoundland','Canada'),

  -- Australia
  ('Melbourne','Australia'), ('New South Wales','Australia'),
  ('Queensland','Australia'), ('Victoria','Australia')
) r(name,country)
JOIN country c ON c.name = r.country
ON CONFLICT (name, country_id) DO NOTHING;


INSERT INTO provider (name, region_id)
SELECT p.name, r.id
FROM (
  VALUES
  -- India
  ('Punjab Motors','Punjab'), ('Punjab Auto','Punjab'), ('Punjab Spares','Punjab'),
  ('Delhi Motors','Delhi'), ('Delhi Auto','Delhi'), ('Delhi Spares','Delhi'),
  ('Mumbai Motors','Mumbai'), ('Mumbai Auto','Mumbai'), ('Mumbai Spares','Mumbai'),
  ('Kerala Motors','Kerala'), ('Kerala Auto','Kerala'), ('Kerala Spares','Kerala'),
  ('Bangalore Motors','Bangalore'), ('Bangalore Auto','Bangalore'), ('Bangalore Spares','Bangalore'),
  ('Tamil Motors','Tamil Nadu'), ('Tamil Auto','Tamil Nadu'), ('Tamil Spares','Tamil Nadu'),

  -- USA
  ('California Motors','California'), ('California Auto','California'), ('California Spares','California'),
  ('Texas Motors','Texas'), ('Texas Auto','Texas'), ('Texas Spares','Texas'),
  ('Georgia Motors','Georgia'), ('Georgia Auto','Georgia'), ('Georgia Spares','Georgia'),
  ('NY Motors','New York'), ('NY Auto','New York'), ('NY Spares','New York'),
  ('Houston Motors','Houston'), ('Houston Auto','Houston'), ('Houston Spares','Houston'),
  ('Arizona Motors','Arizona'), ('Arizona Auto','Arizona'), ('Arizona Spares','Arizona'),

  -- Canada
  ('Toronto Motors','Toronto'), ('Toronto Auto','Toronto'), ('Toronto Spares','Toronto'),
  ('Alberta Motors','Alberta'), ('Alberta Auto','Alberta'), ('Alberta Spares','Alberta'),
  ('Ontario Motors','Ontario'), ('Ontario Auto','Ontario'), ('Ontario Spares','Ontario'),
  ('NFL Motors','Newfoundland'), ('NFL Auto','Newfoundland'), ('NFL Spares','Newfoundland'),

  -- Australia
  ('Melbourne Motors','Melbourne'), ('Melbourne Auto','Melbourne'), ('Melbourne Spares','Melbourne'),
  ('NSW Motors','New South Wales'), ('NSW Auto','New South Wales'), ('NSW Spares','New South Wales'),
  ('Queensland Motors','Queensland'), ('Queensland Auto','Queensland'), ('Queensland Spares','Queensland'),
  ('Victoria Motors','Victoria'), ('Victoria Auto','Victoria'), ('Victoria Spares','Victoria')
) p(name,region)
JOIN region r ON r.name = p.region
ON CONFLICT DO NOTHING;


INSERT INTO inventory (provider_id, part_name, quantity)
SELECT
  p.id,
  v.part_name,
  floor(random() * 20 + 1)::int AS quantity
FROM provider p
CROSS JOIN (
  VALUES
    ('Brake Oil'),
    ('Pads'),
    ('Brake Hose Kit Front'),
    ('Brake Hose Kit Rear'),
    ('Gear Oil'),
    ('Chain'),
    ('Sprocket Set'),
    ('Damper (7 inches)'),
    ('Damper (5.5 inches)'),
    ('Springs secondary'),
    ('Springs primary'),
    ('Rim'),
    ('Tyres'),
    ('Tie Rod'),
    ('Clevis'),
    ('Dashboard'),
    ('Auxillary Lights'),
    ('Battery Charger 10A'),
    ('Battery Charger 40A')
) v(part_name);


INSERT INTO vehicle (vin) VALUES
('MA1TA2HG5A1234567'),
('JTDBR32E720123456'),
('1HGCM82633A004352'),
('WBA3A5C56DF123789'),
('KMHDU46D07U123456'),
('SALWR2EF9FA123456'),
('VF1BZ0A064A123456'),
('2T1BURHE6FC123456'),
('JHMFA16586S123456'),
('YV1MS382762123456'),
('3VWFE21C04M123456'),
('JN1CV6EK9BM123456'),
('WAUZZZ8K9DA123456'),
('MMBJNKG10FH123456'),
('MR0EX8CD2K1234567');



