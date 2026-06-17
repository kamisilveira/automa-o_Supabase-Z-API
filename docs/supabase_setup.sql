create table if not exists contacts (
    id     bigint generated always as identity primary key,
    name   text    not null,
    phone  text    not null,     
    active boolean not null default true,
    created_at timestamptz default now()
);

insert into contacts (name, phone, active) values
    ('Geovana',   '552192000009', true),
    ('Carlos',    '552196600000', true),
    ('Paula',     '552196640005', true);
